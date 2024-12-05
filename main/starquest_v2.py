import pygame
import heapq
import math
import random
import time

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
GRID_SIZE = 50
TILE_SIZE = WINDOW_WIDTH // GRID_SIZE
PLAYER_SIZE = TILE_SIZE - 2
MOVEMENT_SPEED = 2
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def difficulty_menu():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Select Difficulty")
    font = pygame.font.Font(None, 50)
    
    running = True
    while running:
        screen.fill(BLACK)
        draw_text(screen, "Select Difficulty", font, WHITE, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
        draw_text(screen, "1. Easy", font, GREEN, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        draw_text(screen, "2. Medium", font, YELLOW, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        draw_text(screen, "3. Hard", font, RED, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 13, 50
                elif event.key == pygame.K_2:
                    return 9, 35
                elif event.key == pygame.K_3:
                    return 5, 20

class Fireball:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 5
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.size = 10

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)

class Game:
    def __init__(self, enemy_cooldown, maze_change_interval):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Enhanced Maze Game")
        self.clock = pygame.time.Clock()
        
        self.enemy_cooldown = enemy_cooldown
        self.maze_change_interval = maze_change_interval
        self.last_maze_change_time = time.time()
        
        self.player_x = TILE_SIZE
        self.player_y = TILE_SIZE
        self.player_grid_pos = [1, 1]
        
        self.enemy_x = TILE_SIZE * (GRID_SIZE - 2)
        self.enemy_y = TILE_SIZE
        self.enemy_grid_pos = [GRID_SIZE - 2, 1]
        
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.fireballs = []
        self.last_fireball_time = time.time()
        
        self.player_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.player_img.fill(BLUE)
        self.enemy_img = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.enemy_img.fill(RED)
        
        self.goal_pos = [GRID_SIZE - 2, GRID_SIZE - 2]
        
        self.generate_maze()

    def generate_maze(self):
        def create_walls():
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if random.random() < 0.3:
                        if (not (i == 1 and j == 1) and
                            not (i == GRID_SIZE-2 and j == GRID_SIZE-2) and
                            not (i == GRID_SIZE-2 and j == 1)):
                            self.grid[i][j] = 1

        for i in range(GRID_SIZE):
            self.grid[0][i] = 1
            self.grid[GRID_SIZE-1][i] = 1
            self.grid[i][0] = 1
            self.grid[i][GRID_SIZE-1] = 1

        create_walls()
        self.ensure_path_exists()

    def ensure_path_exists(self):
        def create_path(start, end):
            x1, y1 = start
            x2, y2 = end
            
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.grid[y1][x] = 0
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.grid[y][x2] = 0

        create_path((1, 1), (GRID_SIZE-2, 1))
        create_path((GRID_SIZE-2, 1), (GRID_SIZE-2, GRID_SIZE-2))

    def check_collision(self, x, y):
        points_to_check = [
            (x, y),
            (x + PLAYER_SIZE, y),
            (x, y + PLAYER_SIZE),
            (x + PLAYER_SIZE, y + PLAYER_SIZE)
        ]
        
        for px, py in points_to_check:
            grid_x = int(px // TILE_SIZE)
            grid_y = int(py // TILE_SIZE)
            if grid_x >= GRID_SIZE or grid_y >= GRID_SIZE or self.grid[grid_y][grid_x] == 1:
                return True
        return False

    def handle_player_movement(self, keys):
        new_x = self.player_x
        new_y = self.player_y
        
        if keys[pygame.K_LEFT]:
            new_x -= MOVEMENT_SPEED
        if keys[pygame.K_RIGHT]:
            new_x += MOVEMENT_SPEED
        if keys[pygame.K_UP]:
            new_y -= MOVEMENT_SPEED
        if keys[pygame.K_DOWN]:
            new_y += MOVEMENT_SPEED

        if not self.check_collision(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            self.player_grid_pos = [int(self.player_x // TILE_SIZE),
                                  int(self.player_y // TILE_SIZE)]

    def update_enemy(self):
        if pygame.time.get_ticks() % 30 == 0:
            dx = self.player_grid_pos[0] - self.enemy_grid_pos[0]
            dy = self.player_grid_pos[1] - self.enemy_grid_pos[1]
            
            new_x = self.enemy_x
            new_y = self.enemy_y
            
            if abs(dx) > abs(dy):
                new_x += MOVEMENT_SPEED * (1 if dx > 0 else -1)
            else:
                new_y += MOVEMENT_SPEED * (1 if dy > 0 else -1)
                
            if not self.check_collision(new_x, new_y):
                self.enemy_x = new_x
                self.enemy_y = new_y
                self.enemy_grid_pos = [int(self.enemy_x // TILE_SIZE),
                                     int(self.enemy_y // TILE_SIZE)]

        current_time = time.time()
        if current_time - self.last_fireball_time >= self.enemy_cooldown/10:
            self.fireballs.append(Fireball(self.enemy_x + PLAYER_SIZE/2,
                                         self.enemy_y + PLAYER_SIZE/2,
                                         self.player_x + PLAYER_SIZE/2,
                                         self.player_y + PLAYER_SIZE/2))
            self.last_fireball_time = current_time

    def update_fireballs(self):
        for fireball in self.fireballs[:]:
            fireball.move()
            grid_x = int(fireball.x // TILE_SIZE)
            grid_y = int(fireball.y // TILE_SIZE)
            if (fireball.x < 0 or fireball.x > WINDOW_WIDTH or
                fireball.y < 0 or fireball.y > WINDOW_HEIGHT or
                (0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and
                 self.grid[grid_y][grid_x] == 1)):
                self.fireballs.remove(fireball)
                continue
            
            if (abs(fireball.x - (self.player_x + PLAYER_SIZE/2)) < PLAYER_SIZE/2 and
                abs(fireball.y - (self.player_y + PLAYER_SIZE/2)) < PLAYER_SIZE/2):
                return True
        return False

    def draw(self):
        self.screen.fill(WHITE)
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 1:
                    wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                                         TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, BLACK, wall_rect)
        
        goal_rect = pygame.Rect(self.goal_pos[0] * TILE_SIZE, self.goal_pos[1] * TILE_SIZE,
                              TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(self.screen, GREEN, goal_rect)

        self.screen.blit(self.player_img, (self.player_x, self.player_y))
        self.screen.blit(self.enemy_img, (self.enemy_x, self.enemy_y))
        
        for fireball in self.fireballs:
            fireball.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.handle_player_movement(keys)
            self.update_enemy()
            
            current_time = time.time()
            if current_time - self.last_maze_change_time >= self.maze_change_interval:
                self.generate_maze()
                self.last_maze_change_time = current_time
            
            if self.update_fireballs():
                print("Game Over - Hit by fireball!")
                running = False
                
            if (self.player_grid_pos == self.goal_pos):
                print("You Win!")
                running = False

            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    enemy_cooldown, maze_change_interval = difficulty_menu()
    game = Game(enemy_cooldown, maze_change_interval)
    game.run()