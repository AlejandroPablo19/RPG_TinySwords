import math
from pathlib import Path

import pygame


class Arrow(pygame.sprite.Sprite):

  def __init__(self, x, y, direction, image_path, speed=420, damage=25):
    super().__init__()
    self.position = pygame.Vector2(x, y)
    self.velocity = pygame.Vector2(direction).normalize() * speed
    self.damage = damage

    path = Path(image_path)
    if not path.exists():
      raise FileNotFoundError(f"No se encontró el sprite de la flecha: {path}")

    arrow_image = pygame.image.load(str(path)).convert_alpha()
    arrow_image = pygame.transform.scale(arrow_image, (48, 48))
    angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x))
    self.image = pygame.transform.rotate(arrow_image, -angle)
    self.rect = self.image.get_rect(center=(round(x), round(y)))

  def update(self, dt):
    self.position += self.velocity * dt
    self.rect.center = (round(self.position.x), round(self.position.y))

  def draw(self, surface):
    surface.blit(self.image, self.rect)