import numpy as np

def big_m_simplex():
    M = 1e5

    var_names = ["x1", "x2", "s1", "s2", "A1", "A2"]
    c = np.array([4.0, 1.0, 0.0, 0.0, M, M])

    A = np.array([
        [3.0, 1.0, 0.0,  0.0, 1.0, 0.0],
        [4.0, 3.0, 0.0, -1.0, 0.0, 1.0],
        [1.0, 2.0, 1.0,  0.0, 0.0, 0.0]
    ])

    b = np.array([3.0, 6.0, 4.0])

    basis = [4, 5, 2]
    num_rows, num_cols = A.shape

    iteration = 0
    max_iter = 100

    while iteration < max_iter:
        iteration += 1
        c_B = c[basis]

       
        z_c = np.dot(c_B, A) - c

        # Optimal when all reduced costs <= 0
        if np.all(z_c <= 1e-5):
            print(f"Optimal solution found in {iteration - 1} iterations.")
            break

      
        entering = np.argmax(z_c)

        col = A[:, entering]
        ratios = []

        # Minimum ratio test
        for i in range(num_rows):
            if col[i] > 1e-9:
                ratios.append(b[i] / col[i])
            else:
                ratios.append(np.inf)

        leaving = np.argmin(ratios)

        if ratios[leaving] == np.inf:
            print("Problem is unbounded.")
            return

    
        pivot = A[leaving, entering]
        A[leaving, :] /= pivot
        b[leaving] /= pivot

        for i in range(num_rows):
            if i != leaving:
                factor = A[i, entering]
                A[i, :] -= factor * A[leaving, :]
                b[i] -= factor * b[leaving]

        basis[leaving] = entering

   
    sol = np.zeros(num_cols)
    for i, idx in enumerate(basis):
        sol[idx] = b[i]

    optimal_cost = np.dot(c[:4], sol[:4])

    print("\n--- Big-M Results ---")
    for name, val in zip(var_names, sol):
        print(f"{name} = {val:.4f}")

    print(f"Optimal Value (Min Z) = {optimal_cost:.4f}")

if __name__ == "__main__":
    big_m_simplex()