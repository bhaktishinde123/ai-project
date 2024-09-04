import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 8
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
MAX_MOVES = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
GOLD = (255, 223, 0)

# Load images
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (CELL_SIZE - 10, CELL_SIZE - 10))
treasure_img = pygame.image.load("treasure.png")
treasure_img = pygame.transform.scale(treasure_img, (CELL_SIZE, CELL_SIZE))
trap_img = pygame.image.load("trap.png")
trap_img = pygame.transform.scale(trap_img, (CELL_SIZE, CELL_SIZE))

# Screen and Fonts
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Smooth Treasure Hunt')
font = pygame.font.Font(None, 36)

# Function to place treasure and traps
def place_items(num_traps):
    treasure_x, treasure_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    traps = []
    while len(traps) < num_traps:
        trap_x, trap_y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (trap_x, trap_y) != (treasure_x, treasure_y) and (trap_x, trap_y) not in traps:
            traps.append((trap_x, trap_y))
    return treasure_x, treasure_y, traps

# Randomly place the treasure and traps
treasure_x, treasure_y, traps = place_items(num_traps=5)

# Player start position
player_x, player_y = 0, 0
moves = 0
game_over = False
found_treasure = False

# Function to calculate distance
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Function to draw the game elements
def draw_elements():
    screen.blit(background_img, (0, 0))
    # Draw player, treasure, and traps
    screen.blit(player_img, (player_x * CELL_SIZE + (CELL_SIZE - player_img.get_width()) // 2, 
                             player_y * CELL_SIZE + (CELL_SIZE - player_img.get_height()) // 2))
    if found_treasure:
        screen.blit(treasure_img, (treasure_x * CELL_SIZE + (CELL_SIZE - treasure_img.get_width()) // 2, 
                                   treasure_y * CELL_SIZE + (CELL_SIZE - treasure_img.get_height()) // 2))
        # Display win message
        text = font.render("Congratulations! You found the treasure!", True, GOLD)
        screen.blit(text, (50, WINDOW_HEIGHT - 50))
    else:
        # Draw traps
        for (trap_x, trap_y) in traps:
            screen.blit(trap_img, (trap_x * CELL_SIZE + (CELL_SIZE - trap_img.get_width()) // 2, 
                                   trap_y * CELL_SIZE + (CELL_SIZE - trap_img.get_height()) // 2))
        
        # Calculate and display distance to treasure
        dist = distance(player_x, player_y, treasure_x, treasure_y)
        hint_text = font.render(f"Distance to treasure: {dist:.2f}", True, WHITE)
        screen.blit(hint_text, (10, WINDOW_HEIGHT - 50))

        # Check for traps
        if (player_x, player_y) in traps:
            text = font.render("You fell into a trap! Game Over!", True, RED)
            screen.blit(text, (200, WINDOW_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            return False

    # Display remaining moves
    moves_text = font.render(f"Moves left: {MAX_MOVES - moves}", True, WHITE)
    screen.blit(moves_text, (10, 10))

    pygame.display.flip()
    return True

# Main game loop
running = True

while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Player movement within the grid
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < GRID_SIZE - 1:
                player_x += 1
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_SIZE - 1:
                player_y += 1
            
            # Increase move count
            moves += 1

            # Check if player is on treasure
            if player_x == treasure_x and player_y == treasure_y:
                found_treasure = True
                game_over = True  # Mark game as over

    # Check for game over conditions
    if not found_treasure:
        if moves >= MAX_MOVES:
            text = font.render("Out of moves! Game Over!", True, RED)
            screen.blit(text, (250, WINDOW_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            running = False
    
    running = draw_elements()

# Quit game
pygame.quit()
