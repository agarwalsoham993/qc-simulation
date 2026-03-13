import pygame
import random
import matplotlib.pyplot as plt
import numpy as np

pygame.init()

LINE = (153, 153, 153)
DEAD = (255, 255, 255)
ALIVE = (0, 0, 0)
WHITE = (255, 255, 255)
GENERATION_BG = (123, 123, 123)
PLAY_COLOR = (39, 174, 96)
PAUSE_COLOR = (192, 57, 43)

TILE_SIZE = 20
FPS = 240

# Get grid size from the user
GRID_WIDTH = int(input("Enter the width of the grid (number of tiles): "))
GRID_HEIGHT = int(input("Enter the height of the grid (number of tiles): "))

# Random initialization settings
SEED = input("Enter seed for randomization (leave blank for random): ")
PROBABILITY = float(input("Enter probability of a cell being alive (0 to 1, e.g., 0.2): "))

WIDTH = GRID_WIDTH * TILE_SIZE
HEIGHT = GRID_HEIGHT * TILE_SIZE

pygame.display.set_caption("Conway's Game of Life")

clock = pygame.time.Clock()

# Initializing the grid
def draw_grid(positions, tile_size):
    for position in positions:
        col, row = position
        top_left = (col * tile_size, row * tile_size)
        pygame.draw.rect(screen, ALIVE, (*top_left, tile_size, tile_size))

    for row in range(0, HEIGHT, tile_size):
        pygame.draw.line(screen, LINE, (0, row), (WIDTH, row))

    for col in range(0, WIDTH, tile_size):
        pygame.draw.line(screen, LINE, (col, 0), (col, HEIGHT))

# Returning neighbors of pos
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH: # If the current cell is not inside the grid
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_HEIGHT: # If the current cell not inside the grid
                continue
            if dx == 0 and dy == 0: # If the current cell is the pos cell
                continue
            
            neighbors.append((x + dx, y + dy))
    
    return neighbors

def calculate_com(positions):
    if not positions:
        return 0
    # Average Y coordinate (invert it so that moving UP the grid means a HIGHER price)
    sum_y = sum(pos[1] for pos in positions)
    avg_y = sum_y / len(positions)
    return GRID_HEIGHT - avg_y

# Updating the grid
def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()
    
    # Survival
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)
        
        # Updating neighbors to include only alive cells
        neighbors = list(filter(lambda x: x in positions, neighbors))
        
        # If the number of alive neighbors of a cell is 2 or 3, then the cell survives this generation, else it dies due to isolation or overpopulation
        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    
    # Reproduction
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        
        # Updating neighbors to include only alive cells
        neighbors = list(filter(lambda x: x in positions, neighbors))
        
        # If the number of alive neighbors of a dead cell is 3, then it becomes alive in the next generation
        if len(neighbors) == 3:
            new_positions.add(position)
    
    return new_positions

