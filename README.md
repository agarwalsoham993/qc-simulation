<div align = "center">

# Game of Life for Quantitative Finance

Quant CLUB

</div>


This project explores the intersection of **Conway's Game of Life** and **quantitative finance**, investigating whether cellular automaton dynamics can model or provide insights into stock price movements and market behavior. Rather than treating Game of Life as a standalone simulation, we leverage its mathematical properties—particularly the center of mass dynamics—to generate synthetic price signals and compare them with real financial data.

## Overview

The core hypothesis is that the evolving patterns and momentum of a Game of Life grid, when converted to a synthetic price signal via center of mass tracking, may reveal underlying market dynamics or serve as an alternative mathematical model for price discovery. This repository contains multiple implementations and analyses of this concept.

## Project Components

### 1. **Interactive Game of Life Simulation** (`source_code.py`)
A real-time pygame-based visualization where users can:
- Configure custom grid dimensions and initial cell probabilities
- Watch the cellular automaton evolve according to Conway's rules
- Track the center of mass (CoM) in real-time
- Monitor aggregate statistics of the living population
- Observe emergent patterns and their price-like behavior

### 2. **Real Stock Simulation** (`real_stock_simulation.py`)
An advanced analysis tool that:
- Fetches real historical stock data using yfinance for any ticker symbol
- Runs a parallel Game of Life simulation over the same time horizon
- Converts grid dynamics to a synthetic price signal via Euclidean distance of center of mass from grid center
- Normalizes and scales the simulated signal to match the volatility characteristics of actual stock prices
- Generates side-by-side visualizations comparing GoL-derived prices with real market data
- Analyzes correlation patterns and potential predictive relationships

### 3. **Comprehensive Analysis Notebook** (`colab.ipynb`)
A Jupyter notebook containing:
- Detailed walkthroughs of both simulation methodologies
- Interactive visualizations and statistical analysis
- Comparative studies across multiple stock tickers and time periods
- Pattern recognition and anomaly detection in cellular dynamics
- Performance metrics and correlation analysis

## Key Features

- **Market-Finance Hybrid Approach**: Bridges cellular automata theory with quantitative finance
- **Center of Mass Tracking**: Generates synthetic price signals from grid dynamics
- **Volatility Matching**: Normalizes simulated data to match real market volatility
- **Real vs. Simulated Comparison**: Side-by-side analysis of actual stock prices and GoL-derived signals
- **Customizable Parameters**: Grid size, initial probability, time horizons, and stock selection
- **Interactive Visualization**: Both pygame and matplotlib/plotly for exploration


## Installation

### Prerequisites

- Python 3.7 or higher installed on your system

### Dependencies

This project requires the following Python libraries:

- `pygame` - For interactive grid visualization
- `matplotlib` - For plotting and analysis
- `numpy` - For numerical computations
- `pandas` - For data manipulation and analysis
- `yfinance` - For fetching real stock price data
- `scipy` - For advanced numerical operations (convolution-based GoL)
- `plotly` - For interactive visualizations (used in the notebook)

Install dependencies with:

```bash
pip install pygame matplotlib numpy pandas yfinance scipy plotly
```

Optionally, set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Use

### Option 1: Interactive Game of Life Visualization

Run the interactive pygame application to watch Game of Life evolve and see center of mass dynamics in action:

```bash
python source_code.py
```

You'll be prompted to enter:
- Grid width and height (in number of tiles)
- A seed for reproducibility (or leave blank for random)
- Probability of cells being alive (0 to 1, e.g., 0.3)

The simulation displays the grid evolution and can be used to observe emergent patterns and their relationship to price-like signals.

### Option 2: Real Stock vs. Game of Life Comparison

Compare a Game of Life simulation against real historical stock data:

```bash
python real_stock_simulation.py
```

Or modify the script to test specific stocks and parameters:

```python
run_simulation(ticker='AAPL', period='1y', grid_size=300, init_prob=0.3)
```

This generates a visualization overlaying:
- Actual stock price movements (in neon green)
- Game of Life-derived synthetic price signal (in blue)

### Option 3: Comprehensive Analysis (Colab Notebook)

Open and run the Jupyter notebook for detailed analysis:

```bash
jupyter notebook colab.ipynb
```

