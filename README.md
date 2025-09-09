# AIML Project
#Autonomous Delivery agent
# 🚚 Autonomous Delivery Agent

## 📖 Project Overview
This project implements an **autonomous delivery agent** that navigates a 2D grid city to deliver packages efficiently.  
The agent:
- Models the environment with **static obstacles, terrain movement costs, and dynamic obstacles**.
- Implements multiple search strategies:
  - **Uninformed Search:** BFS, Uniform-Cost Search (UCS)
  - **Informed Search:** A* with admissible Manhattan heuristic
  - **Local Search Replanning:** Hill-Climbing with random restarts (for dynamic environments)
- Compares algorithms on multiple test maps.

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.8+  
- Install required dependencies:
```bash
pip install -r requirements.txt
