import argparse
from environment import load_map
from search import bfs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", required=True, help="Map file path")
    parser.add_argument("--algo", choices=["bfs"], default="bfs")
    args = parser.parse_args()

    grid, start, goal, rows, cols = load_map(args.map)
    print(f"Start: {start}, Goal: {goal}")

    if args.algo == "bfs":
        path = bfs(grid, start, goal, rows, cols)
        print("Path:", path)

if __name__ == "__main__":
    main()
