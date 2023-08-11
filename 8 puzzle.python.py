from queue import PriorityQueue

class PuzzleState:
    def __init__(self, puzzle, parent=None, move=None):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.g = 0 if parent is None else parent.g + 1
        self.h = self.calculate_heuristic()

    def calculate_heuristic(self):
        goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] != goal[i][j]:
                    misplaced += 1
        return misplaced

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j

    def get_neighbors(self):
        row, col = self.get_blank_position()
        neighbors = []
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_puzzle = [list(row) for row in self.puzzle]
                new_puzzle[row][col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[row][col]
                neighbors.append(PuzzleState(new_puzzle, parent=self, move=(dr, dc)))
        return neighbors

def solve_8puzzle(initial_state):
    open_set = PriorityQueue()
    open_set.put(initial_state)

    closed_set = set()

    while not open_set.empty():
        current_state = open_set.get()

        if current_state.puzzle == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            return current_state

        closed_set.add(current_state)

        for neighbor in current_state.get_neighbors():
            if neighbor not in closed_set:
                open_set.put(neighbor)

    return None

def print_solution(solution_state):
    path = []
    current = solution_state
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for i, state in enumerate(path):
        print("Move", i)
        for row in state.puzzle:
            print(row)
        print()

def main():
    initial_puzzle = []
    print("Enter the initial 3x3 puzzle configuration:")
    for _ in range(3):
        row = list(map(int, input().split()))
        initial_puzzle.append(row)

    initial_state = PuzzleState(initial_puzzle)
    solution_state = solve_8puzzle(initial_state)

    if solution_state:
        print("Solution found!")
        print_solution(solution_state)
    else:
        print("No solution exists.")

if __name__ == "__main__":
    main()
