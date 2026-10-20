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

from entities.enemy import Enemy
from entities.arrow import Arrow

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

    # Enemigos colocados en posiciones del mapa.
    enemy_group = pygame.sprite.Group(
        Enemy(x=400, y=300, unit_type="red", patrol_radius=150),
        Enemy(x=650, y=400, unit_type="black", patrol_radius=120),
    )
    arrow_group = pygame.sprite.Group()
    map_bounds = pygame.Rect(0, 0, world.width, world.height)

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

                elif event.key == pygame.K_f:
                    arrow = player.shoot_arrow()
                    if arrow is not None:
                        arrow_group.add(arrow)

        if not running:
            break

        keys = pygame.key.get_pressed()
        player.update(dt, keys, world)

        # Actualizar enemigos después de actualizar al jugador.
        for enemy in enemy_group:
            enemy.update(player)

        arrow_group.update(dt)
        for arrow in arrow_group:
            if not map_bounds.colliderect(arrow.rect):
                arrow.kill()
                continue

            for enemy in pygame.sprite.spritecollide(arrow, enemy_group, False):
                enemy.health -= arrow.damage
                enemy.health_bar.health = max(0, enemy.health)
                arrow.kill()
                if enemy.health <= 0:
                    enemy.kill()
                break

        # Dibujar el mapa completo sin cámara.
        world.draw(screen)

        # Dibujar enemigos entre el mapa y el jugador.
        for enemy in enemy_group:
            enemy.draw(screen)

        for arrow in arrow_group:
            arrow.draw(screen)

        # Dibujar al jugador encima del escenario.
        player.draw(screen)

        # Indicaciones de controles.
        controls = font.render(
            "WASD/Flechas: mover | Espacio: ataque 1 | k: ataque 2 | j: defenderse |"
            " F: arco | h: curarse | m: morir | r: revivir | F5: guardar | ESC: salir",
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