The notebook contains multiple interactive analyses, visualizations, and comparative studies across different stocks and parameters.

## Game Rules

Conway's Game of Life operates on the following rules, which generate complex emergent behavior from simple local interactions:

1. **Underpopulation**: Any live cell with fewer than two live neighbors dies
2. **Survival**: Any live cell with two or three live neighbors survives to the next generation
3. **Overpopulation**: Any live cell with more than three live neighbors dies
4. **Reproduction**: Any dead cell with exactly three live neighbors becomes alive

## Quantitative Finance Application

### The Core Idea

We hypothesize that the dynamics of a Game of Life grid—specifically through center of mass tracking—can serve as a mathematical analog for market movements. Key aspects include:

1. **Center of Mass as Price Signal**: The position of the center of mass becomes a natural "location" metric that evolves over time, analogous to price movements
2. **Volatility Matching**: We normalize the cellular automaton's distance metrics to match the statistical properties of real stock price volatility
3. **Emergent Patterns**: Just as Game of Life produces oscillators, spaceships, and stable patterns, markets exhibit mean reversion, trends, and cyclical behavior

### Methods

- **Euclidean Distance Metric**: Convert 2D center of mass position to a scalar representing distance from grid center
- **Z-Score Normalization**: Standardize the simulated distances and scale them to match real price volatility
- **Comparative Analysis**: Overlay synthetic GoL prices with actual stock data to find correlations or divergences

### Potential Applications

- Alternative market models unrelated to traditional econometrics
- Pattern recognition in market behavior
- Risk analysis through cellular automata dynamics
- Machine learning features derived from GoL simulations
- Theoretical exploration of emergence in complex systems (markets vs. cellular automata)

## Project Structure

```
qc simulation/
├── source_code.py              # Interactive Game of Life visualization
├── real_stock_simulation.py    # GoL vs. real stock comparison
├── colab.ipynb                 # Comprehensive Jupyter notebook with analyses
├── README.md                   # This file
├── Instructions.md             # Detailed usage instructions
└── reference/                  # Additional resources and demonstrations
    ├── QCintrosemdemonstration.ipynb
    └── script.md
```

## Research Motivation

This project bridges two seemingly unrelated domains:
- **Cellular Automata Theory**: Self-organizing systems with simple local rules producing global complexity
- **Quantitative Finance**: Markets driven by information, sentiment, and agent behavior

The investigation explores whether the mathematical structure of emergence in cellular automata offers any insights into market dynamics, serving as both a theoretical exploration and a framework for feature engineering in algorithmic trading.

## Performance Notes

- Grid simulations use numpy convolution for efficiency
- Pygame visualization is optimized for interactive exploration
- Real stock data queries are cached to minimize API calls
- Plotly visualizations provide interactive exploration of results

## Limitations & Disclaimers

⚠️ **This is a research/educational project**, not financial advice or a prediction tool.

- Game of Life dynamics are NOT a proven predictor of real markets
- Results shown are correlative exploration, not causative relationships
- Past simulations and market data do not guarantee future performance
- This work is intended to inspire further research, not to trade real money

## Expected Outcomes

Users should expect to:
- Understand cellular automata fundamentals through interactive simulation
- Learn how to convert complex system dynamics into quantifiable metrics
- Explore the overlap between emergence and market behavior from a theoretical perspective
- Develop custom experiments using provided tools and frameworks

What this project is NOT:
- A trading strategy or market prediction algorithm
- A replacement for statistical/econometric analysis
- A proof that Game of Life models real markets

## Acknowledgments

- **John Conway** for inventing Game of Life—one of mathematics' most elegant systems
- **Pygame developers** for providing accessible game development tools
- **yfinance contributors** for easy stock data access
- **NumPy/Matplotlib/Plotly communities** for powerful scientific visualization libraries
- **Quantitative finance researchers** whose work inspires exploring unconventional approaches

## References & Further Reading

- Conway, J. H. (1970). "The Game of Life." Scientific American.
- Wolfram, S. (2002). "A New Kind of Science."
- Taleb, N. N. (2007). "The Black Swan" – on complex systems and markets.


## License

This project is provided as-is for educational and research purposes. Feel free to fork, modify, and extend for your own explorations.
