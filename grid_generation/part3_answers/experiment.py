import numpy as np
import matplotlib.pyplot as plt
import time
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from grid_generation.environment.grid_world import GridWorld
from grid_generation.part2_answers.repeated_forward_a_star import RepeatedForwardAStar
from grid_generation.part3_answers.repeated_backward_a_star import RepeatedBackwardAStar

def run_forward_experiment(maze_index):
    grid_world = GridWorld.load(maze_index)
    
    agent = RepeatedForwardAStar(
        grid=grid_world.grid,
        start=grid_world.start_pos,
        goal=grid_world.end_pos,
        favor_larger_g=True  # Use larger g-value for tie-breaking
    )
    
    start_time = time.time()
    success, message = agent.run()
    end_time = time.time()
    
    return {
        "maze_index": maze_index,
        "algorithm": "Forward",
        "success": success,
        "message": message,
        "expanded_cells": agent.expanded_cells,
        "total_path_length": agent.total_path_length,
        "search_count": agent.search_count,
        "runtime": end_time - start_time
    }

def run_backward_experiment(maze_index):
    grid_world = GridWorld.load(maze_index)
    
    agent = RepeatedBackwardAStar(
        grid=grid_world.grid,
        start=grid_world.start_pos,
        goal=grid_world.end_pos,
        favor_larger_g=True  # Use larger g-value for tie-breaking
    )
    
    start_time = time.time()
    success, message = agent.run()
    end_time = time.time()
    
    return {
        "maze_index": maze_index,
        "algorithm": "Backward",
        "success": success,
        "message": message,
        "expanded_cells": agent.expanded_cells,
        "total_path_length": agent.total_path_length,
        "search_count": agent.search_count,
        "runtime": end_time - start_time
    }

def compare_forward_backward(num_mazes=50):
    results_forward = []
    results_backward = []
    
    for i in range(num_mazes):
        print(f"Running experiment on maze {i}...")
        
        result_forward = run_forward_experiment(i)
        results_forward.append(result_forward)
        
        result_backward = run_backward_experiment(i)
        results_backward.append(result_backward)
    
    expanded_forward = [r["expanded_cells"] for r in results_forward]
    expanded_backward = [r["expanded_cells"] for r in results_backward]
    
    runtime_forward = [r["runtime"] for r in results_forward]
    runtime_backward = [r["runtime"] for r in results_backward]
    
    path_forward = [r["total_path_length"] for r in results_forward]
    path_backward = [r["total_path_length"] for r in results_backward]
    
    avg_expanded_forward = np.mean(expanded_forward)
    avg_expanded_backward = np.mean(expanded_backward)
    
    avg_path_forward = np.mean(path_forward)
    avg_path_backward = np.mean(path_backward)
    
    avg_runtime_forward = np.mean(runtime_forward)
    avg_runtime_backward = np.mean(runtime_backward)
    
    print("\nResults:")
    print(f"Average expanded cells (Forward): {avg_expanded_forward:.2f}")
    print(f"Average expanded cells (Backward): {avg_expanded_backward:.2f}")
    print(f"Average path length (Forward): {avg_path_forward:.2f}")
    print(f"Average path length (Backward): {avg_path_backward:.2f}")
    print(f"Average runtime (Forward): {avg_runtime_forward:.4f} seconds")
    print(f"Average runtime (Backward): {avg_runtime_backward:.4f} seconds")
    
    # Create visualizations
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].bar(['Forward', 'Backward'], [avg_expanded_forward, avg_expanded_backward])
    axes[0].set_title('Average Number of Expanded Cells')
    axes[0].set_ylabel('Expanded Cells')
    
    axes[1].bar(['Forward', 'Backward'], [avg_path_forward, avg_path_backward])
    axes[1].set_title('Average Path Length')
    axes[1].set_ylabel('Path Length')
    
    axes[2].bar(['Forward', 'Backward'], [avg_runtime_forward, avg_runtime_backward])
    axes[2].set_title('Average Runtime')
    axes[2].set_ylabel('Runtime (seconds)')
    
    plt.tight_layout()
    
    output_dir = Path("grid_generation/part3_answers")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "forward_backward_comparison.png")
    plt.close()
    
    plt.figure(figsize=(10, 6))
    plt.scatter(expanded_forward, expanded_backward, alpha=0.7)
    plt.plot([0, max(expanded_forward + expanded_backward)], [0, max(expanded_forward + expanded_backward)], 'r--')
    plt.xlabel('Forward A* Expanded Cells')
    plt.ylabel('Backward A* Expanded Cells')
    plt.title('Expanded Cells Comparison: Forward vs Backward A*')
    plt.savefig(output_dir / "expanded_cells_scatter.png")
    plt.close()
    
    with open(output_dir / "forward_backward_results.txt", "w") as f:
        f.write("Forward vs Backward A* Comparison Results\n")
        f.write("======================================\n\n")
        
        f.write("Average Results:\n")
        f.write(f"Average expanded cells (Forward): {avg_expanded_forward:.2f}\n")
        f.write(f"Average expanded cells (Backward): {avg_expanded_backward:.2f}\n")
        if avg_expanded_backward > 0:
            f.write(f"Ratio (Forward/Backward): {avg_expanded_forward/avg_expanded_backward:.2f}x\n")
        f.write(f"Average path length (Forward): {avg_path_forward:.2f}\n")
        f.write(f"Average path length (Backward): {avg_path_backward:.2f}\n")
        f.write(f"Average runtime (Forward): {avg_runtime_forward:.4f} seconds\n")
        f.write(f"Average runtime (Backward): {avg_runtime_backward:.4f} seconds\n\n")
        
        f.write("Detailed Results:\n")
        for i in range(num_mazes):
            f.write(f"\nMaze {i}:\n")
            f.write(f"  Forward: {expanded_forward[i]} cells, {runtime_forward[i]:.4f} seconds, path length: {path_forward[i]}\n")
            f.write(f"  Backward: {expanded_backward[i]} cells, {runtime_backward[i]:.4f} seconds, path length: {path_backward[i]}\n")
            if expanded_backward[i] > 0:
                f.write(f"  Ratio (Forward/Backward): {expanded_forward[i]/expanded_backward[i]:.2f}x\n")
    
    return {
        "forward": results_forward,
        "backward": results_backward,
        "expanded_forward": expanded_forward,
        "expanded_backward": expanded_backward,
        "runtime_forward": runtime_forward,
        "runtime_backward": runtime_backward,
        "path_forward": path_forward,
        "path_backward": path_backward
    } 