def main():
    global screen, WIDTH, HEIGHT
    game_active = True
    simulating = False
    count = 0
    update_freq = 60 # Speed control
    generation_count = 0
    tile_size = TILE_SIZE

    def randomize_positions():
        if SEED:
            random.seed(SEED)
        new_positions = set()
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if random.random() < PROBABILITY:
                    new_positions.add((col, row))
        return new_positions

    positions = set()
    
    font = pygame.font.SysFont(None, 24)
    button_rect = pygame.Rect(10, 10, 180, 40)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialize Price Plot variables
    plt.ion()
    fig = None
    ax = None
    price_plot = None
    plot_active = False
    
    price_history = []
    generation_history = []
    
    # Horizon text box variables
    horizons_text = "1, 3, 5"
    editing_horizons = False
    horizons_rect = pygame.Rect(WIDTH - 230, 10, 220, 40)
    
    log_fig = None
    log_axes = None
    log_lines = []
    log_plot_active = False
    current_horizons = []
    
    def update_log_plot():
        nonlocal log_fig, log_axes, log_lines, log_plot_active, current_horizons
        if log_plot_active and log_fig and plt.fignum_exists(log_fig.number):
            prices = np.array(price_history)
            prices_safe = np.where(prices == 0, 1e-9, prices)
            logs = np.log(prices_safe)
            
            for i, h in enumerate(current_horizons):
                if len(logs) > h:
                    lr = logs[h:] - logs[:-h]
                    t = generation_history[h:]
                    log_lines[i].set_data(t, lr)
                    log_axes[i].relim()
                    log_axes[i].autoscale_view()
            
            # Using tight layout or just draw
            log_fig.canvas.draw()
            try:
                log_fig.canvas.flush_events()
            except:
                pass
        elif log_plot_active:
            log_plot_active = False
    
    # Store initial price
    current_price = calculate_com(positions)
    price_history.append(current_price)
    generation_history.append(generation_count)
    
    def update_plot():
        nonlocal fig, ax, price_plot, plot_active
        if plot_active and fig and plt.fignum_exists(fig.number):
            price_plot.set_data(generation_history, price_history)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            try:
                fig.canvas.flush_events()
            except:
                pass
        elif plot_active:
            plot_active = False
        update_log_plot()

    while game_active:
        screen.fill(DEAD)
        draw_grid(positions, tile_size)
        clock.tick(FPS)
        
        # Display generation count and Simulation Status Button
        status_text = "Running" if simulating else "Paused"
        button_color = PLAY_COLOR if simulating else PAUSE_COLOR
        
        ui_text = font.render(f"Generations: {generation_count} | {status_text}", True, WHITE)
        text_rect = ui_text.get_rect(topleft = (10, 10))
        button_rect = text_rect.inflate(10, 10)
        
        pygame.draw.rect(screen, button_color, button_rect, border_radius = 10)
        screen.blit(ui_text, text_rect)
        
        panel_color = (200, 200, 200) if editing_horizons else (100, 100, 100)
        # Ensure we always anchor to the top right dynamically if WIDTH changes (e.g. zoom)
        horizons_rect.x = screen.get_width() - 250
        pygame.draw.rect(screen, panel_color, horizons_rect, border_radius = 5)
        hz_label = font.render(f"Horizons: {horizons_text}", True, ALIVE)
        screen.blit(hz_label, horizons_rect.move(10, 10))

        # Updating the grid after each 'update_freq' frames if the simulation is running
        if simulating:
            count += 1
            if count == update_freq:
                count = 0
                positions = adjust_grid(positions)
                generation_count += 1
                
                # Update Price Plot
                current_price = calculate_com(positions)
                price_history.append(current_price)
                generation_history.append(generation_count)
                
                update_plot()

        for event in pygame.event.get():
            # Quit the game if pressed the close button
            if event.type == pygame.QUIT:
                game_active = False
            
            # Select or deselect a cell or click the status button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the Play/Pause button was clicked
                if button_rect.collidepoint(event.pos):
                    simulating = not simulating
                    editing_horizons = False
                    continue
                    
                if horizons_rect.collidepoint(event.pos):
                    editing_horizons = True
                    continue
                else:
                    editing_horizons = False

                # Extracting off the position user's clicked cell col, row
                x, y = event.pos
                col = x // tile_size
                row = y // tile_size
                pos = (col, row)
                
                # Selecting or deselecting user's clicked cell
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN:
                if editing_horizons:
                    if event.key == pygame.K_RETURN:
                        editing_horizons = False
                    elif event.key == pygame.K_BACKSPACE:
                        horizons_text = horizons_text[:-1]
                    elif event.unicode.isdigit() or event.unicode in ', ':
                        horizons_text += event.unicode
                    continue

                if event.key == pygame.K_l:
                    if not log_plot_active:
                        try:
                            current_horizons = [int(x.strip()) for x in horizons_text.split(',') if x.strip()]
                        except ValueError:
                            current_horizons = [1, 3, 5]
                        if not current_horizons:
                            current_horizons = [1]
                        
                        log_fig, log_axes = plt.subplots(len(current_horizons), 1, figsize=(8, max(2*len(current_horizons), 4)), sharex=True)
                        if len(current_horizons) == 1:
                            log_axes = [log_axes]
                            
                        log_fig.canvas.manager.set_window_title('Log Returns')
                        log_fig.patch.set_facecolor('#0d1117')
                        log_lines = []
                        COLORS = ['#39ff14', '#ffaa00', '#ff4444', '#58a6ff', '#cc44ff']
                        
                        for i, h in enumerate(current_horizons):
                            ax = log_axes[i]
                            ax.set_facecolor('#161b22')
                            ax.tick_params(colors='#c9d1d9')
                            for spine in ax.spines.values():
                                spine.set_color('#21262d')
                            ax.set_title(f'Log Return h={h}', color='#58a6ff', fontsize=10)
                            line, = ax.plot([], [], color=COLORS[i % len(COLORS)], linewidth=1)
                            ax.axhline(0, color='#30363d', linewidth=1)
                            log_lines.append(line)
                        
                        log_fig.tight_layout()
                        log_plot_active = True
                        update_log_plot()
                    else:
                        if log_fig and plt.fignum_exists(log_fig.number):
                            plt.close(log_fig)
                        log_plot_active = False

                # Toggle Price Plot
                if event.key == pygame.K_p:
                    if not plot_active:
                        fig, ax = plt.subplots(figsize=(6, 4))
                        fig.canvas.manager.set_window_title('Price (Center of Mass Y-axis)')
                        ax.set_xlabel('Generation')
                        ax.set_ylabel('Price')
                        ax.set_title('Center of Mass Price Tracking')
                        price_plot, = ax.plot(generation_history, price_history, 'b-', linewidth=2)
                        plot_active = True
                        update_plot()
                    else:
                        if fig and plt.fignum_exists(fig.number):
                            plt.close(fig)
                        plot_active = False
                        
                # Start or pause continous generation advancement
                if event.key == pygame.K_SPACE:
                    simulating = not simulating
                
                # Reset the grid
                if event.key == pygame.K_c:
                    positions = set()
                    simulating = False
                    count = 0
                    generation_count = 0
                    
                    price_history = [calculate_com(positions)]
                    generation_history = [generation_count]
                    update_plot()

                # Randomize the grid (Start Initialization)
                if event.key == pygame.K_s:
                    positions = randomize_positions()
                    generation_count = 0
                    
                    price_history = [calculate_com(positions)]
                    generation_history = [generation_count]
                    update_plot()
                
                # Manually advance generations
                if event.key == pygame.K_RIGHT:
                    positions = adjust_grid(positions)
                    generation_count += 1
                    
                    price_history.append(calculate_com(positions))
                    generation_history.append(generation_count)
                    update_plot()
                
                # Zoom in
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    tile_size += 5
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                
                # Zoom out
                if event.key == pygame.K_MINUS:
                    if tile_size > 5:
                        tile_size -= 5
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
        pygame.display.update()
        
        # Keep matplotlib GUI responsive
        try:
            if plot_active and fig and plt.fignum_exists(fig.number):
                fig.canvas.flush_events()
            if log_plot_active and log_fig and plt.fignum_exists(log_fig.number):
                log_fig.canvas.flush_events()
        except:
            pass

    pygame.quit()
    plt.close('all')

if __name__ == "__main__":
    main()
