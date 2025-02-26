from environment.grid_world import GridWorld
from utils.visualization import save_maze_visualization
import numpy as np
import shutil
from pathlib import Path

def generate_mazes(count: int = 50, base_path: str = "mazes"):
    """Generate multiple mazes and save them.
    
    Args:
        count: Number of mazes to generate
        base_path: Base directory to save mazes
    """
    # Clean up existing mazes
    if Path(base_path).exists():
        print(f"Removing existing mazes from {base_path}")
        shutil.rmtree(base_path)
    
    print(f"Generating {count} new mazes...")
    
    generated = 0
    attempts = 0
    max_attempts = count * 2
    
    while generated < count and attempts < max_attempts:
        attempts += 1
        print(f"Generating maze {generated+1}/{count} (attempt {attempts})")
        
        # Create and generate maze
        grid_world = GridWorld()
        if not grid_world.generate_maze():
            print("Failed to generate valid maze, retrying...")
            continue
        

        if not grid_world.validate():
            print("Maze failed validation, retrying...")
            continue
            
        # Save maze data and visualization
        text_path = grid_world.save(generated, base_path)
        image_path = save_maze_visualization(
            grid_world.grid, 
            grid_world.start_pos, 
            grid_world.end_pos, 
            generated, 
            base_path
        )
        print(f"Saved maze {generated} to {text_path} and {image_path}")
        generated += 1

    if generated < count:
        print(f"Warning: Only generated {generated} valid mazes out of {count} requested")
    else:
        print(f"Successfully generated {count} mazes in {attempts} attempts")

if __name__ == "__main__":
    np.random.seed(42)

    generate_mazes()