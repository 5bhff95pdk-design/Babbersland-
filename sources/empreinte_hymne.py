#!/usr/bin/env python3
"""Empreinte sémantique de l'enregistrement de référence de l'hymne national (R1.4.c).

L'hymne est **décrété** (Avis royal n° 8) et son enregistrement entre dans
`make tout` : il doit donc être reproductible, et la CI doit le vérifier
sans se laisser embarquer par le hasard des octets.

Ce que le contrôle compare. Le fichier `audio/hymne_national_babberland.wav` est
synthétisé par la bibliothèque standard (graine 1847) : ses octets ne dépendent
théoriquement que de `math.sin` et du drapeau IEEE 754. En pratique, un ULP de la
libm d'une autre distribution, ou un chunk RIFF ajouté par une autre version de
`wave`, suffit à changer le SHA-256 sans changer une note. La charge ignore ces
hasards et retient ce qui **s'entend** :

- `frames` / `rate` / `bits` / `chan` : la géométrie du signal (72,5 s à 22 050 Hz,
  16 bits, mono) — la durée est la promesse du dossier officiel (§ V) ;
- `profil` : l'**enveloppe** du signal, RMS par fenêtre de 250 ms quantifiée sur 8 bits,
  hachée — elle bouge dès qu'une entrée sort, qu'une nuance change ou qu'un silence
  se raccourcit, et ne bouge pas d'un cheveu de codage ;
- `pcm8` : le signal entier **replié sur 8 bits** puis haché — une permutation de deux
  notes de même durée change ce haché, un ULP d'arrondi non ;
- `crete` : l'amplitude crête à crête normalisée (-2,9 dBFS), au millième.

Ce que le contrôle ignore, et le dit : les chunks RIFF autres que `fmt `/`data`
(un `LIST/INFO` horodaté, par exemple) ne sont pas dans la charge ; ils sont
**signalés** dans le diagnostic, pour qu'une tolérance ne devienne jamais un angle mort.

Le reste de la politique est celui de R1.4.b (voir `sources/sceaux.py`) : on grave
l'ensemble des charges observées, une charge inédite bloque, une charge légitime
d'un nouvel environnement s'accepte à la main et se commite.

Usage :
    python sources/empreinte_hymne.py                          # affiche la charge courante
    python sources/empreinte_hymne.py --write [--variante N]   # grave la charge courante
    python sources/empreinte_hymne.py --accepter '<charge>' N # grave une charge observée (ex. CI)
    python sources/empreinte_hymne.py --check                  # échoue si la charge est inédite
"""
from __future__ import annotations

import array
import hashlib
import struct
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sources"))

from sceaux import Sceau, STAMP, sha256  # noqa: E402

WAV = ROOT / "audio" / "hymne_national_babberland.wav"
FENETRE_MS = 250          # granularité de l'enveloppe : 50 ms = une double-croche à ♩=60

ENTETE = (
    "# Signé par sources/empreinte_hymne.py — modèle « variantes acceptées » (R1.4.c).\n"
    "# Le WAV est synthétisé par la bibliothèque standard (graine 1847) : bit-stable\n"
    "# par machine, pas entre machines (un ULP de libm, un chunk RIFF ajouté).\n"
    "# La charge compare ce qui s'entend :\n"
    "#   frames/rate/bits/chan : géométrie du signal (72,5 s à 22 050 Hz, 16 bits, mono) ;\n"
    "#   profil : RMS par fenêtre de 250 ms, quantifié sur 8 bits, haché ;\n"
    "#   pcm8   : tout le signal replié sur 8 bits, haché (sensible à l'ordre des notes) ;\n"
    "#   crete  : amplitude crête normalisée, au millième.\n"
    "# Les chunks RIFF hors fmt /data sont ignorés par la charge et signalés au\n"
    "# diagnostic : une tolérance doit rester nommée, pas devenir un angle mort.\n"
    "# Nouvelle machine légitime ? Lire l'annotation CI, puis\n"
    "# `python sources/empreinte_hymne.py --accepter '<charge>' <étiquette>`.\n"
)

