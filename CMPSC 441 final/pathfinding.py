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
    queue = deque([(start, 0)])  # Track depth with each node
    came_from = {start: None}

    while queue:
        current, depth = queue.popleft()

        if depth >= max_depth:
            break  # Stop if depth exceeds max_depth

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid)
                    and grid[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from):
                came_from[neighbor] = current
                queue.append((neighbor, depth + 1))
    return []  # Return an incomplete path


def dfs(start, goal, grid, max_depth=float("inf")):
    """Perform DFS to find a path with limited depth."""
    stack = [(start, 0)]  # Track depth with each node
    came_from = {start: None}

    while stack:
        current, depth = stack.pop()

        if depth >= max_depth:
            continue  # Skip nodes beyond max_depth

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid)
                    and grid[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from):
                came_from[neighbor] = current
                stack.append((neighbor, depth + 1))
    return []  # Return an incomplete path


def greedy(start, goal, grid, max_depth=float("inf")):
    """Perform Greedy Best-First Search to find a path with limited depth."""
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    steps = 0

    while open_set and steps < max_depth:
        _, current = heapq.heappop(open_set)
        steps += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid)
                    and grid[neighbor[1]][neighbor[0]] == 0 and neighbor not in came_from):
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))
    return []  # Return an incomplete path

