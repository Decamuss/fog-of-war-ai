import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

def visualize_maze(grid: np.ndarray, start_pos=None, end_pos=None, save_path: str = None, show: bool = True):
    """Visualize a maze and optionally save it to a file.
    
    Args:
        grid: Boolean numpy array where True represents blocked cells
        start_pos: Optional tuple (x, y) for start position
        end_pos: Optional tuple (x, y) for end position
        save_path: Optional path to save the visualization
        show: Whether to display the plot
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap='binary')
    if start_pos is not None:
        plt.plot(start_pos[1], start_pos[0], 'go', markersize=10, label='Start')
        

        plt.plot(end_pos[1], end_pos[0], 'ro', markersize=10, label='End')
        
    if start_pos is not None or end_pos is not None:
        plt.legend()
        
    plt.axis('off')
    
    if save_path:
        Path(os.path.dirname(save_path)).mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    
    if show:
        plt.show()
    
    plt.close()

def save_maze_visualization(grid: np.ndarray, start_pos, end_pos, index: int, base_path: str = "mazes"):
    """Save a visualization of the maze.
    
    Args:
        grid: Boolean numpy array where True represents blocked cells
        start_pos: Tuple (x, y) for start position
        end_pos: Tuple (x, y) for end position
        index: Index of the maze (0-49)
        base_path: Base directory to save visualizations
    
    Returns:
        str: Path to the saved visualization
    """
    image_path = os.path.join(base_path, f"maze_{index:02d}.png")
    visualize_maze(grid, start_pos, end_pos, save_path=image_path, show=False)
    return image_path 