class PathfinderAgent:
    """Agent 1: Greedy Best-First Search f(n) = h(n)"""
    def __init__(self, search_engine):
        self.engine = search_engine

    def find_route(self, start, goal):
        return self.engine.search(start, goal, algorithm="Greedy")


class OrbitAgent:
    """Agent 2: A* Search f(n) = g(n) + h(n)"""
    def __init__(self, search_engine):
        self.engine = search_engine

    def find_route(self, start, goal):
        return self.engine.search(start, goal, algorithm="A*")