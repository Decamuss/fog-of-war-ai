import sys
import os
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from grid_generation.part5_answers.experiment import compare_forward_adaptive

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare Repeated Forward A* and Adaptive A*')
    parser.add_argument('--num-mazes', type=int, default=5, help='Number of mazes to use for comparison')
    args = parser.parse_args()
    
    print(f"Running comparison on {args.num_mazes} mazes...")
    results = compare_forward_adaptive(num_mazes=args.num_mazes)
    
    print("\nExperiment completed. Results saved to grid_generation/part5_answers/") 