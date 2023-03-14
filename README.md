# AI801-8-puzzle-project
Repository for the A-I 801 Group 5 project. Original code and project setup was pulled from a separate [GitHub](https://github.com/JohnHofbauer/Artificial-Intelligence/tree/main/Assignment%203) repository and was trimmed to fit the needs of our project. Additional heuristics and algorithms are being developed by our team to expand upon this original code base.

## Environment Setup

### Python Installation
This is a python based project so it is assumed that for local development and usage you have python installed. If not please visit the [Python](https://www.python.org/downloads/) page and install it on your machine. 

### Git Workflow and Setup
This code base is stored in GitHub and can be found [here](https://github.com/JohnnyZ67/AI801-8-puzzle-project). Our team operates under a trunk-based development model with branches from and merges to our 'main' branch. All reports and final code will be presented from this 'main' branch. Merges are controlled through pull requests to ensure the team has maintains a clear overview of all changes and additions throughout the projects lifespan.

## Running locally
With python installed you can run this code by running the puzzle_solver.py code and providing it the size of the puzzle table. An example command for your terminal can be seen below and will initiate a 3x3 8-puzzle:
```
python puzzle_gui.py 3 3
```
### Heuristics and Algorithms
The GUI offers multiple heuristics and brute force algorithms to choose to solve the 8-puzzle. First select 'Scramble' to randomize the board and then simply press the button to solve the puzzle with your desired algorithm.