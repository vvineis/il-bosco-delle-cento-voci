# -*- coding: utf-8 -*-
"""
La mappa del Bosco delle Cento Voci.

Il paesaggio è l'illustrazione in img/map_img.png; sopra ci va uno strato SVG
con i luoghi cliccabili e i loro nomi. Le etichette restano vettoriali, quindi
nitide a qualsiasi ingrandimento anche se l'immagine sotto è un raster.

Uso:  python tools/mappa.py   prepara l'immagine per il web e scrive il provino
"""
import sys

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SORGENTE = ROOT / "img" / "map_img.png"
DEST = ROOT / "docs" / "assets" / "img" / "mappa.jpg"

L = 1672   # dimensioni dell'illustrazione, che sono anche il viewBox
A = 941

CREMA = "#fdf7e7"

# (slug del racconto, nome sulla mappa, x, y in frazione dell'immagine, posizione etichetta)
LUOGHI = [
    # in cielo: non hanno un oggetto disegnato, e non serve
    ("i-piccoli-riti-del-bosco",                   "Il Ramo delle Stelle",     0.300, 0.090, "sotto"),
    ("il-pipistrello-che-leggeva-il-buio",         "Il Cielo di Pìndaro",      0.850, 0.100, "sotto"),

    # colline e bosco alto
    ("la-volpe-che-cuciva-le-nuvole",              "La Collina delle Nuvole",  0.130, 0.190, "sotto"),
    ("l-albero-dei-campanellini",                  "L'Albero dei Campanellini", 0.675, 0.275, "sotto"),
    ("il-vento-smemorato",                         "Le Fronde del Vento",      0.200, 0.355, "sotto"),
    ("il-carillon-del-tempo",                      "La Quercia di Petronio",   0.378, 0.360, "sopra"),
    ("la-civetta-che-non-voleva-perdersi-nulla",   "Il Ramo di Celestina",     0.825, 0.345, "sotto"),
    ("l-ultima-voce-del-bosco",                    "La Grande Radura",         0.485, 0.400, "sotto"),

    # il bosco basso
    ("la-sorgente-disuguale",                      "La Sorgente",              0.070, 0.490, "sotto"),
    ("la-biblioteca-delle-foglie",                 "Il Castagno Cavo",         0.280, 0.450, "sotto"),
    ("la-cicala-che-collezionava-echi",            "Le Rocce dell'Eco",        0.755, 0.470, "sotto"),
    ("il-corvo-che-ingigantiva-le-sue-gesta",      "La Radura dei Racconti",   0.880, 0.435, "sotto"),
    ("il-prato-in-finito",                         "Il Prato (In)finito",      0.780, 0.680, "sotto"),

    # l'acqua
    ("la-libellula-che-non-trovava-il-suo-perche", "Il Volo di Livia",         0.432, 0.620, "sopra"),
    ("lo-stagno-degli-specchi",                    "Lo Stagno degli Specchi",  0.500, 0.665, "sotto"),
    ("la-nascita-dello-stagno",                    "Il Salice e il Sasso",     0.600, 0.598, "sopra"),
    ("il-fiore-di-tilda",                          "Il Fiore di Tilda",        0.605, 0.716, "sotto"),
    ("un-insolita-amicizia",                       "La Tana di Brumildo",      0.885, 0.612, "sopra"),
    ("premessa",                                   "Il Sentiero d'Ingresso",   0.200, 0.700, "sopra"),

    # sottoterra, una camera illuminata per ciascuno
    ("i-cunicoli-di-tamarinda",                    "I Cunicoli di Tamarinda",  0.155, 0.876, "sopra"),
    ("la-formica-infaticabile",                    "Il Formicaio",             0.455, 0.855, "sopra"),
    ("il-tasso-che-collezionava-ombre",            "La Tana di Tenebrio",      0.635, 0.886, "sopra"),
    ("il-serpente-che-ascoltava-i-colori",         "Le Radici Profonde",       0.845, 0.886, "sopra"),
]

SCARTO = 40   # quanto sta l'etichetta sopra o sotto il punto, in unità del viewBox


def prepara_immagine():
    """Da PNG pesante a JPEG per il web, alla stessa dimensione."""
    from PIL import Image

    if not SORGENTE.exists():
        return None
    im = Image.open(SORGENTE).convert("RGB")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    im.save(DEST, quality=86, optimize=True, progressive=True)
    return im.size, DEST.stat().st_size


