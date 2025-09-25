# 📦 Autonomous Delivery Agent — Grid Path Planning with Dynamic Obstacles  

## 📖 Overview  
This project implements an **autonomous delivery agent** navigating a **2D grid city** with static and dynamic obstacles. The agent must deliver packages efficiently while considering terrain costs, limited time, and moving obstacles.  

We implemented and compared **BFS, Uniform Cost Search (UCS), A\*, and a local search replanning strategy (hill climbing)**. The system includes:  
- **Static environments** (different terrains, walls).  
- **Dynamic environments** (deterministic vehicle schedules & unpredictable obstacles).  
- **Experimental runner** to benchmark algorithms across maps.  
- **Plots & logs** for your report.  

---

## ⚙️ Setup Instructions  

### 1. Clone / Copy the Project  
```bash
cd path/to/project
## 2. Create Virtual Environment 
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
## 3. Install Dependencies
pip install -r requirements.txt
