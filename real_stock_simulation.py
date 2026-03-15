import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import convolve
import sys

# Conway's Rules using Convolution
_KERNEL = np.array([[1, 1, 1],
                    [1, 0, 1],
                    [1, 1, 1]], dtype=np.int32)

def make_grid(N, init_prob):
    return (np.random.rand(N, N) < init_prob).astype(np.int32)

def gol_step(X):
    nbrs = convolve(X, _KERNEL, mode='wrap')
    return (((X == 1) & ((nbrs == 2) | (nbrs == 3))) | ((X == 0) & (nbrs == 3))).astype(np.int32)

def center_of_mass(X):
    total = X.sum()
    N = X.shape[0]
    if total == 0:
        return N / 2.0, N / 2.0
    
    y, a = np.indices((N, N)) # y corresponds to rows, "a" corresponds to columns (x)
    x = a # x corresponds to columns
    x_cm = (X * x).sum() / total
    y_cm = (X * y).sum() / total
    
    return x_cm, y_cm

def get_euclidean_distance(X):
    N = X.shape[0]
    x_cm, y_cm = center_of_mass(X)
    # Origin is the center of the grid
    origin_x, origin_y = N / 2.0, N / 2.0
    return np.sqrt((x_cm - origin_x)**2 + (y_cm - origin_y)**2)

def run_simulation(ticker='AAPL', period='1y', grid_size=300, init_prob=0.3):
    print(f"Fetching {period} of historical data for {ticker}...")
    stock_data = yf.download(ticker, period=period)
    
    if stock_data.empty:
        print("Failed to download stock data.")
        sys.exit(1)
        
    real_prices = stock_data['Close'].values.flatten()
    dates = stock_data.index
    num_steps = len(real_prices)
    print(f"Downloaded {num_steps} trading days.")

    print(f"Initializing a {grid_size}x{grid_size} Game of Life grid...")
    grid = make_grid(grid_size, init_prob)
    
    simulated_distances = []
    
    print("Running simulation over time horizon...")
    for step in range(num_steps):
        dist = get_euclidean_distance(grid)
        simulated_distances.append(dist)
        grid = gol_step(grid)
        
    simulated_distances = np.array(simulated_distances)
    
    # User Request: "normalize it and multiply it with the price of the stock"
    # To make the variance comparable, we will first standardize (z-score) the 
    # simulated distances. Then, we apply the standard deviation of the real stock 
    # prices (or a scaled version) and shift it to start at the exact Day 0 real price.
    
    if len(simulated_distances) > 0:
        sim_std = np.std(simulated_distances)
        real_std = np.std(real_prices)
        
        if sim_std > 0:
            # Z-score normalize the GoL simulation
            z_scores = (simulated_distances - simulated_distances[0]) / sim_std
            # Apply the real stock's variance scale, and shift to intercept
            # You can tweak the multiplier here if you want it slightly more/less volatile
            volatility_multiplier = 1.0 
            simulated_prices = (z_scores * real_std * volatility_multiplier) + real_prices[0]
        else:
            simulated_prices = simulated_distances - simulated_distances[0] + real_prices[0]
    else:
        simulated_prices = np.zeros_like(real_prices)
        
    # Plotting Real vs Simulated
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, real_prices, label=f"Real {ticker} Price", color='#39ff14', linewidth=1.5)
    ax.plot(dates, simulated_prices, label="Simulated GoL Price (Scaled Euclidean Distance)", color='#58a6ff', linewidth=1.5, alpha=0.85)
    
    ax.set_title(f"Market Simulation: Game of Life vs. {ticker} (1 Year)", color='white', fontsize=14)
    ax.set_ylabel("Price")
    ax.set_xlabel("Date")
    ax.grid(color='#21262d', linestyle='-', linewidth=0.5)
    ax.legend()
    
    plt.tight_layout()
    output_png = f"{ticker}_gol_simulation.png"
    plt.savefig(output_png, facecolor='#0d1117', edgecolor='none')
    print(f"Comparison plot saved successfully as {output_png}!")

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'AAPL'
    run_simulation(ticker)
