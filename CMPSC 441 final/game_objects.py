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
        """Initialize the enemy with its starting position."""
        self.x = start_x
        self.y = start_y
        self.path = []  # Store the current path

    def move_towards(self, target, grid, pathfinding_func):
        """Move the enemy towards the target using the specified pathfinding function."""
        # If the path is empty or the target has changed, recalculate the path
        if not self.path or self.path[-1] != target:
            self.path = pathfinding_func((self.x, self.y), target, grid)


        # Move along the path if it's valid
        if self.path:
            next_position = self.path.pop(0)
            self.x, self.y = next_position
        


class GameDrawer:
    @staticmethod
    def draw_grid(screen):
        """Draw the grid lines on the screen."""
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, GRID_SIZE * CELL_SIZE))
        for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (GRID_SIZE * CELL_SIZE, y))

    @staticmethod
    def draw_game(screen, player, enemy, obstacles, goal):
        """Draw the current state of the game."""
        screen.fill(WHITE)
        GameDrawer.draw_grid(screen)
        for obs in obstacles:
            pygame.draw.rect(screen, BLACK, (obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLUE, (player.x * CELL_SIZE, player.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (enemy.x * CELL_SIZE, enemy.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
