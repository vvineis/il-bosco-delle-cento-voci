# -*- coding: utf-8 -*-
"""
Estrae il testo dal manoscritto .docx e produce docs/data/racconti.json

Uso:  python tools/estrai.py
"""
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # console Windows
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

ROOT = Path(__file__).resolve().parent.parent
DOCX = ROOT / "Il_Bosco_delle_Cento_Voci_completo.docx"
SINOSSI = ROOT / "Il_Bosco_delle_Cento_Voci_SINOSSI.docx"
OUT = ROOT / "docs" / "data" / "racconti.json"


def q(tag):
    return f"{{{W}}}{tag}"


def paragrafi(path):
    """Restituisce [(stile, testo)] preservando le interruzioni di riga come \n."""
    root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    body = root.find("w:body", NS)
    out = []
    for p in body.iter(q("p")):
        stile = ""
        pPr = p.find("w:pPr", NS)
        if pPr is not None:
            ps = pPr.find("w:pStyle", NS)
            if ps is not None:
                stile = ps.get(q("val"), "")
        pezzi = []
        for node in p.iter():
            if node.tag == q("t"):
                pezzi.append(node.text or "")
            elif node.tag == q("br"):
                pezzi.append("\n")
            elif node.tag == q("tab"):
                pezzi.append(" ")
        out.append((stile, "".join(pezzi)))
    return out


def pulisci(testo):
    righe = [re.sub(r"[ \t]+", " ", r).strip() for r in testo.split("\n")]
    righe = [r for r in righe if r]
    return "\n".join(righe)


def slugify(testo):
    t = unicodedata.normalize("NFKD", testo)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower().replace("’", " ").replace("'", " ")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


# Blocchi in versi da rendere come poesia (chiave: slug -> stringa iniziale del blocco)
VERSI = {
    "il-fiore-di-tilda": "Ci sono vite che durano un istante",
    "l-ultima-voce-del-bosco": "Nel Bosco che hai appena visitato",
}

# Nota tematica per chi legge insieme ai bambini
TEMI = {
    "premessa":
        "Il Bosco delle Cento Voci non è solo un luogo, ma un modo di ascoltare.",
    "i-piccoli-riti-del-bosco":
        "Piccoli gesti che ritornano e pensieri che non ci lasciano. Sull’amicizia che insegna ad accogliersi.",
    "la-volpe-che-cuciva-le-nuvole":
        "Dedicarsi a qualcosa che gli altri non comprendono. Sul coraggio di seguire ciò che ci rende noi stessi.",
    "l-albero-dei-campanellini":
        "Un albero che monopolizza tutta l’attenzione del Bosco. Una favola sulle "
        "notifiche, molto prima che si chiamassero così.",
    "la-civetta-che-non-voleva-perdersi-nulla":
        "Tenere sempre gli occhi aperti per non perdersi nulla. Sul timore di restare esclusi e sulla scoperta che non tutto ciò che accade merita di essere inseguito.",
    "il-corvo-che-ingigantiva-le-sue-gesta":
        "Quando pensiamo di dover essere straordinari per avere un posto nel mondo. Sulla bellezza delle imperfezioni che ci rendono noi stessi.",
    "il-tasso-che-collezionava-ombre":
        "Sull’accumulare oggetti e pensieri. E sull’importanza di scegliere con cura quei pochi "
        "che meritano di restare con noi.",
    "i-cunicoli-di-tamarinda":
        "Sull’illusione di essere sempre connessi con tutti e sulla bellezza di tornare presenti "
        "nel mondo.",
    "lo-stagno-degli-specchi":
        "Specchiarsi mille volte e non sentirsi mai abbastanza. Sull’immagine di sé, e su quanto poco "
        "basti a dire chi siamo.",
    "la-sorgente-disuguale":
        "La stessa acqua non raggiunge tutti allo stesso modo. Sulle disuguaglianze "
        "e su chi decide di non farci l’abitudine.",
    "il-carillon-del-tempo":
        "Sul lavoro spesso invisibile o dato per scontato, che però, pur nel suo piccolo, sostiene il mondo.",
    "la-cicala-che-collezionava-echi":
        "Cantare per sapere di essere ascoltati. Sul bisogno di conferme e sulla gioia liberatoria del liberarsene.",
    "la-libellula-che-non-trovava-il-suo-perche":
        "Non trovare la propria etichetta. Sul definirsi oltre i ruoli predefiniti e sulla scoperta"
        "che il nostro talento si compie quando siamo davvero noi stessi.",
    "il-prato-in-finito":
        "Una risorsa che sembra infinita...finché non finisce. Sui beni comuni e sulla cura di ciò che "
        "è di tutti.",
    "la-biblioteca-delle-foglie":
        "Le stagioni perdono la bussola e le foglie non sanno più che storia scrivere. Sul cambiamento climatico, "
        "la memoria e le storie ancora da scrivere.",
    "il-pipistrello-che-leggeva-il-buio":
        "Chi non vede come gli altri può vedere altro. Sui molti modi di abitare il mondo.",
    "la-nascita-dello-stagno":
        "Un ramoscello alla volta, finché ciò che sembrava impossibile prende forma. Sulla pazienza e sulla fiducia nei cambiamenti lenti.",
    "la-formica-infaticabile":
        "Chi sostiene il mondo sulle spalle finché non si spegne. Sull’importanza del lavoro condiviso e del vedere "
        "davvero l’altro.",
    "il-vento-smemorato":
        "Anche chi ha sempre saputo la strada può smarrirla. Sulla memoria incarnata e l'importanza degli affetti per ricordare chi siamo.",
    "il-serpente-che-ascoltava-i-colori":
        "Sensi che si tengono per mano. Sui molti modi di percepire ciò che ci circonda e il regalo prezioso dei cinque sensi.",
    "un-insolita-amicizia":
        "Il sapore perduto nel miele e la fatica di fermarsi. Sulle due forme della tristezza e la cura dell’amicizia.",
    "il-fiore-di-tilda":
        "Il racconto del congedo di Tilda. Una storia sul lutto, da leggere con calma e, se "
        "serve, con qualcuno accanto.",
    "l-ultima-voce-del-bosco":
        "La centesima voce non è di nessuno, è di tutti insieme.",
}


