"""
Verwerk logo_raw.png naar icon.png (256x256) en logo.png (512x512).

Gebruik:
    python3 process_logo.py

Vereiste: Pillow  ->  pip install Pillow
Input:  logo_raw.png  (het originele logo met lichte achtergrond)
Output: icon.png      (256x256, transparante achtergrond)
        logo.png      (512x512, transparante achtergrond)
"""

from pathlib import Path
from PIL import Image

SCRIPT_DIR = Path(__file__).parent
INPUT = SCRIPT_DIR / "logo_raw.png"
ICON = SCRIPT_DIR / "icon.png"
LOGO = SCRIPT_DIR / "logo.png"

# Kleur van de achtergrond die weggehaald moet worden
# De afbeelding heeft een lichte mint/teal achtergrond (~#e0f2f1)
BG_THRESHOLD = 30  # hoe hoger, hoe meer kleurnuances als achtergrond worden gezien


def remove_background(img: Image.Image) -> Image.Image:
    """Vervang de lichte achtergrondkleur door transparantie."""
    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size

    # Sample de achtergrondkleur uit de hoeken
    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    bg_r = sum(c[0] for c in corners) // 4
    bg_g = sum(c[1] for c in corners) // 4
    bg_b = sum(c[2] for c in corners) // 4

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            diff = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)
            if diff < BG_THRESHOLD * 3:
                pixels[x, y] = (r, g, b, 0)

    return img


def process(size: int, output: Path) -> None:
    img = Image.open(INPUT)
    img = remove_background(img)

    # Bijsnijden tot vierkant (centreren)
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    img = img.resize((size, size), Image.LANCZOS)
    img.save(output, "PNG")
    print(f"Opgeslagen: {output} ({size}x{size})")


if __name__ == "__main__":
    if not INPUT.exists():
        print(f"Fout: {INPUT} niet gevonden. Sla het logo eerst op als logo_raw.png")
        raise SystemExit(1)

    process(256, ICON)
    process(512, LOGO)
    print("Klaar! icon.png en logo.png zijn aangemaakt.")
