"""Jugador: movimiento, animaciones, ataques, defensa, muerte y curación con carne."""

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
from ui.health_bar import HealthBar
from entities.arrow import Arrow

ROOT = Path(__file__).resolve().parents[2]
SPRITES = ROOT / "assets" / "images" / "player" / "Warrior"
EFFECTS = ROOT / "assets" / "images" / "effects"
ARROW_SPRITE = ROOT / "assets" / "images" / "player" / "Archer" / "Arrow.png"


class Player:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.speed = PLAYER_SPEED
        self.facing = "down"

        self.moving = False
        self.attacking = False
        self.defending = False
        self.healing = False
        self.is_dead = False
        self.arrow_cooldown = 0.0
        self.heal_frame_index = 0
        self.heal_animation_elapsed = 0.0

        self.attack_type = 1
        self.attack_elapsed = 0.0
        self.frame_index = 0
        self.animation_elapsed = 0.0

        self.scale = PLAYER_DRAW_SIZE
        self.max_health = 100
        self.health = 100
        self.health_bar = HealthBar(-15, -35, 52, 8, self.max_health)

        # Carga de frames de animaciones del jugador
        self.idle_frames = self._load_sheet(SPRITES, "Warrior_Idle.png")
        self.run_frames = self._load_sheet(SPRITES, "Warrior_Run.png")
        self.attack1_frames = self._load_sheet(SPRITES, "Warrior_Attack1.png")
        self.attack2_frames = self._load_sheet(SPRITES, "Warrior_Attack2.png")
        self.guard_frames = self._load_sheet(SPRITES, "Warrior_Guard.png")

        self.heal_effect_frames = self._load_sheet(
            EFFECTS,
            "Heal_Effect.png",
            draw_size=PLAYER_DRAW_SIZE,
        )

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(center=(round(x), round(y)))

    @property
    def collision_rect(self):
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

    def _load_sheet(
        self,
        folder,
        filename,
        frame_width=SPRITE_FRAME_WIDTH,
        frame_height=SPRITE_FRAME_HEIGHT,
        draw_size=None,
    ):
        path = folder / filename
        if not path.exists():
            raise FileNotFoundError(f"No se encontró el sprite: {path}")

        sheet = pygame.image.load(str(path)).convert_alpha()
        frames = []
        count = sheet.get_width() // frame_width
        draw_size = draw_size or self.scale

        for i in range(count):
            frame = pygame.Surface(
                (frame_width, frame_height), pygame.SRCALPHA
            )
            frame.blit(
                sheet,
                (0, 0),
                (
                    i * frame_width,
                    0,
                    frame_width,
                    frame_height,
                ),
            )
            frame = pygame.transform.scale(frame, (draw_size, draw_size))
            frames.append(frame)
        return frames

    def start_attack(self, combo=1):
        if not self.is_dead and not self.attacking and not self.defending and not self.healing:
            self.attacking = True
            self.attack_type = combo
            self.attack_elapsed = 0.0
            self.frame_index = 0
            self.animation_elapsed = 0.0

    def shoot_arrow(self):
        if self.is_dead or self.defending or self.healing or self.arrow_cooldown > 0:
            return None

        directions = {
            "up": pygame.Vector2(0, -1),
            "down": pygame.Vector2(0, 1),
            "left": pygame.Vector2(-1, 0),
            "right": pygame.Vector2(1, 0),
        }
        direction = directions[self.facing]
        self.arrow_cooldown = 0.35

        return Arrow(
            self.position.x + direction.x * 28,
            self.position.y + direction.y * 28,
            direction,
            ARROW_SPRITE,
        )

    def update(self, dt, keys, world):
        self.arrow_cooldown = max(0.0, self.arrow_cooldown - dt)

        # Comprobaciones de control por teclado para Pruebas:
        if keys[pygame.K_m]:  # Simular Muerte
            self.is_dead = True
            self.health = 0
        if keys[pygame.K_r]:  # Revivir
            self.is_dead = False
            self.health = self.max_health

        if self.is_dead:
            self.health_bar.health = 0
            return  # Si está muerto, bloquea el resto de acciones

        # Curación con carne (Tecla H)
        if keys[pygame.K_h]:
            if not self.healing:
                self.heal_frame_index = 0
                self.heal_animation_elapsed = 0.0
            self.healing = True
            self.health = min(self.max_health, self.health + 0.3)
        else:
            self.healing = False

        # Defensa (Tecla J)
        if keys[pygame.K_j]:
            self.defending = True
        else:
            self.defending = False

        # Ataques (Espacio / K)
        if keys[pygame.K_SPACE]:
            self.start_attack(1)
        elif keys[pygame.K_k]:
            self.start_attack(2)

        direction = pygame.Vector2(0, 0)
        if not self.defending:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                direction.x -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                direction.x += 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                direction.y -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                direction.y += 1

        self.moving = direction.length_squared() > 0

        if self.moving and not self.attacking and not self.defending:
            direction = direction.normalize()
            if abs(direction.x) > abs(direction.y):
                self.facing = "right" if direction.x > 0 else "left"
            else:
                self.facing = "down" if direction.y > 0 else "up"

            previous_x = self.position.x
            self.position.x += direction.x * self.speed * dt
            if world.collides(self.collision_rect):
                self.position.x = previous_x

            previous_y = self.position.y
            self.position.y += direction.y * self.speed * dt
            if world.collides(self.collision_rect):
                self.position.y = previous_y

        # Limitar al mapa
        half = self.scale / 2
        self.position.x = max(half, min(world.width - half, self.position.x))
        self.position.y = max(half, min(world.height - half, self.position.y))

        # Selección de animación según estado actual
        if self.is_dead:
            frames = self.death_frames
        elif self.attacking:
            frames = self.attack2_frames if self.attack_type == 2 else self.attack1_frames
            self.attack_elapsed += dt
            if self.attack_elapsed >= (len(frames) / ANIMATION_FPS):
                self.attacking = False
                self.frame_index = 0
                self.animation_elapsed = 0.0
        elif self.defending:
            frames = self.guard_frames
        elif self.healing:
            frames = self.idle_frames
        else:
            frames = self.run_frames if self.moving else self.idle_frames

        # Control de fotogramas
        if self.attacking:
            self.frame_index = min(int(self.attack_elapsed * ANIMATION_FPS), len(frames) - 1)
        else:
            self.animation_elapsed += dt
            if self.animation_elapsed >= 1 / ANIMATION_FPS:
                self.animation_elapsed = 0.0
                self.frame_index = (self.frame_index + 1) % len(frames)

        if self.healing:
            self.heal_animation_elapsed += dt
            if self.heal_animation_elapsed >= 1 / ANIMATION_FPS:
                self.heal_animation_elapsed = 0.0
                self.heal_frame_index = (
                    self.heal_frame_index + 1
                ) % len(self.heal_effect_frames)

        frame = frames[self.frame_index % len(frames)]
        if self.facing == "left":
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame
        self.rect = self.image.get_rect(center=(round(self.position.x), round(self.position.y)))
        self.health_bar.health = self.health

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.healing and not self.is_dead:
            effect = self.heal_effect_frames[self.heal_frame_index]
            surface.blit(effect, effect.get_rect(center=self.rect.center))

        # Dibujar barra de vida encima del personaje
        self.health_bar.draw(surface, self.position.x, self.position.y - (self.scale // 2))