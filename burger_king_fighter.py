import pygame
import random
import os

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Burger King Street Fighter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
asset_folder = "assets"
character_images = {
    "whopper": pygame.image.load(os.path.join(asset_folder, "whopper.png")),
    "big_king": pygame.image.load(os.path.join(asset_folder, "big_king.png"))
}

# Character class
class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = character_images[name]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def attack(self, other):
        if self.rect.colliderect(other.rect):
            other.health -= 10

# AI logic
def ai_move(character, target):
    dx = 0
    dy = 0
    if character.rect.x < target.rect.x:
        dx = 1
    elif character.rect.x > target.rect.x:
        dx = -1
    if character.rect.y < target.rect.y:
        dy = 1
    elif character.rect.y > target.rect.y:
        dy = -1
    return dx, dy

# Game setup
player1 = Character("whopper", 100, 300)
player2 = Character("big_king", 700, 300)
all_sprites = pygame.sprite.Group(player1, player2)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI movement and attacks
    p1_dx, p1_dy = ai_move(player1, player2)
    p2_dx, p2_dy = ai_move(player2, player1)

    player1.move(p1_dx, p1_dy)
    player2.move(p2_dx, p2_dy)

    # Random attacks
    if random.random() < 0.02:  # 2% chance to attack each frame
        player1.attack(player2)
    if random.random() < 0.02:
        player2.attack(player1)

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display health
    font = pygame.font.Font(None, 36)
    health_text1 = font.render(f"{player1.name}: {player1.health}", True, BLACK)
    health_text2 = font.render(f"{player2.name}: {player2.health}", True, BLACK)
    screen.blit(health_text1, (10, 10))
    screen.blit(health_text2, (SCREEN_WIDTH - 200, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()