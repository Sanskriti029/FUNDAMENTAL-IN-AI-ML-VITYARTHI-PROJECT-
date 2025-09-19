# agent.py
from typing import Tuple, List, Optional
from grid import GridWorld, DynamicObstacle
import search
import time
import copy

Pos = Tuple[int,int]

class DeliveryAgent:
    def __init__(self, grid: GridWorld, algo: str = "astar", replanner: str = "hill", planning_horizon: int = 200):
        """
        algo: 'bfs', 'ucs', 'astar'
        replanner: 'hill' (greedy hill-climb) used when unpredictable obstacle appears
        planning_horizon: max future timesteps to consider when planning
        """
        self.grid = grid
        self.algo = algo
        self.replanner = replanner
        self.planning_horizon = planning_horizon

    def plan(self, start: Pos, goal: Pos, start_time: int = 0):
        """
        Plan using the selected algorithm in a time-aware manner.
        Returns path (list of positions) and search stats.
        """
        if self.algo == "bfs":
            return search.bfs_time_aware(self.grid, start, goal, start_time, max_time=self.planning_horizon)
        elif self.algo == "ucs":
            return search.ucs_time_aware(self.grid, start, goal, start_time, max_time=self.planning_horizon)
        elif self.algo == "astar":
            return search.astar_time_aware(self.grid, start, goal, start_time, max_time=self.planning_horizon)
        else:
            raise ValueError("Unknown algo")

    def follow_and_replan(self, start: Pos, goal: Pos, dynamic_unpredictable: bool = False, max_steps: int = 1000):
        """
        Simulate the agent executing the plan step-by-step. If the next cell is occupied unexpectedly,
        perform replanning with either time-aware planner (if deterministic schedule known) or local replanner.
        Returns log dict with metrics and history.
        """
        history = []
        logs = {
            "plans": [],
            "total_nodes_expanded": 0,
            "total_plan_time": 0.0,
            "final_path": [],
            "success": False
        }

        current = start
        t = 0
        plan, stats = self.plan(current, goal, start_time=t)
        logs["plans"].append({"time": t, "path": plan, "stats": stats.__dict__})
        logs["total_nodes_expanded"] += stats.nodes_expanded
        logs["total_plan_time"] += stats.time_taken

        if not plan:
            return logs

        # iterate following plan
        step_idx = 1  # next index to move to in plan
        for step in range(max_steps):
            # if reached goal
            if current == goal:
                logs["success"] = True
                logs["final_path"] = history[:]
                return logs

            # if plan exhausted or next step mismatch, replan
            if step_idx >= len(plan):
                # need to replan from current
                plan, stats = self.plan(current, goal, start_time=t)
                logs["plans"].append({"time": t, "path": plan, "stats": stats.__dict__})
                logs["total_nodes_expanded"] += stats.nodes_expanded
                logs["total_plan_time"] += stats.time_taken
                step_idx = 1
                if not plan:
                    break

            next_pos = plan[step_idx]

            # If dynamic_unpredictable is True, a "surprise" obstacle may appear at the next cell at this time
            if dynamic_unpredictable and self.grid.occupied_at(next_pos, t+1):
                # unexpected block -> try local replanner (greedy hill climb)
                local = []
                if self.replanner == "hill":
                    local = search.greedy_hill_climb(self.grid, current, goal)
                # if local found a route, follow it (no time-awareness here)
                if local:
                    # adopt local route as new plan
                    plan = [current] + local[1:]
                    step_idx = 1
                    logs["plans"].append({"time": t, "path": plan, "stats": {"nodes_expanded": 0, "time_taken": 0}})
                else:
                    # fallback: try time-aware replanning (A*)
                    plan, stats = self.plan(current, goal, start_time=t)
                    logs["plans"].append({"time": t, "path": plan, "stats": stats.__dict__})
                    logs["total_nodes_expanded"] += stats.nodes_expanded
                    logs["total_plan_time"] += stats.time_taken
                    step_idx = 1
                    if not plan:
                        break

            # If deterministic schedule: just ensure cell isn't occupied at arrival
            if self.grid.occupied_at(next_pos, t+1):
                # must replan now (should not happen if planner had correct schedule, but robust)
                plan, stats = self.plan(current, goal, start_time=t)
                logs["plans"].append({"time": t, "path": plan, "stats": stats.__dict__})
                logs["total_nodes_expanded"] += stats.nodes_expanded
                logs["total_plan_time"] += stats.time_taken
                step_idx = 1
                if not plan:
                    break
                continue

            # execute move
            current = next_pos
            history.append(current)
            t += 1
            step_idx += 1

        # out of steps
        logs["final_path"] = history
        logs["success"] = (current == goal)
        return logs
