# -*- coding: utf-8 -*-
"""
Genera le pagine del sito a partire da docs/data/racconti.json

Uso:  python tools/estrai.py && python tools/costruisci.py
"""
import html
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from mappa import svg_mappa

ROOT = Path(__file__).resolve().parent.parent
SITO = ROOT / "docs"
DATI = SITO / "data" / "racconti.json"
DOMANDE = SITO / "data" / "domande.json"
RACCONTI = SITO / "racconti"

SITO_URL = "https://vvineis.github.io/il-bosco-delle-cento-voci/"

TITOLO_SITO = "Il Bosco delle Cento Voci"
AUTRICE = "Vittoria Vineis"
EMAIL = "vineisvittoria@gmail.com"

BIO = [
    "Da bambina voleva fare, alternativamente, il gabbiano oppure l’avvocata che difende "
    "i diritti umani. Crescendo, sta ancora cercando di capire cosa farà da grande.",

    "Nel frattempo ha lasciato il suo amato Monte Mucrone per migrare verso climi più miti, "
    "prima la Toscana, poi Roma. Ultimamente si è avventurata nel mondo dell’ingegneria "
    "informatica, dove ha scoperto che la sua anima è più affascinata dal complesso che dal "
    "complicato e che ama le domande più delle risposte. Le favole nascono da questa "
    "consapevolezza.",

    "Adora assaggiare gusti di gelato improbabili nei luoghi più sperduti del mondo, sceglie "
    "sempre i biscotti rotti in fondo alla scatola, ascolta solo podcast long format, indossa "
    "con fierezza corone da principessa dall’inconfondibile fascino kitsch (perdonala, "
    "Madre Terra), vive un rapporto complicato con le unità di misura e prova una naturale "
    "attrazione per le persone appassionate.",
]

BIO_CONTATTI = (
    "Scrivile per qualsiasi cosa riguardi il Bosco: per raccontarle com’è andata una "
    "lettura, per proporle un disegno o una storia, o solo per dire che una favola ti ha "
    "detto qualcosa."
)

NOTA_IMMAGINI = (
    "I ritratti degli abitanti, l'illustrazione della mappa e la copertina sono immagini "
    "generate con l'intelligenza artificiale, tenute qui come segnaposto. I racconti "
    "restano volutamente senza illustrazioni, perché quel posto sia di chi disegna davvero."
)


# ---------------------------------------------------------------- abitanti ---
# (nome, specie, file del medaglione, racconto, descrizione)

ABITANTI = [
    ("Velia", "Volpe", "velia", "la-volpe-che-cuciva-le-nuvole",
     "Cuce le nuvole con fili di ragnatela. Nessuno capisce perché, ma lei continua."),
    ("Rubino", "Riccio", "rubino", "i-piccoli-riti-del-bosco",
     "Ogni mattina allinea le foglie davanti alla tana. Una verde, una rossa, una gialla."),
    ("Lola", "Lepre", "lola", "i-piccoli-riti-del-bosco",
     "Non parte mai per una corsa senza aver fatto prima tre capriole. Una, due, tre!"),
    ("Gedeone", "Gufo", "gedeone", "i-piccoli-riti-del-bosco",
     "Passa le notti a contare le stelle, per paura che una si spenga per dispetto."),
    ("Celestina", "Civetta", "celestina", "la-civetta-che-non-voleva-perdersi-nulla",
     "Ha occhi grandi come due pozze di luna, spalancati giorno e notte, finchè non impara a sognare."),
    ("Petronio", "Picchio", "petronio", "il-carillon-del-tempo",
     "L'orologiaio del Bosco. Tic, tic. Finché il suo becco lavora, il tempo sa dove andare."),
    ("Savino", "Scoiattolo", "savino", "il-carillon-del-tempo",
     "Il magazziniere delle ghiande. Con le parole non ci sa fare, ma ha un cuore grande quanto il suo magazzino."),
    ("Curzio", "Corvo", "curzio", "il-corvo-che-ingigantiva-le-sue-gesta",
     "Un cantastorie dalle piume nere e lucide come inchiostro fresco."), 
    ("Tenebrio", "Tasso", "tenebrio", "il-tasso-che-collezionava-ombre",
     "Stacca le ombre dai rami al tramonto e le insegue perfino sotto le zampe degli altri."),
    ("Lucia", "Lucciola", "lucia", "il-tasso-che-collezionava-ombre",
     "Di giorno quasi non si vede, ma al buio illumina tutto il Bosco."),
    ("Tamarinda", "Talpa", "tamarinda", "i-cunicoli-di-tamarinda",
     "Esperta scavastrice di cunicoli, con un sorriso che sa di radici."),
    ("Romualdo", "Rospo", "romualdo", "lo-stagno-degli-specchi",
     "Cerca un principe nello Stagno degli Specchi e ci trova solo mille rospi."),
    ("Prospero", "Pavone", "prospero", "lo-stagno-degli-specchi",
     "Ha la coda più bella del Bosco e non gli sembra mai abbastanza lucente."),
    ("Carisio", "Cervo", "carisio", "la-sorgente-disuguale",
     "Ha una voce che rimbomba come un'eco di montagna e non sa restare in silenzio davanti alle ingiustizie."),
    ("Clizia", "Cicala", "clizia", "la-cicala-che-collezionava-echi",
     "Canta e poi rincorre l'eco del suo canto per chiuderlo in un sacchetto."),
    ("Livia", "Libellula", "livia", "la-libellula-che-non-trovava-il-suo-perche",
     "Troppo veloce perfino per il proprio riflesso. Non genera colori, ma li dona al mondo."),
    ("Pìndaro", "Pipistrello", "pindaro", "il-pipistrello-che-leggeva-il-buio",
     "Di giorno inciampa, di notte legge il Bosco forma per forma."),
    ("Fiammetta", "Formica", "fiammetta", "la-formica-infaticabile",
     "Un punto rosso in movimento, una fiamma apparentemente instancabile."),
    ("Brumildo", "Orso", "brumildo", "un-insolita-amicizia",
     "Ama il miele più di ogni altra cosa e dorme mesi interi senza vergognarsene."),
    ("Raminga", "Rondine", "raminga", "un-insolita-amicizia",
     "Vola per il mondo e non si posa mai, perché teme che nessun ramo la sostenga."),
    ("Sinestesio", "Serpente", "sinestesio", "il-serpente-che-ascoltava-i-colori",
     "Ascolta i colori e vede i suoni. Per lui ogni senso è una porta sull'altro."),
    ("Lara", "Lontra", "lara", "la-nascita-dello-stagno",
     "Passa le giornate a farsi portare dal torrente e la sua risata si mescola al canto dell'acqua."),
    ("Callisto", "Castoro", "callisto", "la-nascita-dello-stagno",
      "Ha un manto bruno come il miele di castagno e la dedizione paziente d'altri tempi."),
    ("Il Vento", "Amico invisibile", "vento", "il-vento-smemorato",
     "Il direttore d'orchestra che non si vede."),
    ("Tilda", "Tartaruga", "tilda", "il-fiore-di-tilda",
     "Cammina piano e si ferma prima di parlare. Non dà consigli, ma dona presenza."),
]


