# -*- coding: utf-8 -*-
"""
Gli Spunti di lettura in PDF, formato A4: il fascicolo da stampare e portarsi
in classe. Per ogni racconto il tema, le tre domande e l'attività.

Uso:  python tools/spunti_pdf.py
"""
import html
import json
import sys

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

try:
    from reportlab import rl_config
    rl_config.invariant = 1   # due ricostruzioni danno lo stesso file

    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (KeepTogether, PageBreak, Paragraph,
                                    SimpleDocTemplate, Spacer)
except ImportError:
    print("Per generare il PDF degli spunti serve reportlab. Installalo con:")
    print()
    print("    python -m pip install reportlab")
    print()
    print("Il resto del sito si costruisce lo stesso: il fascicolo verrà saltato.")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "docs" / "data" / "racconti.json"
DOMANDE = ROOT / "docs" / "data" / "domande.json"
DEST = ROOT / "docs" / "download" / "Spunti-di-lettura.pdf"

TITOLO = "Il Bosco delle Cento Voci"
AUTRICE = "Vittoria Vineis"
SITO = "vvineis.github.io/il-bosco-delle-cento-voci"

VERDE = colors.HexColor("#12402c")
ORO = colors.HexColor("#a87f2e")
VOLPE = colors.HexColor("#b8551f")
INCHIOSTRO = colors.HexColor("#1d2a22")
TENUE = colors.HexColor("#5b6b60")

MARGINE = 22 * mm


def e(t):
    return html.escape(t, quote=False)


def stili():
    s = {}
    s["titolone"] = ParagraphStyle("t", fontName="Times-Bold", fontSize=24, leading=29,
                                   alignment=TA_CENTER, textColor=VERDE)
    s["sottotitolone"] = ParagraphStyle("st", fontName="Times-Italic", fontSize=12.5,
                                        leading=17, alignment=TA_CENTER, textColor=ORO,
                                        spaceBefore=4 * mm, spaceAfter=8 * mm)
    s["intro"] = ParagraphStyle("i", fontName="Times-Roman", fontSize=11, leading=15.5,
                                textColor=INCHIOSTRO, spaceAfter=3.5 * mm)
    s["occhiello"] = ParagraphStyle("o", fontName="Times-Italic", fontSize=9,
                                    leading=11, textColor=ORO)
    s["titolo"] = ParagraphStyle("ti", fontName="Times-Bold", fontSize=13.5, leading=17,
                                 textColor=VERDE, spaceAfter=1.5 * mm)
    s["tema"] = ParagraphStyle("te", fontName="Times-Italic", fontSize=10, leading=13.5,
                               textColor=TENUE, spaceAfter=2.5 * mm)
    s["avvertenza"] = ParagraphStyle("av", fontName="Times-Italic", fontSize=9.5,
                                     leading=13, textColor=VOLPE, leftIndent=4 * mm,
                                     spaceAfter=2.5 * mm)
    s["domanda"] = ParagraphStyle("d", fontName="Times-Roman", fontSize=10.5, leading=14.5,
                                  textColor=INCHIOSTRO, leftIndent=6 * mm,
                                  firstLineIndent=-6 * mm, spaceAfter=1.2 * mm)
    s["attivita"] = ParagraphStyle("a", fontName="Times-Roman", fontSize=10, leading=14,
                                   textColor=INCHIOSTRO, leftIndent=4 * mm,
                                   spaceBefore=2 * mm)
    s["pie"] = ParagraphStyle("p", fontName="Times-Italic", fontSize=8.5, leading=11,
                              alignment=TA_CENTER, textColor=TENUE)
    return s


def pieno_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont("Times-Italic", 8.5)
    canvas.setFillColor(TENUE)
    canvas.drawString(MARGINE, 12 * mm, f"{TITOLO} — Spunti di lettura")
    canvas.drawRightString(A4[0] - MARGINE, 12 * mm, str(canvas.getPageNumber()))
    canvas.setStrokeColor(colors.HexColor("#d8cfae"))
    canvas.line(MARGINE, 16 * mm, A4[0] - MARGINE, 16 * mm)
    canvas.restoreState()


