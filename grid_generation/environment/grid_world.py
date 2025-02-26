import numpy as np
import os
from pathlib import Path

class GridWorld:
    def __init__(self, size: int = 101):
        """Initialize a grid world of given size.
        
        Args:
            size: The size of the grid (size x size). Defaults to 101.
        """
        self.size = size
        self.grid = np.zeros((size, size), dtype=bool)
        self.start_pos = None  # (x, y) tuple
        self.end_pos = None    # (x, y) tuple
        
    def set_start_end_positions(self):
        """Set random start and end positions on unblocked cells."""
        # Get all unblocked positions
        unblocked = np.where(~self.grid)
        if len(unblocked[0]) < 2:  # Need at least 2 unblocked cells
            return False
            
        # Choose random positions for start and end
        indices = np.random.choice(len(unblocked[0]), size=2, replace=False)
        self.start_pos = (unblocked[0][indices[0]], unblocked[1][indices[0]])
        self.end_pos = (unblocked[0][indices[1]], unblocked[1][indices[1]])
        return True
        
    def generate_maze(self):
        """Generate a maze using DFS with 30% probability of blocked cells."""
        visited = np.zeros((self.size, self.size), dtype=bool)
        stack = []
        
        def is_valid(x: int, y: int) -> bool:
            return 0 <= x < self.size and 0 <= y < self.size
        
        def get_unvisited_neighbors(x: int, y: int) -> list:
            neighbors = []
            # Check all 4 directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if is_valid(new_x, new_y) and not visited[new_x, new_y]:
                    neighbors.append((new_x, new_y))
            return neighbors
        
        start_x = np.random.randint(0, self.size)
        start_y = np.random.randint(0, self.size)
        visited[start_x, start_y] = True
        self.grid[start_x, start_y] = False  # Start cell is unblocked
        stack.append((start_x, start_y))
        
        while True:
            # If stack is empty but there are still unvisited cells
            if not stack:
                if not visited.all():
                    # Find an unvisited cell to start new path
                    unvisited_positions = np.where(~visited)
                    idx = np.random.randint(0, len(unvisited_positions[0]))
                    x, y = unvisited_positions[0][idx], unvisited_positions[1][idx]
                    visited[x, y] = True
                    self.grid[x, y] = False
                    stack.append((x, y))
                else:
                    break
            
            current_x, current_y = stack[-1]
            neighbors = get_unvisited_neighbors(current_x, current_y)
            
            if not neighbors:
                stack.pop()
                continue
                
            # Choose random neighbor
            next_x, next_y = neighbors[np.random.randint(0, len(neighbors))]
            visited[next_x, next_y] = True
            
            # 30% chance of being blocked
            if np.random.random() < 0.3:
                self.grid[next_x, next_y] = True
            else:
                self.grid[next_x, next_y] = False
                stack.append((next_x, next_y))
        
        # Set start and end positions after generating the maze
        return self.set_start_end_positions()
    
    def save(self, index: int, base_path: str = "mazes") -> tuple[str, str]:
        """Save the maze to both text and image files.
        
        Args:
            index: The index of the maze (0-49)
            base_path: Base directory to save mazes
            
        Returns:
            Tuple of (text_path, image_path)
        """
        if self.start_pos is None or self.end_pos is None:
            raise ValueError("Start and end positions not set")
            
        # Create directory if it doesn't exist
        Path(base_path).mkdir(parents=True, exist_ok=True)
        
        # Save text file
        text_path = os.path.join(base_path, f"maze_{index:02d}.txt")
        with open(text_path, 'w') as f:
            # First line: start position
            f.write(f"{self.start_pos[0]} {self.start_pos[1]}\n")
            # Second line: end position
            f.write(f"{self.end_pos[0]} {self.end_pos[1]}\n")
            # Remaining lines: maze data
            for row in self.grid:
                f.write(''.join('1' if cell else '0' for cell in row) + '\n')
        
        return text_path
    
    @classmethod
    def load(cls, index: int, base_path: str = "mazes") -> 'GridWorld':
        """Load a maze from a text file.
        
        Args:
            index: The index of the maze to load (0-49)
            base_path: Base directory where mazes are stored
            
        Returns:
            GridWorld instance with loaded maze
        """
        text_path = os.path.join(base_path, f"maze_{index:02d}.txt")
        
        instance = cls()
        with open(text_path, 'r') as f:
            # Read start position
            start_x, start_y = map(int, f.readline().strip().split())
            instance.start_pos = (start_x, start_y)
            # Read end position
            end_x, end_y = map(int, f.readline().strip().split())
            instance.end_pos = (end_x, end_y)
            # Read grid data
            grid = []
            for line in f:
                row = [c == '1' for c in line.strip()]
                grid.append(row)
            
        instance.grid = np.array(grid, dtype=bool)
        return instance
    
    def validate(self) -> bool:
        """Validate the maze meets requirements.
        
        Returns:
            bool: True if maze is valid
        """
        # Check size
        if self.grid.shape != (self.size, self.size):
            return False
        
        # Check blocked ratio (should be approximately 30%)
        blocked_ratio = np.mean(self.grid)
        if not (0.25 <= blocked_ratio <= 0.35):  # Allow some deviation
            return False
            
        # Check that start and end positions exist and are unblocked
        if self.start_pos is None or self.end_pos is None:
            return False
            
        if self.grid[self.start_pos] or self.grid[self.end_pos]:
            return False
        
        return True 