# -*- coding: utf-8 -*-
"""
Piccole cose che servono a più script.

La più importante è `data_fonti()`: dà la data dell'ultima modifica ai file
scritti a mano. Serve a rendere PDF, EPUB e sitemap sempre identici a sé stessi
finché non cambia davvero qualcosa. Senza, ogni ricostruzione produrrebbe file
diversi solo perché contengono l'ora in cui sono stati fatti — e in un
repository git quella differenza si accumulerebbe per sempre.
"""
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# i file da cui dipende davvero il contenuto del libro e del sito
FONTI = [
    ROOT / "Il_Bosco_delle_Cento_Voci_completo.docx",
    ROOT / "Il_Bosco_delle_Cento_Voci_SINOSSI.docx",
    ROOT / "Nota_bio.docx",
    ROOT / "docs" / "data" / "domande.json",
    ROOT / "docs" / "assets" / "css" / "stile.css",
]
FONTI += sorted((ROOT / "tools").glob("*.py"))


def data_fonti():
    """Il momento dell'ultima modifica a un file scritto a mano, in UTC."""
    momenti = [f.stat().st_mtime for f in FONTI if f.exists()]
    return datetime.fromtimestamp(max(momenti) if momenti else 0, tz=timezone.utc)
