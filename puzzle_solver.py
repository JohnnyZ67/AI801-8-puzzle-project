from random import choice
from queue import PriorityQueue
from math import sqrt
import time

def create_tile_puzzle(rows, cols):
    return TilePuzzle([[0 if x*y == cols*rows else x+(cols*(y-1)) for x in range(1, cols+1)] for y in range(1, rows+1)])

class TilePuzzle(object):
    
    def __init__(self, board):
        self.board = board
        self.emptyspot = []
        for index in range(len(board)):
            if 0 in board[index]:
                self.emptyspot = [board[index].index(0), index]
        #print("emptyspot: " + str(self.emptyspot))

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        if direction == "up" and 0 <= self.emptyspot[1]-1 <= len(self.board)-1: # Swap the empty spot with the one above it
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]-1][self.emptyspot[0]]
            self.board[self.emptyspot[1]-1][self.emptyspot[0]] = 0
            self.emptyspot[1] = self.emptyspot[1]-1 # update the empty spot
            return True

        if direction == "down" and 0 <= self.emptyspot[1]+1 <= len(self.board)-1: # Swap the empty spot with the one below it
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]+1][self.emptyspot[0]]
            self.board[self.emptyspot[1]+1][self.emptyspot[0]] = 0
            self.emptyspot[1] = self.emptyspot[1]+1 # update the empty spot
            return True

        if direction == "left" and 0 <= self.emptyspot[0]-1 <= len(self.board[0])-1: # Swap the empty spot with the one to the left
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]][self.emptyspot[0]-1]
            self.board[self.emptyspot[1]][self.emptyspot[0]-1] = 0
            self.emptyspot[0] = self.emptyspot[0]-1 # update the empty spot
            return True

        if direction == "right" and  0 <= self.emptyspot[0]+1 <= len(self.board[0])-1: # Swap the empty spot with the one to the right
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]][self.emptyspot[0]+1]
            self.board[self.emptyspot[1]][self.emptyspot[0]+1] = 0
            self.emptyspot[0] = self.emptyspot[0]+1 # update the empty spot
            return True

        return False

    def scramble(self, num_moves):
        for index in range(num_moves):
            self.perform_move(choice(["right", "left", "up", "down"]))

    def is_solved(self):
        if self.board == create_tile_puzzle(len(self.board[0]), len(self.board)).get_board():
            return True
        return False

    def copy(self):
        """ This creates a DeepCopy of the board, then returns a new object with the copyed bord. """
        return TilePuzzle([[n for n in self.board[x]] for x in range(len(self.board))])


    def successors(self):
        for index in ["up", "down", "left", "right"]:
            newBord = TilePuzzle(self.copy().get_board())
            newBord.perform_move(index)
            yield (index, newBord)

    # Required
    def find_solutions_bfs(self):
        """
        Finds the solution to the puzzle using;
        Breadth First Search
        """
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts on.

        goal = create_tile_puzzle(len(self.board), len(self.board[0])).get_board()

        def nextLevel(prevouse = ()):
            succ = 0
            #print("Origial: " + str(self.get_board()))
            for moves, new_board in self.successors(): # Find the successors.
                
                # make sure they were not visited.  #Save when more than one goal if found
                if new_board.get_board() not in self.visited or new_board.get_board() == goal: 
                    #print("successors: " + str(moves) + "   "+ str(new_board.get_board()))
                    
                    succ = 1
                    #print("Succ = " + str(succ))

                    # Populete the lists.
                    if len(prevouse) > 0:
                        newnewlist = prevouse
                        if type(newnewlist) == type(list()):
                            newnewlist = prevouse[:]
                            newnewlist.append(moves)

                        else: # speciel case for the first itteration.
                            newnewlist = [prevouse]
                            newnewlist.append(moves)
                        self.steps.append([newnewlist, new_board.get_board()])
                    else:
                        self.steps.append([[moves], new_board.get_board()])
                    self.visited.append(new_board.get_board())
                #else:
                #    print("Already seen: " + str(moves) + "   "+ str(new_board.get_board()))
            return succ

        

        def checkThem(index):
            """
            Check for all false in the steps list.
            """
            #print("Checking: " + str(create_tile_puzzle(len(self.board[0]), len(self.board)).get_board()))
            #print("with: " + str(self.steps[index][1]))

            # Return if an answer has been found in the list of posibilites
            if create_tile_puzzle(len(self.board), len(self.board[0])).get_board() == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0
        #Special case for no moves
        if goal == self.board:
            yield []
            return

        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return answer

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries
                    if len(self.steps[index]) < 3:
                        # save the current board
                        currentBoard = self.copy().get_board()
                        
                        self.board = self.steps[index][1] # Set the board
                        #print("Origial Stored: " + str(self.steps[index][1]))
                        #print("Origial After set: " + str(self.get_board()))
                        

                        succ = nextLevel(self.steps[index][0])
                        self.steps[index].append(1)
                        if succ == 1:
                            self.successorsFound = 1
                        #print("Succ = " + str(succ))
                        #print("successorsFound = " + str(self.successorsFound))

                        self.board = currentBoard
            

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    yield answer #list(dict.fromkeys()) # remove dup
                    self.successorsFound = 0 #this stops the recursion, when answers are found at this level
        return None

    # Required
    def find_solutions_iddfs(self):
        """
        Finds the solution to the puzzle using;
        Iterative deepenging search using the.
        """
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts on.

        goal = create_tile_puzzle(len(self.board), len(self.board[0])).get_board()

        def nextLevel(prevouse = ()):
            succ = 0
            #print("Origial: " + str(self.get_board()))
            for moves, new_board in self.successors(): # Find the successors.
                
                # make sure they were not visited.  #Save when more than one goal if found
                if new_board.get_board() not in self.visited or new_board.get_board() == goal: 
                    #print("successors: " + str(moves) + "   "+ str(new_board.get_board()))
                    
                    succ = 1
                    #print("Succ = " + str(succ))

                    # Populete the lists.
                    if len(prevouse) > 0:
                        newnewlist = prevouse
                        if type(newnewlist) == type(list()):
                            newnewlist = prevouse[:]
                            newnewlist.append(moves)

                        else: # speciel case for the first itteration.
                            newnewlist = [prevouse]
                            newnewlist.append(moves)
                        self.steps.append([newnewlist, new_board.get_board()])
                    else:
                        self.steps.append([[moves], new_board.get_board()])
                    self.visited.append(new_board.get_board())
                #else:
                #    print("Already seen: " + str(moves) + "   "+ str(new_board.get_board()))
            return succ

        

        def checkThem(index):
            """
            Check for all false in the steps list.
            """
            #print("Checking: " + str(create_tile_puzzle(len(self.board[0]), len(self.board)).get_board()))
            #print("with: " + str(self.steps[index][1]))

            # Return if an answer has been found in the list of posibilites
            if create_tile_puzzle(len(self.board), len(self.board[0])).get_board() == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0
        #Special case for no moves
        if goal == self.board:
            yield []
            return

        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return answer

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries
                    if len(self.steps[index]) < 3:
                        # save the current board
                        currentBoard = self.copy().get_board()
                        
                        self.board = self.steps[index][1] # Set the board
                        #print("Origial Stored: " + str(self.steps[index][1]))
                        #print("Origial After set: " + str(self.get_board()))
                        

                        succ = nextLevel(self.steps[index][0])
                        self.steps[index].append(1)
                        if succ == 1:
                            self.successorsFound = 1
                        #print("Succ = " + str(succ))
                        #print("successorsFound = " + str(self.successorsFound))

                        self.board = currentBoard
            

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    yield answer #list(dict.fromkeys()) # remove dup
                    self.successorsFound = 0 #this stops the recursion, when answers are found at this level
        return None

    # Required
    def find_solution_a_star(self):
        """
        Finds the solution to the puzzle using;
        A* search using the Manhattan distance heuristic
        """
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts on.

        goal = create_tile_puzzle(len(self.board), len(self.board[0])).get_board()
        goalPositions = {}
        for row in range(len(goal)):
            for element in range(len(goal[row])):
                # find the distance to where it should be.
                goalPositions[goal[row][element]] = (row, element)

        def nextLevel(prevouse = ()):
            succ = 0
            #print("Origial: " + str(self.get_board()))
            moves = []
            new_board = []
            h_values = []
            lowset_F = 100000000000000000000000000 # large number
            for moves2, new_board2 in self.successors(): # Find the successors.
                # implement A* by only visiting the board closest to the goal
                ### Store F = p + h in the steps table. 
                # sort the table by the lowset F.
                # then alays find the successors of the lowest F first.
                f = 0
                #Evaluate the bord to see find h
                dic = {}
                for row in range(len(new_board2.get_board())):
                    for element in range(len(new_board2.get_board()[row])):
                        # find the distance to where it should be.
                        dic[new_board2.get_board()[row][element]] = (row, element)

                #print(dic)
                h = 0
                for i in dic:
                    #print(dic[i], goalPositions[i])
                    h += abs(abs(dic[i][0]) - abs(goalPositions[i][0])) # add the hroazontal diffrence, add the vertical diffrence.
                    h += abs(abs(dic[i][1]) - abs(goalPositions[i][1])) 
                    #print(dic[i][0] - goalPositions[i][0])
                #print(h)

                # Get p 
                p = len(prevouse)

                # Solve for f
                f = p + h

                if f <= lowset_F and new_board2.get_board() not in self.visited:
                    lowset_F = f
                    h_values.append(h)
                    moves.append(moves2)
                    new_board.append(new_board2)

            for x in range(len(new_board)):
                # only save values that get us closser to the goal
                #if new_board.get_board() not in self.visited: 
                succ = 1
                
                # Populete the lists.
                if len(prevouse) > 0:
                    newnewlist = prevouse
                    if type(newnewlist) == type(list()):
                        newnewlist = prevouse[:]
                        newnewlist.append(moves[x])

                    else: # speciel case for the first itteration.
                        newnewlist = [prevouse]
                        newnewlist.append(moves[x])
                    self.steps.append((newnewlist, new_board[x].get_board(), h_values[x]))
                else:
                    self.steps.append(([moves[x]], new_board[x].get_board(), h_values[x]))
                self.visited.append(new_board[x].get_board())
            return succ


        def checkThem(index):
            # Return if an answer has been found in the list of posibilites
            if create_tile_puzzle(len(self.board), len(self.board[0])).get_board() == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0
        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return answer

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries
                # save the current board
                #if 
                currentBoard = self.copy().get_board()
                self.board = self.steps[index][1] # Set the board
                succ = nextLevel(self.steps[index][0])
                if succ == 1:
                    self.successorsFound = 1
                self.board = currentBoard
            #print("__________STEPS____________")
            #for i in self.steps:
            #    print(i)
            #print("__________VISITED____________")
            #for i in self.visited:
            #    print(i)

            # SPEEED UP DAT MOFO< ___________________________ (Delete this portion if it doesn't work)
            # Find the bEst H
            best_H_Value = 100000000000000000000 # Large number
            for index in range(len(self.steps)):
                #print("H_Value: " + str(self.steps[index][2]))
                if self.steps[index][2] <= best_H_Value:
                    best_H_Value = self.steps[index][2]
            #print("Purging all values grater than: " + str(best_H_Value))
            # Perge all the bad H values.
            x = 0
            for index in range(len(self.steps)):

                if self.steps[x][2] > best_H_Value + 7: # <--- REMOVE THIS portion BEFORE SUBMITTING!!!
                    self.steps.pop(x)                   # this lowers the runtime. but adds a posablitiy of the program not finnshing.
                    x-=1
                x+=1
            # _________________________________________________
            

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    return answer #list(dict.fromkeys()) # remove dup
        return None

