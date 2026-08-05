# -*- coding: utf-8 -*-
"""
Il libro impaginato in PDF, formato A4.

Ordine: copertina, frontespizio, nota sulla licenza, indice, mappa (a pagina
orizzontale), poi la premessa e i ventidue racconti, ognuno da pagina nuova,
e la Filastrocca del Bosco a chiudere.

I caratteri sono i Times standard del PDF: non vengono incorporati, quindi il
file resta leggero e non ci sono font di terzi da ridistribuire.

Uso:  python tools/libro_pdf.py
"""
import html
import json
import sys

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

try:
    # « invariant » toglie dal PDF la data di creazione e l'identificativo
    # casuale: due ricostruzioni danno lo stesso file, byte per byte
    from reportlab import rl_config
    rl_config.invariant = 1

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (BaseDocTemplate, Frame, Image, NextPageTemplate,
                                    PageBreak, PageTemplate, Paragraph, Spacer)
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError:
    print("Per generare il PDF serve reportlab, che qui non c'è. Installalo con:")
    print()
    print("    python -m pip install reportlab")
    print()
    print("Il resto del sito si costruisce lo stesso: il PDF verrà semplicemente saltato.")
    sys.exit(2)   # 2 = manca una libreria, non è un errore del progetto

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "docs" / "data" / "racconti.json"
COPERTINA = ROOT / "docs" / "assets" / "img" / "copertina.jpg"
MAPPA = ROOT / "docs" / "assets" / "img" / "mappa.jpg"
DEST = ROOT / "docs" / "download" / "Il-Bosco-delle-Cento-Voci.pdf"

TITOLO = "Il Bosco delle Cento Voci"
AUTRICE = "Vittoria Vineis"
EMAIL = "vineisvittoria@gmail.com"
LICENZA = "https://creativecommons.org/licenses/by-nc-nd/4.0/deed.it"

VERDE = colors.HexColor("#12402c")
VERDE_NOTTE = colors.HexColor("#0c2e20")
ORO = colors.HexColor("#a87f2e")
INCHIOSTRO = colors.HexColor("#1d2a22")
TENUE = colors.HexColor("#5b6b60")

MARGINE = 24 * mm
MARGINE_ALTO = 22 * mm


# ------------------------------------------------------------------- stili ---

def stili():
    s = {}
    s["corpo"] = ParagraphStyle(
        "corpo", fontName="Times-Roman", fontSize=11.5, leading=16.4,
        alignment=TA_JUSTIFY, textColor=INCHIOSTRO,
        firstLineIndent=5 * mm, spaceAfter=0)
    s["corpo-primo"] = ParagraphStyle(
        "corpo-primo", parent=s["corpo"], firstLineIndent=0, spaceBefore=2 * mm)
    s["titolo-racconto"] = ParagraphStyle(
        "titolo-racconto", fontName="Times-Bold", fontSize=19, leading=23,
        alignment=TA_CENTER, textColor=VERDE, spaceAfter=9 * mm)
    s["occhiello"] = ParagraphStyle(
        "occhiello", fontName="Times-Italic", fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=ORO, spaceAfter=2.5 * mm)
    s["versi"] = ParagraphStyle(
        "versi", fontName="Times-Italic", fontSize=11.5, leading=17,
        alignment=TA_CENTER, textColor=VERDE, spaceBefore=6 * mm, spaceAfter=6 * mm)
    s["firma"] = ParagraphStyle(
        "firma", fontName="Times-Roman", fontSize=9, leading=12,
        alignment=TA_CENTER, textColor=TENUE, spaceBefore=5 * mm)
    s["titolone"] = ParagraphStyle(
        "titolone", fontName="Times-Bold", fontSize=30, leading=36,
        alignment=TA_CENTER, textColor=VERDE)
    s["sottotitolone"] = ParagraphStyle(
        "sottotitolone", fontName="Times-Italic", fontSize=15, leading=20,
        alignment=TA_CENTER, textColor=ORO, spaceBefore=6 * mm)
    s["colophon"] = ParagraphStyle(
        "colophon", fontName="Times-Roman", fontSize=9.5, leading=14,
        alignment=TA_CENTER, textColor=TENUE, spaceAfter=3 * mm)
    s["didascalia"] = ParagraphStyle(
        "didascalia", fontName="Times-Italic", fontSize=9.5, leading=13,
        alignment=TA_CENTER, textColor=TENUE, spaceBefore=3 * mm)
    s["voce-indice"] = ParagraphStyle(
        "voce-indice", fontName="Times-Roman", fontSize=11.5, leading=19,
        textColor=INCHIOSTRO)
    s["voce-indice-premessa"] = ParagraphStyle(
        "voce-indice-premessa", parent=s["voce-indice"], fontName="Times-Italic")
    return s


