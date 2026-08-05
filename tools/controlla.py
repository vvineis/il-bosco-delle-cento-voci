# -*- coding: utf-8 -*-
"""
Controlla il sito generato: link interni rotti, immagini mancanti,
pagine senza titolo o senza testo alternativo sulle immagini.

Uso:  python tools/controlla.py
"""
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path
from urllib.parse import unquote, urldefrag

ROOT = Path(__file__).resolve().parent.parent
SITO = ROOT / "docs"

RIF = re.compile(r'(?:href|src)="([^"]+)"')
IMG = re.compile(r"<img\b[^>]*>", re.I)
TITOLO = re.compile(r"<title>(.*?)</title>", re.S)
ANCORA = re.compile(r'id="([^"]+)"')


def main():
    pagine = sorted(SITO.rglob("*.html"))
    problemi = []
    ancore = {}

    for p in pagine:
        ancore[p] = set(ANCORA.findall(p.read_text(encoding="utf-8")))

    for p in pagine:
        testo = p.read_text(encoding="utf-8")
        rel = p.relative_to(SITO).as_posix()

        if not TITOLO.search(testo):
            problemi.append(f"{rel}: manca il <title>")

        for tag in IMG.findall(testo):
            if 'alt="' not in tag:
                problemi.append(f"{rel}: <img> senza alt -> {tag[:70]}")

        for rif in RIF.findall(testo):
            if rif.startswith(("http://", "https://", "mailto:", "data:", "#")):
                continue
            percorso, frammento = urldefrag(unquote(rif))
            percorso = percorso.split("?", 1)[0]   # la versione anti-cache non è parte del percorso
            bersaglio = (p.parent / percorso).resolve()
            if not bersaglio.exists():
                problemi.append(f"{rel}: riferimento rotto -> {rif}")
            elif frammento and bersaglio.suffix == ".html":
                if frammento not in ancore.get(bersaglio, set()):
                    problemi.append(f"{rel}: ancora inesistente -> {rif}")

    # l'indirizzo pubblico va impostato prima di pubblicare, o i motori di ricerca
    # seguono link che non esistono
    indice = SITO / "index.html"
    segnaposto = indice.exists() and "ESEMPIO.github.io" in indice.read_text(encoding="utf-8")

    print(f"{len(pagine)} pagine controllate")
    if segnaposto:
        print("  ⚠ SITO_URL in tools/costruisci.py è ancora il segnaposto:")
        print("    va messo l'indirizzo vero prima di pubblicare (canonical, sitemap, robots)")
    if problemi:
        for x in problemi:
            print("  ✗ " + x)
        sys.exit(1)
    print("  ✓ nessun link rotto, nessuna immagine mancante, tutte con alt")


if __name__ == "__main__":
    main()
