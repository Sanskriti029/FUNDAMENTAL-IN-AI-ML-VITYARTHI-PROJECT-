# test_project.py
import numpy as np
from grid import GridWorld, DynamicObstacle
import search

def test_small_astar_no_dynamic():
    grid_data = np.array([
        [1,1,1],
        [1,-1,1],
        [1,1,1]
    ])
    gw = GridWorld(grid_data, [])
    path, stats = search.astar_time_aware(gw, (0,0), (2,2), start_time=0)
    assert path != []
    assert path[0] == (0,0)
    assert path[-1] == (2,2)

def test_dynamic_blocking():
    grid_data = np.ones((5,5), dtype=int)
    dyn = [DynamicObstacle("o1", [(1,0),(1,1),(1,2)], start_time=0)]
    gw = GridWorld(grid_data, dyn)
    # planner should avoid (1,2) at time 2 etc.
    path, stats = search.astar_time_aware(gw, (0,0), (2,2), start_time=0)
    assert path != []  # some path should exist
