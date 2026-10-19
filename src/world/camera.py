import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        self.offset = pygame.Vector2(0, 0)

    def update(self, target):
        self.offset.x = target.position.x - SCREEN_WIDTH / 2
        self.offset.y = target.position.y - SCREEN_HEIGHT / 2
        self.offset.x = max(0, min(self.world_width - SCREEN_WIDTH, self.offset.x))
        self.offset.y = max(0, min(self.world_height - SCREEN_HEIGHT, self.offset.y))

    @property
    def x(self):
        return int(self.offset.x)

    @property
    def y(self):
        return int(self.offset.y)
