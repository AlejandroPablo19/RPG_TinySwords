import math
from pathlib import Path

import pygame

from settings import (
  ANIMATION_FPS,
  ENEMY_ATTACK_DAMAGE,
  FPS,
  PLAYER_DRAW_SIZE,
  PLAYER_COLLISION_HEIGHT,
  PLAYER_COLLISION_OFFSET_Y,
  PLAYER_COLLISION_WIDTH,
  SPRITE_FRAME_HEIGHT,
  SPRITE_FRAME_WIDTH,
)
from ui.health_bar import HealthBar


ROOT = Path(__file__).resolve().parents[2]
ENEMY_SPRITES = ROOT / "assets" / "images" / "enemies"
SOUNDS = ROOT / "assets" / "sounds"
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
    self.attack_range = 54
    self.attack_cooldown = 0.0
    self.attacking = False
    self.attack_type = 2
    self.attack_elapsed = 0.0
    self.attack_hit_applied = False
    self.facing = "down"
    footsteps_path = SOUNDS / "Walking In Suit Of Armour Sound Effect.mp3"
    if not footsteps_path.exists():
      raise FileNotFoundError(f"No se encontró el sonido: {footsteps_path}")
    self.footsteps_sound = pygame.mixer.Sound(str(footsteps_path))
    self.footsteps_channel = None

    self.state = 'PATROL'  # Estados: PATROL, CHASE, RETURN
    self.patrol_direction = 1
    self.patrol_timer = 0

    unit_folder = "Red Units" if unit_type == "red" else "Black Units"
    self.sprite_folder = ENEMY_SPRITES / unit_folder / "Warrior"
    self.idle_frames = self._load_frames("Warrior_Idle.png")
    self.run_frames = self._load_frames("Warrior_Run.png")
    self.attack1_frames = self._load_frames("Warrior_Attack1.png")
    self.attack2_frames = self._load_frames("Warrior_Attack2.png")
    self.attack_sounds = {
      1: self._load_sound("Sword Attack 1 Sound Effect.mp3"),
      2: self._load_sound("Sword Attack 2 Sound Effect.mp3"),
    }
    self.frame_index = 0
    self.animation_elapsed = 0.0
    self.image = self.idle_frames[0]
    self.rect = self.image.get_rect(center=(round(x), round(y)))

    self.max_health = 100
    self.health = 100
    self.health_bar = HealthBar(-25, -54, 50, 6, self.max_health)

  @property
  def collision_rect(self):
    return pygame.Rect(
      round(self.x - PLAYER_COLLISION_WIDTH / 2),
      round(
        self.y
        + PLAYER_COLLISION_OFFSET_Y
        - PLAYER_COLLISION_HEIGHT / 2
      ),
      PLAYER_COLLISION_WIDTH,
      PLAYER_COLLISION_HEIGHT,
    )

  def _move(self, dx, dy, world):
    moved_x = False
    moved_y = False

    next_x = self.x + dx
    self.x = next_x
    if (
        self.x < ENEMY_DRAW_SIZE / 2
        or self.x > world.width - ENEMY_DRAW_SIZE / 2
        or self.y < ENEMY_DRAW_SIZE / 2
        or self.y > world.height - ENEMY_DRAW_SIZE / 2
        or world.collides(self.collision_rect)
    ):
      self.x -= dx
    else:
      moved_x = dx != 0

    next_y = self.y + dy
    self.y = next_y
    if (
        self.x < ENEMY_DRAW_SIZE / 2
        or self.x > world.width - ENEMY_DRAW_SIZE / 2
        or self.y < ENEMY_DRAW_SIZE / 2
        or self.y > world.height - ENEMY_DRAW_SIZE / 2
        or world.collides(self.collision_rect)
    ):
      self.y -= dy
    else:
      moved_y = dy != 0

    return moved_x or moved_y

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

  @staticmethod
  def _load_sound(filename):
    path = SOUNDS / filename
    if not path.exists():
      raise FileNotFoundError(f"No se encontró el sonido: {path}")
    return pygame.mixer.Sound(str(path))

  def _attack_hitbox(self):
    reach = 44
    width = 38
    center_x = round(self.x)
    center_y = round(self.y + PLAYER_COLLISION_OFFSET_Y)
    if self.facing == "up":
      return pygame.Rect(center_x - width // 2, center_y - reach + 11, width, reach)
    if self.facing == "down":
      return pygame.Rect(center_x - width // 2, center_y - 11, width, reach)
    if self.facing == "left":
      return pygame.Rect(center_x - reach + 11, center_y - width // 2, reach, width)
    return pygame.Rect(center_x - 11, center_y - width // 2, reach, width)

  def _start_attack(self, player):
    dx = player.position.x - self.x
    dy = player.position.y - self.y
    if abs(dx) > abs(dy):
      self.facing = "right" if dx > 0 else "left"
    else:
      self.facing = "down" if dy > 0 else "up"

    self.attacking = True
    self.attack_type = 1 if self.attack_type == 2 else 2
    self.attack_elapsed = 0.0
    self.attack_hit_applied = False
    self.frame_index = 0
    self.attack_sounds[self.attack_type].play()

  def _update_attack(self, dt, player):
    frames = self.attack2_frames if self.attack_type == 2 else self.attack1_frames
    self.attack_elapsed += dt
    self.frame_index = min(
      int(self.attack_elapsed * ANIMATION_FPS),
      len(frames) - 1,
    )
    hit_frame = max(1, len(frames) // 2)
    if (
        self.frame_index >= hit_frame
        and not self.attack_hit_applied
    ):
      self.attack_hit_applied = True
      if self._attack_hitbox().colliderect(player.collision_rect):
        player.take_damage(ENEMY_ATTACK_DAMAGE)

    if self.attack_elapsed >= len(frames) / ANIMATION_FPS:
      self.attacking = False
      self.attack_cooldown = 0.8
      self.frame_index = 0

  def update(self, player, world, dt):
    self.attack_cooldown = max(0.0, self.attack_cooldown - dt)
    previous_position = (self.x, self.y)
    dist_to_player = math.hypot(
      player.position.x - self.x,
      player.position.y - self.y,
    )
    dist_to_start = math.hypot(self.start_x - self.x, self.start_y - self.y)

    if self.state == 'PATROL':
      # Movimiento de patrulla horizontal/perímetro
      moved = self._move(self.speed * 0.7 * self.patrol_direction, 0, world)
      if not moved:
        self.patrol_direction *= -1
      self.patrol_timer += 1
      if self.patrol_timer > 120:
        self.patrol_direction *= -1
        self.patrol_timer = 0

      # Detectar al jugador
      if not player.is_dead and dist_to_player <= self.detection_radius:
        self.state = 'CHASE'

    elif self.state == 'CHASE':
      # Dejar de seguir si se aleja demasiado (Leashing)
      if (
          player.is_dead
          or dist_to_player > self.lose_radius
          or dist_to_start > self.patrol_radius * 2.5
      ):
        self.state = 'RETURN'
      elif self.attacking:
        pass
      elif dist_to_player <= self.attack_range:
        if self.attack_cooldown <= 0:
          self._start_attack(player)
      elif dist_to_player > 0:
        dx = (player.position.x - self.x) / dist_to_player
        dy = (player.position.y - self.y) / dist_to_player
        self._move(dx * self.speed, dy * self.speed, world)

    elif self.state == 'RETURN':
      # Regresar al punto de patrulla original
      dist_home = math.hypot(self.start_x - self.x, self.start_y - self.y)
      if dist_home < 4:
        self.state = 'PATROL'
      else:
        dx = (self.start_x - self.x) / dist_home
        dy = (self.start_y - self.y) / dist_home
        self._move(dx * self.speed, dy * self.speed, world)

    if self.attacking:
      self._update_attack(dt, player)

    walking = previous_position != (self.x, self.y) and not self.attacking
    if walking:
      if (
          self.footsteps_channel is None
          or not self.footsteps_channel.get_busy()
      ):
        self.footsteps_channel = self.footsteps_sound.play(loops=-1)
    elif self.footsteps_channel is not None:
      self.footsteps_channel.stop()
      self.footsteps_channel = None

    frames = (
      self.attack2_frames if self.attack_type == 2 else self.attack1_frames
    ) if self.attacking else self.run_frames
    self.animation_elapsed += 1 / FPS
    if not self.attacking and self.animation_elapsed >= 1 / ANIMATION_FPS:
      self.animation_elapsed = 0.0
      self.frame_index = (self.frame_index + 1) % len(frames)

    frame = frames[self.frame_index % len(frames)]
    if self.facing == "left":
      frame = pygame.transform.flip(frame, True, False)
    self.image = frame
    self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
    self.health_bar.health = self.health

  def kill(self):
    if self.footsteps_channel is not None:
      self.footsteps_channel.stop()
      self.footsteps_channel = None
    super().kill()

  def draw(self, surface):
    surface.blit(self.image, self.rect)
    self.health_bar.draw(surface, self.x, self.y)