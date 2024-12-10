# 2D Maze Game
A 2D maze game implemented in Python using Pygame. Navigate through a procedurally generated maze while being chased by an AI-controlled enemy that uses different pathfinding algorithms.
## Github Repository Link
https://github.com/Ab-Salem/Star-Quest-CMPSC-441-

## Purpose
This project demonstrates the implementation and comparison of different pathfinding algorithms in a real-time gaming environment. It serves as an educational tool to visualize how different search algorithms behave in practice, while providing an engaging gaming experience.

## Features
- Procedurally generated 2D mazes that change every 35 seconds
- Multiple AI pathfinding algorithms for enemy behavior:
  - A* Search (optimal pathfinding)
  - Breadth-First Search (shortest path)
  - Depth-First Search (depth exploration)
  - Greedy Best-First Search (direct pursuit)
- Visual enemy detection radius
- Difficulty levels affecting enemy search depth
- Grid-based movement system
- Interactive menus for algorithm and difficulty selection

## Requirements
- Python 3.x
- Pygame

## Installation
1. Clone the repository
2. Install required packages:
```bash
pip install pygame
```

## Running the Game
Run the game using:
```bash
python main.py
```

## Controls
### Menu Controls
- 1-4: Select AI algorithm
  - 1: A* Search
  - 2: Breadth-First Search
  - 3: Depth-First Search
  - 4: Greedy Best-First Search
- 1-3: Select difficulty level
  - 1: Easy
  - 2: Medium
  - 3: Hard
- R: Restart game
- Q: Quit game

### Game Controls
- Arrow Keys: Move player

## Project Structure
```
CMPSC 441 Final/
├── constants.py       # Game configuration and constants
├── generated_maze.py  # Maze generation algorithm
├── pathfinding.py     # AI pathfinding algorithms
├── game_objects.py    # Game entity classes
├── menu.py           # Menu system
└── main.py           # Game loop and initialization
```

## Game Mechanics
- Navigate through the maze to reach the goal (green tile)
- Avoid the enemy (red square)
- Enemy patrols randomly until player enters its detection radius
- Maze regenerates every 35 seconds
- Game ends when either:
  - Player reaches the goal (win)
  - Enemy catches the player (lose)

## Difficulty Levels
- Easy: Limited enemy search depth (500)
- Medium: Moderate enemy search depth (750)
- Hard: Unlimited enemy search depth

## AI Algorithms
1. **A* Search**
   - Optimal pathfinding using distance and heuristic
   - Most efficient chase behavior
   - Balances exploration and goal-directed movement

2. **Breadth-First Search (BFS)**
   - Guarantees shortest path in unweighted grid
   - Explores all directions equally
   - More predictable pursuit pattern

3. **Depth-First Search (DFS)**
   - Explores deeply before backtracking
   - May not find optimal path
   - Creates more erratic chase patterns

4. **Greedy Best-First**
   - Always moves toward player using heuristic
   - Can get stuck in local minima
   - Most direct but potentially suboptimal pursuit

## Challenges Faced
1. **Maze Generation**
   - Ensuring consistent connectivity
   - Balancing maze complexity with playability
   - Handling maze regeneration without trapping players

2. **Enemy AI**
   - Implementing different pathfinding algorithms
   - Managing computational efficiency
   - Creating natural-feeling patrol behavior
   - Handling edge cases when no path exists

3. **Game Balance**
   - Tuning enemy visibility range
   - Adjusting difficulty levels
   - Balancing maze regeneration timing

## Future Improvements
1. **Gameplay Enhancements**
   - Add power-ups and collectibles
   - Implement multiple enemies with different behaviors
   - Add sound effects and background music
   - Include a scoring system

2. **Technical Improvements**
   - Optimize pathfinding for larger mazes
   - Add path visualization options
   - Implement diagonal movement
   - Add maze complexity settings

3. **Visual Upgrades**
   - Improve graphics and animations
   - Add particle effects
   - Implement dynamic lighting
   - Add custom sprites for game elements

4. **Features**
   - Save/load game state
   - Leaderboard system
   - Custom maze editor
   - Multiple game modes

## Contributing

- Abdallah Salem
- Huy Nguyen
