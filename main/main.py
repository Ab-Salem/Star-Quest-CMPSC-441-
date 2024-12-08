# main.py
import sys
import pygame
from game import Game
from menu import Menu

def main():
    try:
        # Start with menu
        menu = Menu()
        pathfinder_class, maze_size = menu.run()
        
        # Initialize and run game with selected options
        game = Game(maze_size=maze_size, pathfinder=pathfinder_class())
        game.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()