def e(testo):
    """Testo pronto per reportlab, con le interruzioni di riga del manoscritto."""
    return html.escape(testo, quote=False).replace("\n", "<br/>")


# --------------------------------------------------------------- documento ---

class Libro(BaseDocTemplate):
    """Tiene il conto delle pagine per costruire l'indice."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.voci = []

    def afterFlowable(self, flowable):
        if getattr(flowable, "_voce_indice", None):
            livello, testo = flowable._voce_indice
            self.notify("TOCEntry", (livello, testo, self.page))


def numero_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Roman", 9)
    canvas.setFillColor(TENUE)
    canvas.drawCentredString(A4[0] / 2, 13 * mm, str(canvas.getPageNumber()))
    canvas.restoreState()


def pagina_scura(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(VERDE_NOTTE)
    canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    canvas.restoreState()


def pagina_scura_orizzontale(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(VERDE_NOTTE)
    canvas.rect(0, 0, A4[1], A4[0], stroke=0, fill=1)
    canvas.restoreState()


def immagine_adattata(percorso, larghezza_max, altezza_max):
    from PIL import Image as PILImage
    with PILImage.open(percorso) as im:
        w, h = im.size
    scala = min(larghezza_max / w, altezza_max / h)
    return Image(str(percorso), width=w * scala, height=h * scala)


# ---------------------------------------------------------------- contenuto ---

def costruisci():
    d = json.loads(DATI.read_text(encoding="utf-8"))
    st = stili()
    DEST.parent.mkdir(parents=True, exist_ok=True)

    doc = Libro(str(DEST), pagesize=A4,
                title=TITOLO, author=AUTRICE, subject="Favole",
                leftMargin=MARGINE, rightMargin=MARGINE,
                topMargin=MARGINE_ALTO, bottomMargin=MARGINE_ALTO)

    utile_l = A4[0] - 2 * MARGINE
    utile_a = A4[1] - 2 * MARGINE_ALTO
    oriz_l = A4[1] - 2 * MARGINE
    oriz_a = A4[0] - 2 * MARGINE

    doc.addPageTemplates([
        # i riquadri delle immagini senza imbottitura, o l'immagine non ci sta per un soffio
        PageTemplate(id="copertina", pagesize=A4, onPage=pagina_scura,
                     frames=[Frame(14 * mm, 14 * mm, A4[0] - 28 * mm, A4[1] - 28 * mm,
                                   id="cop", leftPadding=0, rightPadding=0,
                                   topPadding=0, bottomPadding=0)]),
        PageTemplate(id="liscia", pagesize=A4,
                     frames=[Frame(MARGINE, MARGINE_ALTO, utile_l, utile_a, id="lis")]),
        PageTemplate(id="mappa", pagesize=landscape(A4), onPage=pagina_scura_orizzontale,
                     frames=[Frame(MARGINE, MARGINE, oriz_l, oriz_a, id="map",
                                   leftPadding=0, rightPadding=0,
                                   topPadding=0, bottomPadding=0)]),
        PageTemplate(id="corpo", pagesize=A4, onPage=numero_pagina,
                     frames=[Frame(MARGINE, MARGINE_ALTO, utile_l, utile_a, id="cor")]),
    ])

    f = []

    # --- copertina ---------------------------------------------------------
    # il cambio di modello va dopo l'immagine: se sta prima, reportlab lo applica
    # già alla prima pagina e la copertina finisce nel riquadro sbagliato
    f.append(immagine_adattata(COPERTINA, A4[0] - 30 * mm, A4[1] - 30 * mm))
    f.append(NextPageTemplate("liscia"))
    f.append(PageBreak())

    # --- frontespizio ------------------------------------------------------
    f.append(Spacer(1, 55 * mm))
    f.append(Paragraph(TITOLO, st["titolone"]))
    f.append(Paragraph(AUTRICE, st["sottotitolone"]))
    f.append(PageBreak())

    # --- colophon ----------------------------------------------------------
    f.append(Spacer(1, 105 * mm))
    f.append(Paragraph(f"{TITOLO}<br/>© {AUTRICE}", st["colophon"]))
    f.append(Paragraph(
        "Quest'opera è concessa in licenza con Creative Commons<br/>"
        "Attribuzione - Non commerciale - Non opere derivate 4.0 Internazionale<br/>"
        f"{LICENZA}", st["colophon"]))
    f.append(Paragraph(
        "Si può leggere, stampare, fotocopiare e condividere liberamente,<br/>"
        "citando l'autrice. Non si può vendere né modificare.", st["colophon"]))
    f.append(Paragraph(
        "La poesia di Roberto Juarroz citata in «Il fiore di Tilda» è opera di terzi<br/>"
        "e non è coperta da questa licenza. La copertina e l'illustrazione della mappa<br/>"
        "sono immagini generate con l'intelligenza artificiale, provvisorie,<br/>"
        "in attesa di illustrazioni realizzate da una persona.", st["colophon"]))
    f.append(Paragraph(EMAIL, st["colophon"]))
    f.append(PageBreak())

    # --- indice ------------------------------------------------------------
    f.append(Paragraph("Indice", st["titolo-racconto"]))
    indice = TableOfContents()
    indice.levelStyles = [st["voce-indice"], st["voce-indice-premessa"]]
    indice.dotsMinLevel = 0
    f.append(indice)
    f.append(NextPageTemplate("mappa"))
    f.append(PageBreak())

    # --- la mappa, su pagina orizzontale -----------------------------------
    f.append(immagine_adattata(MAPPA, oriz_l, oriz_a - 12 * mm))
    f.append(Paragraph("La mappa del Bosco", st["didascalia"]))
    f.append(NextPageTemplate("corpo"))
    f.append(PageBreak())

    # --- premessa e racconti, ognuno da pagina nuova ------------------------
    for i, sez in enumerate(d["sezioni"]):
        if sez["numero"]:
            f.append(Paragraph(f"Racconto {sez['numero']}", st["occhiello"]))
        titolo = Paragraph(sez["titolo"], st["titolo-racconto"])
        titolo._voce_indice = (0 if sez["numero"] else 1, sez["titolo"])
        f.append(titolo)

        for k, testo in enumerate(sez["paragrafi"]):
            f.append(Paragraph(e(testo), st["corpo-primo" if k == 0 else "corpo"]))

        if sez["versi"]:
            versi = sez["versi"]
            # nell'ultimo racconto i versi sono la filastrocca: pagina propria
            if sez["slug"] == "l-ultima-voce-del-bosco":
                f.append(PageBreak())
                f.append(Spacer(1, 18 * mm))
                fila = Paragraph("Filastrocca del Bosco", st["titolo-racconto"])
                fila._voce_indice = (1, "Filastrocca del Bosco")
                f.append(fila)
            for blocco in versi:
                f.append(Paragraph(e(blocco), st["versi"]))

        if i < len(d["sezioni"]) - 1:
            f.append(PageBreak())

    doc.multiBuild(f)
    return DEST


def main():
    percorso = costruisci()
    peso = percorso.stat().st_size
    try:
        import fitz
        pagine = fitz.open(percorso).page_count
        print(f"PDF -> {percorso.relative_to(ROOT)}  ({pagine} pagine, {peso // 1024} KB)")
    except ImportError:
        print(f"PDF -> {percorso.relative_to(ROOT)}  ({peso // 1024} KB)")


if __name__ == "__main__":
    main()
