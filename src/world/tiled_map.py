"""Carga el mapa de Tiled y administra sus colisiones."""

from pathlib import Path

import pygame
import pytmx


ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = ROOT / "assets" / "maps" / "camp.tmx"


class TiledMap:
    def __init__(self):
        if not MAP_PATH.exists():
            raise FileNotFoundError(
                f"No se encontró el mapa: {MAP_PATH}"
            )

        self.tmx = pytmx.util_pygame.load_pygame(str(MAP_PATH))

        self.width = self.tmx.width * self.tmx.tilewidth
        self.height = self.tmx.height * self.tmx.tileheight

        # Rectángulos de colisión definidos en Tiled.
        self.collision_rects = []

        if "Colisiones" not in self.tmx.layernames:
            raise ValueError(
                "No existe una capa llamada 'Colisiones' en camp.tmx."
            )

        collision_layer = self.tmx.get_layer_by_name("Colisiones")

        for obj in collision_layer:
            if obj.width > 0 and obj.height > 0:
                rect = pygame.Rect(
                    round(obj.x),
                    round(obj.y),
                    round(obj.width),
                    round(obj.height),
                )
                self.collision_rects.append(rect)

    def draw(self, surface):
        """Dibuja las capas de tiles del mapa."""
        
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if image is not None:
                        surface.blit(
                            image,
                            (
                                x * self.tmx.tilewidth,
                                y * self.tmx.tileheight,
                            ),
                            
                        )

    

    def collides(self, rect):
        """Devuelve True si el rectángulo toca algún obstáculo."""
        return any(
            rect.colliderect(obstacle)
            for obstacle in self.collision_rects
        )