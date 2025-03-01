import pygame
import random
from character import Character

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burger King Street Fighter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Create characters
player1 = Character("Burger King", 100, HEIGHT - 150, (255, 0, 0))
player2 = Character("Whopper Warrior", WIDTH - 200, HEIGHT - 150, (0, 0, 255))

# Game variables
round_time = 60
start_time = pygame.time.get_ticks()

def draw_health_bars():
    pygame.draw.rect(screen, RED, (50, 30, player1.health * 2, 20))
    pygame.draw.rect(screen, RED, (WIDTH - 250, 30, player2.health * 2, 20))

def draw_timer():
    time_left = max(round_time - (pygame.time.get_ticks() - start_time) // 1000, 0)
    timer_text = font.render(str(time_left), True, WHITE)
    screen.blit(timer_text, (WIDTH // 2 - 20, 30))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw characters
    player1.draw(screen)
    player2.draw(screen)

    # Draw health bars
    draw_health_bars()

    # Draw timer
    draw_timer()

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()