from sim import Cube,TurnSequence, countChanges
from time import perf_counter

# optimized for the goal, lower = better
def heuristic(cube : Cube):
    #corners = sum(1 for k,v in cube.corners.items() if k != v.initialPosition)
    gears = abs(sum(1 for k,v in cube.gears.items() if k != v.initialPosition) - 8)
    return gears#+corners

opposites = {"R":"L", "L":"R", "U":"D", "D":"U", "F":"B", "B":"F"}

allMoves = []
for i in ["R","L","U","D","F","B"]:
    allMoves.append(i)
    allMoves.append(i+"2")
    allMoves.append(i+"3")
    allMoves.append(i+"4")
    allMoves.append(i+"'")
    allMoves.append(i+"'2")
    allMoves.append(i+"'3")

def ida_star(cube : Cube, max_depth : int):
    """
    Iterative Deepening A* search for solving the cube.
    """
    global_depth = 0
    solution = None

    def dfs(cube : Cube, depth, threshold, path, last_move = None):
        nonlocal global_depth, solution

        h = heuristic(cube)
        f = depth + h  # f = g + h

        #print(f"Depth: {depth}, Move: {last_move}, Path: {path}, Heuristic: {h}")

        # If f-value exceeds the threshold, return that f-value as a new threshold.
        if f > threshold: return f
        if depth >= max_depth:
            return float('inf')  # Don't go deeper than max_depth
        
        # If the cube is solved, return the solution path.
        if h == 0:
            solution = path.copy()
            return path

        # Initialize the minimum threshold for the next iteration
        min_threshold = float('inf')

        # Try every possible move, called "neighbors"
        for move in allMoves:
            if last_move and move[0] == last_move[0]: continue
            if last_move and move[0] == opposites[last_move[0]]: continue
            # maybe restrict opposites...

            # Apply the move
            cube.executeSequence(TurnSequence(move))
            path.append(move)

            # Perform DFS
            result = dfs(cube, depth + 1, threshold, path, move)

            # Undo the move (backtrack)
            cube.executeSequence(TurnSequence(move).reverse())
            path.pop()

            if isinstance(result, list):
                # Solution found!
                return result
            else:
                # Update minimum threshold for the next iteration
                min_threshold = min(min_threshold, result)
                
        
        global_depth = max(depth,global_depth)
        return min_threshold

    # Iteratively increase depth limit
    threshold = heuristic(cube)
    while True:
        start = perf_counter()
        path = []
        result = dfs(cube, 0, threshold, path)
        end = perf_counter()

        # If the result is a solution path, return it
        if solution or isinstance(result,list):
            return solution

        # Otherwise, update the threshold for the next iteration
        print(f"Updating threshold to {result} - [prev. took {str(round(float(end-start),9))}] [depth {global_depth} reached].")
        threshold = result

        # If no solution was found within max_depth
        if threshold == float('inf'):
            return None

# Example Usage
cube = Cube()  # Initialize your cube state
max_depth = 18  # Set an arbitrary maximum depth for the search

solution = ida_star(cube, max_depth)

if solution:
    print("Solution found:", solution)
else:
    print("No solution found within the given depth.")