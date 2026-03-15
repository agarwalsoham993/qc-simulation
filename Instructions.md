## Overview

This interactive Conway's Game of Life simulator combines classical cellular automaton rules with financial market simulation. The grid's center of mass (CoM) is tracked and normalized to generate synthetic "Price" movements, which can be compared against real stock data.

## Getting Started

When you first run the program, you'll be prompted to enter:
- **Grid Width**: Number of horizontal tiles
- **Grid Height**: Number of vertical tiles
- **Seed**: (Optional) A random seed for reproducible grid initialization
- **Probability**: A value between 0 and 1 indicating the likelihood of a cell being alive initially (e.g., 0.2 for 20%)

## Controls

### Grid Interaction
* **Left-Click on Grid**: Select or deselect individual cells to manually configure the initial state

### Simulation Controls
* **Spacebar**: Start/pause the continuous simulation
* **Right Arrow**: Manually advance one generation forward
* **Click Play/Pause Button**: Alternative way to start/pause the simulation

### Grid Initialization
* **'s' key**: Randomize the grid based on the provided seed and probability from startup
* **'c' key**: Clear/reset the entire grid (all cells become dead)

### Visualization & Zoom
* **'+' or '=' key**: Zoom in on the grid
* **'-' key**: Zoom out from the grid

### Price & Analysis Features
* **'p' key**: Toggle Price Plot window - displays the grid's vertical Center of Mass (CoM) as "Price" over generations
* **'l' key**: Toggle Log Returns Plot - visualizes logarithmic returns at multiple time horizons. Edit the horizon values in the top-right panel (comma-separated, e.g., "1, 3, 5") before pressing 'l'
* **Illustration Mode Button**: Toggle visualization of the Center of Mass (displays as a circle with a center point on the grid)

### Advanced Settings (Top-Right Panel)
* **Horizons Input**: Click the horizons text box to edit the time horizons for log returns calculation (format: comma-separated numbers, e.g., "1, 3, 5")

## Understanding the Display

- **Status Indicator**: Top-left shows the current generation count and simulation status (Running/Paused)
- **Illustration Mode**: When enabled, displays a circle centered at the grid's Center of Mass, with the radius proportional to the number of alive cells
- **Price Tracking**: The vertical position of the Center of Mass is converted to a "Price" value for financial analysis

