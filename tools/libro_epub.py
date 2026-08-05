# -*- coding: utf-8 -*-
"""
Il libro in formato EPUB 3, per e-reader e app di lettura.

Scritto a mano: un EPUB è uno ZIP con dentro dei file XHTML e un paio di
manifesti, quindi non serve nessuna libreria esterna.

Ordine: copertina, frontespizio, licenza, mappa, premessa, i ventidue racconti
e la Filastrocca del Bosco.

Uso:  python tools/libro_epub.py
"""
import html
import json
import sys
import uuid
import zipfile

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

from comune import data_fonti

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "docs" / "data" / "racconti.json"
COPERTINA = ROOT / "docs" / "assets" / "img" / "copertina.jpg"
MAPPA = ROOT / "docs" / "assets" / "img" / "mappa.jpg"
DEST = ROOT / "docs" / "download" / "Il-Bosco-delle-Cento-Voci.epub"

TITOLO = "Il Bosco delle Cento Voci"
AUTRICE = "Vittoria Vineis"
EMAIL = "vineisvittoria@gmail.com"
LICENZA = "https://creativecommons.org/licenses/by-nc-nd/4.0/"

# identificativo stabile: lo stesso libro deve avere lo stesso id fra una
# versione e l'altra, altrimenti i lettori lo trattano come un libro diverso
IDENTIFICATIVO = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL,
                                              "bosco-delle-cento-voci-vineis"))

STILE = """@charset "utf-8";
body { font-family: serif; line-height: 1.55; margin: 0 5%; color: #1d2a22; }
h1 { font-size: 1.5em; text-align: center; margin: 1.2em 0 0.2em; font-weight: normal; }
h1.titolo-libro { font-size: 2em; margin-top: 3em; }
p.occhiello { text-align: center; font-style: italic; font-size: 0.85em;
              color: #8a6a24; margin: 0 0 1.4em; letter-spacing: 0.06em; }
p.autrice { text-align: center; font-style: italic; font-size: 1.15em; color: #8a6a24; }
p { text-align: justify; text-indent: 1.4em; margin: 0; }
p.primo { text-indent: 0; margin-top: 1.2em; }
p.versi { text-align: center; font-style: italic; text-indent: 0;
          margin: 1.2em 0; color: #14402c; }
p.nota { text-align: center; text-indent: 0; font-size: 0.85em; color: #5b6b60;
         margin: 0.6em 0; }
div.copertina { text-align: center; margin: 0; padding: 0; }
div.copertina img { max-width: 100%; max-height: 100%; }
figure { margin: 1.5em 0; text-align: center; }
figure img { max-width: 100%; }
figcaption { font-style: italic; font-size: 0.85em; color: #5b6b60; margin-top: 0.5em; }
nav ol { list-style: none; padding-left: 0; }
nav li { margin: 0.4em 0; }
"""


def e(testo):
    return html.escape(testo, quote=False)


def paragrafo(testo, classe=""):
    righe = "<br/>".join(e(r) for r in testo.split("\n"))
    c = f' class="{classe}"' if classe else ""
    return f"<p{c}>{righe}</p>"


def xhtml(titolo, corpo):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      lang="it" xml:lang="it">
<head>
  <meta charset="utf-8"/>
  <title>{e(titolo)}</title>
  <link rel="stylesheet" type="text/css" href="stile.css"/>
</head>
<body>
{corpo}
</body>
</html>
"""


def costruisci():
    d = json.loads(DATI.read_text(encoding="utf-8"))
    sezioni = d["sezioni"]
    DEST.parent.mkdir(parents=True, exist_ok=True)

    file = {}          # percorso dentro l'epub -> contenuto
    capitoli = []      # (nome file, titolo per l'indice)

    file["stile.css"] = STILE

    # --- copertina ---------------------------------------------------------
    file["copertina.xhtml"] = xhtml("Copertina", f"""<div class="copertina" epub:type="cover">
  <img src="img/copertina.jpg" alt="Copertina di {e(TITOLO)}"/>
</div>""")

    # --- frontespizio ------------------------------------------------------
    file["frontespizio.xhtml"] = xhtml(TITOLO, f"""<section epub:type="titlepage">
  <h1 class="titolo-libro">{e(TITOLO)}</h1>
  <p class="autrice">{e(AUTRICE)}</p>
