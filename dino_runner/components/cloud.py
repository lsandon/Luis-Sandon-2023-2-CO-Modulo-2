import random
from dino_runner.utils.constants import CLOUD
from dino_runner.utils.constants import SCREEN_WIDTH


class Cloud:

    def __init__(self):
        # Se extrae la imagen
        self.image = CLOUD
        # Se extrae el rectangulo de la imagen
        self.cloud_rect = self.image.get_rect()
        # Tamaño de la imagen
        self.width = self.image.get_width()
        self.cloud_rect.x = SCREEN_WIDTH + random.randint(100, 300)
        self.cloud_rect.y = random.randint(50, 100)
        # Velocidad a la que va el juego
        self.game_speed = 20

    def update(self):
        self.cloud_rect.x -= self.game_speed
        if self.cloud_rect.x < -self.width:
            self.cloud_rect.x = SCREEN_WIDTH + random.randint(100, 300)
            self.cloud_rect.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.cloud_rect.x, self.cloud_rect.y))
