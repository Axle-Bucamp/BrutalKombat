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
            self.jump_count = 10

    def update_jump(self):
        if self.jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jumping = False

    def punch(self, other):
        if self.rect.colliderect(other.rect):
            damage = random.randint(5, 10)
            other.health -= damage

    def kick(self, other):
        if self.rect.colliderect(other.rect):
            damage = random.randint(7, 15)
            other.health -= damage

    def special_move(self, other):
        if self.rect.colliderect(other.rect):
            damage = random.randint(10, 20)
            other.health -= damage

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)