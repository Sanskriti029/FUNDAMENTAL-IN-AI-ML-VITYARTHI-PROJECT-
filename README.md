# 📦 Autonomous Delivery Agent — Grid Path Planning with Dynamic Obstacles  

## 📖 Overview  
This project implements an **autonomous delivery agent** navigating a **2D grid city** with static and dynamic obstacles.  
The agent delivers packages efficiently while considering **terrain costs, limited time, and moving obstacles**.  

We implemented and compared:  
- **BFS (Breadth-First Search)**  
- **UCS (Uniform Cost Search)**  
- **A\*** (with Manhattan heuristic)  
- **Hill Climbing with Random Restarts** (local replanning for unpredictable obstacles)  

The system supports:  
- Static maps (terrain & walls)  
- Deterministic dynamic obstacles (predefined vehicle schedules)  
- Unpredictable dynamic obstacles (random surprises)  
- Experiment benchmarking and plotting  

---

## ⚙️ Setup Instructions  

### 1. Clone / Copy the Project  
```bash
cd path/to/project
```
### 2. Create Virtual Environment (Recommended)
```bash

python -m venv venv
# Activate:
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```
bash

pip install -r requirements.txt
```
Dependencies include:
- numpy
- matplotlib
- pandas
- pytest


# 🚀 Usage Examples
### 1. Run Agent on a Static Map
```
bash

python main.py --map maps/small.txt --algo astar --start 0 0 --goal 4 4
```

### 2. Run with Deterministic Dynamic Obstacles
```
bash

python main.py --map maps/small.txt --algo astar --start 0 0 --goal 4 4 --dynamic maps/dynamic.json --visualize
```

### 3. Run with Unpredictable Dynamic Obstacles
 ```
bash

python main.py --map maps/small.txt --algo astar --start 0 0 --goal 4 4 --dynamic unpredictable
```

### 4. Run Experiments (Generate Results + Plots)
```
bash

python experiments.py
```

# Outputs:


- experiment_results.csv
- nodes_vs_map.png
- time_vs_map.png


# ✅ Testing
Run unit tests:

```
bash

python -m pytest test_project.py
```

# 📊 Example Results
```
bash
Map	Algo	PathLen	Nodes	Time (s)
Small	BFS	8	20	0.001
Small	UCS	8	15	0.001
Small	A*	8	10	0.0005
Medium	BFS	20	300	0.01
Medium	UCS	22	180	0.008
Medium	A*	22	90	0.005
```

#📌 Conclusion
A* is most efficient (fewer nodes, faster planning).

BFS works only for small, unweighted maps.

UCS is cost-optimal but slower at scale.

Replanning (deterministic + unpredictable) allows the agent to adapt in dynamic environments.

This demonstrates how classical AI search methods extend naturally into time-aware planning for real-world inspired delivery problems.
