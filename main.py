import pygame
import random
from character import Character

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burger King Street Fighter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create characters
player1 = Character(100, HEIGHT - 100, RED)
player2 = Character(WIDTH - 200, HEIGHT - 100, GREEN)

# Game variables
clock = pygame.time.Clock()
game_over = False
round_time = 60 * 1000  # 60 seconds in milliseconds
start_time = pygame.time.get_ticks()

def draw_health_bars():
    pygame.draw.rect(screen, RED, (50, 30, player1.health * 2, 20))
    pygame.draw.rect(screen, GREEN, (WIDTH - 250, 30, player2.health * 2, 20))

def draw_timer():
    font = pygame.font.Font(None, 36)
    time_left = max(round_time - (pygame.time.get_ticks() - start_time), 0)
    timer_text = font.render(f"Time: {time_left // 1000}", True, WHITE)
    screen.blit(timer_text, (WIDTH // 2 - 50, 30))

def ai_action(player):
    action = random.choice(["move", "attack", "jump"])
    if action == "move":
        direction = random.choice([-1, 1])
        player.move(direction)
    elif action == "attack":
        attack_type = random.choice(["punch", "kick", "special"])
        if attack_type == "punch":
            player.punch()
        elif attack_type == "kick":
            player.kick()
        else:
            player.special_move()
    elif action == "jump":
        player.jump()

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    screen.fill(BLACK)

    # AI actions
    ai_action(player1)
    ai_action(player2)

    # Update characters
    player1.update()
    player2.update()

    # Draw characters
    player1.draw(screen)
    player2.draw(screen)

    # Draw health bars and timer
    draw_health_bars()
    draw_timer()

    # Check for game over conditions
    current_time = pygame.time.get_ticks()
    if current_time - start_time >= round_time or player1.health <= 0 or player2.health <= 0:
        game_over = True
        font = pygame.font.Font(None, 72)
        if player1.health > player2.health:
            winner_text = font.render("Player 1 Wins!", True, WHITE)
        elif player2.health > player1.health:
            winner_text = font.render("Player 2 Wins!", True, WHITE)
        else:
            winner_text = font.render("It's a Draw!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 150, HEIGHT // 2 - 36))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()