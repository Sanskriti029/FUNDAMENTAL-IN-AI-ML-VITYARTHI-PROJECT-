# main.py
import argparse
import numpy as np
import json
from grid import GridWorld, DynamicObstacle
from agent import DeliveryAgent
import time
import matplotlib.pyplot as plt
import os

def load_dynamic(json_path):
    with open(json_path, 'r') as f:
        j = json.load(f)
    obstacles = []
    for o in j.get("moving_obstacles", []):
        obstacles.append(DynamicObstacle(o["id"], o["path"], o.get("start_time", 0)))
    return obstacles

def print_ascii(grid: GridWorld, agent_pos=None, goal=None, occupied_positions=None):
    rows, cols = grid.rows, grid.cols
    for r in range(rows):
        line = ""
        for c in range(cols):
            if agent_pos == (r,c):
                ch = "A"
            elif goal == (r,c):
                ch = "G"
            elif grid.grid[r,c] == -1:
                ch = "#"
            elif occupied_positions and (r,c) in occupied_positions:
                ch = "X"
            elif grid.grid[r,c] == 1:
                ch = "."
            else:
                ch = str(int(grid.grid[r,c]))
            line += ch + " "
        print(line)
    print()

def visualize_path(grid: GridWorld, path, out_file="path.png"):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xticks([])
    ax.set_yticks([])
    arr = grid.grid.copy()
    rows, cols = grid.rows, grid.cols
    # show grid as image
    ax.imshow(arr, cmap='gray_r', origin='upper')
    # plot obstacles from dynamic as red crosses
    for obs in grid.dynamic_obstacles:
        for i,p in enumerate(obs.path):
            ax.plot(p[1], p[0], marker='x')
    if path:
        ys = [p[0] for p in path]
        xs = [p[1] for p in path]
        ax.plot(xs, ys, marker='o', linestyle='-')
    plt.savefig(out_file)
    print(f"Saved visualization to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", required=True, help="map file (txt)")
    parser.add_argument("--algo", default="astar", choices=["bfs","ucs","astar"])
    parser.add_argument("--start", type=int, nargs=2, required=True)
    parser.add_argument("--goal", type=int, nargs=2, required=True)
    parser.add_argument("--dynamic", help="path to dynamic json schedule OR 'unpredictable' for random surprises", default=None)
    parser.add_argument("--visualize", action="store_true", help="Save visualization PNG")
    args = parser.parse_args()

    # load grid
    grid = GridWorld.from_file(args.map, dynamic_json=(args.dynamic if args.dynamic and args.dynamic!="unpredictable" else None))
    # if unpredictable, we'll not load schedule (but main will simulate surprises by marking random occupied cells using a seed)
    agent = DeliveryAgent(grid, algo=args.algo)

    start = tuple(args.start)
    goal = tuple(args.goal)

    # If dynamic schedule specified, attach obstacles
    if args.dynamic and args.dynamic != "unpredictable":
        obstacles = load_dynamic(args.dynamic)
        for o in obstacles:
            grid.add_dynamic_obstacle(o)

    print("Map loaded. Start:", start, "Goal:", goal, "Algo:", args.algo, "Dynamic:", args.dynamic)
    logs = agent.follow_and_replan(start, goal, dynamic_unpredictable=(args.dynamic=="unpredictable"))

    # print summary
    print("Success:", logs.get("success"))
    print("Total nodes expanded (sum across plans):", logs.get("total_nodes_expanded"))
    print("Total planning time (s):", logs.get("total_plan_time"))
    print("Number of plans made:", len(logs.get("plans",[])))
    print("Final path length (steps):", len(logs.get("final_path",[])))
    print()

    # show first plan and final path
    if logs.get("plans"):
        print("First plan (sample):", logs["plans"][0]["path"])
    print("Final path:", logs.get("final_path"))

    if args.visualize:
        out_file = f"visual_{int(time.time())}.png"
        # visualize either the last plan or final path
        path_to_draw = logs.get("final_path") or (logs["plans"][0]["path"] if logs.get("plans") else [])
        if path_to_draw:
            # path contains positions only; visualize them on grid
            visualize_path(grid, path_to_draw, out_file)
        else:
            print("No path to visualize.")
