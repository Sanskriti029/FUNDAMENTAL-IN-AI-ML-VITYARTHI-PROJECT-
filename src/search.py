from collections import deque
from environment import neighbors

def bfs(grid, start, goal, rows, cols):
    frontier = deque([start])
    came_from = {start: None}
    while frontier:
        current = frontier.popleft()
        if current == goal:
            break
        for nb in neighbors(current, rows, cols):
            if nb not in grid:  # obstacle
                continue
            if nb not in came_from:
                came_from[nb] = current
                frontier.append(nb)
    return reconstruct_path(came_from, start, goal)

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    return path[::-1]
