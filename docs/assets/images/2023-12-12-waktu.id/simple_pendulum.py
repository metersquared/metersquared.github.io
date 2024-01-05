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
from scipy.special import ellipj

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


def parametrization(u, A=0.4, r=1, w=1):
    l = 4 * r
    k = np.sin(A * np.pi / 2)
    theta = lambda t: 2 * np.arcsin(k * ellipj(w * t, k)[1] / ellipj(w * t, k)[2])
    return [l * np.sin(theta(u)), -l * np.cos(theta(u))]


# Trajectory geometry
smooth_domain = [[0, 2 * np.pi]]

trajectory_snet = ddg.nets.SmoothNet(parametrization, domain=smooth_domain)
trajectory_dnet = ddg.sample_smooth_net(trajectory_snet, sampling=sampling_curve)


#############################################
# Example
#############################################

# [visualization-1]
black = material("black", (0, 0, 0), 0, 0)
red = material("red", (204, 0, 0), 0, 0)


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


def visualize_simple_pendulum(
    idx,
    amplitudes=[0.4],
    n_sampling=100,
    link=False,
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
    domain = [[0, 2 * np.pi]]

    bobj_list = []

    for A in amplitudes:
        # New function to wrap amplitude choice
        def amp_parametrization(u):
            return parametrization(u, A=A)

        def energy_pot(u, A=0.4, r=1, w=1):
            """Potential energy"""
            l = 4 * r
            k = np.sin(A * np.pi / 2)
            theta = lambda t: 2 * np.arcsin(
                k * ellipj(w * t, k)[1] / ellipj(w * t, k)[2]
            )
            return [4, l * (1 - np.cos(theta(u))) - l]

        def energy_kin(u, A=0.4, r=1, w=1):
            """Kinetic energy"""
            l = 4 * r
            k = np.sin(A * np.pi / 2)
            theta = lambda t: 2 * np.arcsin(
                k * ellipj(w * t, k)[1] / ellipj(w * t, k)[2]
            )
            return [5, l * (np.cos(theta(u)) - np.cos(A * np.pi)) - l]

        # Net to sample mass trajectory
        path_snet = ddg.nets.SmoothNet(amp_parametrization, domain=domain)
        path_dnet = ddg.sample_smooth_net(path_snet, sampling=sampling)

        # Potential and kinetic energy
        energy_pot_snet = ddg.nets.SmoothNet(energy_pot, domain=domain)
        energy_pot_dnet = ddg.sample_smooth_net(energy_pot_snet, sampling=sampling)

        energy_kin_snet = ddg.nets.SmoothNet(energy_kin, domain=domain)
        energy_kin_dnet = ddg.sample_smooth_net(energy_kin_snet, sampling=sampling)

        # Mass of pendulum
        mass = Point([*path_dnet.fct(idx), 0, 1])
        mass_snet = ddg.to_smooth_net(mass)

        # String
        straight_string = join(mass, Point([0, 0, 0, 1]))

        # Energy bar
        top_energy_pot = Point([*energy_pot_dnet.fct(idx), 0, 1])
        top_energy_kin = Point([*energy_kin_dnet.fct(idx), 0, 1])

        bar_energy_pot = join(top_energy_pot, Point([4, -4, 0, 1]))
        bar_energy_kin = join(top_energy_kin, Point([5, -4, 0, 1]))

        # Render visualization

        # Mass visualization
        mass_bobj = ddg.to_blender_object_helper(
            mass_snet,
            sphere_radius=0.1,
            material=black,
            name=f"Pendulum Mass - Amplitude={A}",
            link=link,
        )

        str_string_bobj = ddg.to_blender_object_helper(
            straight_string,
            sampling=1,
            domain=[[0, 1]],
            curve_properties={"bevel_depth": bevel_line},
            material=black,
            name=f"Pendulum String - Straight Component - Anplitude={A}",
            link=link,
        )

        energy_pot_bobj = ddg.to_blender_object_helper(
            bar_energy_pot,
            sampling=1,
            domain=[[0, 1]],
            curve_properties={"bevel_depth": bevel_line},
            material=red,
            name=f"Energy potential - Anplitude={A}",
            link=link,
        )

        energy_kin_bobj = ddg.to_blender_object_helper(
            bar_energy_kin,
            sampling=1,
            domain=[[0, 1]],
            curve_properties={"bevel_depth": bevel_line},
            material=black,
            name=f"Energy potential - Anplitude={A}",
            link=link,
        )

        bobj_list.append(mass_bobj)
        bobj_list.append(str_string_bobj)
        bobj_list.append(energy_pot_bobj)
        bobj_list.append(energy_kin_bobj)

    return bobj_list


# Trajectory of cycloid
trajectory_bobj = visualize_2d_curve(trajectory_dnet.fct, name="Discrete Curve")

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


# visualize_simple_pendulum(179, link=True)

callback = props.hide_callback(
    "construction", visualize_simple_pendulum
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