MOTIF = (r"frames:\d+\|rate:\d+\|bits:\d+\|chan:\d+\|profil:[0-9a-f]{32}"
         r"\|pcm8:[0-9a-f]{32}\|crete:0\.\d{3}")


def chunks_riff(chemin: Path) -> list[tuple[str, int]]:
    """Liste des chunks RIFF du WAV — l'audit que R1.4.c demandait (timestamp ?)."""
    with chemin.open("rb") as f:
        entete = f.read(12)
        if entete[:4] != b"RIFF" or entete[8:12] != b"WAVE":
            return []
        trouve = []
        while True:
            tete = f.read(8)
            if len(tete) < 8:
                return trouve
            quatre, taille = tete[:4].decode("latin-1"), struct.unpack("<I", tete[4:])[0]
            trouve.append((quatre, taille))
            f.seek(taille + (taille % 2), 1)   # les chunks sont paddés à 2 octets


def echantillons(w: wave.WAVE_read) -> array.array:
    """Le signal en int16 (mono implicite : les canaux sont fusionnés s'il y en a plusieurs)."""
    brut = w.readframes(w.getnframes())
    e = array.array("h")
    e.frombytes(brut[: len(brut) - len(brut) % 2])
    if sys.byteorder == "big":
        e.byteswap()
    canaux = w.getnchannels()
    if canaux > 1:
        e = array.array("h", [sum(e[i:i + canaux]) // canaux
                              for i in range(0, len(e) - canaux + 1, canaux)])
    return e


def charge_courante() -> str | None:
    if not WAV.is_file():
        return None
    with wave.open(str(WAV), "rb") as w:
        frames, rate, canaux, largeur = (w.getnframes(), w.getframerate(),
                                         w.getnchannels(), w.getsampwidth())
        e = echantillons(w)
    if largeur != 2:
        return None          # hors promesse du dossier : le contrôle refusera, faute de gravure
    n = len(e)
    taille_fenetre = max(1, rate * FENETRE_MS // 1000)
    profil = bytearray()
    for i in range(0, n, taille_fenetre):
        morceau = e[i:i + taille_fenetre]
        energie = sum(x * x for x in morceau) / max(1, len(morceau))
        profil.append(min(255, int(energie ** 0.5) * 256 // 12000))
    pli = bytes((x + 32768) >> 8 for x in e)      # repli 16 bits → 8 bits, sans table
    crete = (max(abs(x) for x in e) if n else 0) / 32767.0
    return (f"frames:{n}|rate:{rate}|bits:{largeur * 8}|chan:{canaux}"
            f"|profil:{hashlib.md5(bytes(profil)).hexdigest()}"
            f"|pcm8:{hashlib.md5(pli).hexdigest()}"
            f"|crete:{crete:.3f}")


def diagnostic() -> str:
    if not WAV.is_file():
        return "fichier absent"
    hors = [c for c, _ in chunks_riff(WAV) if c not in ("fmt ", "data")]
    return (f"sha256={sha256(WAV)[:16]}… poids={WAV.stat().st_size:,} o "
            f"chunks={chunks_riff(WAV)}"
            + (f" — ATTENTION chunks hors fmt /data ignorés par la charge : {hors}" if hors else ""))


sceau = Sceau(marqueur="HYMNE NATIONAL", prefixe="hymne", entete=ENTETE, motif=MOTIF,
              charge=charge_courante, diagnostic=diagnostic, ligne_tete="hymne_pcm",
              libelle="hymne")


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if "--chunks" in argv:
        for quatre, taille in chunks_riff(WAV):
            signe = "" if quatre in ("fmt ", "data") else "  ← hors charge, signalé"
            print(f"  chunk {quatre!r} : {taille:,} octets{signe}")
        return 0
    return sceau.main([a for a in argv if a != "--chunks"], descriptif=__doc__.splitlines()[0])


if __name__ == "__main__":
    raise SystemExit(main())
