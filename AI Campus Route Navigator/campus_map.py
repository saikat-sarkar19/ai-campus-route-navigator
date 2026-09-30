import json
import math
from typing import Dict, List, Tuple, Optional, Set

CSE_LOCATIONS = {"CSE Laboratory", "CSE_AKC Seminar Hall", "CSE_Reflxon Room"}
TOWER2_ENTRIES = {"Tower 2 Front Entry", "Tower 2 Rear Entry"}
LIFT_AREA = "Lift Area"


class Location:
    """Represents a physical node on the campus map."""

    def __init__(self, name: str, coordinates: List[float], is_cse: bool = False, description: str = ""):
        self.name = name
        self.x = float(coordinates[0])
        self.y = float(coordinates[1])
        self.is_cse = is_cse
        self.description = description

    def __repr__(self):
        return f"Location('{self.name}')"


class SearchState:
    """
    State representation for pathfinding algorithms enforcing CSE zone routing rules.
    CSE Modes:
      - 'OUTSIDE': Normal state outside the CSE zone.
      - 'READY_TO_ENTER': At Lift Area having entered directly from Tower 2 Front/Rear Entry.
      - 'INSIDE': Inside the CSE zone (at a CSE-labelled location).
      - 'EXITING': At Lift Area having arrived directly from a CSE-labelled location.
    """

    def __init__(self, node_name: str, cse_mode: str = "OUTSIDE"):
        self.node_name = node_name
        self.cse_mode = cse_mode

    def __eq__(self, other):
        if not isinstance(other, SearchState):
            return False
        return self.node_name == other.node_name and self.cse_mode == other.cse_mode

    def __hash__(self):
        return hash((self.node_name, self.cse_mode))

    def __repr__(self):
        return f"State({self.node_name}, mode={self.cse_mode})"


class CampusGraph:
    """Graph representation of the campus layout and connections."""

    def __init__(self, json_path: Optional[str] = None):
        self.locations: Dict[str, Location] = {}
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        if json_path:
            self.load_from_json(json_path)

    def load_from_json(self, json_path: str):
        """Loads graph nodes and weighted edges from campus.json."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.locations.clear()
        self.adj.clear()

        for name, info in data["nodes"].items():
            loc = Location(
                name=name,
                coordinates=info["coordinates"],
                is_cse=info.get("is_cse", False),
                description=info.get("description", "")
            )
            self.locations[name] = loc
            self.adj[name] = []

        for edge in data["edges"]:
            u = edge["from"]
            v = edge["to"]
            w = float(edge["weight"])
            if u in self.locations and v in self.locations:
                self.adj[u].append((v, w))
                self.adj[v].append((u, w))

    def get_heuristic(self, node_name: str, goal_name: str) -> float:
        """
        Calculates the Euclidean distance heuristic h(n) between current node and goal node.
        Used as the estimated remaining cost in search algorithms.
        """
        if node_name not in self.locations or goal_name not in self.locations:
            return 0.0
        loc1 = self.locations[node_name]
        loc2 = self.locations[goal_name]
        return math.sqrt((loc1.x - loc2.x) ** 2 + (loc1.y - loc2.y) ** 2)

    def get_initial_state(self, start_node: str, goal_node: str) -> SearchState:
        """Determines the appropriate initial SearchState for search algorithms."""
        if start_node in CSE_LOCATIONS:
            return SearchState(start_node, "INSIDE")
        elif start_node == LIFT_AREA and goal_node in CSE_LOCATIONS:
            return SearchState(start_node, "READY_TO_ENTER")
        else:
            return SearchState(start_node, "OUTSIDE")

    def get_valid_neighbors(self, state: SearchState) -> List[Tuple[SearchState, float]]:
        """
        Returns valid neighboring search states and edge weights according to the
        Special CSE Routing Rule (Part 7 of Assignment).

        Rule summary:
        1. Entry to CSE zone: Tower 2 Front/Rear Entry -> Lift Area -> CSE-labelled location.
        2. Inside CSE zone: Only CSE-labelled locations can be visited until returning to Lift Area.
        3. Exiting CSE zone: CSE-labelled location -> Lift Area -> Tower 2 Front/Rear Entry -> Other locations.
        """
        u = state.node_name
        mode = state.cse_mode
        valid_neighbors: List[Tuple[SearchState, float]] = []

        for v, weight in self.adj.get(u, []):
            is_v_cse = v in CSE_LOCATIONS

            if mode == "OUTSIDE":
                if is_v_cse:
                    # Cannot enter CSE location directly from OUTSIDE mode
                    continue
                elif v == LIFT_AREA:
                    next_mode = "READY_TO_ENTER" if u in TOWER2_ENTRIES else "OUTSIDE"
                    valid_neighbors.append((SearchState(v, next_mode), weight))
                else:
                    valid_neighbors.append((SearchState(v, "OUTSIDE"), weight))

            elif mode == "READY_TO_ENTER":
                # Currently at Lift Area after entering from Tower 2 Front/Rear Entry
                if is_v_cse:
                    valid_neighbors.append((SearchState(v, "INSIDE"), weight))
                elif v == LIFT_AREA:
                    continue
                else:
                    # Can also choose to go to non-CSE locations from Lift Area
                    valid_neighbors.append((SearchState(v, "OUTSIDE"), weight))

            elif mode == "INSIDE":
                # Currently inside CSE zone
                if is_v_cse:
                    valid_neighbors.append((SearchState(v, "INSIDE"), weight))
                elif v == LIFT_AREA:
                    valid_neighbors.append((SearchState(v, "EXITING"), weight))
                else:
                    # Cannot jump to other non-CSE campus locations directly from CSE
                    continue

            elif mode == "EXITING":
                # Currently at Lift Area after coming from CSE zone
                if v in TOWER2_ENTRIES:
                    valid_neighbors.append((SearchState(v, "OUTSIDE"), weight))
                else:
                    # Must pass through Tower 2 Front/Rear Entry to return to general campus
                    continue

        return valid_neighbors
