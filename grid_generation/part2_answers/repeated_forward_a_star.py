import numpy as np

class RepeatedForwardAStar:
    def __init__(self, grid, start, goal, favor_larger_g=False):
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
        OPEN = {}
        f_values = {}
        CLOSED = set()

        self.g[self.start] = 0
        f_value = self.g[self.start] + self.heuristic(self.start)
        OPEN[self.start] = f_value
        if f_value not in f_values:
            f_values[f_value] = []
        f_values[f_value].append(self.start)

        while OPEN:
            min_f = min(f_values.keys())
            states = f_values[min_f]
            
            s = None
            if self.favor_larger_g:
                max_g = -np.inf
                for state in states:
                    if self.g[state] > max_g:
                        max_g = self.g[state]
                        s = state
            else:
                min_g = np.inf
                for state in states:
                    if self.g[state] < min_g:
                        min_g = self.g[state]
                        s = state
            
            del OPEN[s]
            f_values[min_f].remove(s)
            if not f_values[min_f]:
                del f_values[min_f]
            
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
                    
                    if succ in OPEN:
                        old_f = OPEN[succ]
                        f_values[old_f].remove(succ)
                        if not f_values[old_f]:
                            del f_values[old_f]
                    
                    OPEN[succ] = f_value
                    if f_value not in f_values:
                        f_values[f_value] = []
                    f_values[f_value].append(succ)
        
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
            
            for step in path:
                if self.known_grid[step]:
                    break
                
                self.start = step
                self.total_path_length += 1
                
                if self.start == self.goal:
                    return True, "I reached the target."
                
                self.observe_surroundings()
        
        return True, "I reached the target." 