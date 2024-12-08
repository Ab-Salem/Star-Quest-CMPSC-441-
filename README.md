# 3D Maze Game

A 3D maze game implemented in Python using PyOpenGL and Pygame. Navigate through a procedurally generated maze while being chased by an AI-controlled enemy that uses different pathfinding algorithms.

## Features

- 3D maze environment with first-person and overhead camera views
- Multiple AI pathfinding algorithms for enemy behavior:
  - A* Search (optimal pathfinding)
  - Breadth-First Search (shortest path)
  - Depth-First Search (depth exploration)
  - Greedy Best-First Search (direct pursuit)
- Different maze sizes for varying difficulty levels
- Grid-based movement system
- Enemy that shoots bouncing fireballs
- Dynamic lighting and 3D rendering
- Interactive start menu for game configuration

## Requirements

- Python 3.x
- PyOpenGL
- Pygame
- NumPy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ab-Salem/Star-Quest-CMPSC-441-.git
cd Star-Quest-CMPSC-441-
```

2. Install required packages:
```bash
pip install pygame PyOpenGL numpy
```

## Running the Game

Run the game using:
```bash
python main.py
```

## Controls

### Menu Controls
- UP/DOWN: Select AI algorithm
- SHIFT + UP/DOWN: Select maze size
- ENTER: Start game

### Game Controls
- Arrow UP/DOWN: Move forward/backward
- Arrow LEFT/RIGHT: 
  - In overhead view: Rotate camera
  - In first-person view: Strafe left/right
- V: Switch between first-person and overhead view
- ESC: Quit game
- 1-4: Switch enemy AI algorithm during gameplay
  - 1: A* Search
  - 2: Breadth-First Search
  - 3: Depth-First Search
  - 4: Greedy Best-First Search

## Project Structure

```
maze_game/
├── config.py           # Game configuration and constants
├── maze_generator.py   # Maze generation algorithm
├── renderer.py         # OpenGL rendering engine
├── pathfinding.py      # AI pathfinding algorithms
├── game_objects.py     # Game entity classes
├── game.py            # Main game logic
├── menu.py            # Start menu system
└── main.py            # Entry point
```

## Game Mechanics

- Navigate through the maze to find the exit (green tile)
- Avoid the enemy (red cube) and its fireballs
- Enemy uses pathfinding to chase the player
- Fireballs bounce off walls
- Game ends when either:
  - Player reaches the exit (win)
  - Player gets hit by a fireball (lose)

## Difficulty Levels

- Small (10x10): Easy difficulty, shorter paths to exit
- Medium (15x15): Moderate difficulty, more complex maze
- Large (20x20): Hard difficulty, challenging navigation

## AI Algorithms

1. **A* Search**
   - Optimal pathfinding
   - Balances distance and heuristic
   - Most efficient chase behavior

2. **Breadth-First Search (BFS)**
   - Guarantees shortest path
   - Explores uniformly
   - Methodical pursuit

3. **Depth-First Search (DFS)**
   - May not find shortest path
   - Creates unpredictable chase patterns
   - More erratic movement

4. **Greedy Best-First**
   - Always moves toward player
   - Can get stuck in local minima
   - Aggressive pursuit behavior

## Contributing

Feel free to fork the project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments

- Pygame community for graphics and game loop handling
- PyOpenGL for 3D rendering capabilities
- Various pathfinding algorithm implementations