# ------------------------------------------------------------------ pezzi ---

def e(t):
    return html.escape(t, quote=False)


def para(testo):
    """Un paragrafo, con le interruzioni di riga del manoscritto preservate."""
    righe = [e(r) for r in testo.split("\n")]
    return "<p>" + "<br>\n".join(righe) + "</p>"


FOGLIA_SVG = (
    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
    '<path d="M20 4C10 4 4 9 4 16c0 1.4.3 2.7.8 3.9C6.6 14 10.6 10.6 16 9.4'
    'c-4.6 2-7.7 5.4-9.3 10.4 1.2.5 2.5.8 3.9.8 7 0 12-6 12-16 0-.2 0-.4-.6-.6z" '
    'fill="currentColor"/></svg>'
)

FREGIO = (
    '<div class="fregio" aria-hidden="true">'
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" opacity=".9">'
    '<path d="M20 4C10 4 4 9 4 16c0 1.4.3 2.7.8 3.9C6.6 14 10.6 10.6 16 9.4'
    'c-4.6 2-7.7 5.4-9.3 10.4 1.2.5 2.5.8 3.9.8 7 0 12-6 12-16 0-.2 0-.4-.6-.6z"/>'
    '</svg></div>'
)


def testata(attiva, prefisso=""):
    voci = [
        ("index.html", "Home", "home"),
        ("racconti.html", "Racconti", "racconti"),
        ("abitanti.html", "Abitanti", "abitanti"),
        ("mappa.html", "Mappa", "mappa"),
        ("spunti.html", "Spunti di lettura", "spunti"),
        ("scarica.html", "Scarica", "scarica"),
        ("autrice.html", "Autrice", "autrice"),
        ("il-bosco-e-aperto.html", "Il Bosco è aperto", "aiuto"),
    ]
    li = []
    for href, testo, chiave in voci:
        corrente = ' aria-current="page"' if chiave == attiva else ""
        li.append(f'<li><a href="{prefisso}{href}"{corrente}>{e(testo)}</a></li>')
    return f"""<a class="salta" href="#contenuto">Salta al contenuto</a>
<header class="testata">
  <div class="contenitore">
    <a class="marchio" href="{prefisso}index.html">
      {FOGLIA_SVG}<span>Il Bosco delle Cento Voci</span>
    </a>
    <nav aria-label="Navigazione principale">
      <ul class="menu">
        {"".join(li)}
      </ul>
    </nav>
  </div>
</header>"""


def pie(prefisso=""):
    return f"""<footer class="pie">
  <div class="contenitore">
    <div class="pie-griglia">
      <div>
        <h3>Il Bosco delle Cento Voci</h3>
        <p>Ventidue favole per bambini che non hanno paura delle domande
           e per i grandi che non hanno mai smesso di farsele.</p>
        <p>Un posto che si costruisce insieme a chi ci passa.
           <a href="{prefisso}il-bosco-e-aperto.html">Il Bosco è aperto</a></p>
      </div>
      <div>
        <h3>Leggi</h3>
        <ul>
          <li><a href="{prefisso}racconti.html">Tutti i racconti</a></li>
          <li><a href="{prefisso}mappa.html">La mappa del Bosco</a></li>
          <li><a href="{prefisso}abitanti.html">Gli abitanti del Bosco</a></li>
          <li><a href="{prefisso}racconti/24-filastrocca-del-bosco.html">Filastrocca del Bosco</a></li>
          <li><a href="{prefisso}libro.html">Il libro intero</a></li>
          <li><a href="{prefisso}spunti.html">Spunti di lettura</a></li>
          <li><a href="{prefisso}scarica.html">Scarica il libro</a></li>
        </ul>
      </div>
      <div>
        <h3>Contatti</h3>
        <ul>
          <li><a href="{prefisso}autrice.html">Chi è l'autrice</a></li>
          <li><a href="{prefisso}il-bosco-e-aperto.html">Il Bosco è aperto</a></li>
          <li><a href="{prefisso}licenza.html">Licenza e diritti</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="pie-basso">
      <p>Testo © {AUTRICE} — <a href="{prefisso}licenza.html">CC BY-NC-ND 4.0</a>.
         Copertina e ritratti sono immagini generate con l'IA, provvisorie.</p>
    </div>
  </div>
</footer>"""


def riquadro_scarica(sigla, titolo, descrizione, percorso, etichetta):
    """Se il file non è ancora stato generato, invece di un link rotto si mostra
    il riquadro «In arrivo»."""
    if (SITO / percorso).exists():
        azione = (f'<a class="bottone bottone-verde" href="{percorso}" download>'
                  f'{etichetta}{peso_file(percorso)}</a>')
        classe = "formato"
    else:
        azione = '<p class="etichetta-arrivo">In arrivo</p>'
        classe = "formato in-arrivo"
    return (f'<article class="{classe}">\n'
            f'        <span class="sigla" aria-hidden="true">{sigla}</span>\n'
            f'        <h3>{titolo}</h3>\n'
            f'        <p>{descrizione}</p>\n'
            f'        {azione}\n      </article>')


def peso_file(percorso):
    """« (2,1 MB) » da mettere accanto al bottone, o niente se il file non c'è.
    Sotto il mezzo megabyte si scrive in KB, o un fascicolo leggero risulterebbe
    « 0,0 MB »."""
    f = SITO / percorso
    if not f.exists():
        return ""
    byte = f.stat().st_size
    if byte < 512 * 1024:
        return f" ({byte // 1024} KB)"
    return f" ({byte / 1024 / 1024:.1f} MB)".replace(".", ",")


def versione_stile():
    """Impronta del foglio di stile: cambia a ogni modifica e invalida la cache."""
    css = SITO / "assets" / "css" / "stile.css"
    return int(css.stat().st_mtime) if css.exists() else 0


def assoluto(percorso):
    """Da percorso interno a URL completo, come vogliono i motori di ricerca."""
    return SITO_URL.rstrip("/") + "/" + percorso.lstrip("/")


def dati_strutturati():
    """Scheda del libro in JSON-LD: aiuta Google a capire che è un libro,
    di chi è e che si legge gratis."""
    import json as _json
    dati = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": TITOLO_SITO,
        "author": {"@type": "Person", "name": AUTRICE},
        "inLanguage": "it",
        "bookFormat": "https://schema.org/EBook",
        "numberOfPages": 72,
        "genre": ["Favole", "Letteratura per ragazzi"],
        "url": SITO_URL,
        "image": assoluto("assets/img/copertina.jpg"),
        "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        "isAccessibleForFree": True,
        "description": (
            "Ventidue favole di Vittoria Vineis: un bosco in cui ogni animale cerca "
            "la propria voce. Si legge online gratuitamente."),
    }
    return ('<script type="application/ld+json">'
            + _json.dumps(dati, ensure_ascii=False) + "</script>")


