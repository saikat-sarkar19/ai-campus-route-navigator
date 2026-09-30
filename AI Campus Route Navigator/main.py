import os
import sys
from campus_map import CampusGraph
from agents import PathfinderAgent, OrbitAgent
from experiment import ExperimentRunner


def display_header():
    print("=" * 65)
    print("      CU TECHNOLOGY CAMPUS - AI ROUTE NAVIGATOR")
    print("  PATHFINDER (Greedy Best-First) vs ORBIT (A* Search)")
    print("=" * 65)


def list_locations(graph: CampusGraph):
    print("\n--- Available Campus Locations ---")
    normal_locs = [name for name, loc in graph.locations.items() if not loc.is_cse]
    cse_locs = [name for name, loc in graph.locations.items() if loc.is_cse]

    print("General Campus Locations:")
    for i, loc in enumerate(normal_locs, 1):
        print(f"  {i:2d}. {loc}")

    print("\nCSE Zone Locations (Special Access Rule Applies):")
    for i, loc in enumerate(cse_locs, 1):
        print(f"  * {loc}")
    print()


def interactive_navigation(graph: CampusGraph, pathfinder: PathfinderAgent, orbit: OrbitAgent):
    print("\n--- Interactive Route Navigation ---")
    start = input("Enter starting location: ").strip()
    destination = input("Enter destination: ").strip()

    if start not in graph.locations:
        print(f"\n[ERROR] Location '{start}' not found on campus map.")
        list_locations(graph)
        return

    if destination not in graph.locations:
        print(f"\n[ERROR] Location '{destination}' not found on campus map.")
        list_locations(graph)
        return

    res_pf = pathfinder.solve(graph, start, destination)
    res_ob = orbit.solve(graph, start, destination)

    print("\n" + "=" * 50)
    print("PATHFINDER")
    print("Route:")
    print(res_pf["path_str"])
    print(f"\nCost: {res_pf['cost']:.1f} m")
    print(f"Nodes explored: {res_pf['nodes_explored']}")
    print(f"Time: {res_pf['execution_time']:.6f} s")

    print("\nand:")

    print("\nORBIT")
    print("Route:")
    print(res_ob["path_str"])
    print(f"\nCost: {res_ob['cost']:.1f} m")
    print(f"Nodes explored: {res_ob['nodes_explored']}")
    print(f"Time: {res_ob['execution_time']:.6f} s")
    print("=" * 50 + "\n")


def main():
    json_path = "campus.json"
    if not os.path.exists(json_path):
        json_path = os.path.join(os.path.dirname(__file__), "campus.json")

    graph = CampusGraph(json_path)
    pathfinder = PathfinderAgent()
    orbit = OrbitAgent()

    # Check if arguments provided via command line for non-interactive mode
    if len(sys.argv) == 3:
        start_node, goal_node = sys.argv[1], sys.argv[2]
        if start_node in graph.locations and goal_node in graph.locations:
            res_pf = pathfinder.solve(graph, start_node, goal_node)
            res_ob = orbit.solve(graph, start_node, goal_node)

            print("PATHFINDER")
            print("Route:")
            print(res_pf["path_str"])
            print(f"\nCost: {res_pf['cost']:.1f} m")
            print(f"Nodes explored: {res_pf['nodes_explored']}")
            print(f"Time: {res_pf['execution_time']:.6f} s")
            print("\nand:")
            print("\nORBIT")
            print("Route:")
            print(res_ob["path_str"])
            print(f"\nCost: {res_ob['cost']:.1f} m")
            print(f"Nodes explored: {res_ob['nodes_explored']}")
            print(f"Time: {res_ob['execution_time']:.6f} s")
            return

    display_header()

    while True:
        print("1. Find Route between two locations")
        print("2. Run Benchmark Experiments & Save to results.csv")
        print("3. List all campus locations")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            interactive_navigation(graph, pathfinder, orbit)
        elif choice == "2":
            runner = ExperimentRunner(json_path=json_path)
            results = runner.run_experiments()
            print("\n[SUCCESS] Benchmark experiments completed!")
            runner.print_summary_table(results)
            print("[INFO] Results saved to results.csv\n")
        elif choice == "3":
            list_locations(graph)
        elif choice == "4":
            print("\nExiting AI Campus Route Navigator. Goodbye!\n")
            break
        else:
            print("\n[ERROR] Invalid choice. Please select 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
