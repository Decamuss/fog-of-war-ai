import numpy as np
from utils.min_heap import MinHeap  
from grid_generation.environment.priority_queue import PriorityQueue  

class RepeatedForwardAStar:
    def __init__(self, grid, start, goal, favor_larger_g=False):
        """Initialize Repeated Forward A*"""
        self.grid = grid
        self.size = len(grid)
        self.start = start
        self.goal = goal
        self.g = np.full((self.size, self.size), np.inf)  # Cost from start
        self.search = np.zeros((self.size, self.size), dtype=int)  # Search iteration count
        self.tree = {}  # Backpointers for path reconstruction
        self.counter = 0  # Search counter
        self.favor_larger_g = favor_larger_g  # Tie-breaking strategy

    def heuristic(self, s):
        """Compute Manhattan distance heuristic."""
        return abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1])

    def compute_path(self):
        """A* pathfinding with tie-breaking."""
        OPEN = PriorityQueue(self.favor_larger_g)
        CLOSED = set()

        OPEN.put(self.start, self.g[self.start] + self.heuristic(self.start), self.g[self.start])

        while not OPEN.empty():
            s = OPEN.get()  # Get the state with the best priority
            CLOSED.add(s)

            # Stop if the goal is reached
            if s == self.goal:
                return True

            # Expand neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
                succ = (s[0] + dx, s[1] + dy)

                if not (0 <= succ[0] < self.size and 0 <= succ[1] < self.size):  # Out of bounds
                    continue
                if self.grid[succ]:  # Blocked cell
                    continue
                
                if self.search[succ] < self.counter:
                    self.g[succ] = np.inf
                    self.search[succ] = self.counter

                cost = self.g[s] + 1  # Assume uniform cost

                if self.g[succ] > cost:
                    self.g[succ] = cost
                    self.tree[succ] = s  # Store backpointer
                    OPEN.put(succ, self.g[succ] + self.heuristic(succ), self.g[succ])

        return False  # No path found

    def run(self):
        """Main loop for Repeated Forward A*."""
        self.counter += 1
        self.g[self.start] = 0
        self.search[self.start] = self.counter
        self.g[self.goal] = np.inf
        self.search[self.goal] = self.counter

        if not self.compute_path():
            print("I cannot reach the target.")
            return False

        # Follow the path from goal to start
        path = []
        state = self.goal
        while state != self.start:
            path.append(state)
            state = self.tree[state]
        path.reverse()

        # Move along the path
        for step in path:
            self.start = step
            print(f"Moved to {self.start}")

        print("I reached the target.")
        return True