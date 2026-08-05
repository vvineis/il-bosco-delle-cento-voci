# -*- coding: utf-8 -*-
"""
Ritaglia dalle immagini di img/ i pezzi usati come decorazione del sito:
 - medaglioni tondi per la pagina "Gli abitanti"

Sono l'unico uso delle immagini generate: nessuna banda, nessuno sfondo.

Le immagini originali NON vengono usate come illustrazioni dei racconti.

Uso:  python tools/ritagli.py           genera in docs/assets/img/
      python tools/ritagli.py --provino genera anche un provino di controllo
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
SORGENTI = ROOT / "img"
DEST = ROOT / "docs" / "assets" / "img"
MEDAGLIONI = DEST / "abitanti"

LATO_MEDAGLIONE = 320  # px, il doppio della dimensione massima a schermo

# nome, file, centro x (0-1), centro y (0-1), lato del ritaglio (frazione della larghezza)
RITAGLI = [
    ("tilda",       "tilda.png",            0.489, 0.641, 0.62),
    ("velia",       "velia2.png",           0.660, 0.520, 0.40),
    ("rubino",      "ricciolepregede.png",  0.356, 0.719, 0.32),
    ("lola",        "ricciolepregede.png",  0.704, 0.576, 0.36),
    ("gedeone",     "ricciolepregede.png",  0.224, 0.116, 0.22),
    ("celestina",   "civett.png",           0.300, 0.410, 0.34),
    ("petronio",    "scoiattolo.png",       0.185, 0.205, 0.17),
    ("savino",      "scoiattolo.png",       0.459, 0.492, 0.46),
    ("curzio",      "curzio.png",           0.280, 0.430, 0.32),
    ("tenebrio",    "tasso.png",            0.597, 0.623, 0.46),
    ("lucia",       "tasso tenebrio.png",   0.807, 0.792, 0.15),
    ("tamarinda",   "talpa2.png",           0.502, 0.648, 0.26),
    ("romualdo",    "romo.png",             0.179, 0.244, 0.30),
    ("prospero",    "romo.png",             0.700, 0.170, 0.22),
    ("carisio",     "cervoo.png",           0.670, 0.210, 0.30),
    ("clizia",      "clizia_new.png",       0.499, 0.497, 0.440),
    ("livia",       "livia.png",            0.548, 0.337, 0.40),
    ("pindaro",     "pipistrello.png",      0.468, 0.183, 0.36),
    ("fiammetta",   "fiametta2.png",        0.484, 0.632, 0.36),
    ("brumildo",    "orsorondine.png",      0.320, 0.513, 0.40),
    ("raminga",     "orsorondine.png",      0.420, 0.239, 0.20),
    ("sinestesio",  "sinestesio.png",       0.778, 0.566, 0.28),
    ("lara",        "lontra castoro.png",   0.636, 0.440, 0.36),
    ("callisto",    "lontra castoro.png",   0.340, 0.453, 0.40),
    ("vento",       "vento2.png",           0.500, 0.320, 0.42),
]



def apri(nome):
    return Image.open(SORGENTI / nome).convert("RGB")


def ritaglio_quadrato(im, cx, cy, lato_frazione):
    lato = int(im.width * lato_frazione)
    lato = min(lato, im.width, im.height)
    x = int(im.width * cx - lato / 2)
    y = int(im.height * cy - lato / 2)
    x = max(0, min(x, im.width - lato))
    y = max(0, min(y, im.height - lato))
    return im.crop((x, y, x + lato, y + lato))


def maschera_tonda(lato):
    grande = lato * 4
    m = Image.new("L", (grande, grande), 0)
    ImageDraw.Draw(m).ellipse((0, 0, grande - 1, grande - 1), fill=255)
    return m.resize((lato, lato), Image.LANCZOS)


# ritagli troppo scuri da schiarire un po'
SCHIARISCI = {"petronio": 1.32, "tenebrio": 1.15, "pindaro": 1.25}

# ritagli poco leggibili da rinforzare nel contrasto
CONTRASTO = {"petronio": 1.18, "tamarinda": 1.15, "vento": 1.15}


def genera_medaglioni():
    """Rifà i medaglioni dalle immagini di partenza.

    Se una immagine di partenza non c'è — per esempio perché img/ non è stata
    caricata su GitHub — il medaglione già pronto in docs/ va benissimo così:
    si tiene quello e si tira avanti.
    """
    MEDAGLIONI.mkdir(parents=True, exist_ok=True)
    fatti, tenuti, persi = [], [], []

    for nome, file, cx, cy, lato in RITAGLI:
        if not (SORGENTI / file).exists():
            (tenuti if (MEDAGLIONI / f"{nome}.png").exists() else persi).append(nome)
            continue
        im = ritaglio_quadrato(apri(file), cx, cy, lato)
        # non si ingrandisce oltre un quarto: meglio un medaglione più piccolo che sfocato
        finale = min(LATO_MEDAGLIONE, max(216, int(im.width * 1.25)))
        im = im.resize((finale, finale), Image.LANCZOS)
        if nome in SCHIARISCI:
            im = ImageEnhance.Brightness(im).enhance(SCHIARISCI[nome])
        if nome in CONTRASTO:
            im = ImageEnhance.Contrast(im).enhance(CONTRASTO[nome])
        fuori = Image.new("RGBA", im.size, (0, 0, 0, 0))
        fuori.paste(im, (0, 0), maschera_tonda(im.width))
        fuori.save(MEDAGLIONI / f"{nome}.png", optimize=True)
        fatti.append(nome)

    return fatti, tenuti, persi


def genera_autrice():
    """Ritaglio tondo della foto dell'autrice, stesso trattamento dei personaggi."""
    origine = ROOT / "vitto_img.jpeg"
    if not origine.exists():
        return "già pronto" if (DEST / "autrice.png").exists() else None
    im = Image.open(origine).convert("RGB")
    im = ritaglio_quadrato(im, 0.44, 0.33, 0.82)
    lato = 480
    im = im.resize((lato, lato), Image.LANCZOS)
    maschera = maschera_tonda(lato)
    fuori = Image.new("RGBA", im.size, (0, 0, 0, 0))
    fuori.paste(im, (0, 0), maschera)
    fuori.save(DEST / "autrice.png", optimize=True)
    return "autrice.png"