def costruisci():
    d = json.loads(DATI.read_text(encoding="utf-8"))
    domande = {k: v for k, v in json.loads(DOMANDE.read_text(encoding="utf-8")).items()
               if not k.startswith("_")}
    st = stili()
    DEST.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(DEST), pagesize=A4,
                            title=f"{TITOLO} — Spunti di lettura", author=AUTRICE,
                            leftMargin=MARGINE, rightMargin=MARGINE,
                            topMargin=MARGINE, bottomMargin=MARGINE)
    f = []

    # --- apertura -----------------------------------------------------------
    f.append(Spacer(1, 12 * mm))
    f.append(Paragraph("Spunti di lettura", st["titolone"]))
    f.append(Paragraph(f"{TITOLO} — {AUTRICE}", st["sottotitolone"]))
    f.append(Paragraph(
        "<b>Come usarli.</b> Le favole del Bosco non dichiarano mai la loro morale: la "
        "lasciano succedere. Le domande qui sotto servono a tenere aperta quella porta. "
        "Funzionano meglio <b>dopo</b> la lettura ad alta voce, senza fretta e senza "
        "risposte giuste da raggiungere.", st["intro"]))
    f.append(Paragraph(
        "Il libro si legge gratuitamente su "
        f"<b>{SITO}</b>, dove si trovano anche il PDF e l'EPUB da scaricare.", st["intro"]))
    f.append(Spacer(1, 6 * mm))

    # --- una scheda per racconto -------------------------------------------
    def scheda(numero, titolo, voce, tema=""):
        pezzi = []
        if numero:
            pezzi.append(Paragraph(f"Racconto {numero}", st["occhiello"]))
        pezzi.append(Paragraph(e(titolo), st["titolo"]))
        if tema:
            pezzi.append(Paragraph(e(tema), st["tema"]))
        if voce.get("avvertenza"):
            pezzi.append(Paragraph("◆ " + e(voce["avvertenza"]), st["avvertenza"]))
        for i, dom in enumerate(voce.get("domande", []), start=1):
            pezzi.append(Paragraph(f"<b>{i}.</b>&nbsp;&nbsp;{e(dom)}", st["domanda"]))
        if voce.get("attivita"):
            pezzi.append(Paragraph(
                f"<b>Da fare insieme.</b> {e(voce['attivita'])}", st["attivita"]))
        pezzi.append(Spacer(1, 7 * mm))
        # una scheda non si spezza mai fra due pagine
        return KeepTogether(pezzi)

    for sez in d["sezioni"]:
        voce = domande.get(sez["slug"])
        if voce:
            f.append(scheda(sez["numero"], sez["titolo"], voce, sez.get("tema", "")))

    fila = domande.get("filastrocca-del-bosco")
    if fila:
        f.append(scheda(None, "Filastrocca del Bosco", fila,
                        "I versi che chiudono il libro. Si leggono ad alta voce, tutti "
                        "insieme, e poi se ne scrive una propria."))

    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph(
        f"{TITOLO} © {AUTRICE} — Creative Commons BY-NC-ND 4.0.<br/>"
        "Questo fascicolo si può stampare e fotocopiare liberamente per uso didattico.",
        st["pie"]))

    doc.build(f, onFirstPage=pieno_pagina, onLaterPages=pieno_pagina)
    return DEST


def main():
    percorso = costruisci()
    peso = percorso.stat().st_size
    try:
        import fitz
        pagine = fitz.open(percorso).page_count
        print(f"spunti -> {percorso.relative_to(ROOT)}  ({pagine} pagine, {peso // 1024} KB)")
    except ImportError:
        print(f"spunti -> {percorso.relative_to(ROOT)}  ({peso // 1024} KB)")


if __name__ == "__main__":
    main()
