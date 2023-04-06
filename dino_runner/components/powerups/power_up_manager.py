import random
import pygame
import os

from dino_runner.utils.constants import AUDIO_DIR
from dino_runner.components.powerups.shield import Shield
from dino_runner.components.powerups.hammer import Hamer


class Power_Up_Manager:
    def __init__(self):
        self.power_ups = []
        self.when_apears = 0

    def generate_power(self, score):
        if len(self.power_ups) == 0 and self.when_apears == score:
            self.when_apears += random.randint(200, 300)
            select_Powerup = random.randint(0, 20)
            if select_Powerup %2 == 0:
                self.power_ups.append(Hamer())
            else:
               self.power_ups.append(Shield()) 

    def update(self, score, game_speed, player):
        self.generate_power(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                AUDIO_POWER = AUDIO_JUMP = pygame.mixer.Sound(os.path.join(AUDIO_DIR,'audios/coin.wav'))
                AUDIO_POWER.play()
                power_up.start_time = pygame.time.get_ticks()
                player.image_type = power_up.power_type
                player.has_power_up = True
                player.shield = True
                player.shield_time_up = power_up.start_time + (power_up.duration * 100)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_powerups(self):
        self.power_ups = []
        self.when_apears = random.randint(200, 300)