#!/usr/bin/env python3
"""Enregistrement de référence de l'hymne national « Debout, tout doucement ».

Dossier HYMNE-01 (RM-2026-IV). L'hymne est *proposé, non décrété* : ce générateur
n'entre ni dans `make tout` ni dans la CI, pas plus que l'atlas (`make carte`).

Principes
---------
1. **Source unique** : la partition ABC vit dans `gouvernance/HYMNE_NATIONAL.md`,
   bloc ```` ```abc ````. Le présent script la lit, l'analyse et la chante note à
   note — le document et l'enregistrement ne peuvent pas diverger.
2. **Déterminisme au bit près** : bibliothèque standard seule (wave, math,
   struct, random), graine 1847 (l'année de la Nappe). Deux exécutions donnent
   le même fichier ; aucune dépendance à épingler, contrairement au PDF.
3. **Auto-contrôle** : le générateur refuse de chanter si la partition ne tient
   pas ses promesses — 17 mesures, 68 temps, 56 notes, 55 syllabes,
   1 queue instrumentale, 72,5 secondes pile.

Chaîne sonore : Pshitt réglementaire (0,5 s) → refrain complet (17 mesures à
♩=60, cuivres posés et basse « aux chopes ») → silence contemplatif final
(4 s, une par épreuve des Jeux Lents).
"""
from __future__ import annotations

import hashlib
import math
import random
import re
import struct
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTITION = ROOT / "gouvernance" / "HYMNE_NATIONAL.md"
SORTIE = ROOT / "audio" / "hymne_national_babberland.wav"

SR = 22050                 # fréquence d'échantillonnage (Hz)
DEUX_PI = 2.0 * math.pi
GRAINE = 1847              # l'année de la Nappe — le hasard aussi a une mémoire

# Promesses du dossier officiel (§ III et § V) : le générateur les vérifie.
MESURES_ATTENDUES = 17
TEMPS_ATTENDUS = 68        # 17 mesures × 4 temps, à ♩=60 → 68 s de chant
NOTES_ATTENDUES = 57       # dont la 17e mesure, instrumentale
SYLLABES_ATTENDUS = 56
QUEUE_INSTRUMENTALE = 1    # l'accord final G, sans syllabe
PSHITT = 0.5               # décapsulage réglementaire (s)
SILENCE_FINAL = 4.0        # une seconde par épreuve des Jeux Lents (proposé)

# Basse « aux chopes » : fondamentale (ronde) + quinte (à la 3e temps), par mesure.
# G2 E2 A2 D3 G2 G2 C3 G2 G2 D3 G2 D3 E2 D3 G2 D3 G2
BASSE = [98.00, 82.41, 110.00, 146.83, 98.00, 98.00, 130.81, 98.00,
         98.00, 146.83, 98.00, 146.83, 82.41, 146.83, 98.00, 146.83, 98.00]

# Nuance par mesure : crescendo vers la fermata, écho plus doux, reprise pleine.
NUANCES = [0.62, 0.66, 0.70, 0.72, 0.76, 0.80, 0.78, 0.82,
           0.86, 0.94, 0.82, 0.62, 0.70, 0.78, 0.88, 0.94, 1.00]

# Timbres : cuivres posés (le chant), bourdon feutré (la basse).
HARMONIQUES_CHANT = [1.00, 0.50, 0.33, 0.22, 0.14, 0.09, 0.05]
HARMONIQUES_BASSE = [1.00, 0.30, 0.12]

NOTE = re.compile(r"^([A-Ga-g])([,']*)(\d*)$")
DIATONIQUE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


# ─────────────────────────────────────────────────────────────────────────────
# 1. Lecture de la partition (ABC simplifié du dossier officiel)
# ─────────────────────────────────────────────────────────────────────────────

def extraire_abc(texte: str) -> list[str]:
    m = re.search(r"```abc\n(.*?)```", texte, re.S)
    if not m:
        raise SystemExit("aucun bloc ```abc trouvé dans gouvernance/HYMNE_NATIONAL.md")
    return m.group(1).splitlines()


