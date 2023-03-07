#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:11:08 2023

@author: vincenzomarquez
"""

############################################################
# CIS 521: Homework 3
############################################################

student_name = "Aayushi Dwivedi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import  copy 
from queue import PriorityQueue

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    return TilePuzzle([[(r*cols) + c +1 if (r*cols) + c +1 < rows*cols \
                     else 0 for c in range(cols)] for r in range(rows)]);
    


class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board;
        self.rows = len(board);
        self.cols = len(board[0]);
        self.goal = [[(r*self.cols) + c +1 if (r*self.cols) + c +1 < self.rows*self.cols \
                    else 0 for c in range(self.cols)] for r in range(self.rows)];

        for i in range(self.rows):
          for j in range(self.cols):
            if self.board[i][j] == 0:
              (self.i, self.j) = i,j;

    def get_board(self):
        return self.board;

    def perform_move(self, direction):
        if direction == "up":
            if  self.i - 1 >=0:
                (self.board[self.i - 1][self.j], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i - 1][self.j]);
                self.i = self.i - 1;
                return True;
            else:
                return False;
       
        if direction == "down":
            if  self.i + 1 < self.rows:
                (self.board[self.i + 1][self.j], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i + 1][self.j]);
                self.i = self.i + 1;
                return True;
            else:
                return False;

        if direction == "right":
            if  self.j + 1 < self.cols:
                (self.board[self.i][self.j + 1], self.board[self.i][self.j ])=\
                    (self.board[self.i][self.j], self.board[self.i ][self.j + 1]);
                self.j = self.j + 1;
                return True;
            else:
                return False;

        if direction == "left":
            if  self.j - 1 >= 0:
                (self.board[self.i][self.j - 1], self.board[self.i][self.j])=\
                    (self.board[self.i][self.j], self.board[self.i][self.j - 1]);
                self.j = self.j - 1;
                return True;
            else:
                return False;
           

    def scramble(self, num_moves):
        seq = ["up", "down", "right", "left"];
        for i in range(num_moves):
            self.perform_move(random.choice(seq));
    
    def get_goal(self):
        return self.goal;
    def is_solved(self):
        if self.board == self.goal:
            return True;
        else:
            return False;
    
    def copy(self):
        return TilePuzzle(copy.deepcopy(self.get_board()));
    
    def successors(self):
        new_board = self.copy();
        if new_board.perform_move("up"):
            yield ("up", new_board);
        
        new_board = self.copy();
        if new_board.perform_move("down"):
            yield ("down", new_board);
        
        new_board = self.copy();
        if new_board.perform_move("right"):
            yield ("right", new_board);

        new_board = self.copy();
        if new_board.perform_move("left"):
            yield ("left", new_board);
    
    def bfs(self):
        if self.is_solved():
            return []
        
    

    def iddfs_helper(self, limit, moves):
        if limit == len(moves):
            yield (moves, self);
        else:
            for (direction, new_board) in self.successors():
                if (new_board.is_solved()):
                    yield (moves + [direction], new_board);
                else:
                    for (updated_moves, config) in  new_board.iddfs_helper(limit, moves + [direction]):
                        yield (updated_moves, config);

    # Required
    def find_solutions_iddfs(self):
        limit = 0;
        found = False
        while not found:
            for (moves, config) in self.iddfs_helper(limit, []):
                if config.is_solved():
                    yield moves;
                    found = True;        
            limit += 1;
    
    def create_goal_indicies(self):
        self.goal_indices = dict((self.goal[i][j],(i,j)) for i in range(self.rows) for j in range(self.cols));

    def manhattan_distance(self, board):
        distance = 0;
        for r1 in range(self.rows):
            for c1 in range(self.cols):
                (r2, c2) = self.goal_indices[board[r1][c1]]
                distance += (abs(r1-r2) + abs(c1 -c2));       
        return distance
    # Required
    def find_solution_a_star(self):
        if (self.is_solved()):
            return [];
        self.create_goal_indicies();        
        frontier = PriorityQueue();
        frontier.put((self.manhattan_distance(self.board), ([],self)));
        explored = set();
        explored.add( tuple (tuple(row) for row in self.get_board()))
        while not frontier.empty():
            (distance, (moves, config)) = frontier.get();
            for (new_move, new_config) in config.successors():
                solution = moves + [new_move];
                if new_config.is_solved():
                    return solution;
                state = (solution, new_config);
                new_board = tuple(tuple(row) for row in new_config.get_board());
                if new_board not in explored:
                    frontier.put((self.manhattan_distance(new_config.get_board())\
                                    +len(solution),state));
                    explored.add(new_board);

b = [[4,1,2],[0,5,3],[7,8,6]]
p = TilePuzzle(b)
solutions = p.find_solution_a_star()
print(list(solutions))

############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
20 hrs
"""

feedback_question_2 = """
Optimizing Grid navigation.
Took a while to figure out heuristics fuction for
linear disk movements. 
"""

feedback_question_3 = """
I liked problem 3 because it gave a comparision
between something I had previously implemented.
No, I wouldn't change anything about this assignment.
"""