def estrai_libro():
    ps = paragrafi(DOCX)

    dedica = []
    sezioni = []
    corrente = None
    stato = "testa"

    for stile, grezzo in ps:
        testo = pulisci(grezzo)
        if not testo:
            continue

        if stile.startswith("TOC") or testo == "Indice":
            stato = "indice"
            continue

        if stile.startswith("Heading"):
            stato = "corpo"
            corrente = {
                "titolo": testo[0].upper() + testo[1:],
                "slug": slugify(testo),
                "paragrafi": [],
            }
            sezioni.append(corrente)
            continue

        if stato == "testa":
            if testo.upper() == "IL BOSCO DELLE CENTO VOCI":
                continue
            dedica.append(testo)
        elif stato == "corpo" and corrente is not None:
            corrente["paragrafi"].append(testo)

    # separa i blocchi in versi
    for sez in sezioni:
        marcatore = VERSI.get(sez["slug"])
        blocchi = []
        versi = []
        in_versi = False
        for testo in sez["paragrafi"]:
            if marcatore and testo.startswith(marcatore):
                in_versi = True
            if in_versi:
                versi.append(testo)
            else:
                blocchi.append(testo)
        sez["paragrafi"] = blocchi
        sez["versi"] = versi

    # numerazione: la premessa non conta come racconto
    n = 0
    for sez in sezioni:
        if sez["slug"] == "premessa":
            sez["numero"] = None
        else:
            n += 1
            sez["numero"] = n
        sez["tema"] = TEMI.get(sez["slug"], "")
        sez["file"] = f"{len([s for s in sezioni[:sezioni.index(sez)+1]]):02d}-{sez['slug']}.html"

    return dedica, sezioni


def estrai_semplice(path, salta=0):
    fuori = []
    for _stile, grezzo in paragrafi(path):
        testo = pulisci(grezzo)
        if testo:
            fuori.append(testo)
    return fuori[salta:]


def gia_estratto():
    """Il racconti.json di prima, se c'è: serve quando i .docx non sono su
    questo computer e non c'è niente da rileggere."""
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return None


def main():
    vecchio = gia_estratto()

    if not DOCX.exists():
        if not vecchio:
            print(f"Manca {DOCX.name} e non c'è nemmeno un {OUT.name} da cui ripartire.")
            print("Rimetti il manoscritto al suo posto: senza, non c'è nessun testo.")
            sys.exit(2)
        print(f"{DOCX.name} non è su questo computer: si tiene il testo già estratto")
        print(f"  in {OUT.relative_to(ROOT).as_posix()} ({len(vecchio['sezioni'])} sezioni).")
        print("  Serve rimettere il manoscritto solo per cambiare il testo dei racconti.")
        return

    dedica, sezioni = estrai_libro()

    if SINOSSI.exists():
        sinossi = estrai_semplice(SINOSSI)
    else:
        sinossi = vecchio["sinossi"] if vecchio else []
        print(f"{SINOSSI.name} non c'è: si tiene la sinossi già estratta.")
    if SINOSSI.exists():
        # via intestazione, etichetta "SINOSSI:" e recapiti
        sinossi = [t for t in sinossi
                   if t.upper() != "IL BOSCO DELLE CENTO VOCI"
                   and not t.startswith("Recapito")
                   and not t.startswith("Email")]
        if sinossi and sinossi[0].startswith("SINOSSI:"):
            sinossi[0] = sinossi[0][len("SINOSSI:"):].strip()
        sinossi = [t for t in sinossi if t]

    dati = {
        "titolo": "Il Bosco delle Cento Voci",
        "autrice": "Vittoria Vineis",
        "dedica": dedica,
        "sinossi": sinossi,
        "sezioni": sezioni,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{OUT.relative_to(ROOT)}")
    print(f"  {len(sezioni)} sezioni, {sum(len(s['paragrafi']) for s in sezioni)} paragrafi")
    for s in sezioni:
        num = f"{s['numero']:2d}." if s["numero"] else "  ·"
        versi = f"  (+{len(s['versi'])} versi)" if s["versi"] else ""
        manca = "  ⚠ senza nota tematica" if not s["tema"] else ""
        print(f"  {num} {s['titolo']}  [{s['slug']}]{versi}{manca}")


if __name__ == "__main__":
    main()
