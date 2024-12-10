# generated_maze.py
import random

def generate_maze(grid_size):
    """Generate a new maze."""
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

def regenerate_maze(grid_size, player_pos, enemy_pos):
    """
    Regenerate the maze and update the grid and obstacles list.

    Parameters:
    - grid_size: The size of the grid
    - player_pos: Tuple of (x, y) for the player's position
    - enemy_pos: Tuple of (x, y) for the enemy's position

    Returns:
    - A tuple containing:
        - Updated maze (2D list)
        - Updated grid (2D list)
        - List of obstacle positions
    """
    maze = generate_maze(grid_size)
    grid = [[maze[y][x] for x in range(grid_size)] for y in range(grid_size)]
    obstacles = [(x, y) for y in range(grid_size) for x in range(grid_size) if maze[y][x] == 1]

    # Ensure the player and enemy positions are walkable
    grid[player_pos[1]][player_pos[0]] = 0
    grid[enemy_pos[1]][enemy_pos[0]] = 0

    return maze, grid, obstacles
