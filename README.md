# Star-Quest-CMPSC-441-

This project is a simple 2D grid-based game built using Python and Pygame. Players navigate a maze while avoiding an enemy and trying to reach the goal. The game dynamically changes the maze and offers difficulty levels to provide a challenging experience.

## Features

- **Maze Generation**: Randomly generated mazes with multiple paths.
- **Dynamic Maze Changes**: Maze updates periodically, adding to the challenge.
- **A* Pathfinding**: The enemy uses the A* algorithm to pursue the player.
- **Difficulty Levels**: Choose between Easy, Medium, and Hard modes to adjust the game's challenge.

## Gameplay

- The player starts at the top-left corner of the grid and must navigate to the bottom-right corner.
- Avoid the enemy, which dynamically follows the player.
- Reach the goal before getting caught by the enemy.

## Controls

- Use arrow keys (`↑`, `↓`, `←`, `→`) to move the player.
- Avoid obstacles and the enemy to reach the goal.

## Requirements

- Python 3.x
- Pygame library

To install Pygame, use:

```bash
pip install pygame
```

## How to Play

1. Clone or download the repository.
2. Run the game script:

   ```bash
   python game.py
   ```

3. Select a difficulty level:
   - **1**: Easy
   - **2**: Medium
   - **3**: Hard
4. Use the arrow keys to navigate the maze.
5. Avoid the enemy and reach the green goal block.

## File Structure

- `game.py`: Main game script.

## Code Highlights

### Maze Generation

The maze is generated using a recursive backtracking algorithm with added random paths for multiple solutions:

```python
def generate_maze(grid_size):
    # Recursive backtracking algorithm
    ...
```

### A* Pathfinding

The enemy uses the A* algorithm to find the shortest path to the player:

```python
def a_star_search(start, goal, grid):
    # A* search implementation
    ...
```

### Dynamic Difficulty

The game changes the maze periodically based on the selected difficulty:

- **Easy**: Long intervals, slower enemy.
- **Medium**: Moderate intervals, faster enemy.
- **Hard**: Short intervals, very fast enemy.

## Future Enhancements

- Add more obstacles and power-ups.
- Introduce additional enemy AI behaviors.
- Implement multiplayer mode.


Enjoy the game!
```
