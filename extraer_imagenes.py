#!/usr/bin/env python3
"""
Extrae las imágenes base64 del juego a archivos externos (carpeta img/).
Ejecutar UNA VEZ desde la carpeta del juego:

    python extraer_imagenes.py

Resultado: crea img/avatar.png, img/logo.png, img/nina.jpg, etc.
El HTML ya busca esos archivos y usa base64 solo como fallback si no existen.
"""
import re, base64, os, sys

HTML_FILE = 'juego_cumple_nicole_v3.html'
IMG_DIR   = 'img'

# Mapa: clave JS → (nombre de archivo, extensión)
MAPPING = {
    'avatar':    ('avatar',    'png'),
    'logo':      ('logo',      'jpg'),
    'nina':      ('nina',      'jpg'),
    'formal':    ('formal',    'jpg'),
    'gracioso':  ('gracioso',  'jpg'),
    'nina2':     ('nina2',     'jpg'),
    # 'roja' ya está reemplazada por portada.jpg — no se extrae
}

if not os.path.exists(HTML_FILE):
    print(f'ERROR: No se encontró {HTML_FILE}')
    print('Ejecuta este script desde la misma carpeta que el HTML.')
    sys.exit(1)

os.makedirs(IMG_DIR, exist_ok=True)

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# Captura:  clave: "data:image/TYPE;base64,DATA"
pattern = re.compile(
    r'(\w+):\s*"data:image/([\w+]+);base64,([A-Za-z0-9+/=\s]+?)"',
    re.DOTALL
)

extraidos = 0
for m in pattern.finditer(content):
    key  = m.group(1)
    data = m.group(3).replace('\n', '').replace('\r', '').strip()

    if key not in MAPPING:
        continue

    fname, ext = MAPPING[key]
    filepath   = os.path.join(IMG_DIR, f'{fname}.{ext}')

    try:
        raw = base64.b64decode(data)
    except Exception as e:
        print(f'⚠️  Error decodificando {key}: {e}')
        continue

    with open(filepath, 'wb') as f:
        f.write(raw)

    print(f'✅  {filepath:30s} ({len(raw)//1024} KB)')
    extraidos += 1

if extraidos == 0:
    print('⚠️  No se encontraron imágenes base64 para extraer.')
    print('    Es posible que ya estén externalizadas o el HTML haya cambiado.')
else:
    total_kb = sum(
        os.path.getsize(os.path.join(IMG_DIR, f'{n}.{e}')) // 1024
        for n, e in MAPPING.values()
        if os.path.exists(os.path.join(IMG_DIR, f'{n}.{e}'))
    )
    print(f'\n🎉  {extraidos} imagen(es) extraída(s) → carpeta img/  ({total_kb} KB total)')
    print('    Recarga el juego en el navegador — cargará más rápido.')