def pagina(titolo, descrizione, corpo, attiva, prefisso="", classe_body="",
           script=False, percorso="", strutturati=False, indicizza=True):
    js = (f'\n  <script src="{prefisso}assets/js/lettura.js?v={versione_stile()}" defer></script>'
          if script else "")
    titolo_completo = titolo if titolo == TITOLO_SITO else f"{titolo} — {TITOLO_SITO}"
    return f"""<!doctype html>
<!--
  PAGINA GENERATA AUTOMATICAMENTE — non modificare questo file:
  a ogni «python tools/tutto.py» viene riscritto da capo e le modifiche vanno perse.
  Il testo dei racconti sta nel .docx; gli altri testi in tools/costruisci.py,
  tools/estrai.py e docs/data/domande.json. Vedi README.md.
-->
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titolo_completo)}</title>
  <meta name="description" content="{e(descrizione)}">
  <meta name="author" content="{AUTRICE}">
  <meta property="og:title" content="{e(titolo_completo)}">
  <meta property="og:description" content="{e(descrizione)}">
  <meta property="og:type" content="book">
  <meta property="og:image" content="{assoluto('assets/img/anteprima-social.jpg')}">
  <meta property="og:url" content="{assoluto(percorso)}">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="{TITOLO_SITO}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{assoluto(percorso)}">
  <meta name="theme-color" content="#12402c">
  {"" if indicizza else '<meta name="robots" content="noindex, follow">'}{dati_strutturati() if strutturati else ""}
  <link rel="icon" href="{prefisso}assets/img/foglia.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..700&family=Nunito:ital,wght@0,400..800;1,400..700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefisso}assets/css/stile.css?v={versione_stile()}">{js}
</head>
<body{f' class="{classe_body}"' if classe_body else ""}>
{testata(attiva, prefisso)}
<main id="contenuto">
{corpo}
</main>
{pie(prefisso)}
</body>
</html>
"""


# ------------------------------------------------------------------ pagine ---

def home(d):
    sezioni = d["sezioni"]
    racconti = [s for s in sezioni if s["numero"]]
    premessa = next(s for s in sezioni if s["slug"] == "premessa")

    sinossi_html = "\n".join(f"<p>{e(t)}</p>" for t in d["sinossi"])

    scelti = [s for s in racconti if s["slug"] in (
        "la-volpe-che-cuciva-le-nuvole",
        "il-pipistrello-che-leggeva-il-buio",
        "un-insolita-amicizia",
        "la-libellula-che-non-trovava-il-suo-perche",
        "i-cunicoli-di-tamarinda",
        "la-cicala-che-collezionava-echi",
    )]
    schede = "\n".join(scheda_racconto(s) for s in scelti)

    apertura = e(premessa["paragrafi"][0])
    # in home l'apertura si ferma alla prima frase: il resto lo si legge nella premessa
    seconda = e(premessa["paragrafi"][1].split(". ")[0] + ".")

    return f"""
<section class="hero">
  <div class="contenitore">
    <div class="hero-alto">
      <img class="hero-copertina" src="assets/img/copertina-media.jpg"
           srcset="assets/img/copertina-piccola.jpg 400w, assets/img/copertina-media.jpg 640w, assets/img/copertina.jpg 1024w"
           sizes="(max-width: 800px) 260px, 320px"
           width="640" height="960"
           alt="Copertina del libro: un grande albero verde con un gufo, una volpe, una lepre, un riccio e un uccellino tra i rami.">
      <div>
        <h1>Il Bosco<em>delle Cento Voci</em></h1>
        <p class="hero-autrice">di {AUTRICE}</p>
        <p class="hero-sommario">{apertura}<br>{seconda}</p>
        <div class="azioni">
          <a class="bottone bottone-oro" href="racconti.html">Leggi online</a>
          <a class="bottone bottone-chiaro" href="scarica.html">Scarica il libro</a>
        </div>
      </div>
    </div>
    <p class="hero-pedice">Ventidue favole per bambini che non hanno paura delle domande
       e per i grandi che non hanno mai smesso di farsele.</p>
  </div>
</section>

<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Di che cosa parla</h2>
    <div class="testo-lungo">
      <p> Il Bosco delle Cento Voci è una raccolta di favole intrecciate in cui ogni animale custodisce una fragilità, una domanda, un modo diverso di abitare il mondo.
      Nel Bosco le inquietudini personali e le grandi sfide del nostro tempo prendono la forma di sentieri, alberi, stagni e creature che cercano, si smarriscono, si incontrano. </p>
      <p> Ogni storia aggiunge una voce alle altre, finché il Bosco stesso diventa un racconto corale: un luogo dove 
      la fragilità non chiede di essere nascosta né guarita, ma ascoltata e accolta, e dove l'incontro con l'altro diventa il terreno fertile per una comunità che cura.</p>
      <p style="text-align:center; margin-top:2rem;">
        <a class="bottone bottone-contorno" href="racconti.html">Entra nel Bosco</a>
      </p>
    </div>
  </div>
</section>


<section class="sezione sezione-pergamena">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Qualche voce, per cominciare</h2>
    <p class="sottotitolo-sezione">Le storie si possono leggere in ordine oppure aprendo il Bosco
       dove capita. Gli animali sono sempre gli stessi e si ritrovano da un racconto all'altro.</p>
    <div class="griglia">
      {schede}
    </div>
    <p style="text-align:center; margin-top:2.5rem;">
      <a class="bottone bottone-verde" href="racconti.html">Tutti i {len(racconti)} racconti</a>
    </p>
  </div>
</section>

<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Se vuoi restare ancora un po'</h2>
    <p class="sottotitolo-sezione">Qualche modo per starci dentro un po' più a lungo.</p>
    <div class="griglia">
      <a class="scheda" href="spunti.html">
        <span class="scheda-numero">Per chi legge insieme</span>
        <h3>Spunti di lettura</h3>
        <p>Domande e attività pensate per accompagnare le bambine e i bambini alla scoperta di ciò che si nasconde tra le righe delle storie. </p>
        <span class="scheda-freccia">Vai agli spunti →</span>
      </a>
      <a class="scheda" href="racconti/24-filastrocca-del-bosco.html">
        <span class="scheda-numero">In chiusura</span>
        <h3>Filastrocca del Bosco</h3>
        <p>I versi che chiudono il libro, quando tutti gli animali hanno già
           raccontato la loro storia. Si legge ad alta voce.</p>
        <span class="scheda-freccia">Leggila →</span>
      </a>
      <a class="scheda" href="il-bosco-e-aperto.html">
        <span class="scheda-numero">Un invito</span>
        <h3>Il Bosco è aperto</h3>
        <p>Ci sono ancora tane senza abitanti e racconti senza volto. Chi disegna, chi
           scrive, chi legge ad alta voce. C'è spazio.</p>
        <span class="scheda-freccia">Entra →</span>
      </a>
    </div>
  </div>
</section>

"""


def strofe(versi):
    """Raggruppa i versi in strofe: una strofa che finisce con la virgola
    prosegue nel blocco successivo (nel manoscritto era spezzata a metà)."""
    fuori = []
    for blocco in versi:
        if fuori and fuori[-1].rstrip().endswith(","):
            fuori[-1] = fuori[-1] + "\n" + blocco
        else:
            fuori.append(blocco)
    return fuori


