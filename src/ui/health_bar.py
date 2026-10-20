import pygame


class HealthBar:

  def __init__(self, x, y, w, h, max_health):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.max_health = max_health
    self.health = max_health

  def draw(self, surface, entity_x, entity_y):
    # Posición relativa sobre la entidad
    bx = entity_x + self.x
    by = entity_y + self.y

    # Fondo rojo (daño / vida faltante)
    pygame.draw.rect(surface, (200, 0, 0), (bx, by, self.w, self.h))
    # Barra verde (vida actual)
    current_w = int(self.w * (self.health / self.max_health))
    current_w = max(0, current_w)
    pygame.draw.rect(surface, (0, 200, 0), (bx, by, current_w, self.h))
    # Contorno negro
    pygame.draw.rect(surface, (0, 0, 0), (bx, by, self.w, self.h), 1)