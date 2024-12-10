# main.py
import pygame
import time
from constants import *
from generated_maze import regenerate_maze
from game_objects import Player, Enemy, GameDrawer
from menu import algorithm_menu, difficulty_menu, show_end_screen
from pathfinding import a_star_search, bfs, dfs, greedy

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Grid Game")
clock = pygame.time.Clock()

def main():
    # Display the menus and get user choices
    algorithm_name = algorithm_menu(screen)
    difficulty = difficulty_menu(screen)

    # Map difficulty to max_depth
    difficulty_levels = {
        "easy": 500,  # Limited depth for easy
        "medium": 750,  # Moderate depth for medium
        "hard": float("inf"),  # Unlimited depth for hard
    }
    max_depth = difficulty_levels[difficulty]
    print(f"Selected Algorithm: {algorithm_name}, Difficulty: {difficulty}, Max Depth: {max_depth}")

    # Map algorithm name to function
    algorithms = {
        "a_star_search": lambda start, goal, grid: a_star_search(start, goal, grid, max_depth),
        "bfs": lambda start, goal, grid: bfs(start, goal, grid, max_depth),
        "dfs": lambda start, goal, grid: dfs(start, goal, grid, max_depth),
        "greedy": lambda start, goal, grid: greedy(start, goal, grid, max_depth),
    }

    enemy_algorithm = algorithms[algorithm_name]

    while True:  # Main game loop for restart functionality
        # Generate initial maze and grid
        player_start = (1, 1)
        enemy_start = (1, 48)
        maze, grid, obstacles = regenerate_maze(GRID_SIZE, player_start, enemy_start)

        # Initialize Player, Enemy, and Goal
        player = Player(*player_start)
        enemy = Enemy(*enemy_start)
        goal = (49, 49)

        last_maze_change_time = time.time()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            # Delegate player movement handling to Player class
            player.handle_movement(grid)

            # Handle enemy movement
            enemy.move_towards((player.x, player.y), grid, enemy_algorithm)

            # Check win/lose conditions
            if (player.x, player.y) == (enemy.x, enemy.y):
                if show_end_screen(screen, "You Lose!"):
                    break  # Restart the game

            if (player.x, player.y) == goal:
                if show_end_screen(screen, "You Win!"):
                    break  # Restart the game

            # Regenerate maze if the interval has passed
            current_time = time.time()
            if current_time - last_maze_change_time >= 35:  # Maze changes every 50 seconds
                maze, grid, obstacles = regenerate_maze(GRID_SIZE, (player.x, player.y), (enemy.x, enemy.y))
                last_maze_change_time = current_time

            # Draw game
            GameDrawer.draw_game(screen, player, enemy, obstacles, goal)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
