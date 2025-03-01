import pygame
import random

class Character:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 100
        self.speed = 5
        self.jump_power = 10
        self.y_velocity = 0
        self.is_jumping = False

    def move(self, dx):
        self.rect.x += dx * self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = -self.jump_power

    def update(self):
        if self.is_jumping:
            self.rect.y += self.y_velocity
            self.y_velocity += 0.5
            if self.rect.y >= 300:  # Ground level
                self.rect.y = 300
                self.is_jumping = False
                self.y_velocity = 0

    def punch(self):
        return random.randint(5, 15)

    def kick(self):
        return random.randint(7, 20)

    def special_move(self):
        return random.randint(10, 25)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)