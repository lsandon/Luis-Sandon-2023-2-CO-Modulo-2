from dino_runner.components.powerups.powerup import PowerUp
from dino_runner.utils.constants import HAMMER, HAMMER_TYPE

class Hamer(PowerUp):
    def __init__(self):
        super().__init__(HAMMER, HAMMER_TYPE)