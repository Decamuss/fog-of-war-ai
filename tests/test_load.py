from grid_generation.environment.grid_world import GridWorld
from grid_generation.utils.visualization import visualize_maze

maze = GridWorld.load(0)

print(f"Maze size: {maze.size}x{maze.size}")
print(f"Start position: {maze.start_pos}")
print(f"End position: {maze.end_pos}")
print(f"Blocked ratio: {maze.grid.mean():.2%}")

visualize_maze(maze.grid, maze.start_pos, maze.end_pos, show=True) 