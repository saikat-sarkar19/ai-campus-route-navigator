import heapq
import time
from typing import List, Dict, Any, Optional
from campus_map import CampusGraph, SearchState


class SearchNode:
    """Represents a node in the search tree."""

    def __init__(self, state: SearchState, g: float, h: float, f: float, parent: Optional['SearchNode'] = None):
        self.state = state
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent

    def reconstruct_path(self) -> List[str]:
        """Reconstructs the sequence of node names from start to current node."""
        path = []
        curr: Optional[SearchNode] = self
        while curr is not None:
            path.append(curr.state.node_name)
            curr = curr.parent
        path.reverse()
        return path


def greedy_best_first_search(graph: CampusGraph, start_node: str, goal_node: str) -> Dict[str, Any]:
    """
    PATHFINDER Agent Search Strategy: Greedy Best-First Search
    Evaluation Function: f(n) = h(n)
    Expands the node that appears closest to the destination.
    """
    start_time = time.perf_counter()

    if start_node not in graph.locations or goal_node not in graph.locations:
        return {"path": [], "cost": 0.0, "nodes_explored": 0, "execution_time": 0.0, "found": False}

    initial_state = graph.get_initial_state(start_node, goal_node)
    h0 = graph.get_heuristic(start_node, goal_node)
    start_search_node = SearchNode(state=initial_state, g=0.0, h=h0, f=h0, parent=None)

    # Frontier stores tuple: (f_score, h_score, tie_breaker_counter, search_node)
    counter = 0
    frontier = []
    heapq.heappush(frontier, (h0, h0, counter, start_search_node))

    visited: Dict[SearchState, float] = {initial_state: h0}
    nodes_explored = 0

    while frontier:
        _, _, _, current_node = heapq.heappop(frontier)
        nodes_explored += 1

        if current_node.state.node_name == goal_node:
            end_time = time.perf_counter()
            path = current_node.reconstruct_path()
            return {
                "path": path,
                "cost": current_node.g,
                "nodes_explored": nodes_explored,
                "execution_time": end_time - start_time,
                "found": True
            }

        for next_state, edge_weight in graph.get_valid_neighbors(current_node.state):
            h_val = graph.get_heuristic(next_state.node_name, goal_node)
            g_val = current_node.g + edge_weight

            if next_state not in visited:
                visited[next_state] = h_val
                counter += 1
                child_node = SearchNode(state=next_state, g=g_val, h=h_val, f=h_val, parent=current_node)
                heapq.heappush(frontier, (h_val, h_val, counter, child_node))

    end_time = time.perf_counter()
    return {
        "path": [],
        "cost": 0.0,
        "nodes_explored": nodes_explored,
        "execution_time": end_time - start_time,
        "found": False
    }


def a_star_search(graph: CampusGraph, start_node: str, goal_node: str) -> Dict[str, Any]:
    """
    ORBIT Agent Search Strategy: A* Search
    Evaluation Function: f(n) = g(n) + h(n)
    Combines exact cost travelled g(n) and estimated remaining distance h(n).
    Guarantees optimal shortest path when heuristic h(n) is admissible and consistent.
    """
    start_time = time.perf_counter()

    if start_node not in graph.locations or goal_node not in graph.locations:
        return {"path": [], "cost": 0.0, "nodes_explored": 0, "execution_time": 0.0, "found": False}

    initial_state = graph.get_initial_state(start_node, goal_node)
    h0 = graph.get_heuristic(start_node, goal_node)
    start_search_node = SearchNode(state=initial_state, g=0.0, h=h0, f=h0, parent=None)

    counter = 0
    frontier = []
    heapq.heappush(frontier, (h0, h0, counter, start_search_node))

    g_score: Dict[SearchState, float] = {initial_state: 0.0}
    nodes_explored = 0

    while frontier:
        f_val, _, _, current_node = heapq.heappop(frontier)
        nodes_explored += 1

        if current_node.state.node_name == goal_node:
            end_time = time.perf_counter()
            path = current_node.reconstruct_path()
            return {
                "path": path,
                "cost": current_node.g,
                "nodes_explored": nodes_explored,
                "execution_time": end_time - start_time,
                "found": True
            }

        for next_state, edge_weight in graph.get_valid_neighbors(current_node.state):
            tentative_g = current_node.g + edge_weight

            if next_state not in g_score or tentative_g < g_score[next_state]:
                g_score[next_state] = tentative_g
                h_val = graph.get_heuristic(next_state.node_name, goal_node)
                f_score = tentative_g + h_val
                counter += 1
                child_node = SearchNode(state=next_state, g=tentative_g, h=h_val, f=f_score, parent=current_node)
                heapq.heappush(frontier, (f_score, h_val, counter, child_node))

    end_time = time.perf_counter()
    return {
        "path": [],
        "cost": 0.0,
        "nodes_explored": nodes_explored,
        "execution_time": end_time - start_time,
        "found": False
    }
