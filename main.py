from campus_map import CampusMap
from search import SearchEngine
from agents import PathfinderAgent, OrbitAgent

def display_locations(nodes):
    print("\n--- Available Campus Map Locations ---")
    for key, name in nodes.items():
        print(f"[{key}]: {name}")
    print("---------------------------------------\n")

def main():
    campus = CampusMap()
    engine = SearchEngine(campus)
    pathfinder = PathfinderAgent(engine)
    orbit = OrbitAgent(engine)

    display_locations(campus.nodes)

    start = input("Enter starting location code: ").strip()
    goal = input("Enter destination location code: ").strip()

    if start not in campus.nodes or goal not in campus.nodes:
        print("\nInvalid selection. Please use valid key codes.")
        return

    print("\n" + "="*45)
    # PATHFINDER
    path, cost, nodes, t = pathfinder.find_route(start, goal)
    print("PATHFINDER (Greedy Best-First Search)")
    print(f"Route: {' -> '.join(path) if path else 'None'}")
    print(f"Cost: {cost} m")
    print(f"Nodes explored: {nodes}")
    print(f"Time: {t:.6f} s\n")

    # ORBIT
    path, cost, nodes, t = orbit.find_route(start, goal)
    print("ORBIT (A* Search)")
    print(f"Route: {' -> '.join(path) if path else 'None'}")
    print(f"Cost: {cost} m")
    print(f"Nodes explored: {nodes}")
    print(f"Time: {t:.6f} s")
    print("="*45 + "\n")

if __name__ == "__main__":
    main()