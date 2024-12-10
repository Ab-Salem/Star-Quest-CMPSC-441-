# pathfinding.py
import heapq
from collections import deque

def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, grid, max_depth=float("inf")):
    """Perform A* search on the grid with a limited depth."""
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    steps = 0

    while open_set and steps < max_depth:
        _, current = heapq.heappop(open_set)
        steps += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return the path from start to goal

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid):
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return an incomplete path if depth limit is reached


def bfs(start, goal, grid, max_depth=float("inf")):
    """Perform BFS to find a path with limited depth."""
    from collections import deque

    queue = deque([(start, [start])])  # Track the path with each node
    visited = {start}
    depth = 0

    while queue and depth < max_depth:
        current, path = queue.popleft()
        depth += 1

        if current == goal:
            return path[1:]  # Return path without the start position

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            neighbor = (next_x, next_y)
            
            if (0 <= next_x < len(grid) and 
                0 <= next_y < len(grid) and 
                grid[next_y][next_x] == 0 and 
                neighbor not in visited):
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []  # Return empty path if no path found

def dfs(start, goal, grid, max_depth=float("inf")):
    """Perform DFS to find a path with limited depth."""
    stack = [(start, [start])]  # Track the path with each node
    visited = {start}
    depth = 0

    while stack and depth < max_depth:
        current, path = stack.pop()
        depth += 1

        if current == goal:
            return path[1:]  # Return path without the start position

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            neighbor = (next_x, next_y)
            
            if (0 <= next_x < len(grid) and 
                0 <= next_y < len(grid) and 
                grid[next_y][next_x] == 0 and 
                neighbor not in visited):
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    
    return []  # Return empty path if no path found

def greedy(start, goal, grid, max_depth=float("inf")):
    """Perform Greedy Best-First Search to find a path."""
    import heapq
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    pq = [(heuristic(start, goal), start, [start])]  # Include path in queue
    visited = {start}
    depth = 0

    while pq and depth < max_depth:
        _, current, path = heapq.heappop(pq)
        depth += 1

        if current == goal:
            return path[1:]  # Return path without the start position

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x = current[0] + dx
            next_y = current[1] + dy
            neighbor = (next_x, next_y)
            
            if (0 <= next_x < len(grid) and 
                0 <= next_y < len(grid) and 
                grid[next_y][next_x] == 0 and 
                neighbor not in visited):
                visited.add(neighbor)
                h = heuristic(neighbor, goal)
                heapq.heappush(pq, (h, neighbor, path + [neighbor]))
    
    return []  # Return empty path if no path found

