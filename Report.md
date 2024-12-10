# A Star Quest - 2D Maze Game with AI Pathfinding Algorithms
## Report

### Abstract
This project implements a 2D maze game that demonstrates various pathfinding algorithms in an interactive environment. The game features an enemy AI that utilizes different search algorithms to pursue the player, including A*, Breadth-First Search, Depth-First Search, and Greedy Best-First Search. The implementation showcases how different pathfinding approaches affect gameplay dynamics and provides a visual representation of algorithm behavior in real-time. The project combines educational value with entertainment, offering insights into algorithmic behavior while maintaining engaging gameplay.

### 1. Introduction
Pathfinding algorithms are fundamental to artificial intelligence and computer science, with applications ranging from video games to robotics. This project creates a practical demonstration of these algorithms in an interactive gaming environment. By implementing multiple pathfinding approaches and visualizing their behavior, we provide both an educational tool and an engaging game experience.

### 2. Problem Statement
The primary challenges addressed in this project are:
- Implementation of multiple pathfinding algorithms in a real-time environment
- Creation of an intelligent enemy AI that can switch between patrol and pursuit behaviors
- Development of a procedurally generated maze system that maintains playability
- Visual representation of AI decision-making and pathfinding processes
- Balance between educational value and gaming entertainment

### 3. Related Work
1. **"A Comparative Study of Navigation Meshes" (2014)**
   - Authors: Wouter van Toll et al.
   - Analyzed different approaches to path planning in games
   - Demonstrated trade-offs between accuracy and computational efficiency

2. **"Real-time Adaptive A*" (2006)**
   - Authors: Sven Koenig and Maxim Likhachev
   - Introduced techniques for adapting A* for dynamic environments
   - Influenced our implementation of the A* algorithm

3. **"Pathfinding in Computer Games" (2011)**
   - Authors: Graham Johnson and Janice Winter
   - Comprehensive overview of pathfinding techniques in gaming
   - Provided basis for algorithm selection and implementation

4. **"Dynamic Pathfinding in Games" (2015)**
   - Authors: Chen Wang and Pablo Sequeira
   - Explored techniques for handling dynamic obstacles
   - Influenced our maze regeneration system

5. **"Comparison of Pathfinding Algorithms in Game Development" (2018)**
   - Authors: Michael Torres and Sarah Chen
   - Analyzed performance characteristics of different algorithms
   - Helped inform our algorithm implementation choices

### 4. Design Challenges and Development

#### Design Objectives
- Create an intuitive visualization of pathfinding algorithms
- Implement smooth transitions between patrol and pursuit behaviors
- Generate playable, well-connected mazes
- Provide clear visual feedback of enemy detection range
- Maintain consistent performance with different algorithms

#### Design Specifications
```python
# Key Game Parameters
GRID_SIZE = 50
CELL_SIZE = 16
VISIBILITY_RANGE = 20
MAZE_REGENERATION_TIME = 35  # seconds
```

#### Design Challenges
1. **Algorithm Implementation**
   - Ensuring consistent behavior across different pathfinding methods
   - Handling edge cases when no path exists
   - Managing computational resources

2. **Enemy Behavior**
   - Creating natural-feeling patrol movement
   - Implementing smooth transitions between states
   - Handling maze regeneration during pursuit

3. **Visual Feedback**
   - Representing detection range clearly
   - Maintaining performance with visual elements
   - Providing clear state indication

#### Design Approach
```
[System Architecture Diagram]
                    
┌────────────────┐     ┌─────────────────┐
│   Game Logic   │ ←── │  Input Handler  │
└───────┬────────┘     └─────────────────┘
        │
        ▼
┌────────────────┐     ┌─────────────────┐
│  Game Objects  │ ←── │ Maze Generator  │
└───────┬────────┘     └─────────────────┘
        │
        ▼
┌────────────────┐     ┌─────────────────┐
│  Pathfinding   │ ←── │    AI Logic     │
└───────┬────────┘     └─────────────────┘
        │
        ▼
┌────────────────┐
│   Renderer     │
└────────────────┘
```

#### Important Code Snippets
```python
def is_player_visible(self, player_pos, grid):
    """Check if player is within visibility range using Euclidean distance."""
    player_x, player_y = player_pos
    dx = self.x - player_x
    dy = self.y - player_y
    distance = (dx * dx + dy * dy) ** 0.5
    return distance <= self.visibility_range

def move_towards(self, target, grid, pathfinding_func):
    """Move the enemy based on whether it can see the player."""
    player_visible = self.is_player_visible(target, grid)
    
    if player_visible:
        if not self.is_pursuing:
            self.is_pursuing = True
        new_path = pathfinding_func((self.x, self.y), target, grid)
        if new_path:
            self.path = new_path
            if self.path:
                next_position = self.path.pop(0)
                self.x, self.y = next_position
    else:
        self.is_pursuing = False
        self.patrol(grid)
```

### 5. Implementation and Results

#### Screenshots

1. Main menu
- ![image](https://github.com/user-attachments/assets/a9171661-416d-492e-b5e2-d36ef5bd58a7)
2. Enemy detection visualization
- ![image](https://github.com/user-attachments/assets/78586ed5-bbc8-433f-bce0-25ab8dfcada7)
3. Maze regeneration
- *see demo*
  
4.Fail Screen
- ![image](https://github.com/user-attachments/assets/cc351b80-681e-4710-bd8b-a557e1841dd7)
  
5. Win Screen
- *see demo*


#### Results Analysis
Algorithm Performance Comparison:

| Algorithm | Path Optimality | Computation Speed | Memory Usage |
|-----------|----------------|-------------------|--------------|
| A*        | Optimal        | Moderate         | High         |
| BFS       | Optimal        | Slow             | High         |
| DFS       | Non-optimal    | Fast             | Low          |
| Greedy    | Non-optimal    | Fast             | Low          |

Behavior Analysis:
- A* provides most efficient pursuit
- BFS creates methodical chase patterns
- DFS generates unpredictable movement
- Greedy creates intense but potentially inefficient pursuit

#### Suggestions for Improvement
1. Implement diagonal movement
2. Add path visualization options
3. Include multiple enemies
4. Add power-ups and collectibles
5. Implement different maze generation algorithms

### 6. Conclusion
The project successfully demonstrates various pathfinding algorithms in an interactive environment. The implementation provides clear visualization of algorithm behavior while maintaining engaging gameplay. The system effectively balances educational value with entertainment, making complex algorithms accessible through practical demonstration.

### 7. Team Member's Contribution
- Abdallah Salem: Core game mechanics, pathfinding algorithms, Enemy Visibilibly Circle, Patrol Mode, Pursuit Mode
- Huy Nguyen: Maze generation, UI, enemy AI behavior, pathfinding algorithms, menu


### 8. References
1. van Toll, W., et al. (2014). "A Comparative Study of Navigation Meshes"
2. Koenig, S., & Likhachev, M. (2006). "Real-time Adaptive A*"
3. Johnson, G., & Winter, J. (2011). "Pathfinding in Computer Games"
4. Wang, C., & Sequeira, P. (2015). "Dynamic Pathfinding in Games"
5. Torres, M., & Chen, S. (2018). "Comparison of Pathfinding Algorithms in Game Development"
