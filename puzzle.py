import random
import copy
import itertools
import queue as Q
import math
from datetime import datetime, timedelta


def create_tile_puzzle(rows, cols, timeout=20):
    board = []
    new = []
    cnt = 1
    for i in range(0, rows):
        for j in range(0, cols):
            new.append(cnt)
            cnt += 1
        board.append(new)
        new = []
    board[rows - 1][cols - 1] = 0

    return TilePuzzle(board, timeout)


class TilePuzzle(object):
    
    def __init__(self, board, timeout):
        self.board = board
        self.r = len(board)
        self.c = len(board[0])
        for i in range(self.r):
            for j in range(self.c):
                if board[i][j] == 0:
                    self.loc = (i, j)
        self.sol = self.solved_board()
        self.h = 0
        self.f = 0
        self.g = 0
        self.route = []
        self.timeout = timeout

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        loc = self.loc
        if direction == "up":
            if loc[0] == 0:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0] - 1][loc[1]]
                self.board[loc[0] - 1][loc[1]] = 0
                self.loc = (loc[0] - 1, loc[1])
                return True
        elif direction == "down":
            if loc[0] == self.r - 1:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0] + 1][loc[1]]
                self.board[loc[0] + 1][loc[1]] = 0
                self.loc = (loc[0] + 1, loc[1])
                return True
        elif direction == "left":
            if loc[1] == 0:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0]][loc[1] - 1]
                self.board[loc[0]][loc[1] - 1] = 0
                self.loc = (loc[0], loc[1] - 1)
                return True
        elif direction == "right":
            if loc[1] == self.c - 1:
                return False
            else:
                self.board[loc[0]][loc[1]] = self.board[loc[0]][loc[1] + 1]
                self.board[loc[0]][loc[1] + 1] = 0
                self.loc = (loc[0], loc[1] + 1)
                return True
        return False

    def scramble(self, num_moves):
        directions = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(directions))
        
        puzzle_diff = self.solvable()
        return puzzle_diff
        

    # Basing these algorithms off of those found here -> https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/
    # Updated to allow for larger puzzles using rows * columns
    # tiles is a flattened array of the board.
    def get_inversion_counts(self, tiles, r, c):
        inversions = 0
        empty_value = 0
        for i in range(0, r*c):
            for j in range(i+1, r*c):
                if tiles[j] != empty_value and tiles[i] != empty_value and tiles[i] > tiles[j]:
                    inversions += 1
        return inversions

    def solvable(self):
        inversions = self.get_inversion_counts([j for sub in self.get_board() for j in sub], self.r, self.c)
        return {
            "inversions": inversions,
            "solvable": (inversions % 2 == 0)
        }
    
    def is_solved(self):
        solved = create_tile_puzzle(self.r, self.c)
        if self.board == solved.get_board():
            return True
        return False

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board), self.timeout)

    def successors(self, moves=None ):
        if moves is None:
            p = self.copy()
            if p.perform_move("up"):
                yield ("up", p)
            p = self.copy()
            if p.perform_move("down"):
                yield ("down", p)
            p = self.copy()
            if p.perform_move("left"):
                yield ("left", p)
            p = self.copy()
            if p.perform_move("right"):
                yield ("right", p)
        else:
            p = self.copy()
            if p.perform_move("up"):
                yield ("up", p, moves+["up"])
            p = self.copy()
            if p.perform_move("down"):
                yield ("down", p, moves+["down"])
            p = self.copy()
            if p.perform_move("left"):
                yield ("left", p, moves+["left"])
            p = self.copy()
            if p.perform_move("right"):
                yield ("right", p, moves+["right"])

    def solved_board(self):
        board = []
        new = []
        cnt = 1
        for i in range(0, self.r):
            for j in range(0, self.c):
                new.append(cnt)
                cnt += 1
            board.append(new)
            new = []
        board[self.r - 1][self.c - 1] = 0
        return board

    def find_solution_bfs(self):
        """
        Finds the solution to the puzzle using;
        Breadth First Search
        """
        states_viewed = 0
        state_queue = []
        moves = []
        time_to_live = datetime.now() + timedelta(seconds=self.timeout)
        time_start = datetime.now()

        if (self.is_solved()):
            return {"moves": moves, "states_viewed":states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
        else:
            for state in self.successors(moves):
                state_queue.append(state)


        for direction, board, prev_moves in state_queue:
            states_viewed += 1
            if (board.is_solved()):
                return {"moves": prev_moves, "states_viewed":states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
            elif datetime.now() > time_to_live:
                return {"moves": [], "states_viewed": states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
            else:
                for state in board.successors(prev_moves):
                    state_queue.append(state)


    def iddfs_helper(self, limit, moves):
        if limit == len(moves):
            yield (moves, self)
        else:
            for (direction, new_board) in self.successors():
                if (new_board.is_solved()):
                    yield (moves + [direction], new_board)
                else:
                    for (updated_moves, config) in  new_board.iddfs_helper(limit, moves + [direction]):
                        yield (updated_moves, config)

    # Required
    def find_solution_iddfs(self):
        limit = 0
        states_viewed = 0
        found = False
        time_to_live = datetime.now() + timedelta(seconds=self.timeout)
        time_start = datetime.now()

        while not found:
            for (moves, config) in self.iddfs_helper(limit, []):
                if config.is_solved():
                    return {"moves": moves, "states_viewed": states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
                elif datetime.now() > time_to_live:
                    return {"moves": [], "states_viewed": states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
                states_viewed += 1
            limit += 1
    # Required
    def find_solution_a_star(self, algorithm = "chebyshev"):
        states_viewed=0
        open_set = set()
        closed_set = set()
        open_set.add(self)
        self.h = self.chebyshev(self.sol)
        self.route = []
        time_to_live = datetime.now() + timedelta(seconds=self.timeout)
        time_start = datetime.now()

        while open_set:
            curr = min(open_set, key=lambda x: x.f)

            if curr.board == self.sol:
                return {"moves": curr.route, "states_viewed":states_viewed}
            elif datetime.now() > time_to_live:
                    return {"moves": [], "states_viewed": states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
            open_set.remove(curr)

            for move, puzzle in curr.successors():
                states_viewed += 1

                if puzzle.board == self.sol:
                    puzzle.route = curr.route + [move]
                    return {"moves":puzzle.route, "states_viewed":states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}
                elif datetime.now() > time_to_live:
                    return {"moves": [], "states_viewed": states_viewed, "processing_time": (datetime.now()-time_start).total_seconds()}

                if algorithm == "chebyshev":
                    puzzle.g = curr.g + curr.chebyshev(puzzle.board)
                    puzzle.h = puzzle.chebyshev(self.sol)
                    puzzle.f = puzzle.g + puzzle.h
                elif algorithm == "manhattan":
                    puzzle.g = curr.g + curr.manhattan(puzzle.board)
                    puzzle.h = puzzle.manhattan(self.sol)
                    puzzle.f = puzzle.g + puzzle.h
                elif algorithm == "euclidean":
                    puzzle.g = curr.g + curr.euclidean(puzzle.board)
                    puzzle.h = puzzle.euclidean(self.sol)
                    puzzle.f = puzzle.g + puzzle.h

                go = True
                for board in open_set:
                    if board.board == puzzle.board and board.f < puzzle.f:
                        go = False
                        continue
                for board in closed_set:
                    if board.board == puzzle.board and board.f < puzzle.f:
                        go = False
                        continue
                if go:
                    open_set.add(puzzle)
                    puzzle.route = curr.route + [move]

            closed_set.add(curr)

    def manhattan(self, t1):
        total = 0
        pos = {}

        for x in range(self.r):
            for y in range(self.c):
                pos[t1[x][y]] = (x, y)

        for x in range(self.r):
            for y in range(self.c):
                a = self.board[x][y]
                pos2 = pos[a]
                total += abs(x - pos2[0]) + abs(y - pos2[1])
        return total
    
    def euclidean(self, t1):
        total = 0
        pos = {}

        for x in range(self.r):
            for y in range(self.c):
                pos[t1[x][y]] = (x, y)

        for x in range(self.r):
            for y in range(self.c):
                a = self.board[x][y]
                pos2 = pos[a]
                total += math.pow((x - pos2[0]),2) + math.pow((y - pos2[1]),2)
        return math.sqrt(total)
    
    def chebyshev(self, t1):
        total = 0
        pos = {}
        def maximum(a, b):
            if a >= b:
                return a
            else:
                return b

        for x in range(self.r):
            for y in range(self.c):
                pos[t1[x][y]] = (x, y)

        for x in range(self.r):
            for y in range(self.c):
                a = self.board[x][y]
                pos2 = pos[a]
                total += maximum(abs(x - pos2[0]),abs(y - pos2[1]))
        return math.sqrt(total)