def filastrocca(d):
    """I versi che chiudono il libro, senza la firma della citazione."""
    ultima = next(s for s in d["sezioni"] if s["slug"] == "l-ultima-voce-del-bosco")
    return strofe(ultima["versi"])


def sezione_filastrocca(d, prefisso=""):
    righe = "\n".join(
        '<p>' + "<br>\n".join(e(r) for r in blocco.split("\n")) + '</p>'
        for blocco in filastrocca(d))
    return f"""
<section class="congedo">
  <div class="contenitore">
    <p class="occhiello">Filastrocca del Bosco</p>
    <div class="congedo-versi">
      {righe}
    </div>
    {FREGIO}
  </div>
</section>"""


def pagina_filastrocca(d, ultimo):
    righe = "\n      ".join(
        '<p>' + "<br>\n".join(e(r) for r in blocco.split("\n")) + '</p>'
        for blocco in filastrocca(d))
    corpo = f"""
<section class="congedo congedo-pagina">
  <div class="contenitore">
    <span class="racconto-numero">In chiusura</span>
    <h1>Filastrocca del Bosco</h1>
    <div class="congedo-versi">
      {righe}
    </div>
    {FREGIO}
  </div>
</section>

<div class="racconto">
  <nav class="nav-racconti" aria-label="Navigazione tra i racconti">
    <a class="indietro" href="{ultimo['file']}">
      <span class="verso">← Racconto precedente</span>
      <span class="titolo-nav">{e(ultimo['titolo'])}</span>
    </a>
  </nav>
  <p class="torna-indice"><a class="bottone bottone-contorno" href="../racconti.html">Torna all'indice dei racconti</a></p>
</div>
"""
    return pagina("Filastrocca del Bosco",
                  f"I versi che chiudono {TITOLO_SITO} di {AUTRICE}.",
                  corpo, "racconti", prefisso="../",
                  classe_body="pagina-lettura", script=True,
                  percorso="racconti/24-filastrocca-del-bosco.html")


def scheda_racconto(s, prefisso=""):
    numero = f"Racconto {s['numero']}" if s["numero"] else "Per cominciare"
    return f"""<a class="scheda" href="{prefisso}racconti/{s['file']}">
        <span class="scheda-numero">{numero}</span>
        <h3>{e(s['titolo'])}</h3>
        <p>{e(s['tema'])}</p>
        <span class="scheda-freccia">Leggi →</span>
      </a>"""


def indice_racconti(d):
    sezioni = d["sezioni"]
    schede = "\n".join(scheda_racconto(s) for s in sezioni)
    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Consigli per la lettura</h2>
    <p class="sottotitolo-sezione">Ventidue storie e una premessa. Puoi leggerle in ordine,
       come un libro, oppure scegliere quella che ti chiama di più. Puoi anche esplorarle dalla
       <a href="mappa.html">Mappa del Bosco</a>, o partire dai suoi
       <a href="abitanti.html">Abitanti</a>.</p>
    <p style="text-align:center; margin:-1rem 0 2.5rem;" class="azioni-indice">
      <a class="bottone bottone-contorno" href="libro.html">Leggi tutto il libro in una pagina</a>
    </p>
    <div class="griglia">
      {schede}
      <a class="scheda" href="racconti/24-filastrocca-del-bosco.html">
        <span class="scheda-numero">In chiusura</span>
        <h3>Filastrocca del Bosco</h3>
        <p>I versi che chiudono il libro, quando tutti gli animali hanno già raccontato
           la loro storia. Si legge ad alta voce.</p>
        <span class="scheda-freccia">Leggila →</span>
      </a>
    </div>
  </div>
</section>

"""


def pagina_licenza(d):
    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Licenza e diritti</h2>
    <p class="sottotitolo-sezione">In breve: leggilo, stampalo, passalo a chi vuoi.
       Non venderlo e non riscriverlo.</p>

    <div class="testo-lungo">
      <p class="licenza-riga">
        <strong>Il Bosco delle Cento Voci</strong> di {AUTRICE} è concesso in licenza con
        <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.it" rel="license">
        Creative Commons Attribuzione&#8202;-&#8202;Non commerciale&#8202;-&#8202;Non opere
        derivate 4.0 Internazionale</a> (CC&nbsp;BY-NC-ND&nbsp;4.0).
      </p>

      <h3>Si può, senza chiedere niente</h3>
      <ul class="licenza-elenco">
        <li>leggere, stampare, fotocopiare</li>
        <li>condividere il libro e il link, in qualsiasi formato</li>
        <li>usarlo a scuola, in biblioteca, nei laboratori di lettura</li>
        <li>leggerlo ad alta voce, anche in pubblico, anche registrandosi</li>
      </ul>
      <p>L'unica condizione è citare l'autrice, {AUTRICE}, con il collegamento a questa
         licenza.</p>

      <h3>Serve chiedere</h3>
      <ul class="licenza-elenco">
        <li><strong>per venderlo</strong>, o per usarlo dentro qualcosa a pagamento </li>
        <li><strong>per modificarlo</strong> (riscritture, adattamenti, traduzioni) </li>
      </ul>

      <h3>Tre cose che la licenza non copre</h3>
      <p><strong>La poesia di Roberto Juarroz</strong> citata in <em>Il fiore di Tilda</em>
         è opera di terzi, riportata con attribuzione. I suoi diritti appartengono ai
         legittimi titolari e non possono essere concessi qui.</p>
      <p><strong>La copertina, la mappa del Bosco e i ritratti degli abitanti</strong> sono
         immagini generate con l'intelligenza artificiale generativa. Non vengono rivendicate come opera
         propria e non sono concesse in licenza. Stanno lì provvisoriamente, in attesa di
         illustrazioni fatte da una persona che vorrà prendersene cura.</p>
      <p><strong>I contributi di altre persone</strong> (disegni, racconti, letture
         registrate) restano di chi li ha fatti. Al Bosco viene concesso soltanto il
         permesso di pubblicarli qui, con il loro nome; chi li ha fatti resta libero di
         usarli altrove come vuole.</p>

      <p style="margin-top:2rem;">Per qualsiasi richiesta:
         <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
</section>
"""


def pagina_mappa(d):
    per_slug = {s["slug"]: s for s in d["sezioni"]}
    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">La mappa del Bosco</h2>
    <p class="sottotitolo-sezione">Ogni racconto succede in un posto preciso e qui sotto ci sono
       tutti. Tocca un luogo per entrare nella storia che ci abita. Non dimenticare che c'è vita anche sottoterra.</p>
  </div>

  <!-- la mappa sta fuori dal contenitore, così occupa tutta la larghezza -->
  <div class="mappa-cornice">
    {svg_mappa(per_slug)}
  </div>

  <div class="contenitore">
    <p class="mappa-nota">Passa il cursore su un punto dorato per leggerne il nome.
       Sul telefono la mappa si trascina di lato.</p>
    <p class="mappa-nota" style="font-size:0.85rem; opacity:.75;">L'illustrazione è generata
       con l'intelligenza artificiale e sta qui come segnaposto, in attesa di una mappa
       disegnata da una persona. <a href="il-bosco-e-aperto.html">Se disegni, c'è posto.</a></p>
  </div>
