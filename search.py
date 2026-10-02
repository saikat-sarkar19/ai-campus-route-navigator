import heapq
import time

class SearchEngine:
    def __init__(self, campus_map):
        self.campus = campus_map

    def search(self, start, goal, algorithm="A*"):
        start_time = time.perf_counter()
        
        initial_cse_state = start in {"CSE_Lab", "CSE_Reflxon", "CSE_Seminar"}
        start_state = (start, initial_cse_state)
        
        h0 = self.campus.get_heuristic(start, goal)
        frontier = []
        
        f0 = h0 if algorithm == "Greedy" else h0
        heapq.heappush(frontier, (f0, start_state, [start], 0))
        
        visited = {}
        nodes_explored = 0

        while frontier:
            f, (curr_node, in_cse), path, g = heapq.heappop(frontier)
            
            state = (curr_node, in_cse)
            if state in visited and visited[state] <= g:
                continue
            visited[state] = g
            nodes_explored += 1

            if curr_node == goal:
                exec_time = time.perf_counter() - start_time
                return path, g, nodes_explored, exec_time

            for neighbor, weight in self.campus.adj[curr_node]:
                if not self.campus.is_valid_transition(curr_node, neighbor, in_cse):
                    continue
                
                next_in_cse = in_cse
                if neighbor == "LiftArea" and in_cse:
                    next_in_cse = False
                elif curr_node == "LiftArea" and neighbor in {"CSE_Lab", "CSE_Reflxon", "CSE_Seminar"}:
                    next_in_cse = True

                next_g = g + weight
                h = self.campus.get_heuristic(neighbor, goal)
                next_f = h if algorithm == "Greedy" else (next_g + h)
                
                heapq.heappush(frontier, (next_f, (neighbor, next_in_cse), path + [neighbor], next_g))

        exec_time = time.perf_counter() - start_time
        return None, float("inf"), nodes_explored, exec_time