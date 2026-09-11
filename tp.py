import numpy as np

def vogel_approximation(costs, supply, demand):
    supply = supply.copy().astype(float)
    demand = demand.copy().astype(float)
    costs = costs.copy().astype(float)
    
    m, n = costs.shape
    allocation = np.zeros((m, n))
    row_active = [True] * m
    col_active = [True] * n
    
    while sum(row_active) > 0 and sum(col_active) > 0:
        row_penalties = []
        for i in range(m):
            if not row_active[i]:
                row_penalties.append(-1)
                continue
            valid = [costs[i, j] for j in range(n) if col_active[j]]
            if len(valid) > 1:
                s = sorted(valid)
                row_penalties.append(s[1] - s[0])
            elif len(valid) == 1:
                row_penalties.append(valid[0])
            else:
                row_penalties.append(-1)
                
        col_penalties = []
        for j in range(n):
            if not col_active[j]:
                col_penalties.append(-1)
                continue
            valid = [costs[i, j] for i in range(m) if row_active[i]]
            if len(valid) > 1:
                s = sorted(valid)
                col_penalties.append(s[1] - s[0])
            elif len(valid) == 1:
                col_penalties.append(valid[0])
            else:
                col_penalties.append(-1)
                
        max_row_pen = max(row_penalties)
        max_col_pen = max(col_penalties)
        
        if max_row_pen >= max_col_pen:
            row_idx = row_penalties.index(max_row_pen)
            col_candidates = [(costs[row_idx, j], j) for j in range(n) if col_active[j]]
            col_candidates.sort()
            col_idx = col_candidates[0][1]
        else:
            col_idx = col_penalties.index(max_col_pen)
            row_candidates = [(costs[i, col_idx], i) for i in range(m) if row_active[i]]
            row_candidates.sort()
            row_idx = row_candidates[0][1]
            
        alloc = min(supply[row_idx], demand[col_idx])
        allocation[row_idx, col_idx] = alloc
        supply[row_idx] -= alloc
        demand[col_idx] -= alloc
        
        if supply[row_idx] == 0:
            row_active[row_idx] = False
        if demand[col_idx] == 0:
            col_active[col_idx] = False
            
    return allocation

def find_loop(start, occupied):
    def get_neighbors(node, direction):
        r, c = node
        neighbors = []
        if direction == 'H':
            for (nr, nc) in occupied:
                if nr == r and nc != c:
                    neighbors.append((nr, nc))
        else:
            for (nr, nc) in occupied:
                if nc == c and nr != r:
                    neighbors.append((nr, nc))
        return neighbors

    def dfs(curr, path, direction):
        if len(path) >= 4 and curr == start:
            return path[:-1]
        next_dir = 'V' if direction == 'H' else 'H'
        for neighbor in get_neighbors(curr, direction):
            if neighbor == start and len(path) >= 4:
                return path
            if neighbor not in path:
                res = dfs(neighbor, path + [neighbor], next_dir)
                if res is not None:
                    return res
        return None

    res = dfs(start, [start], 'H')
    if res is None:
        res = dfs(start, [start], 'V')
    return res

def modi_method(costs, allocation):
    m, n = costs.shape
    costs = costs.astype(float)
    
    while True:
        occupied = list(zip(*np.where(allocation > 1e-9)))
        
        if len(occupied) < m + n - 1:
            for i in range(m):
                for j in range(n):
                    if (i, j) not in occupied:
                        occupied.append((i, j))
                        if len(occupied) == m + n - 1:
                            break
                if len(occupied) == m + n - 1:
                    break
                    
        u = [None] * m
        v = [None] * n
        u[0] = 0.0
        
        changed = True
        while changed:
            changed = False
            for (i, j) in occupied:
                if u[i] is not None and v[j] is None:
                    v[j] = costs[i, j] - u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = costs[i, j] - v[j]
                    changed = True

        deltas = np.zeros((m, n))
        min_delta = 0
        entering_cell = None
        
        for i in range(m):
            for j in range(n):
                if (i, j) not in occupied:
                    u_val = u[i] if u[i] is not None else 0.0
                    v_val = v[j] if v[j] is not None else 0.0
                    deltas[i, j] = costs[i, j] - (u_val + v_val)
                    if deltas[i, j] < min_delta:
                        min_delta = deltas[i, j]
                        entering_cell = (i, j)
                        
        if min_delta >= -1e-5 or entering_cell is None:
            break
            
        loop = find_loop(entering_cell, occupied + [entering_cell])
        if not loop:
            break
            
        minus_cells = [loop[k] for k in range(1, len(loop), 2)]
        theta = min(allocation[r, c] for (r, c) in minus_cells)
        
        for idx, (r, c) in enumerate(loop):
            if idx % 2 == 0:
                allocation[r, c] += theta
            else:
                allocation[r, c] -= theta

    total_cost = np.sum(allocation * costs)
    return allocation, total_cost

if __name__ == "__main__":
    costs = np.array([
        [19, 30, 50, 10],
        [70, 30, 40, 60],
        [40,  8, 70, 20]
    ])
    supply = np.array([7, 9, 18])
    demand = np.array([5, 8, 7, 14])

    initial_alloc = vogel_approximation(costs, supply, demand)
    initial_cost = np.sum(initial_alloc * costs)
    
    print("Initial Allocation Matrix:\n", initial_alloc)
    print(f"Initial Feasible Cost: {initial_cost}\n")

    opt_alloc, opt_cost = modi_method(costs, initial_alloc.copy())
    print("Optimal Allocation Matrix:\n", opt_alloc)
    print(f"Minimum Transportation Cost: {opt_cost}")