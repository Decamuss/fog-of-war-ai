import numpy as np
import sys
import os

# Add the project root to the path to import from grid_generation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from grid_generation.environment.priority_queue import PriorityQueue

class RepeatedForwardAStar:
    def __init__(self, grid, start, goal, favor_larger_g=True):
        self.grid = grid
        self.size = len(grid)
        self.start = start
        self.goal = goal
        self.favor_larger_g = favor_larger_g
        
        self.known_grid = np.zeros((self.size, self.size), dtype=bool)
        
        self.g = np.full((self.size, self.size), np.inf)
        self.search = np.zeros((self.size, self.size), dtype=int)
        self.tree = {}
        self.counter = 0
        
        self.expanded_cells = 0
        self.total_path_length = 0
        self.search_count = 0

    def heuristic(self, s):
        return abs(s[0] - self.goal[0]) + abs(s[1] - self.goal[1])

    def compute_path(self):
        # Use PriorityQueue with binary heap instead of dictionaries
        open_queue = PriorityQueue(favor_larger_g=self.favor_larger_g)
        CLOSED = set()
        
        # Track which states are in the open queue
        in_open = set()

        self.g[self.start] = 0
        f_value = self.g[self.start] + self.heuristic(self.start)
        open_queue.put(self.start, f_value, self.g[self.start])
        in_open.add(self.start)

        while not open_queue.empty():
            # Get state with lowest f-value from the priority queue
            s = open_queue.get()
            
            # Skip if already processed (could happen due to duplicate entries in the heap)
            if s not in in_open:
                continue
                
            in_open.remove(s)
            
            CLOSED.add(s)
            self.expanded_cells += 1
            
            if s == self.goal:
                return True
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                succ = (s[0] + dx, s[1] + dy)
                
                if not (0 <= succ[0] < self.size and 0 <= succ[1] < self.size):
                    continue
                if self.known_grid[succ]:
                    continue
                if succ in CLOSED:
                    continue
                
                if self.search[succ] < self.counter:
                    self.g[succ] = np.inf
                    self.search[succ] = self.counter
                
                cost = self.g[s] + 1
                if self.g[succ] > cost:
                    self.g[succ] = cost
                    self.tree[succ] = s
                    
                    f_value = self.g[succ] + self.heuristic(succ)
                    
                    # If already in open, it will be added again with new priority
                    # The heap will handle this by using the new priority when extracted
                    open_queue.put(succ, f_value, self.g[succ])
                    in_open.add(succ)
        
        return False

    def observe_surroundings(self):
        x, y = self.start
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                self.known_grid[nx, ny] = self.grid[nx, ny]

    def run(self):
        while self.start != self.goal:
            self.observe_surroundings()
            
            self.counter += 1
            self.search_count += 1
            self.g[self.start] = 0
            self.search[self.start] = self.counter
            self.g[self.goal] = np.inf
            self.search[self.goal] = self.counter
            
            if not self.compute_path():
                return False, "I cannot reach the target."
            
            path = []
            state = self.goal
            while state != self.start:
                path.append(state)
                state = self.tree[state]
            path.reverse()
            
            # Only move one step at a time
            next_pos = path[0]
            
            # Check if next position is blocked
            if self.known_grid[next_pos]:
                continue  # Replan if blocked
            
            # Move to next position
            self.start = next_pos
            self.total_path_length += 1
            
            # Check if goal reached
            if self.start == self.goal:
                return True, "I reached the target."
        
        return True, "I reached the target." 