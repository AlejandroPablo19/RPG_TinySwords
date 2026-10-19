"""Jugador: movimiento, animaciones y ataque básico."""

from pathlib import Path

import pygame

from settings import (
    SPRITE_FRAME_WIDTH,
    SPRITE_FRAME_HEIGHT,
    PLAYER_DRAW_SIZE,
    PLAYER_COLLISION_WIDTH,
    PLAYER_COLLISION_HEIGHT,
    PLAYER_COLLISION_OFFSET_Y,
    PLAYER_SPEED,
    ANIMATION_FPS,
)


ROOT = Path(__file__).resolve().parents[2]
SPRITES = ROOT / "assets" / "images" / "player"


class Player:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.speed = PLAYER_SPEED
        self.facing = "down"

        self.moving = False
        self.attacking = False
        self.attack_elapsed = 0.0
        self.frame_index = 0
        self.animation_elapsed = 0.0

        self.scale = PLAYER_DRAW_SIZE

        self.idle_frames = self._load_sheet("Warrior_Idle.png")
        self.run_frames = self._load_sheet("Warrior_Run.png")
        self.attack_frames = self._load_sheet("Warrior_Attack1.png")

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(
            center=(round(x), round(y))
        )

    @property
    def collision_rect(self):
        """Área pequeña en los pies del jugador."""
        return pygame.Rect(
            round(self.position.x - PLAYER_COLLISION_WIDTH / 2),
            round(
                self.position.y
                + PLAYER_COLLISION_OFFSET_Y
                - PLAYER_COLLISION_HEIGHT / 2
            ),
            PLAYER_COLLISION_WIDTH,
            PLAYER_COLLISION_HEIGHT,
        )

    def _load_sheet(self, filename):
        path = SPRITES / filename

        if not path.exists():
            raise FileNotFoundError(
                f"No se encontró el sprite: {path}"
            )

        sheet = pygame.image.load(str(path)).convert_alpha()
        frames = []

        count = sheet.get_width() // SPRITE_FRAME_WIDTH

        for i in range(count):
            frame = pygame.Surface(
                (SPRITE_FRAME_WIDTH, SPRITE_FRAME_HEIGHT),
                pygame.SRCALPHA,
            )

            frame.blit(
                sheet,
                (0, 0),
                (
                    i * SPRITE_FRAME_WIDTH,
                    0,
                    SPRITE_FRAME_WIDTH,
                    SPRITE_FRAME_HEIGHT,
                ),
            )

            frame = pygame.transform.scale(
                frame,
                (self.scale, self.scale),
            )

            frames.append(frame)

        return frames

    def start_attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_elapsed = 0.0
            self.frame_index = 0
            self.animation_elapsed = 0.0

    def update(self, dt, keys, world):
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1

        self.moving = direction.length_squared() > 0

        if self.moving and not self.attacking:
            direction = direction.normalize()

            if abs(direction.x) > abs(direction.y):
                self.facing = "right" if direction.x > 0 else "left"
            else:
                self.facing = "down" if direction.y > 0 else "up"

            # Movimiento horizontal.
            previous_x = self.position.x
            self.position.x += direction.x * self.speed * dt

            if world.collides(self.collision_rect):
                self.position.x = previous_x

            # Movimiento vertical.
            previous_y = self.position.y
            self.position.y += direction.y * self.speed * dt

            if world.collides(self.collision_rect):
                self.position.y = previous_y

        # Impedir que el jugador salga de los límites del mapa.
        half = self.scale / 2

        self.position.x = max(
            half,
            min(world.width - half, self.position.x),
        )

        self.position.y = max(
            half,
            min(world.height - half, self.position.y),
        )

        # Actualizar animaciones.
        if self.attacking:
            self.attack_elapsed += dt

            if self.attack_elapsed >= (
                len(self.attack_frames) / ANIMATION_FPS
            ):
                self.attacking = False
                self.frame_index = 0
                self.animation_elapsed = 0.0

        if self.attacking:
            frames = self.attack_frames
            self.frame_index = min(
                int(self.attack_elapsed * ANIMATION_FPS),
                len(frames) - 1,
            )
        else:
            frames = (
                self.run_frames if self.moving
                else self.idle_frames
            )

            self.animation_elapsed += dt

            if self.animation_elapsed >= 1 / ANIMATION_FPS:
                self.animation_elapsed = 0.0
                self.frame_index = (
                    self.frame_index + 1
                ) % len(frames)

        frame = frames[self.frame_index % len(frames)]

        # Los sprites se voltean horizontalmente al mirar a la izquierda.
        if self.facing == "left":
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame
        self.rect = self.image.get_rect(
            center=(
                round(self.position.x),
                round(self.position.y),
            )
        )

    def draw(self, surface):
        """Dibuja al jugador directamente, sin cámara."""
        surface.blit(self.image, self.rect)