def svg_mappa(sezioni_per_slug, prefisso=""):
    """Lo strato navigabile: l'illustrazione e sopra i luoghi."""
    o = [f'<svg class="mappa" viewBox="0 0 {L} {A}" role="img" '
         f'aria-labelledby="mappa-titolo" xmlns="http://www.w3.org/2000/svg">',
         '<title id="mappa-titolo">Mappa del Bosco delle Cento Voci: '
         'i luoghi in cui succedono i racconti</title>',
         f'<image href="{prefisso}assets/img/mappa.jpg" x="0" y="0" '
         f'width="{L}" height="{A}"/>',
         '<g class="luoghi">']

    for slug, nome, fx, fy, dove in LUOGHI:
        sez = sezioni_per_slug.get(slug)
        if not sez:
            continue
        x = round(fx * L)
        y = round(fy * A)
        dy = SCARTO if dove == "sotto" else -SCARTO + 10
        o.append(
            f'<a href="{prefisso}racconti/{sez["file"]}" class="luogo">'
            f'<title>{nome} — {sez["titolo"]}</title>'
            f'<circle class="tocco" cx="{x}" cy="{y}" r="34" fill="transparent"/>'
            f'<circle class="alone" cx="{x}" cy="{y}" r="16"/>'
            f'<circle class="punto" cx="{x}" cy="{y}" r="7.5"/>'
            f'<text class="etichetta" x="{x}" y="{y + dy}" text-anchor="middle">{nome}</text>'
            f'</a>')

    o.append("</g>")
    o.append("</svg>")
    return "\n".join(o)


def provino():
    """Le etichette disegnate sull'illustrazione vera, per controllare
    che siano leggibili, non accavallate e dentro i bordi."""
    from PIL import Image, ImageDraw, ImageFont

    im = Image.open(SORGENTE).convert("RGB")
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("georgiai.ttf", 26)
    except OSError:
        try:
            font = ImageFont.truetype("georgia.ttf", 26)
        except OSError:
            font = ImageFont.load_default()

    riquadri = []
    for _slug, nome, fx, fy, dove in LUOGHI:
        x, y = fx * im.width, fy * im.height
        d.ellipse([x - 16, y - 16, x + 16, y + 16], outline=CREMA, width=3)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill="#e3b552")
        dy = SCARTO if dove == "sotto" else -SCARTO + 10
        ancora = "ma" if dove == "sotto" else "md"
        cassa = d.textbbox((x, y + dy), nome, font=font, anchor=ancora)
        riquadri.append((nome, cassa))
        d.text((x, y + dy), nome, font=font, fill=CREMA, anchor=ancora,
               stroke_width=4, stroke_fill=(10, 34, 22))

    problemi = []
    for nome, c in riquadri:
        if c[0] < 4 or c[2] > im.width - 4 or c[1] < 2 or c[3] > im.height - 2:
            problemi.append(f"{nome}: esce dai bordi")
            d.rectangle(c, outline=(255, 140, 0), width=3)
    for i in range(len(riquadri)):
        for j in range(i + 1, len(riquadri)):
            (n1, a), (n2, b) = riquadri[i], riquadri[j]
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                problemi.append(f"{n1} × {n2}: etichette accavallate")
                d.rectangle(a, outline=(255, 0, 60), width=3)
                d.rectangle(b, outline=(255, 0, 60), width=3)

    p = ROOT / "tools" / "provino-mappa.jpg"
    im.save(p, quality=90)
    return p, problemi


def main():
    esito = prepara_immagine()
    if not esito:
        print(f"  ⚠ manca {SORGENTE.relative_to(ROOT)}: la mappa non è stata aggiornata")
        return
    (w, h), peso = esito
    print(f"mappa    -> docs/assets/img/mappa.jpg  ({w}×{h}, {peso // 1024} KB)")
    if (w, h) != (L, A):
        print(f"  ⚠ l'illustrazione è {w}×{h} ma il viewBox è {L}×{A}: "
              f"aggiorna L e A in tools/mappa.py")
    p, problemi = provino()
    print(f"provino  -> {p}")
    print(f"{len(LUOGHI)} luoghi")
    for x in problemi:
        print("  ✗ " + x)
    if not problemi:
        print("  ✓ etichette tutte leggibili, dentro i bordi e senza sovrapposizioni")


if __name__ == "__main__":
    main()
