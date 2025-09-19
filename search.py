# search.py
import heapq
import time
from collections import deque
from typing import Tuple, Dict, List
from grid import GridWorld, DynamicObstacle

Pos = Tuple[int, int]

class SearchStats:
    def __init__(self):
        self.nodes_expanded = 0
        self.time_taken = 0.0

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_time_path(came_from: Dict[Tuple[Pos,int], Tuple[Pos,int]], start_state, goal_state):
    if goal_state not in came_from:
        return []
    path = []
    cur = goal_state
    while cur != start_state:
        (pos, t) = cur
        path.append(pos)
        cur = came_from[cur]
    path.append(start_state[0])
    path.reverse()
    return path

def bfs_time_aware(grid: GridWorld, start: Pos, goal: Pos, start_time: int = 0, max_time: int = 1000) -> (List[Pos], SearchStats):
    """
    BFS over (pos, time) state space. Each move increments time by 1. Avoid positions occupied at that time.
    """
    stats = SearchStats()
    t0 = time.time()

    start_state = (start, start_time)
    frontier = deque([start_state])
    came_from = {start_state: None}
    visited = {start_state}

    while frontier:
        current = frontier.popleft()
        stats.nodes_expanded += 1
        (pos, t) = current
        if pos == goal:
            stats.time_taken = time.time() - t0
            return reconstruct_time_path(came_from, start_state, current), stats
        if t - start_time > max_time:
            continue
        for nbr in grid.neighbors(pos):
            next_state = (nbr, t+1)
            # skip if occupied at arrival time
            if grid.occupied_at(nbr, t+1):
                continue
            if next_state not in visited:
                visited.add(next_state)
                came_from[next_state] = current
                frontier.append(next_state)

    stats.time_taken = time.time() - t0
    return [], stats

def ucs_time_aware(grid: GridWorld, start: Pos, goal: Pos, start_time: int = 0, max_time: int = 1000):
    stats = SearchStats()
    t0 = time.time()

    start_state = (start, start_time)
    frontier = []
    heapq.heappush(frontier, (0, start_state))
    came_from = {start_state: None}
    cost_so_far = {start_state: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        stats.nodes_expanded += 1
        (pos, t) = current
        if pos == goal:
            stats.time_taken = time.time() - t0
            return reconstruct_time_path(came_from, start_state, current), stats
        if t - start_time > max_time:
            continue
        for nbr in grid.neighbors(pos):
            arrival_time = t+1
            if grid.occupied_at(nbr, arrival_time):
                continue
            new_cost = cost_so_far[current] + grid.cost(nbr)
            next_state = (nbr, arrival_time)
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                heapq.heappush(frontier, (new_cost, next_state))
                came_from[next_state] = current

    stats.time_taken = time.time() - t0
    return [], stats

def astar_time_aware(grid: GridWorld, start: Pos, goal: Pos, start_time: int = 0, max_time: int = 1000):
    stats = SearchStats()
    t0 = time.time()

    start_state = (start, start_time)
    frontier = []
    heapq.heappush(frontier, (0 + manhattan(start, goal), 0, start_state))
    came_from = {start_state: None}
    cost_so_far = {start_state: 0}

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)
        stats.nodes_expanded += 1
        (pos, t) = current
        if pos == goal:
            stats.time_taken = time.time() - t0
            return reconstruct_time_path(came_from, start_state, current), stats
        if t - start_time > max_time:
            continue

        for nbr in grid.neighbors(pos):
            arrival_time = t+1
            if grid.occupied_at(nbr, arrival_time):
                continue
            new_cost = cost_so_far[current] + grid.cost(nbr)
            next_state = (nbr, arrival_time)
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + manhattan(nbr, goal)
                heapq.heappush(frontier, (priority, new_cost, next_state))
                came_from[next_state] = current

    stats.time_taken = time.time() - t0
    return [], stats

# Simple greedy hill-climbing (not time-aware by default) used for replanning in unpredictable mode
import random
def greedy_hill_climb(grid: GridWorld, start: Pos, goal: Pos, max_restarts=10, max_steps=500):
    best_path = []
    best_len = float('inf')
    for r in range(max_restarts):
        current = start
        path = [current]
        for step in range(max_steps):
            if current == goal:
                if len(path) < best_len:
                    best_path = path[:]
                    best_len = len(path)
                break
            nbrs = list(grid.neighbors(current))
            if not nbrs:
                break
            # choose neighbor that reduces heuristic with tie-break random
            nbrs.sort(key=lambda n: (manhattan(n, goal), random.random()))
            current = nbrs[0]
            path.append(current)
        # random restart: choose random start near original start sometimes (simulates random restart)
    return best_path
