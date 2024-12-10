# pathfinding.py
from abc import ABC, abstractmethod
import heapq
from collections import deque
import math

class PathFinder(ABC):
    @abstractmethod
    def find_path(self, maze, start, goal):
        """Find a path from start to goal in the maze"""
        pass

class AStarPathFinder(PathFinder):
    def heuristic(self, a, b):
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, maze, start, goal):
        """A* pathfinding algorithm"""
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal:
                break
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if (0 <= next_pos[0] < len(maze) and 
                    0 <= next_pos[1] < len(maze) and 
                    maze[next_pos[0]][next_pos[1]] != 1):
                    
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + self.heuristic(goal, next_pos)
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current
        
        # Reconstruct path
        path = []
        current = goal
        while current in came_from and current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

class BFSPathFinder(PathFinder):
    def find_path(self, maze, start, goal):
        """Breadth-First Search pathfinding"""
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if current == goal:
                return path[1:]  # Exclude start position
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if (0 <= next_pos[0] < len(maze) and 
                    0 <= next_pos[1] < len(maze) and 
                    maze[next_pos[0]][next_pos[1]] != 1 and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    queue.append((next_pos, new_path))
        
        return []

class DFSPathFinder(PathFinder):
    def find_path(self, maze, start, goal):
        """Depth-First Search pathfinding"""
        stack = [(start, [start])]
        visited = {start}
        
        while stack:
            current, path = stack.pop()
            
            if current == goal:
                return path[1:]  # Exclude start position
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if (0 <= next_pos[0] < len(maze) and 
                    0 <= next_pos[1] < len(maze) and 
                    maze[next_pos[0]][next_pos[1]] != 1 and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    new_path = list(path)
                    new_path.append(next_pos)
                    stack.append((next_pos, new_path))
        
        return []

class GreedyBestFirstPathFinder(PathFinder):
    def heuristic(self, a, b):
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, maze, start, goal):
        """Greedy Best-First Search pathfinding"""
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start, goal), start))
        came_from = {start: None}
        
        while frontier:
            _, current = heapq.heappop(frontier)
            
            if current == goal:
                break
                
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                
                if (0 <= next_pos[0] < len(maze) and 
                    0 <= next_pos[1] < len(maze) and 
                    maze[next_pos[0]][next_pos[1]] != 1 and 
                    next_pos not in came_from):
                    priority = self.heuristic(next_pos, goal)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current
        
        # Reconstruct path
        path = []
        current = goal
        while current in came_from and current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path