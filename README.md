# RPG 2D - Tiny Swords + Tiled

Prototipo inicial en Python + Pygame con los sprites originales de Tiny Swords y el mapa `camp.tmx` creado en Tiled.

## Requisitos
- Python 3.13 recomendado para compatibilidad amplia con Pygame.
- VS Code con la extensión Python.
- Tiled (solo si quieres editar el mapa).

## Instalación (PowerShell, desde la carpeta del proyecto)
```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python src/main.py
```

Si tu entorno `.venv` ya existe y usa una versión compatible de Python, puedes activarlo en lugar de crearlo otra vez.

## Controles
- WASD o flechas: movimiento.
- Espacio: animación de ataque.
- F: disparar una flecha hacia la dirección en la que mira el jugador.
- H: curarse con la animación `Heal_Effect`.
- J: defenderse; K: segundo ataque.
- M: simular muerte; R: revivir.
- F5: guardar posición en `saves/save.json`.
- Esc: guardar y salir.

## Mapa de Tiled
El mapa se encuentra en `assets/maps/camp.tmx`. El archivo que compartiste hace referencia al tileset `../tilesets/Tilemap_color1.tsx`; se agregó ese archivo TSX y se configuró para usar `assets/tilesets/Tilemap_color1.png` del paquete Tiny Swords. El mapa tiene 30 columnas y 20 filas, con tiles de 32 x 32 px, por lo que mide 960 x 640 px.

Si abres el mapa en Tiled, conserva el archivo `.tmx` dentro de `assets/maps/` y el tileset `.tsx` dentro de `assets/tilesets/` para que la ruta relativa siga funcionando.

## Estado actual y siguientes pasos
- Integrado: mapa TMX y capas visibles, colisiones según los GIDs de `BLOCKED_TILES` en `src/settings.py`, movimiento, animaciones Idle/Run/Attack1, enemigos con patrulla y persecución, cámara básica y guardado JSON de posición.
- Pendiente: daño/vida, inventario y misiones.
- El mapa tiene el mismo tamaño que la ventana actual (960 x 640), así que por ahora la cámara no necesita desplazarse. Si el mapa crece, la cámara permitirá recorrerlo.
- Las hojas de animación de este guerrero no incluyen una animación independiente para cada dirección; la orientación vertical sigue siendo provisional.
