"""
Example: Animation rendering and cycloidal pendulum
"""

from functools import lru_cache

import bpy

#############################################
# Setup
#############################################
# [setup-1]
# Import necessary libraries
import numpy as np

import ddg
from ddg.datastructures.nets.domain import DiscreteInterval
from ddg.geometry.intersection import intersect, join
from ddg.geometry.subspaces import (
    Point,
    angle_bisector_orientation_reversing,
    orthonormalize_and_center_subspace,
    subspace_from_affine_points,
)
from ddg.visualization.blender import animation, props
from ddg.visualization.blender.material import material

# [setup-1]

# [setup-2]
# Clear the existing objects in the Blender scene
ddg.visualization.blender.scene.clear()
# ddg.visualization.blender.material.clear()
# [setup-2]


#############################################
#  general-functions
#############################################


# [general-functions-1]
def tangent_edges(fct):
    """Returns a function that, for a given index,
    returns the edge tangent line with given index of the
    discrete curve in the input.
    The i'th edge tangent line is the join of fct(i) and fct(i+1).
    """

    @lru_cache(maxsize=128)
    def tangent_edge(i):
        tangent = subspace_from_affine_points(fct(i), fct(i + 1))
        return orthonormalize_and_center_subspace(
            tangent, np.sum([fct(i), fct(i + 1)], axis=0) / 2
        )

    return tangent_edge


def normal_vertices(fct):
    """Returns a function that, for a given index,
    returns the vertex normal line with given index of the
    discrete curve in the input.
    The i'th vertex normal line is the orientation reversing
    angle bisector of the (i-1)'st and i'th edge tangent line.
    """

    @lru_cache(maxsize=128)
    def normal_vertex(i):
        normal = angle_bisector_orientation_reversing(
            tangent_edges(fct)(i - 1), tangent_edges(fct)(i)
        )
        return orthonormalize_and_center_subspace(normal, fct(i))

    return normal_vertex


# [general-functions-2]
def envelope(g):
    """The return value of the function g is assumed to be a line.
    Then this function returns a function that, for a given index i,
    returns the intersection of the (i-1)'st and i'th
    line of g.
    """

    @lru_cache(maxsize=128)
    def new_curve_fct(i):
        point = intersect(g(i - 1), g(i))
        return point.affine_point

    return new_curve_fct


#############################################
# Example
#############################################
# [example-0]
example = "smooth"
if example == "smooth":
    sampling_curve = np.pi / 100
    bevel_curve = 0.01
    bevel_line = 0.02
    edge_domain = [[-5, 5]]

# [example-0]

# [example-1]
# We define a parametrization for a curve.


def parametrization(u, A=1, r=1, w=1):
    theta = lambda t: np.arcsin(A * np.cos(w * t))
    return [r * (2 * theta(u) + np.sin(2 * theta(u))), r * (-3 - np.cos(2 * theta(u)))]


# Trajectory geometry
smooth_domain = [[0, np.pi + np.pi / 100]]

trajectory_snet = ddg.nets.SmoothNet(parametrization, domain=smooth_domain)
trajectory_dnet = ddg.sample_smooth_net(trajectory_snet, sampling=sampling_curve)

# Define evolutes for edge and vertex normalss

trajectory_normal_vertex = normal_vertices(trajectory_dnet.fct)
trajectory_evolute_edge = envelope(trajectory_normal_vertex)

#############################################
# Example
#############################################

# [visualization-1]
black = material("black", (0, 0, 0), 0, 0)


# [visualization-2]
def visualize_2d_curve(
    dnet_fct,
    domain=trajectory_dnet.domain,
    material=black,
    bevel_depth=bevel_curve,
    **kwargs,
):
    dnet = ddg.nets.DiscreteNet(dnet_fct, domain=domain)
    return ddg.to_blender_object_helper(
        ddg.nets.utils.embed(dnet),
        material=material,
        curve_properties={"bevel_depth": bevel_depth},
        **kwargs,
    )


