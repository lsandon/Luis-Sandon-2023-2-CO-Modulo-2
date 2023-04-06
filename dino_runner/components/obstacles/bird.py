import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    BIRD_HEIGHTS = [280, 220, 170]

    def __init__(self):
        self.type = 0
        super().__init__(BIRD, self.type)
        self.rect.y = self.BIRD_HEIGHTS[random.randint(0, 2)]
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0

        screen.blit(BIRD[self.index // 5], self.rect)
        self.index += 1
