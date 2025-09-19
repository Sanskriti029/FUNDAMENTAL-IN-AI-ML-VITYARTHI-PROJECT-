# experiments.py
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

maps = [
    ("maps/small.txt", (0,0), (4,4)),
    ("maps/medium.txt", (0,0), (9,9)),
    ("maps/large.txt", (0,0), (19,19))
]

algos = ["bfs", "ucs", "astar"]

results = []

for map_file, start, goal in maps:
    for algo in algos:
        # run main.py as subprocess
        cmd = [
            "python", "main.py",
            "--map", map_file,
            "--algo", algo,
            "--start", str(start[0]), str(start[1]),
            "--goal", str(goal[0]), str(goal[1])
        ]
        print("Running:", " ".join(cmd))
        proc = subprocess.run(cmd, capture_output=True, text=True)
        out = proc.stdout

        # parse outputs (very simple parsing)
        lines = out.splitlines()
        success = "Success: True" in out
        final_path_len = 0
        for line in lines:
            if line.startswith("Final path length"):
                final_path_len = int(line.split(":")[-1].strip())

        nodes = 0
        time_taken = 0.0
        for line in lines:
            if "Total nodes expanded" in line:
                nodes = int(line.split(":")[-1].strip())
            if "Total planning time" in line:
                time_taken = float(line.split(":")[-1].strip())

        results.append({
            "Map": map_file,
            "Algo": algo,
            "Success": success,
            "PathLen": final_path_len,
            "Nodes": nodes,
            "Time": time_taken
        })

# save to CSV
df = pd.DataFrame(results)
df.to_csv("experiment_results.csv", index=False)
print("\nSaved results to experiment_results.csv")
print(df)

## plot nodes expanded
df.pivot(index="Map", columns="Algo", values="Nodes").plot(kind="bar")
plt.ylabel("Nodes Expanded")
plt.title("Nodes Expanded by Algo & Map")
plt.savefig("nodes_vs_map.png")
plt.close()

# plot planning time
df.pivot(index="Map", columns="Algo", values="Time").plot(kind="bar")
plt.ylabel("Planning Time (s)")
plt.title("Planning Time by Algo & Map")
plt.savefig("time_vs_map.png")
plt.close()

