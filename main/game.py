# game.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
import math
import random

import config
from renderer import Renderer
from maze_generator import generate_maze
from game_objects import Player, Enemy, Fireball
from pathfinding import (
    AStarPathFinder,
    BFSPathFinder,
    DFSPathFinder,
    GreedyBestFirstPathFinder
)

class Game:
    def __init__(self, maze_size=10, pathfinder=None):
        pygame.init()
        self.screen = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT), 
                                            DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Maze Game")
        
        # Initialize components
        self.renderer = Renderer()
        self.maze = generate_maze(maze_size)  # Use selected size
        self.player = Player([1.0, 1.0, 1.0])
        self.enemy = Enemy([float(maze_size - 2), 1.0, float(maze_size - 2)])
        
        # Set initial pathfinder if provided
        if pathfinder:
            self.enemy.set_pathfinder(pathfinder)
            
        self.fireballs = []
        self.game_over = False

        print("Maze layout:")
        print(self.maze)
        print(f"Player starting position: {self.player.pos}")
        print(f"Using pathfinding algorithm: {self.enemy.current_algorithm}")


    def handle_input(self):

        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    self.player.camera_mode = "near" if self.player.camera_mode == "far" else "far"
                    self.renderer.set_perspective()
                elif event.key == pygame.K_ESCAPE:
                    return True
                # AI switching controls
                elif event.key == pygame.K_1:
                    self.enemy.set_pathfinder(AStarPathFinder())
                    print("Switched to A* pathfinding")
                elif event.key == pygame.K_2:
                    self.enemy.set_pathfinder(BFSPathFinder())
                    print("Switched to BFS pathfinding")
                elif event.key == pygame.K_3:
                    self.enemy.set_pathfinder(DFSPathFinder())
                    print("Switched to DFS pathfinding")
                elif event.key == pygame.K_4:
                    self.enemy.set_pathfinder(GreedyBestFirstPathFinder())
                    print("Switched to Greedy Best-First pathfinding")

        """Handle player input"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            if self.player.camera_mode == "far":
                self.player.angle -= config.ROTATION_SPEED
            else:
                self.player.try_move(-1, 0, self.maze)  # Move left
                
        if keys[pygame.K_RIGHT]:
            if self.player.camera_mode == "far":
                self.player.angle += config.ROTATION_SPEED
            else:
                self.player.try_move(1, 0, self.maze)  # Move right
        
        if keys[pygame.K_DOWN]:
            # In both modes, move forward relative to current orientation
            dx = round(math.sin(self.player.angle))  # Round to get grid movement
            dz = round(math.cos(self.player.angle))
            self.player.try_move(dx, dz, self.maze)
            
        if keys[pygame.K_UP]:
            # Move backward relative to current orientation
            dx = -round(math.sin(self.player.angle))
            dz = -round(math.cos(self.player.angle))
            self.player.try_move(dx, dz, self.maze)


    # game.py (continued from previous code)
    def update(self):
        """Update game state"""
        current_time = pygame.time.get_ticks()
        
        # Update enemy
        self.enemy.update(current_time, self.player.pos, self.maze)
        
        # Update fireballs
        active_fireballs = []
        for fireball in self.fireballs:
            if not fireball.is_expired(current_time):
                fireball.update(self.maze)
                if fireball.check_player_collision(self.player.pos):
                    print("Hit by fireball! Game Over!")
                    self.game_over = True
                    return
                active_fireballs.append(fireball)
        self.fireballs = active_fireballs
        
        # Enemy shoots new fireballs
        if len(self.fireballs) < config.MAX_FIREBALLS and random.random() < 0.02:
            self.shoot_fireball()
        
        # Check win condition
        player_tile = (int(self.player.pos[0]), int(self.player.pos[2]))
        if self.maze[player_tile] == 2:
            print("Congratulations! You reached the exit!")
            self.game_over = True

    def shoot_fireball(self):
        """Create a new fireball shot by the enemy"""
        direction = [
            self.player.pos[0] - self.enemy.pos[0],
            0,
            self.player.pos[2] - self.enemy.pos[2]
        ]
        length = math.sqrt(direction[0]**2 + direction[2]**2)
        if length > 0:
            direction = [d/length * 0.2 for d in direction]
            self.fireballs.append(Fireball(
                self.enemy.pos.copy(),
                direction,
                pygame.time.get_ticks()
            ))

    def draw(self):
        """Draw the game scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set up camera
        self.renderer.setup_camera(self.player.pos, self.player.angle, self.player.camera_mode)
        
        # Draw floor
        for x in range(config.MAZE_SIZE):
            for z in range(config.MAZE_SIZE):
                self.renderer.draw_textured_cube(float(x), -0.5, float(z), 
                                              config.FLOOR_COLOR, True)
        
        # Draw walls and exit
        for x in range(config.MAZE_SIZE):
            for z in range(config.MAZE_SIZE):
                if self.maze[x, z] == 1:
                    for y in range(int(config.WALL_HEIGHT)):
                        self.renderer.draw_textured_cube(float(x), float(y), float(z), 
                                                      config.WALL_COLOR)
                elif self.maze[x, z] == 2:
                    self.renderer.draw_textured_cube(float(x), 0, float(z), 
                                                  config.EXIT_COLOR)
        
        # Draw player in overhead view
        if self.player.camera_mode == "far":
            self.renderer.draw_textured_cube(
                self.player.pos[0], self.player.pos[1], self.player.pos[2],
                config.PLAYER_COLOR, False, 0.3
            )
        
        # Draw enemy
        self.renderer.draw_textured_cube(
            self.enemy.pos[0], self.enemy.pos[1], self.enemy.pos[2],
            config.ENEMY_COLOR, False, 0.5
        )
        
        # Draw fireballs
        for fireball in self.fireballs:
            self.renderer.draw_textured_cube(
                fireball.pos[0], fireball.pos[1], fireball.pos[2],
                config.FIREBALL_COLOR, False, 0.2
            )

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        print("Game Started! Use arrow keys to move, 'V' to change view, ESC to quit")
        
        while not self.game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        self.player.camera_mode = "near" if self.player.camera_mode == "far" else "far"
                        self.renderer.set_perspective()
                    elif event.key == pygame.K_ESCAPE:
                        return
            
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        print("Game Over! Close the window to exit.")
        pygame.time.wait(2000)