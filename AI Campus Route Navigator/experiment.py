import csv
import os
from typing import List, Tuple, Dict, Any
from campus_map import CampusGraph
from agents import PathfinderAgent, OrbitAgent


DEFAULT_TEST_PAIRS: List[Tuple[str, str]] = [
    ("Reception", "Library"),
    ("Canteen", "New Building 2"),
    ("Entry Gate 1", "CSE Laboratory"),
    ("Auditorium Hall", "CSE_AKC Seminar Hall"),
    ("Library", "Canteen"),
    ("CSE Laboratory", "Reception"),
    ("Entry Gate 1", "Entry Gate 2"),
    ("Parking Area", "New Building 1"),
    ("CSE_Reflxon Room", "CSE Laboratory"),
    ("Auditorium Hall", "Gate 4")
]


class ExperimentRunner:
    """Runs automated experiments comparing PATHFINDER and ORBIT agents."""

    def __init__(self, json_path: str = "campus.json", csv_path: str = "results.csv"):
        self.graph = CampusGraph(json_path)
        self.csv_path = csv_path
        self.pathfinder = PathfinderAgent()
        self.orbit = OrbitAgent()

    def run_experiments(self, test_pairs: List[Tuple[str, str]] = DEFAULT_TEST_PAIRS) -> List[Dict[str, Any]]:
        """Executes search for all source-destination pairs using both agents."""
        all_results = []

        for start, goal in test_pairs:
            # Run PATHFINDER
            res_pathfinder = self.pathfinder.solve(self.graph, start, goal)
            res_pathfinder["route_label"] = f"{start} -> {goal}"
            all_results.append(res_pathfinder)

            # Run ORBIT
            res_orbit = self.orbit.solve(self.graph, start, goal)
            res_orbit["route_label"] = f"{start} -> {goal}"
            all_results.append(res_orbit)

        self.save_to_csv(all_results)
        return all_results

    def save_to_csv(self, results: List[Dict[str, Any]]):
        """Saves experimental results to results.csv file."""
        fieldnames = ["Route", "Agent", "Path", "Cost", "Nodes Explored", "Time"]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in results:
                writer.writerow({
                    "Route": r.get("route_label", ""),
                    "Agent": r.get("agent", ""),
                    "Path": r.get("path_str", ""),
                    "Cost": f"{r.get('cost', 0.0):.1f} m",
                    "Nodes Explored": r.get("nodes_explored", 0),
                    "Time": f"{r.get('execution_time', 0.0):.6f} s"
                })

    def print_summary_table(self, results: List[Dict[str, Any]]):
        """Prints formatted comparative evaluation summary."""
        print("=" * 110)
        print(f"{'ROUTE':<38} | {'AGENT':<10} | {'COST':<8} | {'EXPLORED':<8} | {'TIME (s)':<10} | {'PATH'}")
        print("=" * 110)

        for i in range(0, len(results), 2):
            pf = results[i]
            ob = results[i+1]

            route_name = pf['route_label']
            print(f"{route_name:<38} | {pf['agent']:<10} | {pf['cost']:<8.1f} | {pf['nodes_explored']:<8} | {pf['execution_time']:<10.6f} | {pf['path_str']}")
            print(f"{'':<38} | {ob['agent']:<10} | {ob['cost']:<8.1f} | {ob['nodes_explored']:<8} | {ob['execution_time']:<10.6f} | {ob['path_str']}")
            
            diff_cost = pf['cost'] != ob['cost']
            status = "DIFFERENT ROUTE DETECTED!" if diff_cost else "Identical Route"
            print(f"  --> Status: {status}")
            print("-" * 110)


if __name__ == "__main__":
    runner = ExperimentRunner()
    results = runner.run_experiments()
    runner.print_summary_table(results)
