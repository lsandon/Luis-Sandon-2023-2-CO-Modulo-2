import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH


class Obstacle(Sprite):

    def __init__(self, image, obstacle_type, bird_or_cactus=''):
        self.image = image
        self.obstacle_type = obstacle_type
        self.rect = self.image[self.obstacle_type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.bird_or_cactus = bird_or_cactus
        self.index = 0

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed

        # Si se pone en negativo el self.rect.width, se elimina el obstaculo cuando sale de la pantalla
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        if self.bird_or_cactus == '':
            screen.blit(self.image[self.obstacle_type], self.rect)
        elif self.bird_or_cactus == 'bird':
            if self.index > 9:
                self.index = 0

            image = self.image[0] if self.index < 5 else self.image[1]
            screen.blit(image, self.rect)
            self.index += 1

            # screen.blit(self.image[self.index//5], self.rect)
            # screen.blit(self.image[0] if self.index < 5 else self.image[1], self.rect)
