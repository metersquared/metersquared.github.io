---
layout: page
title: gummy
description: A Heuristic solver for QUBO Problems.
importance: 1
year: 2023
category: coursework
toc:
  sidebar: left
#redirect: https://github.com/metersquared/physics_sim
---

> *Github Link : [gummy](https://github.com/metersquared/gummy)*
>
> *Stack : C++*
>
> *Collaborators : Francisco Jose Manjon Cabeza Garcia, [Gennesaret Kharistio Tjusila](https://gtjusila.com/), Michael Adipoetra*

As part of a final project in my Scientific Computing course in WiSe 2022/23, we implemented a heuristic solver for QUBO problems using C++.

# Motivation

Quadratic Unconstrained Binary Optimization (QUBO) problems are family of optimization problems that aims to solve

$$
x^{*}:=\arg \max_{x\in\{0,1\}^{n}} x^T Q x.
$$

QUBO problems are known to be NP hard, and therefore not trivial to do.

# State-of-the-art

Solving QUBO problems using brute-force is not feasible for large $n$ due to the exponential growth of the search space. Therefore, heuristic algorithms are often used to find approximate solutions in a reasonable time frame.

Naive approaches include:

- Local search: Starting from a random solution, iteratively flipping bits to find a better solution. This can easily get stuck in local optima.
- Tabu search: Allows for non-improving moves to escape local optima, but can be computationally expensive.

# The work

We implemented an abstract `Heuristic` C++ class to mount different heuristic algorithms. We chose to implement 3 different heuristics and compare their performance:

- Simulated Annealing (SA): A probabilistic technique that allows for occasional uphill moves to escape local optima, with a cooling schedule to reduce the probability of such moves over time, along with a reannealing procedure ([Katayama &amp; Narihisa, 2001](https://doi.org/10.1016/S0377-2217(00)00242-3)).
- Multistart Tabu Search (MSTS): A method that uses tabu search and variable scoring on the subset of variables to select it and do a brute-force steepest ascent on it, with a random restart procedure ([Palubeckis, 2004](https://doi.org/10.1023/B:ANOR.0000039522.58036.68)).
- Diversification-driven Tabu Search (DDTS): A method that uses tabu search and multiple elite solutions to rank variables and perturb the current solution by flipping the top ranked variables, with a random restart procedure ([Glover, 2010](https://doi.org/10.1007/s10288-009-0115-y)).

For each heuristics, we do 100 runs of 23 different QUBO instances from [QPLIB](https://qplib.zib.de/) using the HPC cluster from TU Berlin:

| Operating System                           | CPU                                            | RAM   | Compiler        |
| ------------------------------------------ | ---------------------------------------------- | ----- | --------------- |
| AlmaLinux 8.7 with x86-64 bit architecture | Single core of an Intel Xeon E5-2630V4 2.2 GHz | 16 GB | g++ (GCC) 8.5.0 |

# Findings

We analyze the results in two ways. First, how does the heuristics perform in terms of the instances solved to optimality, and second, how does the heuristics perform compared to each other in terms of the objective value found.

## Optimality

| Instance Name        | $Q$ Matrix Density | $n$ | Avg Gap % (DDTS) | Avg Gap % (MSTS) | Avg Gap % (SA) | Opt. Hit Count (DDTS) | Opt. Hit Count (MSTS) | Opt. Hit Count (SA) |
| :------------------- | :------------------- | :---- | :--------------- | :--------------- | :------------- | :-------------------- | :-------------------- | :------------------ |
| **QPLIB_3506** | 0.8                  | 496   | **0.66**   | 1.25             | 0.71           | 14                    | 1                     | **15**        |
| **QPLIB_3565** | 1.4                  | 276   | 0.46             | **0.04**   | 0.91           | 39                    | **95**          | 7                   |
| **QPLIB_3642** | 0.4                  | 1035  | 2.85             | 7.62             | **1.11** | 0                     | 0                     | 0                   |
| **QPLIB_3650** | 0.4                  | 946   | 2.01             | 6.36             | **0.84** | 0                     | 0                     | **2**         |
| **QPLIB_3693** | 0.3                  | 1128  | 0.20             | 0.63             | **0.06** | 0                     | 0                     | **1**         |
| **QPLIB_3705** | 1                    | 378   | 0.64             | **0.09**   | 0.86           | 24                    | **82**          | 16                  |
| **QPLIB_3706** | 0.6                  | 703   | 1.74             | 4.61             | **1.04** | 1                     | 0                     | **2**         |
| **QPLIB_3738** | 0.9                  | 435   | 0.91             | 0.92             | **0.76** | 2                     | 1                     | **5**         |
| **QPLIB_3745** | 1.2                  | 325   | 0.03             | **0.00**   | 0.51           | 95                    | **100**         | 40                  |
| **QPLIB_3822** | 0.5                  | 861   | 1.69             | 5.64             | **0.84** | 0                     | 0                     | **2**         |
| **QPLIB_3832** | 0.7                  | 561   | 1.17             | 3.18             | **0.94** | 2                     | 0                     | **3**         |
| **QPLIB_3838** | 0.5                  | 780   | 2.71             | 5.82             | **1.35** | 0                     | 0                     | 0                   |
| **QPLIB_3850** | 0.3                  | 1225  | 2.59             | 8.04             | **1.05** | 0                     | 0                     | **1**         |
| **QPLIB_3852** | 1.6                  | 231   | **0.00**   | **0.00**   | 0.08           | **100**         | **100**         | 93                  |
| **QPLIB_3877** | 0.6                  | 630   | 0.79             | 2.05             | **0.75** | **3**           | 0                     | 2                   |
| **QPLIB_5721** | 76.8                 | 300   | 3.73             | **3.00**   | 12.82          | 0                     | 0                     | 0                   |
| **QPLIB_5725** | 1.7                  | 343   | 0.59             | **0.56**   | 16.16          | **34**          | 6                     | 0                   |
| **QPLIB_5755** | 1                    | 400   | **3.15**   | 3.55             | 18.13          | 0                     | 0                     | 0                   |
| **QPLIB_5875** | 78.9                 | 200   | **0.00**   | **0.00**   | 1.65           | **100**         | **100**         | 4                   |
| **QPLIB_5881** | 29.5                 | 120   | **0.00**   | **0.00**   | 1.55           | **100**         | **100**         | 1                   |
| **QPLIB_5882** | 78.1                 | 150   | **0.00**   | **0.00**   | 1.92           | **100**         | **100**         | 5                   |
| **QPLIB_5909** | 9.6                  | 250   | **0.00**   | **0.00**   | 4.58           | **100**         | **100**         | 0                   |
| **QPLIB_5922** | 9.8                  | 500   | **0.00**   | **0.00**   | 1.13           | **100**         | **100**         | 0                   |

We see that:

- DDTS and MSTS performs better at dense instances, while SA performs better at sparse instances.
- MSTS performs better at small instances, while DDTS performs better at large instances.
- SA optimal hit count is generally lower than the other two heuristics, but it performs better at some instances (e.g., QPLIB_3642, QPLIB_3650, QPLIB_3693).

## Objective Value

To analyze the quality of solutions, we define the value $n$ times the second best gap to actual optimal objective value, which is defined as

$$
\text{Gap} = n \cdot f(x^{*}) - n \cdot f(x_\text{2}),
$$

where $x^{*}$ is the best solution found by all the heuristic, and $x_\text{2}$ is the second best solution found by the heuristic. We then compare the distribution of this value across the 100 runs for each instance and heuristics.

Comparing this value with the % of runs with difference $\leq n$, we get the following:

{% include figure.liquid loading="eager" path="assets/img/project/gummy/profile.png" class="img-fluid rounded z-depth-1" zoomable=true %}

We see that :

- DDTS has a higher percentage of runs with difference $\leq n$ compared to MSTS and SA, indicating that it consistently finds solutions close to the best solution found by all heuristics.
- SA performs worse at problems where the second best gap is small, but becomes better when at gap larger than $2.5$, which is consistent with the optimal hit count results where SA performs better at some instances but worse at others.

# Conclusion

For heuristics algorithms, all three heuristics perform well at different types of instances, and there is no clear winner. However, DDTS seems to be more consistent in finding solutions close to the best solution found by all heuristics, while SA performs better at some instances but worse at others.

As an implementation strategy, we suggest that running multiple heuristics in parallel and selecting the best solution among them can be a good approach to solve QUBO problems, as it can leverage the strengths of each heuristic and mitigate their weaknesses.
