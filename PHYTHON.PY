import heapq

class Node:
    def _init_(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def _lt_(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def a_star_search(initial_state, goal_test, successors, heuristic):
    open_list = []
    heapq.heappush(open_list, Node(initial_state, cost=0, heuristic=heuristic(initial_state)))

    while open_list:
        current_node = heapq.heappop(open_list)

        if goal_test(current_node.state):
            path = []
            while current_node:
                path.insert(0, current_node.action)
                current_node = current_node.parent
            return path

        for action, next_state, cost in successors(current_node.state):
            new_cost = current_node.cost + cost
            new_node = Node(next_state, parent=current_node, action=action, cost=new_cost, heuristic=heuristic(next_state))
            heapq.heappush(open_list, new_node)

    return None

# Example usage
def goal_test(state):
    return state == "Goal"

def successors(state):
    # Define your successor function here
    pass

def heuristic(state):
    # Define your heuristic function here
    pass

initial_state = "Start"
path = a_star_search(initial_state, goal_test, successors, heuristic)
print(path)
