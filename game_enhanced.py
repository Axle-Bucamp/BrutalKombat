import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Burger King Fighter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def load_character_assets(folder_name):
    assets = {}
    asset_path = os.path.join('assets', folder_name)
    for filename in os.listdir(asset_path):
        if filename.endswith('.png'):
            asset_name = os.path.splitext(filename)[0]
            assets[asset_name] = pygame.image.load(os.path.join(asset_path, filename))
    return assets

class Character:
    def __init__(self, x, y, assets):
        self.x = x
        self.y = y
        self.assets = assets
        self.current_sprite = 'idle'
        self.health = 100
        self.rect = self.assets['idle'].get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx):
        self.x += dx
        self.rect.x = self.x

    def attack(self):
        self.current_sprite = 'attack'

    def draw(self, screen):
        screen.blit(self.assets[self.current_sprite], self.rect)

    def update(self):
        if self.current_sprite != 'idle':
            self.current_sprite = 'idle'

class SimpleAI:
    def __init__(self, character, opponent):
        self.character = character
        self.opponent = opponent

    def make_decision(self):
        distance = abs(self.character.x - self.opponent.x)
        if distance < 100:
            return 'attack'
        elif self.character.x < self.opponent.x:
            return 'move_right'
        else:
            return 'move_left'

def main():
    clock = pygame.time.Clock()
    player1_assets = load_character_assets('player1')
    player2_assets = load_character_assets('player2')

    player1 = Character(100, 400, player1_assets)
    player2 = Character(600, 400, player2_assets)

    ai1 = SimpleAI(player1, player2)
    ai2 = SimpleAI(player2, player1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # AI decision making
        decision1 = ai1.make_decision()
        decision2 = ai2.make_decision()

        # Execute AI decisions
        if decision1 == 'attack':
            player1.attack()
        elif decision1 == 'move_right':
            player1.move(5)
        elif decision1 == 'move_left':
            player1.move(-5)

        if decision2 == 'attack':
            player2.attack()
        elif decision2 == 'move_right':
            player2.move(5)
        elif decision2 == 'move_left':
            player2.move(-5)

        # Update characters
        player1.update()
        player2.update()

        # Draw everything
        screen.fill(WHITE)
        player1.draw(screen)
        player2.draw(screen)

        # Draw health bars
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, player1.health * 2, 20))
        pygame.draw.rect(screen, RED, (590, 10, 200, 20))
        pygame.draw.rect(screen, GREEN, (590, 10, player2.health * 2, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()