</section>
"""


def pagina_abitanti(d):
    per_slug = {s["slug"]: s for s in d["sezioni"]}
    carte = []
    for nome, specie, immagine, slug, descrizione in ABITANTI:
        sez = per_slug.get(slug)
        rimando = ""
        if sez:
            rimando = (f'<p class="rimando"><a href="racconti/{sez["file"]}">'
                       f'{e(sez["titolo"])} →</a></p>')
        carte.append(f"""<article class="abitante">
        <img class="medaglione" src="assets/img/abitanti/{immagine}.png" alt="{e(specie)} {e(nome)}"
             loading="lazy" width="160" height="160">
        <span class="specie">{e(specie)}</span>
        <h3>{e(nome)}</h3>
        <p>{e(descrizione)}</p>
        {rimando}
      </article>""")

    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Gli abitanti del Bosco</h2>
    <p class="sottotitolo-sezione">Nessuno di loro è un eroe. Sono creature che inciampano,
       che si fermano, che si smarriscono e che proprio da quelle crepe imparano a
       conoscersi. Li incontrerai più volte, da un racconto all'altro.</p>
    <div class="griglia-abitanti">
      {"".join(carte)}
    </div>
  </div>
</section>

<section class="sezione sezione-pergamena">
  <div class="contenitore">
    <div class="testo-lungo" style="text-align:center;">
      <p style="font-size:0.95rem; color:var(--inchiostro-tenue);">{NOTA_IMMAGINI}
        <a href="il-bosco-e-aperto.html">Se disegni, c'è posto.</a></p>
    </div>
  </div>
</section>
"""


def pagina_spunti(d, domande):
    per_slug = {s["slug"]: s for s in d["sezioni"]}
    blocchi = []
    for s in d["sezioni"]:
        voce = domande.get(s["slug"])
        if not voce:
            continue
        numero = f"Racconto {s['numero']}" if s["numero"] else "Premessa"
        avvertenza = ""
        if voce.get("avvertenza"):
            avvertenza = f'<p class="avvertenza">{e(voce["avvertenza"])}</p>'
        elenco = "\n".join(f"<li>{e(q)}</li>" for q in voce.get("domande", []))
        attivita = ""
        if voce.get("attivita"):
            attivita = (f'<p class="attivita"><span>Da fare insieme</span> '
                        f'{e(voce["attivita"])}</p>')
        blocchi.append(f"""<article class="spunto" id="{s['slug']}">
      <span class="scheda-numero">{numero}</span>
      <h3><a href="racconti/{s['file']}">{e(s['titolo'])}</a></h3>
      <p class="spunto-tema">{e(s['tema'])}</p>
      {avvertenza}
      <ul class="domande">{elenco}</ul>
      {attivita}
    </article>""")

    # la Filastrocca ha spunti suoi, ma non è una sezione del manoscritto
    fila = domande.get("filastrocca-del-bosco")
    if fila:
        elenco = "\n".join(f"<li>{e(q)}</li>" for q in fila.get("domande", []))
        attivita = (f'<p class="attivita"><span>Da fare insieme</span> '
                    f'{e(fila["attivita"])}</p>') if fila.get("attivita") else ""
        blocchi.append(f"""<article class="spunto" id="filastrocca-del-bosco">
      <span class="scheda-numero">In chiusura</span>
      <h3><a href="racconti/24-filastrocca-del-bosco.html">Filastrocca del Bosco</a></h3>
      <p class="spunto-tema">I versi che chiudono il libro. Si leggono ad alta voce,
         tutti insieme e poi, se si vuole, se ne scrive una propria.</p>
      <ul class="domande">{elenco}</ul>
      {attivita}
    </article>""")

    sommario = "\n".join(
        f'<li><a href="#{s["slug"]}">{e(s["titolo"])}</a></li>'
        for s in d["sezioni"] if s["slug"] in domande)
    if fila:
        sommario += '\n<li><a href="#filastrocca-del-bosco">Filastrocca del Bosco</a></li>'

    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Spunti di lettura</h2>
    <p class="sottotitolo-sezione">Per classi, gruppi e famiglie: tre domande e una piccola attività per ogni racconto, pensate per accompagnare bambine e bambini alla scoperta di ciò che si nasconde tra le righe delle storie.</p>

    <div class="testo-lungo">
      <div class="nota-metodo">
        <h3>Come usarli</h3>
        <p>Le favole del Bosco non dichiarano esplicitamente la loro morale. La lasciano accadere, prendere e cambiare forma nella mente di chi legge.
          Le domande qui sotto desiderano offrire un piccolo pungolo per generarne altre. Funzionano meglio dopo la lettura, sono allergiche alla fretta e 
non       portano con sé risposte giuste da raggiungere. Ogni nuova intuizione, interpretazione o riflessione è calorosamente benvenuta.</p>
      </div>
    </div>

    <p style="text-align:center; margin:-1rem 0 2.5rem;">
      <a class="bottone bottone-verde" href="download/Spunti-di-lettura.pdf" download>Scarica
         il fascicolo da stampare{peso_file("download/Spunti-di-lettura.pdf")}</a>
    </p>

    <details class="sommario-spunti">
      <summary>Vai direttamente a un racconto</summary>
      <ul>{sommario}</ul>
    </details>

    <div class="elenco-spunti">
      {"".join(blocchi)}
    </div>
  </div>
</section>


<section class="sezione sezione-pergamena">
  <div class="contenitore">
    <div class="testo-lungo">
      <h2 style="font-size:1.5rem;">Hai usato il Bosco in classe?</h2>
      <p>Se hai provato queste domande con dei bambini, o se ne hai inventate di migliori,
         scrivimi; le raccoglierò qui, con i vostri nomi. 
         <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
  </div>
</section>
"""


def pagina_aiuto(d):
    return f"""
<section class="sezione sezione-verde">
  <div class="contenitore">
    <div class="testo-lungo" style="text-align:center;">
      <p class="occhiello">Un invito</p>
      <h2 class="titolo-sezione" style="color:var(--crema);">Il Bosco è aperto</h2>
      <p class="sottotitolo-sezione">Non è finito e va bene così. Nessuno è mai riuscito
         a contarne le voci, nemmeno chi l'ha scritto.</p>
    </div>
  </div>
</section>

<section class="sezione sezione-crema">
  <div class="contenitore">
    <div class="testo-lungo">
      {FREGIO}
      <h2 style="font-size:1.6rem; text-align:center;">Un bosco con una voce sola non è un bosco</h2>
      <p>Il Bosco delle Cento Voci è cominciato da una persona che scriveva la sera e per
         un po' è bastato così. Ma un libro che parla di come nessuna voce sia mai davvero sola non 
         poteva rimanere la storia di una voce soltanto, 
         poiché sarebbe stata la prima favola a non avere il coraggio di credere nelle proprie parole.</p>
      <p>Per questo è rimasto aperto. Più che una raccolta da distribuire, è un posto
         ancora pieno di spazi vuoti (tane senza abitanti, racconti a cui dare un volto, letture
         che non sono ancora successe) e gli spazi vuoti, in fondo, sono inviti. Chi lo ascolta, lo
         disegna, ne scrive o lo legge ad alta voce lo sta già abitando.</p>
      <p>Viviamo in un mondo che va di fretta e che la strada per il Bosco spesso non la
         trova più. Mettersi in cerchio a raccontarsi qualcosa, ascoltare per il gusto di
         ascoltare, fare spazio a chi inciampa invece di correre oltre, sono gesti piccoli
         e, di questi tempi, un po' rivoluzionari. Il Bosco vorrebbe diventare un cerchio
         così. Per farne parte basta averne voglia.</p>
    </div>
  </div>
