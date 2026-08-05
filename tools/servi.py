# -*- coding: utf-8 -*-
"""
Mette in piedi il sito in locale, su http://localhost:8765

A differenza di «python -m http.server», dice al browser di non conservare
nulla in memoria: così dopo ogni «python tools/tutto.py» basta ricaricare la
pagina per vedere le modifiche, senza Ctrl+F5 e senza dubbi.

Uso:  python tools/servi.py         (Ctrl+C per fermarlo)
      python tools/servi.py 9000    per usare un'altra porta
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SITO = ROOT / "docs"
PORTA = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class SenzaMemoria(SimpleHTTPRequestHandler):
    """Come il server standard, ma vieta al browser di tenere copie."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, formato, *args):
        # solo gli errori: le richieste andate a buon fine sono rumore
        if args and str(args[1]).startswith(("4", "5")):
            super().log_message(formato, *args)


def main():
    if not (SITO / "index.html").exists():
        print(f"Non trovo {SITO / 'index.html'}.")
        print("Costruisci prima il sito:  python tools/tutto.py")
        sys.exit(1)

    gestore = partial(SenzaMemoria, directory=str(SITO))
    server = ThreadingHTTPServer(("127.0.0.1", PORTA), gestore)

    print("─" * 60)
    print(f"  Il Bosco è in ascolto su  http://localhost:{PORTA}")
    print(f"  Sta servendo la cartella  {SITO}")
    print("  Niente cache: dopo ogni build basta ricaricare la pagina.")
    print("  Ctrl+C per fermare.")
    print("─" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFermato.")


if __name__ == "__main__":
    main()
