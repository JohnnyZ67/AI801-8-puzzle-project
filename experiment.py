import sys
import puzzle
import os
import csv
from datetime import datetime

difficulties = [
    {"count": 20, "level": "Easy"},
    {"count": 50, "level": "Medium"}, 
    {"count": 100, "level": "Hard"}
]

functions = [
    {
        "name": "Iteratively Deepening Depth First Search",
        "classifier": "IDDFS",
        "fn": "find_solution_iddfs"
    },
    {
        "name": "Breadth First Search",
        "classifier": "BFS",
        "fn": "find_solution_bfs"
    },
    {
        "name": "A* - Manhattan",
        "classifier": "ASMAN",
        "fn": "find_solution_a_star",
        "arg": "manhattan"
    },
    {
        "name": "A* - Euclidean",
        "classifier": "ASEUC",
        "fn": "find_solution_a_star",
        "arg": "euclidean"
    },
    {
        "name": "A* - Chebyshev",
        "classifier": "ASCHEB",
        "fn": "find_solution_a_star",
        "arg": "chebyshev"
    },
    {
        "name": "A* - Linear Conflict",
        "classifier": "ASLINCON",
        "fn": "find_solution_a_star",
        "arg": "lin_conflict"
    }
]

def main(iterations=30):

    fields = ["Board Number", "Inversions", "Algorithm", "Solved", "Total States Viewed", "Processing Time"]
    rows = []
    board_count = 0

    for diff in difficulties:
        print(f"Performing iterations for difficulty: {diff['level']}")
        for i in range(iterations):
            board_count += 1
            board = puzzle.create_tile_puzzle(3, 3, 30)
            
            inversions = board.scramble(diff['count'])['inversions']
            while inversions == 0:
                inversions = board.scramble(diff['count'])['inversions']

            print(f"   Solving for Board: {board_count} with {inversions} inversions")

            for fn in functions:
                result = None
                if "arg" in fn:
                    result = getattr(board, fn['fn'])(fn['arg'])
                else:
                    result = getattr(board, fn['fn'])()
                
                solved = False if len(result['moves']) == 0 else True

                print(f"      Result for {fn['name']}: {result}")
                rows.append([board_count, inversions, fn['classifier'], solved, result['states_viewed'], result['processing_time']])

    with open(f"{os.getcwd()}/reports/data_report_{datetime.now().strftime('%y_%m_%d_%H_%M')}.csv", 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        
        csvwriter.writerow(fields) 
        csvwriter.writerows(rows)




if __name__ == "__main__":  
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main()