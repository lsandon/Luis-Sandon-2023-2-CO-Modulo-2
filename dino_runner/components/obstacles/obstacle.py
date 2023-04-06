from pygame.sprite import Sprite
from dino_runner.utils.constants import  SCREEN_WIDTH

class Obstacle(Sprite):
    def __init__(self, image):
        self.rect = image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.image = image

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed

        if self.rect.x < - 10:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))