# AI801-8-puzzle-project
Repository for the A-I 801 Group 5 project. Original code and project setup was pulled from a separate [GitHub](https://github.com/JohnHofbauer/Artificial-Intelligence/tree/main/Assignment%203) repository and was trimmed to fit the needs of our project. Additional heuristics and algorithms are being developed by our team to expand upon this original code base.

## Running the program

### Individual Program Running
To run the GUI simply run the command
```
python puzzle_gui.py 3 3
```
This command will create a simple 3x3 grid for the 8 puzzle and then has several buttons on the right that represent the different options available to you.
* "Scramble" - Scrambles the board from its current state, to generate harder boards keep hitting the scramble button!
* "Solve Using IDDFS" - Solves the current board using Iteratively Deepening Depth First Search
* "Solve Using BFS" - Solves the current board using Breadth First Search
* "Solve Using A* - Manhattan" - Solves the current board using A* with Manhattan Distance as the heuristic
* "Solve Using A* - Euclidean" - Solves the current board using A* with Euclidean Distance as the heuristic
* "Solve Using A* - Chebyshev" - Solves the current board using A* with Chebyshev Distance as the heuristic
* "Solve Using A* - Linear Conflict" - Solves the current board using A* with the Linear Conflict heuristic

### Batch Running
To collect large amounts of data you can run the experiment script and provide it the number of iterations desired like the following command
```
python experiment.py 10
```
**If you do not provide the number of iteration it will default to 30**

This program does take some time to run, but will create a CSV file under the reports directory with the collected metrics data.

<br/><br/>

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