# game_objects.py
import math
import config
from pathfinding import (
    AStarPathFinder,
    BFSPathFinder,
    DFSPathFinder,
    GreedyBestFirstPathFinder
)

class Player:
    def __init__(self, start_pos):
        # Start position should be center of tile
        self.grid_x = int(start_pos[0])  # Current grid position
        self.grid_z = int(start_pos[2])
        self.pos = [float(self.grid_x), 1.0, float(self.grid_z)]  # Actual 3D position
        self.angle = 0
        self.camera_mode = "far"
        self.is_moving = False
        
    def try_move(self, dx, dz, maze):
        """Try to move to adjacent tile"""
        if self.is_moving:  # Don't allow new movement if already moving
            return
            
        new_grid_x = self.grid_x + dx
        new_grid_z = self.grid_z + dz
        
        # Check if move is valid
        if (0 <= new_grid_x < len(maze) and 
            0 <= new_grid_z < len(maze) and 
            maze[new_grid_x, new_grid_z] != 1):  # Not a wall
            
            # Update grid position
            self.grid_x = new_grid_x
            self.grid_z = new_grid_z
            
            # Update actual position to tile center
            self.pos[0] = float(self.grid_x)
            self.pos[2] = float(self.grid_z)

class Enemy:
    def __init__(self, start_pos):
        self.pos = list(start_pos)
        self.path = []
        self.path_update_time = 0
        # Default to A* pathfinding
        self.pathfinder = AStarPathFinder()
        self.current_algorithm = "A*"
        
    def set_pathfinder(self, pathfinder):
        """Change the pathfinding algorithm"""
        self.pathfinder = pathfinder
        # Get algorithm name from class
        self.current_algorithm = pathfinder.__class__.__name__.replace('PathFinder', '')
    
    def find_path_to_player(self, player_pos, maze):
        """Find path to player using current pathfinding algorithm"""
        start = (int(self.pos[0]), int(self.pos[2]))
        goal = (int(player_pos[0]), int(player_pos[2]))
        
        path = self.pathfinder.find_path(maze, start, goal)
        return [(float(x), float(y)) for x, y in path]

    def update(self, current_time, player_pos, maze):
        """Update enemy position and path"""
        if current_time - self.path_update_time > config.PATH_UPDATE_INTERVAL:
            self.path = self.find_path_to_player(player_pos, maze)
            self.path_update_time = current_time
        
        if self.path:
            next_pos = self.path[0]
            dx = next_pos[0] - self.pos[0]
            dz = next_pos[1] - self.pos[2]
            dist = math.sqrt(dx*dx + dz*dz)
            
            if dist < 0.1:
                self.path.pop(0)
            else:
                speed = 0.05
                self.pos[0] += (dx/dist) * speed
                self.pos[2] += (dz/dist) * speed

class Fireball:
    def __init__(self, pos, velocity, creation_time):
        self.pos = list(pos)
        self.velocity = velocity
        self.creation_time = creation_time

    def update(self, maze):
        """Update fireball position and handle bouncing"""
        self.pos = [p + v for p, v in zip(self.pos, self.velocity)]
        
        # Check wall collision and bounce
        x, z = int(self.pos[0]), int(self.pos[2])
        if 0 <= x < len(maze) and 0 <= z < len(maze):
            if maze[x, z] == 1:
                self.velocity = [-v for v in self.velocity]

    def is_expired(self, current_time):
        """Check if fireball has exceeded its lifetime"""
        return current_time - self.creation_time >= config.FIREBALL_LIFETIME

    def check_player_collision(self, player_pos):
        """Check if fireball has hit player"""
        return (abs(self.pos[0] - player_pos[0]) < 0.5 and
                abs(self.pos[2] - player_pos[2]) < 0.5)