"""
print("______SOLVING USING IDDFS_________")
for i in range(1, 20):
    p = create_tile_puzzle(3, 3)
    p.scramble(100)
    print(p.find_solution_a_star())

print("______SOLVING USING A*_________")
for i in range(1, 20):
    p = create_tile_puzzle(3, 3)
    p.scramble(100)
    print(p.find_solution_a_star())
"""

############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    # True valeus corresponding to obsticals.
    # False values corresponding to empty spaces.

    if (scene[start[0]][start[1]] == True):
        return None # the start is on an obstical
    if (scene[goal[0]][goal[1]] == True):
        return None # the Goal is on an obstical
    if (start == goal):
        return None # You have allready won
    
    def successors (position):
        # yield all options to false squares (you can move diagnal)
        if position[0]-1 >= 0 and position[1]-1 >= 0 and scene[position[0]-1][position[1]-1] == False: # check the top left corner
            yield (position[0]-1, position[1]-1)
        if position[1]-1 >= 0 and scene[position[0]][position[1]-1] == False:# check the top
            yield (position[0], position[1]-1)
        if position[0]+1 < len(scene) and position[1]-1 >= 0 and scene[position[0]+1][position[1]-1] == False: # check the top right corner
            yield (position[0]+1, position[1]-1)

        if position[0]-1 >= 0 and scene[position[0]-1][position[1]] == False:# check the left
            yield (position[0]-1, position[1])
        if position[0]+1 < len(scene) and scene[position[0]+1][position[1]] == False:# check the right
            yield (position[0]+1, position[1])

        if position[0]-1 >= 0 and position[1]+1 < len(scene[0]) and scene[position[0]-1][position[1]+1] == False: # check the bottom left corner
            yield (position[0]-1, position[1]+1)
        if position[1]+1 < len(scene) and scene[position[0]][position[1]+1] == False:# check the bottom
            yield (position[0], position[1]+1)
        if position[0]+1 < len(scene) and position[1]+1 < len(scene[0]) and scene[position[0]+1][position[1]+1] == False: # check the bottom right corner
            yield (position[0]+1, position[1]+1)

    def isAnswer(position):
        # Return if an answer has been found in the list of posibilites
        if position == goal:
            return True
        return False

    # Priority queue only holds the current level in the tree.
    unvisited = PriorityQueue()
    heuristic = int(sqrt((start[0]-goal[0])**2 + (start[1]-goal[1])**2)*100)
    unvisited.put((heuristic, start, [start]))

    # create a visited list
    visited = [start]

    while unvisited.empty() == False:

        # Get the next level of the tree
        heuristic, position, path  = unvisited.get()
        for index in successors(position):

            # evaluate the current height
            if index not in visited:
                templist = path[:]
                templist.append(index)

                # find the shortest path. the priority queue will sort it for me
                heuristic = int(sqrt((index[0]-goal[0])**2 + (index[1]-goal[1])**2)*100)
                unvisited.put((heuristic, index, templist))
                visited.append(index)

                # check if i have the answer
                if isAnswer(index) == True:
                    return templist

    # if no solutions exsist
    return None
