import numpy as np
import matplotlib.pyplot as plt
import time
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from grid_generation.environment.grid_world import GridWorld
from grid_generation.part2_answers.repeated_forward_a_star import RepeatedForwardAStar

def run_experiment(maze_index, favor_larger_g=False):
    grid_world = GridWorld.load(maze_index)
    
    agent = RepeatedForwardAStar(
        grid=grid_world.grid,
        start=grid_world.start_pos,
        goal=grid_world.end_pos,
        favor_larger_g=favor_larger_g
    )
    
    start_time = time.time()
    success, message = agent.run()
    end_time = time.time()
    
    return {
        "maze_index": maze_index,
        "favor_larger_g": favor_larger_g,
        "success": success,
        "message": message,
        "expanded_cells": agent.expanded_cells,
        "total_path_length": agent.total_path_length,
        "search_count": agent.search_count,
        "runtime": end_time - start_time
    }

def compare_tie_breaking_strategies(num_mazes=50):
    results_smaller_g = []
    results_larger_g = []
    
    for i in range(num_mazes):
        print(f"Running experiment on maze {i}...")
        
        result_smaller = run_experiment(i, favor_larger_g=False)
        results_smaller_g.append(result_smaller)
        
        result_larger = run_experiment(i, favor_larger_g=True)
        results_larger_g.append(result_larger)
    
    expanded_smaller = [r["expanded_cells"] for r in results_smaller_g]
    expanded_larger = [r["expanded_cells"] for r in results_larger_g]
    
    runtime_smaller = [r["runtime"] for r in results_smaller_g]
    runtime_larger = [r["runtime"] for r in results_larger_g]
    
    path_smaller = [r["total_path_length"] for r in results_smaller_g]
    path_larger = [r["total_path_length"] for r in results_larger_g]
    
    avg_expanded_smaller = np.mean(expanded_smaller)
    avg_expanded_larger = np.mean(expanded_larger)
    
    avg_path_smaller = np.mean(path_smaller)
    avg_path_larger = np.mean(path_larger)
    
    avg_runtime_smaller = np.mean(runtime_smaller)
    avg_runtime_larger = np.mean(runtime_larger)
    
    print("\nResults:")
    print(f"Average expanded cells (smaller g): {avg_expanded_smaller:.2f}")
    print(f"Average expanded cells (larger g): {avg_expanded_larger:.2f}")
    print(f"Average path length (smaller g): {avg_path_smaller:.2f}")
    print(f"Average path length (larger g): {avg_path_larger:.2f}")
    print(f"Average runtime (smaller g): {avg_runtime_smaller:.4f} seconds")
    print(f"Average runtime (larger g): {avg_runtime_larger:.4f} seconds")
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].bar(['Smaller g', 'Larger g'], [avg_expanded_smaller, avg_expanded_larger])
    axes[0].set_title('Average Number of Expanded Cells')
    axes[0].set_ylabel('Expanded Cells')
    
    axes[1].bar(['Smaller g', 'Larger g'], [avg_path_smaller, avg_path_larger])
    axes[1].set_title('Average Path Length')
    axes[1].set_ylabel('Path Length')
    
    axes[2].bar(['Smaller g', 'Larger g'], [avg_runtime_smaller, avg_runtime_larger])
    axes[2].set_title('Average Runtime')
    axes[2].set_ylabel('Runtime (seconds)')
    
    plt.tight_layout()
    
    output_dir = Path("grid_generation/part2_answers")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "tie_breaking_comparison.png")
    plt.close()
    
    with open(output_dir / "tie_breaking_results.txt", "w") as f:
        f.write("Tie-Breaking Comparison Results\n")
        f.write("==============================\n\n")
        
        f.write("Average Results:\n")
        f.write(f"Average expanded cells (smaller g): {avg_expanded_smaller:.2f}\n")
        f.write(f"Average expanded cells (larger g): {avg_expanded_larger:.2f}\n")
        f.write(f"Improvement ratio: {avg_expanded_smaller/avg_expanded_larger:.2f}x\n")
        f.write(f"Average path length (smaller g): {avg_path_smaller:.2f}\n")
        f.write(f"Average path length (larger g): {avg_path_larger:.2f}\n")
        f.write(f"Average runtime (smaller g): {avg_runtime_smaller:.4f} seconds\n")
        f.write(f"Average runtime (larger g): {avg_runtime_larger:.4f} seconds\n\n")
        
        f.write("Detailed Results:\n")
        for i in range(num_mazes):
            f.write(f"\nMaze {i}:\n")
            f.write(f"  Smaller g: {expanded_smaller[i]} cells, {runtime_smaller[i]:.4f} seconds, path length: {path_smaller[i]}\n")
            f.write(f"  Larger g: {expanded_larger[i]} cells, {runtime_larger[i]:.4f} seconds, path length: {path_larger[i]}\n")
            if expanded_larger[i] > 0:
                f.write(f"  Improvement ratio: {expanded_smaller[i]/expanded_larger[i]:.2f}x\n")
    
    return {
        "smaller_g": results_smaller_g,
        "larger_g": results_larger_g,
        "expanded_smaller": expanded_smaller,
        "expanded_larger": expanded_larger,
        "runtime_smaller": runtime_smaller,
        "runtime_larger": runtime_larger,
        "path_smaller": path_smaller,
        "path_larger": path_larger
    } 