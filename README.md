# Optimization Algorithms in Python

Implementation of classical optimization methods for constrained linear programming and transportation problems using Python and NumPy.

---

## 1. Big-M Simplex Method

Solves linear programming problems involving equality ($=$) and greater-than-or-equal-to ($\ge$) constraints by penalizing artificial variables using a large penalty coefficient $M$.

### Formulation
$$\text{Minimize } Z = 4x_1 + x_2$$

Subject to:
$$3x_1 + x_2 = 3$$
$$4x_1 + 3x_2 \ge 6$$
$$x_1 + 2x_2 \le 4$$
$$x_1, x_2 \ge 0$$

### Key Features
* Standard form conversion using slack, surplus, and artificial variables.
* Iterative tableau pivoting and reduced-cost evaluation ($z_j - c_j$).
* Minimum ratio test to avoid infeasibility and detect unboundedness.

---

## 2. Transportation Optimization (VAM & MODI)

Solves balanced transportation problems to find the minimum cost allocation of goods from sources to destinations.

### Methodologies
* **Vogel's Approximation Method (VAM):** Computes row and column opportunity penalties to generate a high-quality Initial Basic Feasible Solution (IBFS).
* **Modified Distribution (MODI / $u\text{-}v$ Method):** Dual-variable evaluation ($u_i + v_j = c_{ij}$) to test for optimality, followed by loop tracing to shift allocations along basic cells until optimal.

### Problem Instance
* **Sources ($S_1, S_2, S_3$):** Supply = $[7, 9, 18]$
* **Destinations ($D_1, D_2, D_3, D_4$):** Demand = $[5, 8, 7, 14]$
* **Cost Matrix:**
  $$\begin{bmatrix} 19 & 30 & 50 & 10 \\ 70 & 30 & 40 & 60 \\ 40 & 8 & 70 & 20 \end{bmatrix}$$

---

## Setup & Execution

### Prerequisites
* Python 3.8+
* NumPy

```bash
pip install numpy