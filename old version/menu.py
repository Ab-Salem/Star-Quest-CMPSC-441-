# menu.py
import pygame
import sys
from pathfinding import AStarPathFinder, BFSPathFinder, DFSPathFinder, GreedyBestFirstPathFinder

class Menu:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = (800, 600)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("3D Maze Game - Menu")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.HIGHLIGHT = (100, 100, 255)
        
        # Font
        self.title_font = pygame.font.Font(None, 74)
        self.font = pygame.font.Font(None, 48)
        
        # Menu options
        self.algorithms = [
            ("A* Search", AStarPathFinder),
            ("Breadth-First Search", BFSPathFinder),
            ("Depth-First Search", DFSPathFinder),
            ("Greedy Best-First", GreedyBestFirstPathFinder)
        ]
        self.maze_sizes = [
            ("Small (Easy) - 10x10", 10),
            ("Medium - 15x15", 15),
            ("Large (Hard) - 20x20", 20)
        ]
        
        self.selected_algorithm = 0
        self.selected_size = 0

    def draw_text(self, text, font, color, x, y, selected=False):
        background_color = self.HIGHLIGHT if selected else None
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        if background_color:
            padding = 10
            background_rect = pygame.Rect(text_rect.left - padding,
                                        text_rect.top - padding,
                                        text_rect.width + 2*padding,
                                        text_rect.height + 2*padding)
            pygame.draw.rect(self.screen, background_color, background_rect, border_radius=5)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.screen.fill(self.BLACK)
            
            # Draw title
            self.draw_text("3D Maze Game", self.title_font, self.WHITE, 
                          self.WINDOW_SIZE[0] // 2, 80)
            
            # Draw algorithm selection text
            self.draw_text("Select Enemy AI Algorithm:", self.font, self.WHITE, 
                          self.WINDOW_SIZE[0] // 2, 180)
            
            # Draw algorithm options
            for i, (algo_name, _) in enumerate(self.algorithms):
                y_pos = 240 + i * 50
                self.draw_text(algo_name, self.font, self.WHITE,
                             self.WINDOW_SIZE[0] // 2, y_pos,
                             selected=(i == self.selected_algorithm))
            
            # Draw maze size selection text
            '''
            self.draw_text("Select Maze Size:", self.font, self.WHITE,
                          self.WINDOW_SIZE[0] // 2, 420)
            
            # Draw maze size options
            for i, (size_name, _) in enumerate(self.maze_sizes):
                y_pos = 480 + i * 50
                self.draw_text(size_name, self.font, self.WHITE,
                             self.WINDOW_SIZE[0] // 2, y_pos,
                             selected=(i == self.selected_size))
            '''
                
            # Draw start instructions
            self.draw_text("Press ENTER to Start", self.font, self.GRAY,
                          self.WINDOW_SIZE[0] // 2, 550)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.selected_size = (self.selected_size - 1) % len(self.maze_sizes)
                        else:
                            self.selected_algorithm = (self.selected_algorithm - 1) % len(self.algorithms)
                    elif event.key == pygame.K_DOWN:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.selected_size = (self.selected_size + 1) % len(self.maze_sizes)
                        else:
                            self.selected_algorithm = (self.selected_algorithm + 1) % len(self.algorithms)
                    elif event.key == pygame.K_RETURN:
                        # Return selected options
                        selected_algo = self.algorithms[self.selected_algorithm][1]
                        selected_size = self.maze_sizes[self.selected_size][1]
                        return selected_algo, selected_size
            
            pygame.display.flip()
            clock.tick(60)