def analyser(lignes: list[str]):
    tempo, duree_temps = 60, 1.0
    notes: list[tuple[float, float, float]] = []   # (départ s, durée s, fréquence Hz)
    silences = 0
    t = 0.0
    syllabes: list[str] = []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne or ligne.startswith("%"):
            continue
        if ligne.startswith("w:"):
            # Les signes seuls (« ! », « — », « : ») ne sont pas des syllabes :
            # ils s'exclament, ils ne chantent pas.
            syllabes.extend(t for t in ligne[2:].split() if re.search(r"[^\W\d_]", t))
            continue
        m = re.match(r"Q:\s*1/4\s*=\s*(\d+)", ligne)
        if m:
            tempo = int(m.group(1))
            duree_temps = 60.0 / tempo
            continue
        if re.match(r"[A-Z]:", ligne):            # X: T: C: M: L: K: — en-têtes
            continue
        for jeton in ligne.split():
            if jeton in ("|", "|]"):
                continue
            m = NOTE.match(jeton)
            if not m:                              # z, z2 : silence, il n'attend rien
                if not jeton.startswith("z"):
                    raise SystemExit(f"jeton ABC non reconnu : {jeton!r}")
                silences += 1
                t += int(jeton[1:] or 1) * duree_temps
                continue
            lettre, octaves, chiffre = m.groups()
            midi = 60 + DIATONIQUE[lettre.upper()]
            if lettre.islower():
                midi += 12
            midi += 12 * octaves.count("'") - 12 * octaves.count(",")
            if lettre.upper() == "F":              # K:G — le fa est dièsé, il chante en sol
                midi += 1
            duree = int(chiffre or 1) * duree_temps
            notes.append((t, duree, 440.0 * 2.0 ** ((midi - 69) / 12.0)))
            t += duree
    return tempo, notes, silences, syllabes, t


# ─────────────────────────────────────────────────────────────────────────────
# 2. Synthèse (bibliothèque standard, déterminisme garanti par la graine)
# ─────────────────────────────────────────────────────────────────────────────

def env(n: int, attaque: float, retour: float) -> list[float]:
    """Enveloppe : montée douce, tenue, retombée sans bruit de choc."""
    na, nr = int(attaque * SR), int(retour * SR)
    e = [1.0] * n
    for i in range(min(na, n)):
        e[i] = (i + 1) / na
    for i in range(min(nr, n)):
        e[n - 1 - i] *= (i + 1) / nr
    return e


def voix(t_debut: float, duree: float, freq: float, amplitude: float,
         harmoniques: list[float], vibrato: float = 0.0) -> None:
    """Ajoute une note dans le tampon global (phase intégrée échantillon par échantillon)."""
    i0 = int(round(t_debut * SR))
    n = int(round(duree * SR)) - SR // 50          # souffle de 20 ms entre les notes
    if n <= 0:
        return
    envelope = env(n, 0.020, 0.090)
    phase = 0.0
    f_vib, profondeur = 5.2, vibrato
    for i in range(n):
        t = i / SR
        f = freq * (1.0 + profondeur * math.sin(f_vib * DEUX_PI * t)) if (t > 0.15 and profondeur) else freq
        phase += DEUX_PI * f / SR
        s = 0.0
        for k, a in enumerate(harmoniques, start=1):
            s += a * math.sin(phase * k)
        TAMPON[i0 + i] += amplitude * envelope[i] * s / sum(harmoniques)


