# game_objects.py
import pygame
from constants import GRID_SIZE, CELL_SIZE, WHITE, GRAY, BLACK, BLUE, RED, GREEN
from pathfinding import a_star_search, bfs, dfs, greedy

class Player:
    def __init__(self, start_x, start_y):
        """Initialize the player with its starting position."""
        self.x = start_x
        self.y = start_y

    def move(self, dx, dy, grid):
        """Move the player within the grid if the target cell is valid."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            if grid[self.y + dy][self.x + dx] == 0:
                self.x += dx
                self.y += dy

    def handle_movement(self, grid):
        """Handle player movement based on key presses."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move(0, -1, grid)
        if keys[pygame.K_DOWN]:
            self.move(0, 1, grid)
        if keys[pygame.K_LEFT]:
            self.move(-1, 0, grid)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0, grid)

class Enemy:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.path = []
        self.last_move_time = 0
        self.move_cooldown = 1.0
        self.visibility_range = 40
        self.is_pursuing = False
        self.patrol_direction = (1, 0)

    def is_player_visible(self, player_pos, grid):
        """Check if player is within visibility range using Euclidean distance."""
        player_x, player_y = player_pos
        
        # Calculate direct distance to player
        dx = self.x - player_x
        dy = self.y - player_y
        distance = (dx * dx + dy * dy) ** 0.5  # Euclidean distance
        
        return distance <= self.visibility_range

    def patrol(self, grid):
        """Simple patrol movement."""
        import time
        current_time = time.time()
        
        if current_time - self.last_move_time < self.move_cooldown:
            return

        # Try to move in current patrol direction
        new_x = self.x + self.patrol_direction[0]
        new_y = self.y + self.patrol_direction[1]

        # If can't move in current direction, try other directions
        if not (0 <= new_x < len(grid) and 
                0 <= new_y < len(grid) and 
                grid[new_y][new_x] == 0):
            # Try each direction in order: right, down, left, up
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy
                if (0 <= new_x < len(grid) and 
                    0 <= new_y < len(grid) and 
                    grid[new_y][new_x] == 0):
                    self.patrol_direction = (dx, dy)
                    break

        # Move in the chosen direction
        if (0 <= new_x < len(grid) and 
            0 <= new_y < len(grid) and 
            grid[new_y][new_x] == 0):
            self.x = new_x
            self.y = new_y
            self.last_move_time = current_time

    def move_towards(self, target, grid, pathfinding_func):
        """Move the enemy based on whether it can see the player."""
        # Check if player is visible
        player_visible = self.is_player_visible(target, grid)
        
        if player_visible:
            # Switch to pursuit mode
            if not self.is_pursuing:
                print("Player detected! Switching to pursuit mode")  # Debug print
            self.is_pursuing = True
            
            # Use the chosen pathfinding algorithm to pursue
            new_path = pathfinding_func((self.x, self.y), target, grid)
            if new_path:
                self.path = new_path
                if self.path:
                    next_position = self.path.pop(0)
                    self.x, self.y = next_position
        else:
            # Switch back to patrol mode
            if self.is_pursuing:
                print("Lost player! Returning to patrol")  # Debug print
            self.is_pursuing = False
            self.patrol(grid)

        
class GameDrawer:
    @staticmethod
    def draw_grid(screen):
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, GRID_SIZE * CELL_SIZE))
        for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (GRID_SIZE * CELL_SIZE, y))

    @staticmethod
    def draw_game(screen, player, enemy, obstacles, goal):
        # Clear screen
        screen.fill(WHITE)
        
        # Draw grid
        GameDrawer.draw_grid(screen)
        
        # Draw visibility circle
        # Convert enemy position to pixel coordinates and center it
        center_x = enemy.x * CELL_SIZE + (CELL_SIZE // 2)
        center_y = enemy.y * CELL_SIZE + (CELL_SIZE // 2)
        # Convert visibility range to pixels (20 blocks * size of each cell)
        radius = enemy.visibility_range * CELL_SIZE
        
        # Draw the circle in red instead of blue
        pygame.draw.circle(screen, (255, 0, 0, 128), (center_x, center_y), radius, 2)  # Red circle
        
        # Draw all other game elements
        for obs in obstacles:
            pygame.draw.rect(screen, BLACK, 
                           (obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, BLUE, 
                        (player.x * CELL_SIZE, player.y * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, RED, 
                        (enemy.x * CELL_SIZE, enemy.y * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, GREEN, 
                        (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, 
                         CELL_SIZE, CELL_SIZE))