</section>

<section class="sezione sezione-verde">
  <div class="contenitore">
    <div class="testo-lungo">
      <h2 style="font-size:1.6rem; text-align:center; color:var(--crema);">Il Bosco è chi lo abita</h2>
      <p style="color:rgba(253,247,231,0.9);">Il Bosco non è in vendita. Si legge gratis,
         non ha un editore dietro e non produce guadagni per nessuno, nemmeno per chi l'ha
         scritto. Sta in piedi esattamente come la Sorgente Disuguale nel libro: quello che
         c'è si mette in comune e allora basta per tutti.</p>
      <p style="color:rgba(253,247,231,0.9);"> Quindi il patto è uno solo e vale uguale per
         chiunque arrivi. Chi porta qualcosa lo dona al Bosco. 
         E il Bosco restituisce il suo nome accanto a ciò che ha creato. 
         I diritti restano sempre delle autrici e degli autori.
         Il Bosco chiede soltanto il permesso di ospitare quel contributo qui, lasciando a ciascuna e ciascuno 
         la piena libertà di usarlo altrove, come preferisce.</p>
    </div>
  </div>
</section>

<section class="sezione sezione-pergamena">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione" style="font-size:1.7rem;">Da dove si entra</h2>
    <p class="sottotitolo-sezione">Non c'è una porta principale. Ce ne sono almeno tre,
       e si somigliano tutte.</p>
    <div class="griglia">

      <article class="scheda">
        <span class="scheda-numero">Se disegni</span>
        <h3>Dona forma e colore a una storia</h3>
        <p>I racconti sono senza illustrazioni ed è una scelta. Le immagini che vedi qui (la copertina, la mappa del Bosco, i ritratti tondi dei suoi abitanti) sono state generate con l’intelligenza artificiale generativa 
        e sono pensate come segnaposto, per offrire piccoli appigli di fantasia a chi legge ed esplora, in attesa che una mano umana sappia donar loro un respiro autentico.
        Dentro il libro non ce n’è nessuna, perché quel posto è giusto che sia di chi disegna davvero. </p>
        <p>Se ti piace disegnare e vuoi lasciare un segno nel Bosco, basta anche solo un’illustrazione, quella che ti chiama.</p>
        <p class="scheda-freccia"><a href="mailto:{EMAIL}?subject=Un%20disegno%20per%20il%20Bosco">Parliamo di un'illustrazione→</a></p>
      </article>

      <article class="scheda">
        <span class="scheda-numero">Se scrivi</span>
        <h3>Porta una voce nuova</h3>
        <p>Le voci non sono mai state cento davvero e c'è posto per gli abitanti che non
           sono ancora arrivati. Se hai scritto una favola che potrebbe viverci, mandamela.</p>
        <p>Il testo resta tuo, viene pubblicato con il tuo nome, e il Bosco si allarga di una tana. Non c'è nessuna selezione da superare: si legge insieme, con calma, e si scopre come 
        quella voce trova posto accanto alle altre. In fondo, è solo un modo per scambiarsi un po' di umanità. </p>
        <p class="scheda-freccia"><a href="mailto:{EMAIL}?subject=Una%20nuova%20voce%20per%20il%20Bosco">Manda la tua storia →</a></p>
      </article>

      <article class="scheda">
        <span class="scheda-numero">Se leggi</span>
        <h3>Fai il cerchio</h3>
        <p>Leggere una storia ad alta voce a qualcuno è il modo più semplice ed è già moltissimo. 
        In classe, in biblioteca, in un parco, nella sala d'attesa del dentista, a un nipote, a un adulto che fa
           finta di ascoltare per gentilezza e poi si mette comodo.</p>
        <p>Se ti va, poi raccontarmi com'è andata, che cosa hanno chiesto i bambini, dove si sono
           annoiati, quale storia hanno voluto risentire. È da lì che il Bosco impara.</p>
        <p class="scheda-freccia"><a href="spunti.html">Condividi →</a></p>
      </article>

    </div>
  </div>
</section>

<section class="sezione sezione-crema">
  <div class="contenitore">
    <div class="testo-lungo">
      <h2 style="font-size:1.5rem;">E i diritti?</h2>
      <p>I racconti si possono leggere, stampare, fotocopiare, leggere ad alta voce e
         condividere liberamente, citando l'autrice. Non si possono vendere né riscrivere.
         È la licenza <strong>Creative Commons BY-NC-ND 4.0</strong>.</p>
      <p><a href="licenza.html">Che cosa vuol dire e le eccezioni &rarr;</a></p>
    </div>
  </div>
</section>

"""


def pagina_autrice(d):
    bio = "\n      ".join(f"<p>{t}</p>" for t in BIO)
    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">L'autrice</h2>
    <div class="testo-lungo">
      <div class="ritratto">
        <img class="medaglione medaglione-grande" src="assets/img/autrice.png"
             alt="{AUTRICE}, che sorride mentre assaggia un gelato in un mercato" width="200" height="200">
        <div>
          <h3>{AUTRICE}</h3>
          <p class="ritratto-occhiello">Chi ha scritto il Bosco</p>
        </div>
      </div>
      {bio}
      <p style="margin-top:2rem;">
        {BIO_CONTATTI} <a href="mailto:{EMAIL}">{EMAIL}</a>
      </p>
    </div>
  </div>
</section>

"""


