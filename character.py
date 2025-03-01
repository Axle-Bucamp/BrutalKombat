import pygame
import random

class Character:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 100
        self.jumping = False
        self.jump_count = 10

    def move(self, dx):
        self.rect.x += dx

    def jump(self):
        if not self.jumping:
            self.jumping = True

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
                self.jump_count = 10

    def punch(self, other):
        damage = random.randint(5, 15)
        other.health -= damage
        return damage

    def kick(self, other):
        damage = random.randint(10, 20)
        other.health -= damage
        return damage

    def special_move(self, other):
        damage = random.randint(15, 25)
        other.health -= damage
        return damage

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)