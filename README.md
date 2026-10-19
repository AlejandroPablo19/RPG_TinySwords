# RPG 2D - Tiny Swords

Prototipo inicial en Python + Pygame con sprites originales de Tiny Swords Free Pack.

## Requisitos
- Python 3.13 recomendado para compatibilidad amplia con Pygame.
- VS Code con la extensión Python.

## Instalación (PowerShell, desde la carpeta del proyecto)
```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
```

Si el entorno `.venv` ya existe y está usando una versión compatible de Python, no es necesario recrearlo.

## Controles
- WASD o flechas: movimiento
- Espacio: animación de ataque
- F5: guardar posición en `saves/save.json`
- Esc: guardar y salir

## Nota sobre los sprites
Las hojas originales del guerrero tienen cuadros de 192 x 192 px. El prototipo las recorta en cuadros, las escala y anima Idle, Run y Attack1. El paquete del guerrero no ofrece en estas hojas una animación independiente para cada una de las cuatro direcciones; por ahora el personaje se voltea horizontalmente para caminar a la izquierda. La orientación arriba/abajo es provisional.

## Estructura prevista
- `src/entities`: jugador, enemigos y NPC.
- `src/world`: cámara y carga de mapas Tiled.
- `src/systems`: combate, misiones, inventario y guardado JSON.
- `src/ui`: HUD e inventario.
- `assets/maps`: mapas `.tmx` creados con Tiled.
- `assets/tilesets`: imágenes de tilesets.
- `saves`: partidas locales JSON.

El fondo verde cuadriculado es provisional. Todavía no se ha conectado un mapa TMX; eso es el siguiente paso después de validar el movimiento.
