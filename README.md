<<<<<<< Updated upstream
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
=======
# Autonomous Delivery Agent — Grid Planners + Dynamic Replanning

## Overview
This project implements:
- Grid environment with integer terrain costs (>=1) and static obstacles (-1).
- Deterministic moving obstacles (schedule known for planning horizon) and unpredictable moving obstacles (for local search testing).
- Planners: BFS, UCS (time-aware), A* with Manhattan heuristic (time-aware).
- Local replanning strategy: greedy hill-climbing with random restarts.
- CLI to run planners on provided map files and log results (path cost, nodes expanded, planning time).
- Visualization (ASCII or PNG).

## Install
```bash
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
>>>>>>> Stashed changes
pip install -r requirements.txt
