from abc import ABC, abstractmethod
from typing import Dict, Any
from campus_map import CampusGraph
from search import greedy_best_first_search, a_star_search


class Agent(ABC):
    """Abstract Base Class for AI Campus Routing Agents."""

    def __init__(self, name: str, algorithm_name: str):
        self.name = name
        self.algorithm_name = algorithm_name

    @abstractmethod
    def solve(self, graph: CampusGraph, start_node: str, goal_node: str) -> Dict[str, Any]:
        """Solves the route from start_node to goal_node."""
        pass


class PathfinderAgent(Agent):
    """
    PATHFINDER Agent
    Uses Greedy Best-First Search with f(n) = h(n).
    Always selects the node that appears visually/heuristically closest to the destination.
    """

    def __init__(self):
        super().__init__(name="PATHFINDER", algorithm_name="Greedy Best-First Search")

    def solve(self, graph: CampusGraph, start_node: str, goal_node: str) -> Dict[str, Any]:
        res = greedy_best_first_search(graph, start_node, goal_node)
        res["agent"] = self.name
        res["algorithm"] = self.algorithm_name
        res["path_str"] = " -> ".join(res["path"]) if res["found"] else "No valid route found"
        return res


class OrbitAgent(Agent):
    """
    ORBIT Agent
    Uses A* Search with f(n) = g(n) + h(n).
    Considers both actual cost travelled so far g(n) and estimated remaining distance h(n).
    """

    def __init__(self):
        super().__init__(name="ORBIT", algorithm_name="A* Search")

    def solve(self, graph: CampusGraph, start_node: str, goal_node: str) -> Dict[str, Any]:
        res = a_star_search(graph, start_node, goal_node)
        res["agent"] = self.name
        res["algorithm"] = self.algorithm_name
        res["path_str"] = " -> ".join(res["path"]) if res["found"] else "No valid route found"
        return res
