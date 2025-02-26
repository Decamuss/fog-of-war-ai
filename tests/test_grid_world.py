import numpy as np
import shutil
from pathlib import Path
from grid_generation.environment.grid_world import GridWorld

def test_grid_world_initialization():
    """Test basic GridWorld initialization."""
    grid = GridWorld(size=101)
    assert grid.size == 101
    assert grid.grid.shape == (101, 101)
    assert not grid.grid.any()  # All cells should be unblocked initially
    assert grid.start_pos is None
    assert grid.end_pos is None

def test_maze_generation():
    """Test maze generation properties."""
    grid = GridWorld(size=101)
    success = grid.generate_maze()
    
    assert success  # Should successfully generate maze
    assert grid.start_pos is not None
    assert grid.end_pos is not None
    
    # Check blocked ratio (should be approximately 30%)
    blocked_ratio = grid.grid.mean()
    assert 0.25 <= blocked_ratio <= 0.35
    
    # Check start and end positions are valid
    assert 0 <= grid.start_pos[0] < grid.size
    assert 0 <= grid.start_pos[1] < grid.size
    assert 0 <= grid.end_pos[0] < grid.size
    assert 0 <= grid.end_pos[1] < grid.size
    
    # Check start and end positions are unblocked
    assert not grid.grid[grid.start_pos]
    assert not grid.grid[grid.end_pos]

def test_maze_save_load():
    """Test maze saving and loading."""
    # Generate a maze
    original = GridWorld(size=101)
    original.generate_maze()
    
    # Save it
    test_path = "test_mazes"
    original.save(0, test_path)
    
    # Load it
    loaded = GridWorld.load(0, test_path)
    
    # Compare properties
    assert loaded.size == original.size
    assert loaded.start_pos == original.start_pos
    assert loaded.end_pos == original.end_pos
    assert np.array_equal(loaded.grid, original.grid)
    
    # Clean up
    if Path(test_path).exists():
        shutil.rmtree(test_path)

def test_validation():
    """Test maze validation checks."""
    grid = GridWorld(size=101)
    
    # Should fail validation initially (no start/end positions)
    assert not grid.validate()
    
    # Generate valid maze
    grid.generate_maze()
    assert grid.validate()
    
    # Test invalid cases
    original_grid = grid.grid.copy()
    original_start = grid.start_pos
    original_end = grid.end_pos
    
    # Case 1: Block start position
    grid.grid[grid.start_pos] = True
    assert not grid.validate()
    grid.grid = original_grid.copy()
    
    # Case 2: Block end position
    grid.grid[grid.end_pos] = True
    assert not grid.validate()
    grid.grid = original_grid.copy()
    
    # Case 3: Invalid blocked ratio
    grid.grid[:] = True  # All blocked
    assert not grid.validate()
    
    # Restore valid state
    grid.grid = original_grid
    grid.start_pos = original_start
    grid.end_pos = original_end
    assert grid.validate()

def test_multiple_mazes():
    """Test loading multiple generated mazes."""
    # Load first few mazes and check they're different
    mazes = [GridWorld.load(i) for i in range(3)]
    
    # Check all mazes are valid
    for maze in mazes:
        assert maze.validate()
    
    # Check mazes are different from each other
    for i in range(len(mazes)):
        for j in range(i + 1, len(mazes)):
            assert not np.array_equal(mazes[i].grid, mazes[j].grid)
            assert mazes[i].start_pos != mazes[j].start_pos
            assert mazes[i].end_pos != mazes[j].end_pos 