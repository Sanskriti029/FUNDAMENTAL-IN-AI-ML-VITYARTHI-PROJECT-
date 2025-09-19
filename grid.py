# grid.py
import numpy as np
import json
from typing import List, Tuple, Dict

Pos = Tuple[int, int]

class DynamicObstacle:
    def __init__(self, oid: str, path: List[Pos], start_time: int = 0):
        self.id = oid
        self.path = [tuple(p) for p in path]
        self.start_time = int(start_time)

    def position_at(self, t: int):
        idx = t - self.start_time
        if idx < 0 or idx >= len(self.path):
            return None
        return self.path[idx]

class GridWorld:
    def __init__(self, grid: np.ndarray, dynamic_obstacles: List[DynamicObstacle]=None):
        """
        grid: 2D numpy array: -1 => static obstacle, >=1 => terrain cost
        dynamic_obstacles: list of DynamicObstacle
        """
        self.grid = np.array(grid)
        self.rows, self.cols = self.grid.shape
        self.dynamic_obstacles = dynamic_obstacles or []

    @classmethod
    def from_file(cls, file_path: str, dynamic_json: str = None):
        grid = np.loadtxt(file_path, dtype=int)
        dyn = []
        if dynamic_json:
            if dynamic_json.strip().lower() == "unpredictable":
                # caller will handle unpredictable mode (no schedule here)
                dyn = []
            else:
                with open(dynamic_json, 'r') as f:
                    j = json.load(f)
                for o in j.get("moving_obstacles", []):
                    dyn.append(DynamicObstacle(o["id"], o["path"], o.get("start_time", 0)))
        return cls(grid, dyn)

    def in_bounds(self, pos: Pos) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, pos: Pos) -> bool:
        return self.grid[pos] != -1

    def cost(self, pos: Pos) -> int:
        return int(self.grid[pos])

    def neighbors(self, pos: Pos):
        r, c = pos
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        for dr, dc in moves:
            new = (r+dr, c+dc)
            if self.in_bounds(new) and self.passable(new):
                yield new

    def occupied_at(self, pos: Pos, t: int) -> bool:
        """
        Returns True if any dynamic obstacle occupies `pos` at time t.
        """
        for obs in self.dynamic_obstacles:
            p = obs.position_at(t)
            if p is not None and tuple(p) == tuple(pos):
                return True
        return False

    def add_dynamic_obstacle(self, obstacle: DynamicObstacle):
        self.dynamic_obstacles.append(obstacle)
