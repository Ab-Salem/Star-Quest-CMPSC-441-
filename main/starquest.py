import pygame
import heapq
import math
import random
import time

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 50
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Grid Game")
clock = pygame.time.Clock()

# Draw Text Helper Function
def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Difficulty Selection Menu
def difficulty_menu():
    font = pygame.font.Font(None, 50)
    running = True
    while running:
        screen.fill(BLACK)

        # Draw menu options
        draw_text(screen, "Select Difficulty", font, WHITE, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "1. Easy", font, GREEN, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(screen, "2. Medium", font, YELLOW, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "3. Hard", font, RED, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    return 13, 50  # enemy_cooldown, maze_change_interval
                elif event.key == pygame.K_2:  # Medium
                    return 9, 35
                elif event.key == pygame.K_3:  # Hard
                    return 5, 20

# Initialize difficulty
enemy_cooldown, maze_change_interval = difficulty_menu()
last_maze_change_time = time.time()  # Record the last time the maze was updated

# Grid Representation
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Maze Generation
def generate_maze(grid_size):
    maze = [[1 for _ in range(grid_size)] for _ in range(grid_size)]

    def carve(x, y):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < grid_size and 0 < ny < grid_size and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                maze[ny][nx] = 0
                carve(nx, ny)

    maze[1][1] = 0
    carve(1, 1)

    # Add extra paths for multiple solutions
    extra_paths = random.randint(grid_size // 5, grid_size // 3)
    for _ in range(extra_paths):
        x = random.randint(1, grid_size - 2)
        y = random.randint(1, grid_size - 2)
        if maze[y][x] == 1:
            maze[y][x] = 0

    return maze

# Generate initial maze
maze = generate_maze(GRID_SIZE)

# Convert maze to obstacle coordinates
obstacles = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if maze[y][x] == 1]
for obs in obstacles:
    grid[obs[1]][obs[0]] = 1

# Start, Goal, Player, and Enemy
start = (1, 1)
goal = (49, 49)
player = list(start)
enemy = [1, 48]

# Enemy Counter
enemy_counter = 0

# A* Pathfinding
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# Draw Game
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_game():
    screen.fill(WHITE)
    draw_grid()
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, (obs[0] * CELL_SIZE, obs[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (player[0] * CELL_SIZE, player[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (enemy[0] * CELL_SIZE, enemy[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player[1] > 0 and grid[player[1] - 1][player[0]] == 0:
        player[1] -= 1
    if keys[pygame.K_DOWN] and player[1] < GRID_SIZE - 1 and grid[player[1] + 1][player[0]] == 0:
        player[1] += 1
    if keys[pygame.K_LEFT] and player[0] > 0 and grid[player[1]][player[0] - 1] == 0:
        player[0] -= 1
    if keys[pygame.K_RIGHT] and player[0] < GRID_SIZE - 1 and grid[player[1]][player[0] + 1] == 0:
        player[0] += 1

    # Enemy movement with cooldown
    enemy_counter += 1
    if enemy_counter >= enemy_cooldown:
        path = a_star_search(tuple(enemy), tuple(player), grid)
        if path:
            enemy = list(path[0])
        enemy_counter = 0

    # Regenerate maze
    current_time = time.time()
    if current_time - last_maze_change_time >= maze_change_interval:
        maze = generate_maze(GRID_SIZE)
        obstacles.clear()
        obstacles.extend([(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if maze[y][x] == 1])
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                grid[y][x] = maze[y][x]
        grid[player[1]][player[0]] = 0
        grid[enemy[1]][enemy[0]] = 0
        last_maze_change_time = current_time

    if player == list(goal):
        print("You Win!")
        running = False
    if player == enemy:
        print("You Lose!")
        running = False

    draw_game()
    pygame.display.flip()
    clock.tick(FPS)
