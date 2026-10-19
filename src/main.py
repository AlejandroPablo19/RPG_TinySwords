"""Punto de entrada del RPG."""

import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    FPS,
)

from entities.player import Player
from world.tiled_map import TiledMap
from systems.save_game import save_game, load_game


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    pygame.display.set_caption(SCREEN_TITLE)

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Cargar mapa y colisiones.
    world = TiledMap()

    # Recuperar la posición guardada, si existe.
    saved_position = load_game()

    if saved_position is not None:
        start_x = saved_position["x"]
        start_y = saved_position["y"]
    else:
        start_x = world.width / 2
        start_y = world.height * 0.75

    player = Player(start_x, start_y)

    # Si la posición guardada está dentro de un obstáculo,
    # iniciar en una posición segura predeterminada.
    if world.collides(player.collision_rect):
        player.position.update(
            world.width / 2,
            world.height * 0.75,
        )

    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(player)
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game(player)
                    running = False

                elif event.key == pygame.K_F5:
                    save_game(player)

                elif event.key == pygame.K_SPACE:
                    player.start_attack()

        if not running:
            break

        keys = pygame.key.get_pressed()
        player.update(dt, keys, world)

        # Dibujar el mapa completo sin cámara.
        world.draw(screen)

        # Dibujar al jugador encima del escenario.
        player.draw(screen)

        # Indicaciones de controles.
        controls = font.render(
            "WASD/Flechas: mover | Espacio: atacar | "
            "F5: guardar | ESC: salir",
            True,
            (255, 255, 255),
        )

        # Fondo oscuro para que el texto sea legible.
        background = pygame.Surface(
            (controls.get_width() + 16, 30),
            pygame.SRCALPHA,
        )
        background.fill((0, 0, 0, 160))

        screen.blit(background, (5, 5))
        screen.blit(controls, (13, 11))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()