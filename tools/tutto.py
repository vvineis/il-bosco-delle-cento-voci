# -*- coding: utf-8 -*-
"""
Ricostruisce l'intero sito: testo dal manoscritto, ritagli delle immagini,
mappa, PDF ed EPUB, pagine HTML, controllo finale.

Uso:  python tools/tutto.py

Funziona da qualsiasi cartella, purché il percorso al file sia giusto.
Se un passo fallisce si ferma lì e lo dice a chiare lettere.
"""
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (script, obbligatorio?) — PDF ed EPUB sono un di più: se falliscono, il sito
# si costruisce lo stesso e alla fine viene detto che cosa manca.
PASSI = [
    ("estrai.py", True),
    ("ritagli.py", True),
    ("mappa.py", True),
    ("libro_pdf.py", False),
    ("libro_epub.py", False),
    ("spunti_pdf.py", False),
    ("costruisci.py", True),
    ("controlla.py", True),
]


def riga(testo=""):
    """Stampa subito: senza flush le intestazioni finirebbero dopo l'output
    dei sotto-processi, e non si capirebbe più quale passo ha parlato."""
    print(testo, flush=True)


def main():
    inizio = time.time()
    riga(f"Cartella del progetto: {ROOT}")

    saltati = []
    for numero, (passo, obbligatorio) in enumerate(PASSI, start=1):
        riga(f"\n── {numero}/{len(PASSI)}  {passo} " + "─" * max(0, 52 - len(passo)))
        esito = subprocess.run([sys.executable, str(ROOT / "tools" / passo)], cwd=ROOT)
        if esito.returncode == 0:
            continue
        if not obbligatorio:
            riga(f"  ⚠ {passo} saltato: il sito si costruisce lo stesso.")
            saltati.append(passo)
            continue
        riga("")
        riga("╳" * 66)
        riga(f"  {passo} SI È FERMATO CON UN ERRORE.")
        riga("  Il sito NON è stato aggiornato. L'errore è qui sopra:")
        riga("  di solito l'ultima riga dice che cosa non va e a che riga del file.")
        riga("╳" * 66)
        sys.exit(esito.returncode)

    indice = ROOT / "docs" / "index.html"
    quando = datetime.fromtimestamp(indice.stat().st_mtime).strftime("%H:%M:%S")
    pagine = len(list((ROOT / "docs").rglob("*.html")))

    riga("")
    riga("─" * 66)
    riga(f"  Fatto in {time.time() - inizio:.1f} secondi.")
    riga(f"  {pagine} pagine riscritte in docs/, l'ultima alle {quando}.")
    if saltati:
        riga(f"  Saltati: {', '.join(saltati)} — vedi il messaggio qui sopra.")
    riga("  Se nel browser vedi ancora la versione vecchia, ricarica")
    riga("  tenendo premuto Ctrl (Ctrl+F5 su Windows, Cmd+Shift+R su Mac).")
    riga("─" * 66)


if __name__ == "__main__":
    main()
