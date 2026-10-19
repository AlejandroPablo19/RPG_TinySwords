from pathlib import Path
import sys
import pygame

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BACKGROUND_COLOR, WORLD_WIDTH, WORLD_HEIGHT
from entities.player import Player
from world.camera import Camera
from systems.save_game import save_player, load_player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

start_x, start_y = load_player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
player = Player(start_x, start_y)
camera = Camera()
running = True

while running:
    dt = min(clock.tick(FPS) / 1000.0, 0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_player(player)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_player(player)
                running = False
            elif event.key == pygame.K_SPACE:
                player.start_attack()
            elif event.key == pygame.K_F5:
                save_player(player)

    keys = pygame.key.get_pressed()
    player.update(dt, keys)
    camera.update(player)

    screen.fill(BACKGROUND_COLOR)
    # Fondo provisional para probar movimiento y cámara antes de importar el mapa TMX.
    tile = 64
    start_col = camera.x // tile
    end_col = (camera.x + SCREEN_WIDTH) // tile + 1
    start_row = camera.y // tile
    end_row = (camera.y + SCREEN_HEIGHT) // tile + 1
    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            color = (80, 140, 78) if (row + col) % 2 == 0 else (76, 134, 74)
            pygame.draw.rect(screen, color, (col * tile - camera.x, row * tile - camera.y, tile, tile))

    player.draw(screen, camera)
    help_text = "WASD/Flechas: mover   ESPACIO: atacar   F5: guardar   ESC: guardar y salir"
    screen.blit(font.render(help_text, True, (255, 255, 255)), (14, 12))
    screen.blit(font.render("Prototipo: mapa provisional; siguiente paso, cargar el mapa de Tiled.", True, (255, 255, 255)), (14, 39))
    pygame.display.flip()

pygame.quit()