def visualize_cycloid_pendulum(
    idx, amplitudes=[1 / 5, 2 / 5, 3 / 5, 4 / 5, 1.0], n_sampling=100, link=False
):
    """Visualize ( create blender objects) of a cycloidal pendulum.

    Parameters
    ----------
    idx : Index value along the discrete domain of the pendulum path
        Index value along the discrete domain of the pendulum path
    amplitudes : list(float), optional
        Amplitudes of the pendulum to be rendered,
        by default [1 / 5, 2 / 5, 3 / 5, 4 / 5, 1.0]
    n_sampling : int, optional
        Sampling rate, by default 100
    link : bool, optional
        Link to scene. Do not use for callbacks in sliders, by default False

    Returns
    -------
    list(bobj)
        Blender objects of pendulum
    """
    # Sampling is chosen over pi (or half a period)
    sampling = np.pi / n_sampling
    domain = [[0, np.pi]]

    bobj_list = []

    for A in amplitudes:
        # New function to wrap amplitude choice
        def amp_parametrization(u):
            return parametrization(u, A=A)

        # Net to sample mass trajectory
        path_snet = ddg.nets.SmoothNet(amp_parametrization, domain=domain)
        path_dnet = ddg.sample_smooth_net(path_snet, sampling=sampling)

        # String net to sample strings
        string_snet = ddg.nets.SmoothNet(amp_parametrization, domain=domain)
        string_dnet = ddg.sample_smooth_net(string_snet, sampling=sampling)

        # A time dependent domain such that nets are only converted up to the pivot.
        m = np.floor(idx / n_sampling)  # multiplicity of half-periods
        bounds = [
            int(n_sampling * m + np.mod(idx, n_sampling)),
            int(n_sampling * m + int(n_sampling / 2) - 1),
        ]
        bounds.sort()  # Sort by which of the indices is larger
        # (the pivot index n/2-1 or the mass index)
        string_dnet.domain = DiscreteInterval(bounds)

        # Mass of pendulum
        mass = Point([*path_dnet.fct(idx), 0, 1])
        mass_snet = ddg.to_smooth_net(mass)

        # Create curved string by creating evolute along vertex of the string net
        string_normal_vertex = normal_vertices(string_dnet.fct)
        curved_string_evolute_edge = envelope(string_normal_vertex)
        curve_endpoint = Point([*curved_string_evolute_edge(idx), 0, 1])

        # Create straight string by joins of mass with the evolute point where the
        # normal vertex is tangent
        if mass != curve_endpoint:  # Only do it if Points are distinct.
            straight_string_vertex = join(mass, curve_endpoint)

        # Render visualization

        # Straight components
        if mass != curve_endpoint:
            str_string_bobj = ddg.to_blender_object_helper(
                straight_string_vertex,
                sampling=1,
                domain=[[0, 1]],
                curve_properties={"bevel_depth": bevel_line},
                material=black,
                name=f"Pendulum String - Straight Component - Anplitude={A}",
                link=link,
            )

        # Curved component

        curved_string_bobj = visualize_2d_curve(
            curved_string_evolute_edge,
            material=black,
            domain=string_dnet.domain,
            name=f"Pendulum String - Curved Component - Amplitude={A}",
            bevel_depth=bevel_line,
            link=link,
        )

        # Mass visualization
        mass_bobj = ddg.to_blender_object_helper(
            mass_snet,
            sphere_radius=0.1,
            material=black,
            name=f"Pendulum Mass - Amplitude={A}",
            link=link,
        )

        bobj_list.append(mass_bobj)
        bobj_list.append(curved_string_bobj)

        if mass != curve_endpoint:
            bobj_list.append(str_string_bobj)

    return bobj_list


# Trajectory of cycloid
trajectory_bobj = visualize_2d_curve(trajectory_dnet.fct, name="Discrete Curve")
trajectory_evolute_edge_bobj = visualize_2d_curve(
    trajectory_evolute_edge, name="Evolute Edge"
)

# Add a point light and a camera to the scene
light = ddg.visualization.blender.light.light(
    location=(0, 0, 100), type="SUN", energy=5
)
camera = ddg.visualization.blender.camera.camera(location=(0, -2, 15))
ddg.visualization.blender.render.setup_cycles_renderer()

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
    1,
    1,
    1,
    1,
)
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 93.1


# visualize_cycloid_pendulum_index(179, link=True)

callback = props.hide_callback(
    "construction", visualize_cycloid_pendulum
)  # For many pendulum potential to crash with hide_callback

props.add_props_with_callback(
    callback,
    ("i"),  # labels for the properties
    0,  # arbitrarily chosen initial parameters
)

SCENE = bpy.context.scene
FPS = 1
animation.set_keyframe(SCENE, 0 * FPS, "i", 0)
animation.set_keyframe(SCENE, 600 * FPS, "i", 600)
