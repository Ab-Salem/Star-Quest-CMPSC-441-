# maze_generator.py
import numpy as np
import random

def generate_maze(size):
    """Generate a maze using recursive backtracking"""
    maze = np.ones((size, size), dtype=int)
    
    def carve_path(x, y):
        maze[x, y] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < size and 0 <= new_y < size and 
                maze[new_x, new_y] == 1):
                maze[x + dx//2, y + dy//2] = 0
                carve_path(new_x, new_y)
    
    # Start from position (1,1)
    carve_path(1, 1)
    
    # Set start and end points
    maze[1, 1] = 0  # Start
    maze[size-2, size-2] = 2  # Exit
    
    return maze