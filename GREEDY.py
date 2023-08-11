from collections import defaultdict, deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        print(node, end=" ")
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

def create_graph():
    graph = defaultdict(list)
    num_edges = int(input("Enter the number of edges: "))
    
    for _ in range(num_edges):
        source, destination = input("Enter source and destination separated by spaces: ").split()
        graph[source].append(destination)
        graph[destination].append(source)  # Assuming an undirected graph
    
    return graph

def main():
    graph = create_graph()
    start_node = input("Enter the start node: ")
    
    print("\nBreadth-First Search:")
    bfs(graph, start_node)

if __name__ == "__main__":
    main()
