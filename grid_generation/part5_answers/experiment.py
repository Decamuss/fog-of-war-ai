import numpy as np
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from grid_generation.environment.grid_world import GridWorld
from grid_generation.part2_answers.repeated_forward_a_star import RepeatedForwardAStar
from grid_generation.part5_answers.adaptive_a_star import AdaptiveAStar

def run_forward_experiment(maze_index):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mazes'))
    grid_world = GridWorld.load(maze_index, base_path=base_path)
    
    agent = RepeatedForwardAStar(
        grid=grid_world.grid,
        start=grid_world.start_pos,
        goal=grid_world.end_pos,
        favor_larger_g=True
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

def run_adaptive_experiment(maze_index):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mazes'))
    grid_world = GridWorld.load(maze_index, base_path=base_path)
    
    agent = AdaptiveAStar(
        grid=grid_world.grid,
        start=grid_world.start_pos,
        goal=grid_world.end_pos,
        favor_larger_g=True
    )
    
    start_time = time.time()
    success, message = agent.run()
    end_time = time.time()
    
    return {
        "maze_index": maze_index,
        "algorithm": "Adaptive",
        "success": success,
        "message": message,
        "expanded_cells": agent.expanded_cells,
        "total_path_length": agent.total_path_length,
        "search_count": agent.search_count,
        "runtime": end_time - start_time
    }

def compare_forward_adaptive(num_mazes=50):
    results = []
    
    for i in range(num_mazes):
        print(f"Running experiments on maze {i+1}/{num_mazes}")
        
        forward_result = run_forward_experiment(i)
        results.append(forward_result)
        
        adaptive_result = run_adaptive_experiment(i)
        results.append(adaptive_result)
    
    forward_results = [r for r in results if r["algorithm"] == "Forward"]
    adaptive_results = [r for r in results if r["algorithm"] == "Adaptive"]
    
    forward_success = [r for r in forward_results if r["success"]]
    adaptive_success = [r for r in adaptive_results if r["success"]]
    
    avg_forward_expanded = np.mean([r["expanded_cells"] for r in forward_success]) if forward_success else 0
    avg_adaptive_expanded = np.mean([r["expanded_cells"] for r in adaptive_success]) if adaptive_success else 0
    
    avg_forward_path = np.mean([r["total_path_length"] for r in forward_success]) if forward_success else 0
    avg_adaptive_path = np.mean([r["total_path_length"] for r in adaptive_success]) if adaptive_success else 0
    
    avg_forward_runtime = np.mean([r["runtime"] for r in forward_success]) if forward_success else 0
    avg_adaptive_runtime = np.mean([r["runtime"] for r in adaptive_success]) if adaptive_success else 0
    
    report = f"Comparison of Repeated Forward A* and Adaptive A* on {num_mazes} mazes\n"
    report += f"=================================================================\n\n"
    
    report += f"Forward A* success rate: {len(forward_success)}/{len(forward_results)} ({len(forward_success)/len(forward_results)*100:.2f}%)\n"
    report += f"Adaptive A* success rate: {len(adaptive_success)}/{len(adaptive_results)} ({len(adaptive_success)/len(adaptive_results)*100:.2f}%)\n\n"
    
    report += f"Average expanded cells (Forward A*): {avg_forward_expanded:.2f}\n"
    report += f"Average expanded cells (Adaptive A*): {avg_adaptive_expanded:.2f}\n"
    report += f"Reduction in expanded cells: {(1 - avg_adaptive_expanded/avg_forward_expanded)*100:.2f}%\n\n"
    
    report += f"Average path length (Forward A*): {avg_forward_path:.2f}\n"
    report += f"Average path length (Adaptive A*): {avg_adaptive_path:.2f}\n\n"
    
    report += f"Average runtime (Forward A*): {avg_forward_runtime:.6f} seconds\n"
    report += f"Average runtime (Adaptive A*): {avg_adaptive_runtime:.6f} seconds\n"
    report += f"Runtime improvement: {(1 - avg_adaptive_runtime/avg_forward_runtime)*100:.2f}%\n\n"
    
    report += "Detailed Results:\n"
    report += "----------------\n"
    for i, (forward, adaptive) in enumerate(zip(forward_results, adaptive_results)):
        report += f"Maze {i+1}:\n"
        report += f"  Forward A*: {'Success' if forward['success'] else 'Failure'}, Expanded: {forward['expanded_cells']}, Path: {forward['total_path_length']}, Runtime: {forward['runtime']:.6f}s\n"
        report += f"  Adaptive A*: {'Success' if adaptive['success'] else 'Failure'}, Expanded: {adaptive['expanded_cells']}, Path: {adaptive['total_path_length']}, Runtime: {adaptive['runtime']:.6f}s\n\n"
    
    print(report)
    
    with open("forward_adaptive_results.txt", "w") as f:
        f.write(report)
    
    return results 