</section>""")
    capitoli.append(("frontespizio.xhtml", TITOLO))

    # --- licenza -----------------------------------------------------------
    file["licenza.xhtml"] = xhtml("Licenza", f"""<section>
  <h1>Licenza</h1>
  <p class="nota">{e(TITOLO)} © {e(AUTRICE)}</p>
  <p class="nota">Quest'opera è concessa in licenza con Creative Commons
     Attribuzione - Non commerciale - Non opere derivate 4.0 Internazionale.<br/>
     <a href="{LICENZA}">{LICENZA}</a></p>
  <p class="nota">Si può leggere, stampare, fotocopiare e condividere liberamente,
     citando l'autrice. Non si può vendere né modificare.</p>
  <p class="nota">La poesia di Roberto Juarroz citata in «Il fiore di Tilda» è opera
     di terzi e non è coperta da questa licenza. La copertina e l'illustrazione della
     mappa sono immagini generate con l'intelligenza artificiale, provvisorie, in
     attesa di illustrazioni realizzate da una persona.</p>
  <p class="nota">{EMAIL}</p>
</section>""")
    capitoli.append(("licenza.xhtml", "Licenza"))

    # --- mappa -------------------------------------------------------------
    file["mappa.xhtml"] = xhtml("La mappa del Bosco", """<section>
  <h1>La mappa del Bosco</h1>
  <figure>
    <img src="img/mappa.jpg" alt="La mappa del Bosco delle Cento Voci: colline, il
         castagno cavo, la grande radura, lo stagno e, sotto il suolo, i cunicoli."/>
    <figcaption>Ogni racconto succede in un posto preciso.</figcaption>
  </figure>
</section>""")
    capitoli.append(("mappa.xhtml", "La mappa del Bosco"))

    # --- premessa e racconti ------------------------------------------------
    for i, sez in enumerate(sezioni, start=1):
        pezzi = []
        if sez["numero"]:
            pezzi.append(f'<p class="occhiello">Racconto {sez["numero"]}</p>')
        pezzi.append(f'<h1>{e(sez["titolo"])}</h1>')
        for k, testo in enumerate(sez["paragrafi"]):
            pezzi.append(paragrafo(testo, "primo" if k == 0 else ""))

        versi_a_parte = sez["slug"] == "l-ultima-voce-del-bosco"
        if sez["versi"] and not versi_a_parte:
            for blocco in sez["versi"]:
                pezzi.append(paragrafo(blocco, "versi"))

        nome = f"{i:02d}-{sez['slug']}.xhtml"
        file[nome] = xhtml(sez["titolo"], "<section>\n" + "\n".join(pezzi) + "\n</section>")
        capitoli.append((nome, sez["titolo"]))

        if versi_a_parte and sez["versi"]:
            versi = "\n".join(paragrafo(b, "versi") for b in sez["versi"])
            file["24-filastrocca.xhtml"] = xhtml(
                "Filastrocca del Bosco",
                f'<section>\n<h1>Filastrocca del Bosco</h1>\n{versi}\n</section>')
            capitoli.append(("24-filastrocca.xhtml", "Filastrocca del Bosco"))

    # --- indice di navigazione ----------------------------------------------
    voci = "\n".join(f'      <li><a href="{n}">{e(t)}</a></li>' for n, t in capitoli)
    file["nav.xhtml"] = xhtml("Indice", f"""<nav epub:type="toc" id="toc">
  <h1>Indice</h1>
  <ol>
{voci}
  </ol>
</nav>
<nav epub:type="landmarks" hidden="hidden">
  <ol>
    <li><a epub:type="cover" href="copertina.xhtml">Copertina</a></li>
    <li><a epub:type="bodymatter" href="{capitoli[3][0]}">Inizio del testo</a></li>
  </ol>
