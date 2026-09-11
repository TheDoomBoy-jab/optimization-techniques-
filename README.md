# Optimization Algorithms in Python

Implementation of classical Operations Research optimization algorithms in Python using NumPy:
1. **Big-M Simplex Method** for Linear Programming Problems (LPP) with mixed constraints.
2. **Vogel’s Approximation Method (VAM) & MODI (Modified Distribution) Method** for the classic Transportation Problem.

---

## 1. Big-M Simplex Method: The Blending / Product-Mix Problem

### Problem Background
This instance is a canonical benchmark from standard Operations Research textbooks (e.g., *Hamdy A. Taha's Operations Research: An Introduction* and *Hillier & Lieberman's Introduction to Operations Research*). 

It models a constrained resource allocation/blending problem where an exact ingredient requirement ($=$), a minimum quality or active ingredient standard ($\ge$), and a maximum budget or machine-hour limit ($\le$) must all be satisfied simultaneously at minimal total production cost.

### Mathematical Formulation
$$\text{Minimize } Z = 4x_1 + x_2$$

Subject to:
$$3x_1 + x_2 = 3 \quad \text{(Exact specification)}$$
$$4x_1 + 3x_2 \ge 6 \quad \text{(Minimum threshold)}$$
$$x_1 + 2x_2 \le 4 \quad \text{(Resource capacity)}$$
$$x_1, x_2 \ge 0$$

### Standard Form Representation
To formulate the problem for the Simplex tableau, we introduce:
* Slack variable $s_1 \ge 0$ for the $\le$ constraint.
* Surplus variable $s_2 \ge 0$ for the $\ge$ constraint.
* Artificial variables $A_1, A_2 \ge 0$ penalized by a large scalar $M \gg 0$:

$$\text{Minimize } Z = 4x_1 + x_2 + M \cdot A_1 + M \cdot A_2$$

Subject to:
$$\begin{aligned}
3x_1 + x_2 + A_1 &= 3 \\
4x_1 + 3x_2 - s_2 + A_2 &= 6 \\
x_1 + 2x_2 + s_1 &= 4 \\
x_1, x_2, s_1, s_2, A_1, A_2 &\ge 0
\end{aligned}$$

---

## 2. Transportation Problem: The Classic Hitchcock 3×4 Multi-Plant Logistics Problem

### Problem Background
This instance is Frank L. Hitchcock’s classic 3-origin, 4-destination multi-facility shipment benchmark widely cited in OR literature (e.g., *S.D. Sharma*, *Kanti Swarup*, and *Taha*). 

Three manufacturing plants ($S_1, S_2, S_3$) supply finished goods to four regional distribution centers ($D_1, D_2, D_3, D_4$) across a network with heterogeneous freight routes.

### Parameters & Data
* **Source Capacities (Supply):**
  * $S_1 = 7,\; S_2 = 9,\; S_3 = 18 \quad \implies \sum \text{Supply} = 34$
* **Destination Requirements (Demand):**
  * $D_1 = 5,\; D_2 = 8,\; D_3 = 7,\; D_4 = 14 \quad \implies \sum \text{Demand} = 34$
* **Balance:** $\sum \text{Supply} = \sum \text{Demand} = 34$ (Balanced Transportation Problem)
* **Unit Freight Cost Matrix ($C_{ij}$):**

| Origin / Destination | $D_1$ | $D_2$ | $D_3$ | $D_4$ | Supply |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Plant 1 ($S_1$)** | 19 | 30 | 50 | 10 | **7** |
| **Plant 2 ($S_2$)** | 70 | 30 | 40 | 60 | **9** |
| **Plant 3 ($S_3$)** | 40 | 8 | 70 | 20 | **18** |
| **Demand** | **5** | **8** | **7** | **14** | **34** |

### Solution Strategy
1. **Initial Basic Feasible Solution (IBFS):** Computed using **Vogel’s Approximation Method (VAM)** by calculating row and column penalty differences (difference between the two lowest costs).
2. **Optimality Verification & Iteration:** Evaluated using the **MODI ($u\text{-}v$) Method**:
   * Solve dual variables: $u_i + v_j = c_{ij}$ for all basic cells.
   * Compute opportunity costs: $\Delta_{ij} = c_{ij} - (u_i + v_j)$ for all non-basic cells.
   * Trace alternating horizontal/vertical closed loops in the basis to reallocate capacity until all $\Delta_{ij} \ge 0$.

---

## Setup & Running the Code

### Requirements
* Python 3.8+
* NumPy

```bash
pip install numpy
