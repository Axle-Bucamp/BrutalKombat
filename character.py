import pygame
import random

class Character:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 100
        self.speed = 5
        self.jumping = False
        self.jump_count = 10

    def move(self, dx):
        self.rect.x += dx * self.speed

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_count = 10

    def update(self):
        if self.jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jumping = False

    def punch(self):
        return random.randint(5, 10)

    def kick(self):
        return random.randint(7, 12)

    def special_move(self):
        return random.randint(15, 20)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)