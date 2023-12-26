import numpy as np
import heapq
from collections import deque

# Constants for direction
D = "DULR"
dr = [1, -1, 0, 0]
dc = [0, 0, -1, 1]

# Utility functions
def is_valid(i, j, ni, nj, maze):
    return 0 <= i < ni and 0 <= j < nj and maze[i][j] == 1

def heu(i, j, iu, ju):
    return abs(i - iu) + abs(j - ju)

# Pathfinding functions
def dfs(i, j, iu, ju, maze, ni, nj):
    stack, visited = [(i, j, "")], [[False] * nj for _ in range(ni)]
    visited[i][j] = True
    while stack:
        ci, cj, cur_path = stack.pop()
        if ci == iu and cj == ju:
            return cur_path
        for k in range(4):
            nexti, nextj = ci + dr[k], cj + dc[k]
            if is_valid(nexti, nextj, ni, nj, maze) and not visited[nexti][nextj]:
                visited[nexti][nextj] = True
                stack.append((nexti, nextj, cur_path + D[k]))
    return ""

def a_star(i, j, iu, ju, maze, ni, nj):
    pq, visited = [], [[False] * nj for _ in range(ni)]
    heapq.heappush(pq, (0, heu(i, j, iu, ju), i, j, ""))
    visited[i][j] = True
    while pq:
        cost, _, ci, cj, path = heapq.heappop(pq)
        if ci == iu and cj == ju:
            return path
        for k in range(4):
            nexti, nextj = ci + dr[k], cj + dc[k]
            if is_valid(nexti, nextj, ni, nj, maze) and not visited[nexti][nextj]:
                visited[nexti][nextj] = True
                next_cost = cost + 1
                heur = heu(nexti, nextj, iu, ju)
                heapq.heappush(pq, (next_cost + heur, heur, nexti, nextj, path + D[k]))
    return ""         

def bfs(i, j, iu, ju, maze, ni, nj):        
    queue, visited = deque([(i, j, "")]), [[False] * nj for _ in range(ni)]
    visited[i][j] = True
    while queue:
        ci, cj, cur_path = queue.popleft()
        if ci == iu and cj == ju:
            return cur_path
        for k in range(4):
            nexti, nextj = ci + dr[k], cj + dc[k]
            if is_valid(nexti, nextj, ni, nj, maze) and not visited[nexti][nextj]:
                visited[nexti][nextj] = True
                queue.append((nexti, nextj, cur_path + D[k]))
    return ""

def backtracking(i, j, iu, ju, cur_path, visited, maze, ni, nj, answers):
    if i == iu and j == ju:
        answers.append(cur_path)
        return 
    visited[i][j] = True
    for k in range(4):
        nexti, nextj = i + dr[k], j + dc[k]
        if is_valid(nexti, nextj, ni, nj, maze) and not visited[nexti][nextj]:
            backtracking(nexti, nextj, iu, ju, cur_path + D[k], visited, maze, ni, nj, answers)
    visited[i][j] = False
    return answers

# Visualization function
def print_maze_with_path(maze, path, start, end):
    maze_copy = [row[:] for row in maze]  # Make a copy of the actual maze to prevent modifying it
    i, j = start
    path_positions = set([(i, j)])  # Include starting point
    
    # Decode the path and add the coordinates to a set for easy checking
    for move in path:
        if move == 'D':
            i += 1
        elif move == 'U':
            i -= 1
        elif move == 'L':
            j -= 1
        elif move == 'R':
            j += 1
        path_positions.add((i, j))  # Add each new position to the set
    
    print("\nMaze with path [S=start, E=end, *=path]:")
    for r in range(len(maze_copy)):
        for c in range(len(maze_copy[0])):
            if (r, c) == start:
                print('S', end=' ')
            elif (r, c) == end:
                print('E', end=' ')
            elif (r, c) in path_positions:
                print('*', end=' ')
            else:
                print(maze_copy[r][c], end=' ')
        print()  # Newline for next row of the maze
    print("")  # Add an extra newline for readability

# Main loop with option handling
while True:
    ni, nj = int(input("Enter the number of rows: ")), int(input("Enter the number of columns: "))
    op = input("Choose option (1 for custom maze, 2 for random maze): ").strip()
    
    maze = []
    
    if op == '1':
        input_string = input("Enter the maze with elements separated by spaces and rows by ';': ")
        maze = [list(map(int, row.split())) for row in input_string.split(";")]
    elif op == '2':
        maze = np.random.randint(0, 2, size=(ni, nj)).tolist()  # Convert to a list of lists for consistency
        print("\nRandomly generated maze:")
        for row in maze:
            print(' '.join(str(cell) for cell in row))
        print("")  # Add an extra newline for readability
    else:
        print("Invalid maze option.")
        continue
    
    i, j = int(input("Enter the start point i: ")), int(input("Enter the start point j: "))
    iu, ju = int(input("Enter the end point i: ")), int(input("Enter the end point j: "))
    
    if not is_valid(i, j, ni, nj, maze) or not is_valid(iu, ju, ni, nj, maze):
        print("Invalid start or end point.")
        continue
    
    method = input("Choose the method (1 for backtracking, 2 for A_star, 3 for dfs, 4 for bfs): ").strip()
    path = ""
    
    if method == '1':
        visited = [[False] * nj for _ in range(ni)]
        answers = []
        backtracking(i, j, iu, ju, "", visited, maze, ni, nj, answers)
        print("All possible path(s): ",answers)
        path = min(answers, key=len) if answers else ""
    elif method == '2':
        path = a_star(i, j, iu, ju, maze, ni, nj)
    elif method == '3':
        path = dfs(i, j, iu, ju, maze, ni, nj)
    elif method == '4':
        path = bfs(i, j, iu, ju, maze, ni, nj)
    else:
        print("Invalid method option.")
        continue
    
    if path:
        print("Shortest path found:", path)
        print("Path length:", len(path))
        print_maze_with_path(maze, path, (i, j), (iu, ju))
        break
    else:
        print("No path found.")
        continue