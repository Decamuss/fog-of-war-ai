import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from grid_generation.environment.priority_queue import PriorityQueue

class AdaptiveAStar:
    def __init__(self, grid, start, goal, favor_larger_g=True):
        self.grid = grid
        self.size = len(grid)
        self.start = start
        self.goal = goal
        self.favor_larger_g = favor_larger_g
        
        self.known_grid = np.zeros((self.size, self.size), dtype=bool)
        
        self.g = np.full((self.size, self.size), np.inf)
        self.h = np.zeros((self.size, self.size))
        self.search = np.zeros((self.size, self.size), dtype=int)
        self.tree = {}
        self.counter = 0
        
        for i in range(self.size):
            for j in range(self.size):
                self.h[i, j] = abs(i - self.goal[0]) + abs(j - self.goal[1])
        
        self.expanded_cells = 0
        self.total_path_length = 0
        self.search_count = 0

    def compute_path(self):
        open_queue = PriorityQueue(favor_larger_g=self.favor_larger_g)
        CLOSED = set()
        
        in_open = set()

        self.g[self.start] = 0
        f_value = self.g[self.start] + self.h[self.start]
        open_queue.put(self.start, f_value, self.g[self.start])
        in_open.add(self.start)

        while not open_queue.empty():
            s = open_queue.get()
            
            if s not in in_open:
                continue
                
            in_open.remove(s)
            
            if s == self.goal:
                CLOSED.add(s)
                self.expanded_cells += 1
                break
            
            CLOSED.add(s)
            self.expanded_cells += 1
            
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
                
                if self.g[succ] > self.g[s] + 1:
                    self.g[succ] = self.g[s] + 1
                    self.tree[succ] = s
                    
                    f_value = self.g[succ] + self.h[succ]
                    
                    open_queue.put(succ, f_value, self.g[succ])
                    in_open.add(succ)
        
        if self.g[self.goal] != np.inf:
            goal_g = self.g[self.goal]
            for s in CLOSED:
                new_h = goal_g - self.g[s]
                
                if new_h > self.h[s]:
                    self.h[s] = new_h
            return True
        return False

    def observe_surroundings(self):
        x, y = self.start
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                self.known_grid[nx, ny] = self.grid[nx, ny]

    def run(self):
        self.expanded_cells = 0
        self.total_path_length = 0
        self.search_count = 0
        
        while self.start != self.goal:
            self.observe_surroundings()
            
            self.counter += 1
            self.search_count += 1
            
            self.g[self.start] = 0
            self.search[self.start] = self.counter
            self.g[self.goal] = np.inf
            self.search[self.goal] = self.counter
            
            if not self.compute_path():
                return False, "Cannot reach the target"
            
            current = self.goal
            path = []
            while current != self.start:
                path.append(current)
                current = self.tree[current]
            path.reverse()
            
            next_pos = path[0]
            
            if self.known_grid[next_pos]:
                continue
            
            self.start = next_pos
            self.total_path_length += 1
            
            if self.start == self.goal:
                return True, "Target reached"
        
        return True, "Target reached"