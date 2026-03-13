import pygame
import random

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

        # Updating the grid after each 'update_freq' frames if the simulation is running
        if simulating:
            count += 1
            if count == update_freq:
                count = 0
                positions = adjust_grid(positions)
                generation_count += 1

        for event in pygame.event.get():
            # Quit the game if pressed the close button
            if event.type == pygame.QUIT:
                game_active = False
            
            # Select or deselect a cell or click the status button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the Play/Pause button was clicked
                if button_rect.collidepoint(event.pos):
                    simulating = not simulating
                    continue

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
                # Start or pause continous generation advancement
                if event.key == pygame.K_SPACE:
                    simulating = not simulating
                
                # Reset the grid
                if event.key == pygame.K_c:
                    positions = set()
                    simulating = False
                    count = 0
                    generation_count = 0

                # Randomize the grid (Start Initialization)
                if event.key == pygame.K_s:
                    positions = randomize_positions()
                    generation_count = 0
                
                # Manually advance generations
                if event.key == pygame.K_RIGHT:
                    positions = adjust_grid(positions)
                    generation_count += 1
                
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

    pygame.quit()

if __name__ == "__main__":
    main()
