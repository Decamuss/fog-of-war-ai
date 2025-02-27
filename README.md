# Project Structure
```
.
├── grid_generation/          # Grid world generation code
│   ├── environment/         
│   │   ├── grid_world.py    # Core GridWorld class
│   │   ├── maze_generator.py
│   │   ├── priority_queue.py
│   │   └── repeated_a_star.py
│   └── utils/
        ├── min_heap.py       # Custom Built Binary Heap Structure
│       └── visualization.py  # Maze visualization utilities
├── mazes/                    # Generated maze files
│   ├── maze_00.txt          # Text representation
│   ├── maze_00.png          # Visual representation
│   └── ...
├──written_answers
└── tests/                    # Test files
    └── test_grid_world.py   # Grid world tests
```

## Maze File Format
Each maze is stored in two formats:
1. Text file (maze_XX.txt):
   ```
   start_x start_y     # First line: start position
   end_x end_y         # Second line: end position
   0010101...         # Remaining lines: maze data (0=unblocked, 1=blocked)
   ```
2. PNG visualization (maze_XX.png):
   - Black cells: blocked
   - White cells: unblocked
   - Green dot: start position
   - Red dot: end position

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