def pshitt(t_debut: float, duree: float) -> None:
    """Le Pshitt réglementaire (Décapsulage Synchronisé, épreuve 4 des Jeux Lents)."""
    rng = random.Random(GRAINE)
    i0 = int(round(t_debut * SR))
    n = int(round(duree * SR))
    precedent = 0.0
    for i in range(n):
        brut = rng.uniform(-1.0, 1.0)
        passe_haut = brut - precedent                # la mousse ne gronde pas, elle pétille
        precedent = brut
        a = 0.22 * math.exp(-i / (0.080 * SR))
        if i > n - SR // 20:                         # fondu de sortie, la canette est ouverte
            a *= (n - 1 - i) / (SR // 20)
        TAMPON[i0 + i] += a * passe_haut


def accord_final(t_debut: float, duree: float) -> None:
    """Sol majeur empilé (G2 à d5), tintement grave et patient."""
    registres = [98.00, 196.00, 246.94, 293.66, 392.00, 493.88, 587.33]
    poids = [0.30, 0.24, 0.18, 0.16, 0.20, 0.12, 0.10]
    i0 = int(round(t_debut * SR))
    n = int(round(duree * SR))
    for f, a in zip(registres, poids):
        phase = 0.0
        for i in range(n):
            phase += DEUX_PI * f / SR
            TAMPON[i0 + i] += a * math.exp(-i / (1.8 * SR)) * (
                0.6 * math.sin(phase) + 0.4 * math.sin(2 * phase))


# ─────────────────────────────────────────────────────────────────────────────
# 3. Rite : contrôler d'abord, chanter ensuite, rendre compte à la fin
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    lignes = extraire_abc(PARTITION.read_text(encoding="utf-8"))
    tempo, notes, silences, syllabes, duree_chant = analyser(lignes)

    # — Les promesses du dossier sont des contrôles, pas des compliments (cf. E-21).
    temps = round(duree_chant * tempo / 60)
    mesures = temps // 4
    erreurs = []
    if mesures != MESURES_ATTENDUES or temps != TEMPS_ATTENDUS:
        erreurs.append(f"partition : {mesures} mesures / {temps} temps (attendu : 17 / 68)")
    if len(notes) != NOTES_ATTENDUES:
        erreurs.append(f"{len(notes)} notes (attendu : {NOTES_ATTENDUES})")
    if len(syllabes) != SYLLABES_ATTENDUS:
        erreurs.append(f"{len(syllabes)} syllabes (attendu : {SYLLABES_ATTENDUS})")
    if len(notes) - len(syllabes) != QUEUE_INSTRUMENTALE:
        erreurs.append(f"queue instrumentale : {len(notes) - len(syllabes)} (attendu : 1)")
    if not (len(BASSE) == len(NUANCES) == mesures):
        erreurs.append(f"basse {len(BASSE)} mesure(s), nuances {len(NUANCES)}, partition {mesures}")
    if erreurs:
        raise SystemExit("refus de chanter — " + " ; ".join(erreurs))

    duree_totale = PSHITT + duree_chant + SILENCE_FINAL
    n_total = int(round(duree_totale * SR))
    if abs(n_total / SR - 72.5) > 1e-6:
        raise SystemExit(f"durée {n_total / SR:.3f} s ≠ 72,500 s : le dossier ment")

    global TAMPON
    TAMPON = [0.0] * n_total

    # 1. Le Pshitt ouvre : quatre canettes, mais on n'en entend qu'une, c'est l'unité.
    pshitt(0.0, PSHITT)

    # 2. Le chant, à sa place, avec sa nuance — une nuance par mesure.
    for t, duree, freq in notes:
        voix(PSHITT + t, duree, freq, 0.42 * NUANCES[int(t // 4.0)],
             HARMONIQUES_CHANT, vibrato=0.003)

    # 3. La basse aux chopes : une fondamentale qui ne se presse pas, une quinte polie.
    for i, fondamentale in enumerate(BASSE):
        depart = PSHITT + i * 4.0
        voix(depart, 4.0, fondamentale, 0.34, HARMONIQUES_BASSE)
        voix(depart + 2.0, 2.0, fondamentale * 1.5, 0.26, HARMONIQUES_BASSE)

    # 4. L'accord final (17e mesure, instrumentale — la 56e note chante déjà le sol).
    accord_final(PSHITT + 16 * 4.0, 4.0)

    # 5. Normalisation douce (-2,9 dBFS) et gravure.
    crete = max(abs(x) for x in TAMPON)
    facteur = 0.72 / crete
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(SORTIE), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(b"".join(
            struct.pack("<h", max(-32768, min(32767, int(x * facteur * 32767))))
            for x in TAMPON))

    md5 = hashlib.md5(SORTIE.read_bytes()).hexdigest()
    print(f"hymne chanté : {mesures} mesures, {len(notes)} notes, {len(syllabes)} syllabes, "
          f"{silences} silence(s) noté(s)")
    print(f"refrain : {duree_chant:.1f} s à ♩={tempo} ; total {n_total / SR:.3f} s "
          f"({PSHITT} s de Pshitt + {SILENCE_FINAL:.1f} s de contemplation)")
    print(f"gravé : {SORTIE.relative_to(ROOT)} ({SORTIE.stat().st_size:,} octets, md5 {md5[:12]}…)")
    print("reproductible au bit près : graine 1847, bibliothèque standard seule.")


if __name__ == "__main__":
    main()
