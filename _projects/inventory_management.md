---
layout: page
title: Inventory Management and Optimization
description: Deterministic inventory models implemented with analytical methods, SCIP, and network shortest paths.
importance: 2
category: research
---
> *Stack: Python, NumPy, Pandas, NetworkX, PySCIPOpt*
>
> *Repository: [inv-manage-scip](https://github.com/metersquared/inv-manage-scip)*

This project implements deterministic inventory models from *Logic of Logistics*, moving from closed-form policies to mixed-integer optimization and shortest paths. The notebooks connect each model to numerical experiments, inventory trajectories, and cost decompositions.

# Constant-demand policies

With constant demand $D$, ordering cost $K$, holding cost $h$, instantaneous replenishment, and no shortages, the average cost of an order quantity $Q$ is

$$
C(Q)=\frac{KD}{Q}+\frac{hQ}{2}.
$$

The minimizer is the classical economic order quantity

$$
Q^*=\sqrt{\frac{2KD}{h}},
$$

with replenishment interval $T^*=Q^*/D$. `ELSM_ConstDemand` implements the formulas, simulation, grid search, and cost comparisons.

# Finite horizons and practical policies

For a finite horizon $t$ with $m$ orders, equal cycle lengths minimize holding cost:

$$
C(m)=Km+\frac{hDt^2}{2m}.
$$

The implementation checks neighboring integer values of

$$
m^*=t\sqrt{\frac{hD}{2K}},
$$

and returns the selected order times, quantities, cycle lengths, and cost breakdown.

For standardized replenishment intervals, the project also evaluates policies of the form

$$
T=T_B2^k,
$$

where $T_B$ is a base period and $k$ is an integer. It compares adjacent powers of two around the unrestricted optimum for

$$
f(T)=\frac{K}{T}+gT, \qquad g=\frac{hD}{2},
$$

and selects the lower-cost policy. This restriction has a cost guarantee of approximately 6% over the unrestricted optimum.

# Wagner-Whitin optimization

For variable demand $d_t$, setup cost $K_t$, purchase cost $c_t$, and holding cost $h_t$, the finite-horizon model uses

$$
I_t=I_{t-1}+x_t-d_t,
$$

where $x_t$ is the order quantity and $I_t$ is ending inventory. The PySCIPOpt implementation minimizes

$$
\begin{aligned}
\text{Minimize } & \sum_{t=1}^{T}\left(K_ty_t+c_tx_t+h_tI_t\right)\\
\text{subject to } & I_t=I_{t-1}+x_t-d_t,\\
& I_t\geq 0,\quad x_t\geq 0,\\
& x_t\leq \left(\sum_{s=t}^{T}d_s\right)y_t,\\
& y_t\in\{0,1\}.
\end{aligned}
$$

subject to nonnegative inventory, order quantities, and binary setup variables. `WagnerWhitinSCIP` exposes the resulting inventory and setup decisions for inspection.

# Network formulation and T scaling

The zero-inventory-ordering property gives an acyclic network with $T+1$ nodes. An arc $(i,j)$ represents ordering in period $i$ to cover demand through period $j-1$, with setup and holding weight

$$
\ell_{ij}=K_i+h_i\sum_{k=i}^{j-1}(k-i)d_k.
$$

The shortest path from node $0$ to node $T$ identifies order periods. `WagnerWhitinNetworkSolver` reconstructs order quantities, setup decisions, and inventory levels from that path. Prefix sums make each of the $O(T^2)$ possible arcs constant-time to generate, so network construction is $O(T^2)$.

The benchmark below compares both solvers on constant-cost instances for $T\in\{10,25,50,100,200,400\}$. The network-flow fit has exponent $1.93$, close to the predicted quadratic scaling, while both methods return matching objective values.

{% include figure.liquid loading="eager" path="/assets/img/project/inventory_management/t_scaling.png" class="img-fluid rounded z-depth-1" zoomable=true %}

# Validation and implementation

The test suite checks the constant-demand optima, simulation behavior, power-of-two selection, invalid inputs, and the zero-inventory-ordering property of the SCIP model. The notebook also compares SCIP and network objective values on the benchmark instances.

# Implementation

The project is structured as a small reusable Python package rather than a collection of standalone notebook calculations:

- `economic_lot_model.py` contains analytical, simulation, finite-horizon, and power-of-two policies for constant demand.
- `optimization.py` contains the common Wagner-Whitin data model, the PySCIPOpt formulation, and the NetworkX shortest-path solver.
- `examples/` contains notebooks that derive the models and visualize their behavior.
- `tests/` contains focused regression and mathematical-property checks.

The package is organized into `economic_lot_model.py`, `optimization.py`, `examples/`, and `tests/`. Reproduce the environment with `uv sync` and run the suite with `uv run pytest`. Current models assume deterministic demand, instantaneous replenishment, and no shortages; extending the network model to time-varying purchase costs, lead times, and service constraints is future work.
