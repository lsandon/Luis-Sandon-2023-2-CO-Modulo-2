import random

from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import LARGE_CACTUS, SMALL_CACTUS

class Cactus(Obstacle):
  CACTUS = { 'SMALL': (SMALL_CACTUS, 325),
             'LARGE': (LARGE_CACTUS, 300)}
  # image es una lista!
  def __init__(self, cactus_type):
    # self.type es como un indice
    image, cactus_pos = self.CACTUS[cactus_type]
    self.type = random.randint(0, 2)
    super().__init__(image, self.type)
    self.rect.y = cactus_pos

  def draw(self, screen):
    screen.blit(self.image[self.obstacle_type], (self.rect.x, self.rect.y))

