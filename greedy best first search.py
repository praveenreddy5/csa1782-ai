from queue import PriorityQueue

def greedy_best_first_search(graph, start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start))

    while not queue.empty():
        cost, node = queue.get()
        if node == goal:
            return True
        
        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    queue.put((edge_cost, neighbor))
    
    return False

# Example graph
graph = {
    'A': [('B', 5), ('C', 3)],
    'B': [('D', 2)],
    'C': [('E', 4)],
    'D': [('F', 6)],
    'E': [],
    'F': [('G', 1)],
    'G': []
}

start_node = 'A'
goal_node = 'G'

if greedy_best_first_search(graph, start_node, goal_node):
    print("Goal reached!")
else:
    print("Goal not reached.")
