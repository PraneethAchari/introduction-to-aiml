import heapq
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import count

# Heuristics
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def diagonal(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

# small global counter to avoid ambiguous heap comparisons
_counter = count()

# Pathfinding Algorithms 
def greedy_bfs(grid, start, goal, heuristic):
    frontier = [(heuristic(start, goal), next(_counter), start)]
    came_from = {start: None}
    explored = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            break
        explored.add(current)

        for neighbor in get_neighbors(grid, current):
            if neighbor not in came_from:
                heapq.heappush(frontier, (heuristic(neighbor, goal), next(_counter), neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal), len(explored)


def a_star(grid, start, goal, heuristic):
    frontier = [(heuristic(start, goal), 0, next(_counter), start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()

    while frontier:
        _, g, _, current = heapq.heappop(frontier)
        if current == goal:
            break
        explored.add(current)

        for neighbor in get_neighbors(grid, current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, new_cost, next(_counter), neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal), len(explored)

# Helper
def get_neighbors(grid, node):
    rows = len(grid)
    cols = len(grid[0])
    directions = [(1,0), (-1,0), (0,1), (0,-1)]  # 4-directional
    neighbors = []
    for dx, dy in directions:
        nx, ny = node[0] + dx, node[1] + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] != 1:  # not a wall
                neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return []  # no path
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    return path[::-1]

def visualize(grid, path, start, goal):
    # ensure grid is numeric ndarray so imshow doesn't choke on mixed types
    img = np.array(grid, dtype=float)
    plt.imshow(img, cmap="gray_r")
    if path:
        px, py = zip(*path)
        plt.plot(py, px, linewidth=2)
    plt.scatter(start[1], start[0], marker="o", label="Start")
    plt.scatter(goal[1], goal[0], marker="x", label="Goal")
    plt.legend()
    plt.gca().invert_yaxis()  # makes (0,0) top-left like matrix indices
    plt.show()

# Main
if __name__ == "__main__":
    grid = [
        ['S',0,0,0,0],
        [1,1,0,1,0],
        [0,0,0,1,0],
        [0,1,0,0,0],
        [0,0,0,1,'G']
    ]

    # Convert S,G to 0 for processing (and ensure all cells are numeric)
    start, goal = None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
                grid[i][j] = 0
            elif grid[i][j] == 'G':
                goal = (i, j)
                grid[i][j] = 0

    # make sure rows are integers (avoid mixed-type lists)
    grid = [[int(cell) for cell in row] for row in grid]

    heuristics = {"Manhattan": manhattan, "Euclidean": euclidean, "Diagonal": diagonal}

    for name, h in heuristics.items():
        print(f"\n{name} Heuristic")

        path_gbfs, explored_gbfs = greedy_bfs(grid, start, goal, h)
        print("GBFS -> Path length:", len(path_gbfs), "Nodes explored:", explored_gbfs)

        path_astar, explored_astar = a_star(grid, start, goal, h)
        print("A*   -> Path length:", len(path_astar), "Nodes explored:", explored_astar)

        visualize(grid, path_astar, start, goal)
