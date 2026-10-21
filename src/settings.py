"""Configuración general del juego."""

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Mi RPG - Tiny Swords"
FPS = 60

# Tamaño original de cada cuadro de las animaciones.
SPRITE_FRAME_WIDTH = 192
SPRITE_FRAME_HEIGHT = 192

# Tamaño al que se dibuja el personaje.
PLAYER_DRAW_SIZE = 96

# Área que se utiliza para detectar colisiones.
PLAYER_COLLISION_WIDTH = 30
PLAYER_COLLISION_HEIGHT = 22
PLAYER_COLLISION_OFFSET_Y = 22

# Velocidad del jugador en píxeles por segundo.
PLAYER_SPEED = 180

# Daño del ataque enemigo e invulnerabilidad temporal del jugador.
ENEMY_ATTACK_DAMAGE = 10
PLAYER_DAMAGE_COOLDOWN = 1.0

# Velocidad de reproducción de las animaciones.
ANIMATION_FPS = 8