def pagina_scarica(d):
    racconti = [s for s in d["sezioni"] if s["numero"]]
    return f"""
<section class="sezione sezione-crema">
  <div class="contenitore">
    {FREGIO}
    <h2 class="titolo-sezione">Porta il Bosco con te</h2>
    <p class="sottotitolo-sezione">Il libro si può leggere qui sul sito, gratuitamente e senza
       registrarsi. Se preferisci averlo con te, qui sotto trovi i formati da scaricare.</p>
    <div class="griglia-formati">

      <article class="formato">
        <span class="sigla" aria-hidden="true">WEB</span>
        <h3>Leggi online</h3>
        <p>Tutti i {len(racconti)} racconti, con il testo ingrandibile. Funziona su telefono,
           tablet e computer.</p>
        <a class="bottone bottone-verde" href="racconti.html">Vai ai racconti</a>
      </article>

      {riquadro_scarica("PDF", "PDF impaginato",
          "Formato A4 con copertina, indice e la mappa del Bosco. Ogni racconto comincia "
          "da pagina nuova. Si stampa e si rilega.",
          "download/Il-Bosco-delle-Cento-Voci.pdf", "Scarica il PDF")}

      {riquadro_scarica("EPUB", "EPUB",
          "Per e-reader, Kobo, Kindle e app di lettura. Il testo si adatta allo schermo "
          "e la dimensione dei caratteri la scegli tu.",
          "download/Il-Bosco-delle-Cento-Voci.epub", "Scarica l'EPUB")}

      {riquadro_scarica("✎", "Spunti di lettura",
          "Il fascicolo per chi legge insieme ai bambini: tema, tre domande e "
          "un'attività per ogni racconto. Sette pagine A4, da stampare e fotocopiare.",
          "download/Spunti-di-lettura.pdf", "Scarica gli spunti")}

    </div>
  </div>
</section>

<section class="sezione sezione-pergamena">
  <div class="contenitore">
    <div class="testo-lungo">
      <h2 style="font-size:1.5rem;">Si può usare a scuola?</h2>
      <p>Sì. I racconti si prestano alla lettura ad alta voce in classe o a casa. Ciascuno
         dura pochi minuti e in fondo a ogni storia c'è una breve nota per chi legge insieme
         ai bambini, che suggerisce il tema di cui la favola parla senza dirlo mai.</p>
      <p>Trovi tutte le domande, racconto per racconto, nella pagina
         <a href="spunti.html">Spunti di lettura</a>.</p>
      <p>Leggerlo, stamparlo e condividerne il link è libero e, anzi, è la cosa più utile
         che si possa fare. Il libro è pubblicato con licenza
         <a href="licenza.html">Creative Commons BY-NC-ND 4.0</a>.</p>
    </div>
  </div>
</section>
"""


def strumenti_lettura():
    return """<div class="strumenti">
    <span id="stato-testo">Testo 100%</span>
    <span class="strumenti-gruppo">
      <button type="button" id="testo-meno" aria-label="Riduci la dimensione del testo">A−</button>
      <button type="button" id="testo-piu" aria-label="Aumenta la dimensione del testo">A+</button>
    </span>
  </div>"""


def pagina_racconto(d, s, precedente, successivo, avvertenza=None):
    numero = f"Racconto {s['numero']}" if s["numero"] else "Premessa"
    testo = "\n".join(para(t) for t in s["paragrafi"])

    # l'avvertenza degli spunti (per ora solo «Il fiore di Tilda») va messa in
    # cima anche qui: chi apre il racconto deve saperlo prima di cominciare
    avviso = f'<p class="avvertenza avvertenza-lettura">{e(avvertenza)}</p>' if avvertenza else ""

    versi = ""
    if s["slug"] == "l-ultima-voce-del-bosco":
        versi = ""  # la filastrocca ha una sezione tutta sua, fuori dalla colonna di lettura
    elif s["versi"]:
        versi = '<div class="versi">' + "\n".join(para(t) for t in strofe(s["versi"])) + "</div>"

    nota = f"""<p class="rimando-spunti">
    <a href="../spunti.html#{s['slug']}">Domande e spunti su questo racconto &rarr;</a>
  </p>"""

    nav = []
    if precedente:
        nav.append(f"""<a class="indietro" href="{precedente['file']}">
      <span class="verso">← Racconto precedente</span>
      <span class="titolo-nav">{e(precedente['titolo'])}</span>
    </a>""")
    if successivo:
        nav.append(f"""<a class="avanti" href="{successivo['file']}">
      <span class="verso">Racconto successivo →</span>
      <span class="titolo-nav">{e(successivo['titolo'])}</span>
    </a>""")
    else:
        # dopo l'ultimo racconto il libro si chiude con i versi
        nav.append("""<a class="avanti" href="24-filastrocca-del-bosco.html">
      <span class="verso">Per chiudere →</span>
      <span class="titolo-nav">Filastrocca del Bosco</span>
    </a>""")

    corpo = f"""
<article class="racconto">
  {strumenti_lettura()}
  <header class="racconto-intestazione">
    <span class="racconto-numero">{numero}</span>
    <h1>{e(s['titolo'])}</h1>
  </header>
  {avviso}
  <div class="racconto-testo">
    {testo}
    {versi}
  </div>
  {nota}
</article>
<div class="racconto">
  <nav class="nav-racconti" aria-label="Navigazione tra i racconti">
    {"".join(nav)}
  </nav>
  <p class="torna-indice"><a class="bottone bottone-contorno" href="../racconti.html">Torna all'indice dei racconti</a></p>
</div>
"""
    descrizione = s["tema"] or f"{s['titolo']}, da Il Bosco delle Cento Voci di {AUTRICE}."
    return pagina(s["titolo"], descrizione, corpo, "racconti",
                  prefisso="../", classe_body="pagina-lettura", script=True,
                  percorso=f"racconti/{s['file']}")


def pagina_libro(d):
    parti = []
    for s in d["sezioni"]:
        numero = f"Racconto {s['numero']}" if s["numero"] else "Premessa"
        testo = "\n".join(para(t) for t in s["paragrafi"])
        versi = ""
        if s["slug"] == "l-ultima-voce-del-bosco":
            versi = ""  # la filastrocca chiude il libro in una sezione tutta sua
        elif s["versi"]:
            versi = '<div class="versi">' + "\n".join(para(t) for t in strofe(s["versi"])) + "</div>"
        parti.append(f"""<section class="sezione-libro" id="{s['slug']}">
  <header class="racconto-intestazione">
    <span class="racconto-numero">{numero}</span>
    <h2 style="font-size:clamp(1.7rem,4vw,2.4rem); color:var(--verde-scuro); font-weight:500;">{e(s['titolo'])}</h2>
  </header>
  <div class="racconto-testo">
    {testo}
    {versi}
  </div>
</section>""")

    corpo = f"""
<article class="racconto">
  {strumenti_lettura()}
  <header class="racconto-intestazione">
    <span class="racconto-numero">Testo integrale</span>
    <h1>Il Bosco delle Cento Voci</h1>
    <p style="font-family:var(--display); font-style:italic; color:var(--oro-scuro); font-size:1.2rem;">di {AUTRICE}</p>
    <p style="font-size:0.95rem; color:var(--inchiostro-tenue);">
      Questa pagina contiene il libro intero. Per stamparlo o salvarlo in PDF usa la
      funzione di stampa del browser (Ctrl+P, oppure Cmd+P su Mac).
    </p>
  </header>
  {"".join(parti)}
</article>
{sezione_filastrocca(d)}"""
    return pagina("Il libro intero",
                  f"Il testo integrale di {TITOLO_SITO} di {AUTRICE}, da leggere online o da stampare.",
                  corpo, "racconti", classe_body="pagina-lettura", script=True,
                  percorso="libro.html", indicizza=False)


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            '<rect width="32" height="32" rx="7" fill="#12402c"/>'
            '<path d="M26 7C13 7 6 13 6 21c0 1.7.4 3.3 1.1 4.7C9.2 18.6 14 14.5 20.6 13'
            'c-5.6 2.4-9.4 6.5-11.3 12.5 1.4.6 3 1 4.7 1 8.5 0 14-7.2 14-19 0-.3 0-.4-2-.5z" '
            'fill="#e3b552"/></svg>')


