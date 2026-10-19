import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, target):
        self.offset.x = target.position.x - SCREEN_WIDTH / 2
        self.offset.y = target.position.y - SCREEN_HEIGHT / 2
        self.offset.x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, self.offset.x))
        self.offset.y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, self.offset.y))

    @property
    def x(self): return int(self.offset.x)
    @property
    def y(self): return int(self.offset.y)
