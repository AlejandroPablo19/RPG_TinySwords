import math
from pathlib import Path

import pygame

from settings import (
  ANIMATION_FPS,
  FPS,
  PLAYER_DRAW_SIZE,
  SPRITE_FRAME_HEIGHT,
  SPRITE_FRAME_WIDTH,
)
from ui.health_bar import HealthBar


ROOT = Path(__file__).resolve().parents[2]
ENEMY_SPRITES = ROOT / "assets" / "images" / "enemies"
ENEMY_DRAW_SIZE = PLAYER_DRAW_SIZE


class Enemy(pygame.sprite.Sprite):

  def __init__(self, x, y, unit_type='red', patrol_radius=120):
    super().__init__()
    self.x = x
    self.y = y
    self.start_x = x
    self.start_y = y
    self.patrol_radius = patrol_radius
    self.unit_type = unit_type  # 'red' o 'black' (carpetas correspondientes)

    self.speed = 2.0
    self.detection_radius = 160
    self.lose_radius = 260

    self.state = 'PATROL'  # Estados: PATROL, CHASE, RETURN
    self.patrol_direction = 1
    self.patrol_timer = 0

    unit_folder = "Red Units" if unit_type == "red" else "Black Units"
    self.sprite_folder = ENEMY_SPRITES / unit_folder / "Warrior"
    self.idle_frames = self._load_frames("Warrior_Idle.png")
    self.run_frames = self._load_frames("Warrior_Run.png")
    self.frame_index = 0
    self.animation_elapsed = 0.0
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect(center=(round(x), round(y)))

    self.max_health = 100
    self.health = 100
    self.health_bar = HealthBar(-25, -54, 50, 6, self.max_health)

  def _load_frames(self, filename):
    path = self.sprite_folder / filename
    if not path.exists():
      raise FileNotFoundError(f"No se encontró el sprite del enemigo: {path}")

    sheet = pygame.image.load(str(path)).convert_alpha()
    frames = []
    frame_count = sheet.get_width() // SPRITE_FRAME_WIDTH

    for index in range(frame_count):
      frame = pygame.Surface(
        (SPRITE_FRAME_WIDTH, SPRITE_FRAME_HEIGHT),
        pygame.SRCALPHA,
      )
      frame.blit(
        sheet,
        (0, 0),
        (
          index * SPRITE_FRAME_WIDTH,
          0,
          SPRITE_FRAME_WIDTH,
          SPRITE_FRAME_HEIGHT,
        ),
      )
      frames.append(
        pygame.transform.scale(frame, (ENEMY_DRAW_SIZE, ENEMY_DRAW_SIZE))
      )

    return frames

  def update(self, player):
    dist_to_player = math.hypot(
      player.position.x - self.x,
      player.position.y - self.y,
    )
    dist_to_start = math.hypot(self.start_x - self.x, self.start_y - self.y)

    if self.state == 'PATROL':
      # Movimiento de patrulla horizontal/perímetro
      self.x += self.speed * 0.7 * self.patrol_direction
      self.patrol_timer += 1
      if self.patrol_timer > 120:
        self.patrol_direction *= -1
        self.patrol_timer = 0

      # Detectar al jugador
      if dist_to_player <= self.detection_radius:
        self.state = 'CHASE'

    elif self.state == 'CHASE':
      # Perseguir al jugador
      if dist_to_player > 0:
        dx = (player.position.x - self.x) / dist_to_player
        dy = (player.position.y - self.y) / dist_to_player
        self.x += dx * self.speed
        self.y += dy * self.speed

      # Dejar de seguir si se aleja demasiado (Leashing)
      if (
          dist_to_player > self.lose_radius
          or dist_to_start > self.patrol_radius * 2.5
      ):
        self.state = 'RETURN'

    elif self.state == 'RETURN':
      # Regresar al punto de patrulla original
      dist_home = math.hypot(self.start_x - self.x, self.start_y - self.y)
      if dist_home < 4:
        self.state = 'PATROL'
      else:
        dx = (self.start_x - self.x) / dist_home
        dy = (self.start_y - self.y) / dist_home
        self.x += dx * self.speed
        self.y += dy * self.speed

    frames = self.run_frames
    self.animation_elapsed += 1 / FPS
    if self.animation_elapsed >= 1 / ANIMATION_FPS:
      self.animation_elapsed = 0.0
      self.frame_index = (self.frame_index + 1) % len(frames)

    self.image = frames[self.frame_index % len(frames)]
    self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
    self.health_bar.health = self.health

  def draw(self, surface):
    surface.blit(self.image, self.rect)
    self.health_bar.draw(surface, self.x, self.y)