def sitemap(d):
    """La sitemap vuole URL completi: con quelli relativi Google la scarta."""
    # lastmod è la data dell'ultima modifica alle fonti, non quella di oggi:
    # ricostruire il sito senza cambiare niente non deve cambiare la sitemap
    from comune import data_fonti
    oggi = data_fonti().date().isoformat()

    # libro.html non c'è: ripete il testo dei racconti ed è marcata «noindex»
    principali = ["index.html", "racconti.html", "mappa.html", "abitanti.html",
                  "spunti.html", "licenza.html", "il-bosco-e-aperto.html",
                  "scarica.html", "autrice.html"]
    racconti = [f"racconti/{s['file']}" for s in d["sezioni"]]
    racconti.append("racconti/24-filastrocca-del-bosco.html")

    voci = []
    for u in principali + racconti:
        priorita = "1.0" if u == "index.html" else ("0.8" if u in principali else "0.7")
        voci.append(f"  <url>\n    <loc>{assoluto(u)}</loc>\n"
                    f"    <lastmod>{oggi}</lastmod>\n"
                    f"    <priority>{priorita}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(voci) + "\n</urlset>\n")


def robots():
    return ("User-agent: *\n"
            "Allow: /\n"
            "# PDF ed EPUB ripetono il testo delle pagine: si scaricano dal sito,\n"
            "# ma non devono comparire nei risultati al posto dei racconti\n"
            "Disallow: /download/\n\n"
            f"Sitemap: {assoluto('sitemap.xml')}\n")


def pagina_404(d):
    corpo = f"""
<section class="sezione sezione-crema" style="text-align:center; padding-block:5rem;">
  <div class="contenitore">
    <div class="testo-lungo">
      <p class="occhiello" style="color:var(--oro-scuro);">Ti sei perso nel Bosco</p>
      <h2 class="titolo-sezione">Questa pagina non c'è</h2>
      <p>Capita anche agli abitanti: i cunicoli si intrecciano e ci si ritrova
         da tutt'altra parte. Da qui si torna indietro facilmente.</p>
      <p style="margin-top:2rem; display:flex; gap:0.8rem; justify-content:center; flex-wrap:wrap;">
        <a class="bottone bottone-verde" href="{SITO_URL}">Torna all'ingresso</a>
        <a class="bottone bottone-contorno" href="{assoluto('mappa.html')}">Guarda la mappa</a>
      </p>
    </div>
  </div>
</section>
"""
    # servita da qualsiasi indirizzo sbagliato, quindi anche fogli di stile e
    # menu devono puntare in assoluto
    return pagina("Questa pagina non c'è",
                  "La pagina cercata non esiste nel Bosco delle Cento Voci.",
                  corpo, "", prefisso=SITO_URL, percorso="404.html")


# -------------------------------------------------------------------- main ---

def main():
    d = json.loads(DATI.read_text(encoding="utf-8"))
    domande = {k: v for k, v in json.loads(DOMANDE.read_text(encoding="utf-8")).items()
               if not k.startswith("_")}
    sezioni = d["sezioni"]

    extra = set(domande) - {s["slug"] for s in sezioni} - {"filastrocca-del-bosco"}
    if extra:
        print("⚠ spunti che non corrispondono a nessun racconto: " + ", ".join(sorted(extra)))
    senza = [s["slug"] for s in sezioni if s["slug"] not in domande]
    if senza:
        print("⚠ racconti senza spunti di lettura: " + ", ".join(senza))

    RACCONTI.mkdir(parents=True, exist_ok=True)
    for vecchio in RACCONTI.glob("*.html"):
        vecchio.unlink()

    scritti = []

    def scrivi(percorso, contenuto):
        p = SITO / percorso
        p.write_text(contenuto, encoding="utf-8")
        scritti.append(percorso)

    scrivi("index.html", pagina(
        TITOLO_SITO,
        "Ventidue favole di Vittoria Vineis: un bosco dove ogni animale cerca la propria voce. "
        "Si legge online gratuitamente o si scarica.",
        home(d), "home", percorso="index.html", strutturati=True))

    scrivi("racconti.html", pagina(
        "I racconti",
        "L'indice completo dei racconti del Bosco delle Cento Voci, da leggere online.",
        indice_racconti(d), "racconti", percorso="racconti.html"))

    scrivi("licenza.html", pagina(
        "Licenza e diritti",
        "Il Bosco delle Cento Voci è pubblicato con licenza Creative Commons "
        "BY-NC-ND 4.0: si legge, si stampa e si condivide liberamente.",
        pagina_licenza(d), "licenza", percorso="licenza.html"))

    scrivi("mappa.html", pagina(
        "La mappa del Bosco",
        "La mappa illustrata del Bosco delle Cento Voci: ogni luogo porta al racconto "
        "che ci abita.",
        pagina_mappa(d), "mappa", percorso="mappa.html"))

    scrivi("abitanti.html", pagina(
        "Gli abitanti del Bosco",
        "Chi vive nel Bosco delle Cento Voci: Tilda, Velia, Rubino, Lola, Gedeone e tutti gli altri.",
        pagina_abitanti(d), "abitanti", percorso="abitanti.html"))

    scrivi("spunti.html", pagina(
        "Spunti di lettura",
        "Domande e attività, pensate per accompagnare bambine e bambini alla scoperta di ciò che si nasconde tra le righe delle storie.",
        pagina_spunti(d, domande), "spunti", percorso="spunti.html"))

    scrivi("il-bosco-e-aperto.html", pagina(
        "Il Bosco è aperto",
        "Il Bosco delle Cento Voci è un posto aperto. Cerca disegni, storie nuove e voci "
        "che lo leggano ad alta voce.",
        pagina_aiuto(d), "aiuto", percorso="il-bosco-e-aperto.html"))

    scrivi("scarica.html", pagina(
        "Scarica il libro",
        "Leggi online, stampa o scarica Il Bosco delle Cento Voci.",
        pagina_scarica(d), "scarica", percorso="scarica.html"))

    scrivi("autrice.html", pagina(
        "L'autrice",
        f"Nota biografica di {AUTRICE}, autrice del Bosco delle Cento Voci.",
        pagina_autrice(d), "autrice", percorso="autrice.html"))

    scrivi("libro.html", pagina_libro(d))

    for i, s in enumerate(sezioni):
        precedente = sezioni[i - 1] if i > 0 else None
        successivo = sezioni[i + 1] if i < len(sezioni) - 1 else None
        scrivi(f"racconti/{s['file']}",
               pagina_racconto(d, s, precedente, successivo,
                               avvertenza=domande.get(s["slug"], {}).get("avvertenza")))

    scrivi("racconti/24-filastrocca-del-bosco.html", pagina_filastrocca(d, sezioni[-1]))

    scrivi("404.html", pagina_404(d))
    scrivi("assets/img/foglia.svg", favicon())
    scrivi("sitemap.xml", sitemap(d))
    scrivi("robots.txt", robots())
    scrivi(".nojekyll", "")

    print(f"Generate {len(scritti)} pagine in {SITO.relative_to(ROOT)}/")
    for p in scritti[:6]:
        print(f"  {p}")
    print(f"  racconti/  ({len(sezioni)} pagine)")


if __name__ == "__main__":
    main()
