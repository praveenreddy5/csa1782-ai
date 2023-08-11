from heapq import heappop, heappush

# Define the goal state and the initial state
goal_state = ((1, 2, 3), (8, 0, 4), (7, 6, 5))
initial_state = ((2, 8, 3), (1, 6, 4), (7, 0, 5))

# Define the possible moves
moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

# Heuristic function (Manhattan distance)
def heuristic(state):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            num = state[i][j]
            if num != 0:
                goal_i, goal_j = divmod(num - 1, 3)
                total_distance += abs(i - goal_i) + abs(j - goal_j)
    return total_distance

# A* algorithm
def solve(initial_state, goal_state):
    open_list = [(heuristic(initial_state), 0, initial_state)]
    closed_set = set()

    while open_list:
        _, cost, current_state = heappop(open_list)
        if current_state == goal_state:
            return cost

        if current_state in closed_set:
            continue
        closed_set.add(current_state)

        empty_i, empty_j = [(i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0][0]

        for di, dj in moves:
            new_i, new_j = empty_i + di, empty_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [list(row) for row in current_state]
                new_state[empty_i][empty_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[empty_i][empty_j]
                heappush(open_list, (cost + heuristic(new_state), cost + 1, tuple(map(tuple, new_state))))

    return None

# Main function
def main():
    steps = solve(initial_state, goal_state)
    if steps is None:
        print("No solution found.")
    else:
        print(f"Solution found in {steps} steps.")

if _name_ == "_main_":
    main()
