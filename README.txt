# MegaMinds Robotics Internship Assessment
## 2D Robot Navigation and Obstacle Avoidance

### 1. Project Overview
This project implements a 2D robot simulation using Python and Pygame. The robot navigates through an arena containing obstacles and moves from a starting point to a target using the A* pathfinding algorithm.

The simulation supports autonomous navigation and manual keyboard control. It also includes obstacle collision prevention, boundary protection, and basic performance statistics.

### 2. Technologies Used
- Python 3.13
- Pygame 2.6.1
- Heapq (Python standard library)
- Math and Time (Python standard libraries)

### 3. Project Files
- `robot.py` — Main simulation program.
- `robot_manual_backup.py` — Backup of the manual-control version.
- `README.txt` — Project documentation.
- `requirements.txt` — Python dependency list.

### 4. Installation Requirements
- Windows 10 or Windows 11
- Python 3.13 or compatible Python 3 version
- Visual Studio Code (recommended)
- Pygame

### 5. Installation Steps
1. Install Python from https://www.python.org/downloads/.
2. Open the project folder in Visual Studio Code.
3. Open Terminal → New Terminal.
4. Install Pygame by running:

   `python -m pip install pygame`

5. Run the simulation using:

   `python robot.py`

### 6. Controls
- **Arrow keys:** Move the robot one grid cell at a time in manual mode.
- **SPACE:** Switch between autonomous and manual modes.
- **R:** Restart the simulation.
- **ESC:** Exit the program.

### 7. Implemented Features
- 2D grid-based arena.
- Clearly marked start and goal positions.
- Multiple obstacles arranged as walls.
- A* pathfinding for autonomous navigation.
- Visible planned route.
- Smooth robot movement between grid cells.
- Obstacle collision prevention.
- Arena boundary protection.
- Goal-reached notification.
- Elapsed time and distance-travelled statistics.
- Blocked-move counter.
- Manual control for testing.
- Restart functionality.

### 8. Algorithm Explanation
The A* algorithm searches for a low-cost route from the start cell to the goal cell.

The evaluation function is:

f(n) = g(n) + h(n)

Where:
- `g(n)` is the actual cost from the start to the current cell.
- `h(n)` is the estimated remaining cost to the goal.
- `f(n)` is the estimated total path cost through that cell.

The Manhattan-distance heuristic is used because the robot moves horizontally and vertically on a grid.

The algorithm ignores blocked cells and cells outside the arena. Once a path is found, the robot follows the planned sequence of cells.

### 9. Testing
The following tests should be performed before submission:

1. Confirm that the simulation opens successfully.
2. Verify that the robot reaches the goal autonomously.
3. Check that the robot avoids all obstacles.
4. Test manual movement using the arrow keys.
5. Attempt to move into an obstacle and confirm that the move is rejected.
6. Attempt to move beyond the arena boundary.
7. Verify that the blocked-move counter increases after rejected moves.
8. Test the SPACE and R controls.

### 10. Limitations
- The simulation uses a grid-based environment rather than a physical robot model.
- Obstacle positions are known in advance.
- The robot uses four-direction movement; diagonal movement is not implemented.
- The range indicator is visual only and does not represent a functioning physical sensor.
- The project does not implement SLAM or real-world sensor-based navigation.

### 11. Future Improvements
- Add simulated distance sensors.
- Support dynamic obstacle detection and route replanning.
- Add multiple arena layouts.
- Implement diagonal movement.
- Improve the performance summary and visual interface.

### 12. Conclusion
This project demonstrates basic robot navigation, A* pathfinding, obstacle avoidance, boundary protection, and interactive simulation using Python and Pygame.

The project was developed for the MegaMinds Robotics Internship practical assessment.

### 13. Acknowledgement
Python and Pygame documentation were used as learning references. Any AI assistance used during development should be disclosed according to the assessment instructions.
