import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SHIELD_TYPE


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def generate_obstacle(self, obstacle_type):
        if obstacle_type == 0:
            obstacle = Cactus('SMALL')
        elif obstacle_type == 1:
            obstacle = Cactus('LARGE')
        else:
            obstacle = Bird()
        return obstacle

    def update(self, game):
        if len(self.obstacles) == 0:
            obstacle_type = random.randint(0, 1)
            obstacle = self.generate_obstacle(obstacle_type)
            self.obstacles.append(obstacle)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE:
                    pygame.time.delay(1000)
                    game.death_count.update()
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
