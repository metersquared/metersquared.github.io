---
layout: page
title: gummy
description: A Heuristic solver for QUBO Problems.
importance: 1
category: work
#redirect: https://github.com/metersquared/physics_sim
---
*Github Link : [gummy](https://github.com/metersquared/gummy)*

As part of a final project in my Scientific Computing course, I implemented Heuristic solver namely : 

- Diversification Driven Tabu Search ([Glover, 2010](https://doi.org/10.1007/s10288-009-0115-y)),
- Multistart Tabu Search ([Palubeckis, 2004](https://doi.org/10.1023/B:ANOR.0000039522.58036.68)),
- and Multistart Simulated Annealing ([Katayama and Narihisa, 2001](https://doi.org/10.1016/S0377-2217(00)00242-3))

to solve QUBO Problems with my group. 

We created some class to mount different kind of heuristics in C++. We find that Diversification Driven Tabu Search performs bests. There are specific instances in sparse problems where simulated annealing performs better.
