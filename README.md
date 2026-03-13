# Conway's Game of Life

Conway's Game of Life is a cellular automaton developed by mathematician John Conway. It is a zero-player game where the progression of the grid evolves based on its initial configuration. The game consists of a grid of cells, each of which can be in one of two states: alive or dead. The state of the grid evolves in discrete time steps according to a set of simple rules.

This project implements Conway's Game of Life in Python, providing an interactive simulation that visualizes the evolution of the grid over time.

## Features

- **Grid Visualization**: A 2D grid of cells representing alive or dead states.
- **Real-time Simulation**: The grid evolves over time based on Conway's rules.
- **User Input**: Allows the user to manually set the initial configuration of the grid.
- **Speed Control**: Adjust the simulation speed to view the grid evolution in real time.

## Installation

### Prerequisites

Before running the project, ensure you have Python installed on your system. You can download Python from [here](https://www.python.org/downloads/).

### Dependencies

This project requires the following Python libraries:
- `pygame` - For graphical representation of the grid.

You can install the required dependencies by running the following command:

```bash
pip install pygame
```

## How to Run the Game

1. Clone the repository to your local machine:

```bash
git clone https://github.com/sury666/Conways_Game_of_Life.git
```

2. Navigate to the project directory:

```bash
cd Conways_Game_of_Life
```

3. Run the Python script to start the simulation:

```bash
python game_of_life.py
```

The game window will open, and you can observe the evolution of the grid. You can interact with the grid by clicking cells to set their initial state, and adjust the simulation speed as desired.

## Game Rules
The next state of a cell depends on its current state and the number of alive neighbors. The rules for Conway's Game of Life are:

1. Any live cell with fewer than two live neighbors dies (underpopulation).
2. Any live cell with two or three live neighbors lives on to the next generation (survival).
3. Any live cell with more than three live neighbors dies (overpopulation).
4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).

## Acknowledgments

1. The concept of Conway's Game of Life is credited to John Conway, a British mathematician.
2. Thanks to the contributors of the Pygame library for providing easy-to-use game development tools.