def provino(nomi_medaglioni):
    import math
    C = 6
    CELL = 180
    R = math.ceil(len(nomi_medaglioni) / C)
    sheet = Image.new("RGB", (C * CELL, R * (CELL + 22)), (244, 232, 205))
    d = ImageDraw.Draw(sheet)
    for i, nome in enumerate(nomi_medaglioni):
        im = Image.open(MEDAGLIONI / f"{nome}.png").convert("RGBA")
        im.thumbnail((CELL - 12, CELL - 12), Image.LANCZOS)
        x = (i % C) * CELL
        y = (i // C) * (CELL + 22)
        sheet.paste(im, (x + 6, y + 6), im)
        d.text((x + 8, y + CELL + 4), nome, fill=(20, 20, 20))
    p = ROOT / "tools" / "provino-medaglioni.jpg"
    sheet.save(p, quality=88)
    return p


def main():
    if not SORGENTI.exists():
        print(f"La cartella {SORGENTI.name}/ non c'è: le immagini di partenza non sono")
        print("su questo computer (per esempio perché non vengono caricate su GitHub).")

    fatti, tenuti, persi = genera_medaglioni()
    autrice = genera_autrice()

    if fatti:
        print(f"{len(fatti)} medaglioni rifatti  -> docs/assets/img/abitanti/")
    if tenuti:
        print(f"{len(tenuti)} medaglioni tenuti come sono: manca l'immagine di partenza,")
        print("  ma quelli già pronti in docs/ vanno benissimo.")
    if autrice:
        print(f"autrice      -> {autrice}")
    else:
        print("  ⚠ manca sia vitto_img.jpeg sia il ritratto già pronto")

    if persi:
        print()
        print("  ✗ questi non ci sono né come immagine di partenza né come ritaglio:")
        print("    " + ", ".join(persi))
        print("    Rimetti la cartella img/ al suo posto e rilancia.")
        sys.exit(2)

    if "--provino" in sys.argv:
        print(f"provino      -> {provino(fatti + tenuti)}")


if __name__ == "__main__":
    main()
