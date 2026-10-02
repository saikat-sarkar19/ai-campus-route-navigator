import csv
from campus_map import CampusMap
from search import SearchEngine
from agents import PathfinderAgent, OrbitAgent

def run_experiments():
    campus = CampusMap()
    engine = SearchEngine(campus)
    pathfinder = PathfinderAgent(engine)
    orbit = OrbitAgent(engine)

    test_pairs = [
        ("Reception", "Library"),
        ("Canteen", "NewBuilding2"),
        ("G1", "CSE_Lab"),
        ("Auditorium", "CSE_Seminar"),
        ("Library", "Canteen")
    ]

    fieldnames = ["Source", "Destination", "Agent", "Path", "Cost (m)", "Nodes Explored", "Time (s)"]
    
    with open("results.csv", mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for src, dest in test_pairs:
            for agent_name, agent in [("PATHFINDER (Greedy)", pathfinder), ("ORBIT (A*)", orbit)]:
                path, cost, nodes, t = agent.find_route(src, dest)
                writer.writerow({
                    "Source": src,
                    "Destination": dest,
                    "Agent": agent_name,
                    "Path": " -> ".join(path) if path else "No Path Found",
                    "Cost (m)": cost,
                    "Nodes Explored": nodes,
                    "Time (s)": f"{t:.6f}"
                })
    print("Experiments logged to results.csv successfully.")

if __name__ == "__main__":
    run_experiments()