</nav>""")

    # indice in formato vecchio, per i lettori che non leggono l'EPUB 3
    punti = "\n".join(
        f'    <navPoint id="n{k}" playOrder="{k}">\n'
        f'      <navLabel><text>{e(t)}</text></navLabel>\n'
        f'      <content src="{n}"/>\n    </navPoint>'
        for k, (n, t) in enumerate(capitoli, start=1))
    file["toc.ncx"] = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head><meta name="dtb:uid" content="{IDENTIFICATIVO}"/></head>
  <docTitle><text>{e(TITOLO)}</text></docTitle>
  <navMap>
{punti}
  </navMap>
</ncx>
"""

    # --- manifesto ----------------------------------------------------------
    # la data è quella dell'ultima modifica alle fonti, non "adesso": così due
    # ricostruzioni di seguito danno lo stesso file, byte per byte
    quando = data_fonti()
    ora = quando.strftime("%Y-%m-%dT%H:%M:%SZ")
    risorse = [
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="css" href="stile.css" media-type="text/css"/>',
        '    <item id="cop-img" href="img/copertina.jpg" media-type="image/jpeg" properties="cover-image"/>',
        '    <item id="map-img" href="img/mappa.jpg" media-type="image/jpeg"/>',
        '    <item id="copertina" href="copertina.xhtml" media-type="application/xhtml+xml"/>',
    ]
    lettura = ['    <itemref idref="copertina"/>']
    for k, (n, _t) in enumerate(capitoli):
        ident = f"c{k}"
        risorse.append(f'    <item id="{ident}" href="{n}" media-type="application/xhtml+xml"/>')
        lettura.append(f'    <itemref idref="{ident}"/>')

    file["content.opf"] = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="pub-id"
         xml:lang="it">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="pub-id">{IDENTIFICATIVO}</dc:identifier>
    <dc:title>{e(TITOLO)}</dc:title>
    <dc:creator>{e(AUTRICE)}</dc:creator>
    <dc:language>it</dc:language>
    <dc:rights>© {e(AUTRICE)} — CC BY-NC-ND 4.0</dc:rights>
    <dc:description>Ventidue favole in cui ogni animale cerca la propria voce.</dc:description>
    <dc:subject>Favole</dc:subject>
    <dc:subject>Letteratura per ragazzi</dc:subject>
    <meta property="dcterms:modified">{ora}</meta>
  </metadata>
  <manifest>
{chr(10).join(risorse)}
  </manifest>
  <spine toc="ncx">
{chr(10).join(lettura)}
  </spine>
</package>
"""

    # --- lo zip -------------------------------------------------------------
    # ogni voce dell'archivio porta la stessa data delle fonti: altrimenti lo
    # zip cambierebbe a ogni ricostruzione anche a contenuto identico
    stampigli = (quando.year, quando.month, quando.day,
                 quando.hour, quando.minute, quando.second)

    def voce(nome):
        info = zipfile.ZipInfo(nome, date_time=stampigli)
        info.external_attr = 0o644 << 16
        return info

    with zipfile.ZipFile(DEST, "w") as z:
        # il mimetype va per primo e senza compressione: è la firma dell'EPUB
        z.writestr(voce("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr(voce("META-INF/container.xml"),
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
                   '  <rootfiles>\n'
                   '    <rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/>\n'
                   '  </rootfiles>\n</container>\n',
                   compress_type=zipfile.ZIP_DEFLATED)
        for nome, contenuto in file.items():
            z.writestr(voce("OEBPS/" + nome), contenuto, compress_type=zipfile.ZIP_DEFLATED)
        for percorso, dentro in [(COPERTINA, "OEBPS/img/copertina.jpg"),
                                 (MAPPA, "OEBPS/img/mappa.jpg")]:
            z.writestr(voce(dentro), percorso.read_bytes(),
                       compress_type=zipfile.ZIP_DEFLATED)

    return DEST, len(capitoli)


def verifica():
    """Controlli di struttura: XML ben formato e nessun file dichiarato ma assente."""
    import re
    from xml.etree import ElementTree as ET

    problemi = []
    with zipfile.ZipFile(DEST) as z:
        dentro = set(z.namelist())

        if z.namelist()[0] != "mimetype":
            problemi.append("il mimetype non è il primo file dell'archivio")
        if z.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            problemi.append("il mimetype non è memorizzato senza compressione")

        for nome in dentro:
            if nome.endswith((".xhtml", ".opf", ".ncx", ".xml")):
                try:
                    ET.fromstring(z.read(nome))
                except ET.ParseError as err:
                    problemi.append(f"{nome}: XML non valido ({err})")

        opf = z.read("OEBPS/content.opf").decode("utf-8")
        for href in re.findall(r'<item [^>]*href="([^"]+)"', opf):
            if "OEBPS/" + href not in dentro:
                problemi.append(f"dichiarato nel manifesto ma assente: {href}")
    return problemi


def main():
    percorso, capitoli = costruisci()
    problemi = verifica()
    peso = percorso.stat().st_size
    print(f"EPUB -> {percorso.relative_to(ROOT)}  ({capitoli} capitoli, {peso // 1024} KB)")
    for p in problemi:
        print("  ✗ " + p)
    if not problemi:
        print("  ✓ struttura valida, XML ben formato, nessuna risorsa mancante")


if __name__ == "__main__":
    main()
