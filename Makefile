# Chancellerie royale — chaîne de production du volume 2026-I.
# Buts : env · arbre · carte · hymne · vignettes · pdf · empreinte · empreinte-atlas · empreinte-arbre · manifest · controle · scelle · iconographie · galerie · lfs · tout · propre
# Hors venv, remplacer PY=.venv/bin/python par PY=python3 (make PY=python3).

PY      ?= .venv/bin/python
VENV    ?= .venv
PDF     := Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf

.DEFAULT_GOAL := tout
.PHONY: env arbre carte hymne vignettes pdf empreinte empreinte-atlas empreinte-arbre empreinte-hymne empreinte-vignettes manifest controle scelle iconographie galerie lfs batterie workflows tout propre

env: ## crée le venv et y épingle les dépendances (contournement PEP 668, constat E-11)
	@test -x $(PY) || python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -r requirements.txt
	@echo "environnement prêt : $(PY)"

arbre: ## régénère l'arbre généalogique (déterministe au bit près)
	$(PY) sources/generate_genealogy.py

carte: ## atlas géographique (proposé, non décrété) : SVG, PNG, HTML
	$(PY) sources/generate_map.py
	$(PY) sources/check_geography.py
	$(PY) sources/empreinte_atlas.py --check

hymne: ## hymne national (décrété, Avis royal n° 8) : enregistrement de référence du refrain
	$(PY) sources/generate_hymne.py

vignettes: ## vignettes WebP du portail (les maîtres PNG ne sont pas touchés, les scellés non plus)
	$(PY) sources/generate_vignettes.py

pdf: $(PDF) ## régénère l'encyclopédie PDF 2026-I

$(PDF): ENCYCLOPEDIE_CONSOLIDEE_2026_I.md sources/generate_encyclopedie_2026_i.py sources/babberland_images.py $(wildcard images/*.png)
	$(PY) sources/generate_encyclopedie_2026_i.py

empreinte: ## grave l'empreinte sémantique du PDF publié — acte d'assentiment, pas un contrôle
	$(PY) sources/pdf_fingerprint.py --write

empreinte-atlas: ## grave l'empreinte sémantique de l'Atlas (SVG/PNG/HTML) — analogue à `empreinte`
	$(PY) sources/empreinte_atlas.py --write

empreinte-arbre: ## grave l'empreinte sémantique de l'Arbre (PNG) — acte d'assentiment, comme `empreinte`
	$(PY) sources/empreinte_arbre.py --write

empreinte-hymne: ## grave la charge sémantique de l'enregistrement de référence (R1.4.c)
	$(PY) sources/empreinte_hymne.py --write

empreinte-vignettes: ## grave la charge sémantique des vignettes du portail (R1.4.d)
	$(PY) sources/empreinte_vignettes.py --write

workflows: ## installe les deux modèles de CI dans .github/workflows/ (à committer avec un jeton tenant « workflows »)
	@mkdir -p .github/workflows && cp sources/github_actions_continuite.yml .github/workflows/continuite.yml \
	  && cp sources/github_actions_batterie.yml .github/workflows/batterie.yml \
	  && rm -f .github/workflows/main.yml \
	  && echo ".github/workflows/continuite.yml et batterie.yml installés, talon main.yml retiré." \
	  && echo "Pour les activer (constat E-17/F-01 : une App ne peut pas pousser ce fichier) :" \
	  && echo "    git add .github/workflows && git commit -m 'CI : installation des workflows' && git push" \
	  && echo "  ou, sans y toucher : github.com/settings/installations → Arena → Workflows : Read and write."

lfs: ## R1.6 : prépare le passage des binaires lourds en Git LFS (variante A′ — gouvernance/LFS_MIGRATION.md)
	@command -v git-lfs >/dev/null 2>&1 || (echo "git-lfs absent : l'installer d'abord, voir gouvernance/LFS_MIGRATION.md" && exit 1)
	git lfs install
	git lfs track "images/realistes/*.png" "images/vignettes/*.webp" "audio/*"
	git add -u .gitattributes
	git commit -m "LFS : galerie 2026-V, vignettes et audio hors Git (R1.6, variante A′)"
	@echo "Puis « git push » — étape qui exige l'accès au CDN GitHub (bloqué dans l'environnement d'agent, gouvernance/LFS_MIGRATION.md § 2)."

manifest: ## R1.3 : regrave le manifeste des livrables canoniques (gouvernance/MANIFEST.sha256) — acte d'assentiment
	$(PY) sources/make_manifest.py

iconographie: ## scelle les maîtres d'illustration par leur nom (gouvernance/ICONOGRAPHIE.sha256)
	@cd $(CURDIR) && sha256sum images/*.png > gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "gouvernance/ICONOGRAPHIE.sha256 regreffé — $(words $(wildcard images/*.png)) maîtres scellés"

galerie: ## R1.9 : scelle la galerie photoréaliste du portail par son nom (gouvernance/GALERIE.sha256)
	@cd $(CURDIR) && sha256sum images/realistes/*.png > gouvernance/GALERIE.sha256 \
	  && echo "gouvernance/GALERIE.sha256 regreffé — $(words $(wildcard images/realistes/*.png)) clichés scellés"

# R1.9 : la galerie (77 pièces, 211 Mio) était le seul corpus d'images sans scellé —
# la charge des vignettes (R1.4.d) ne regarde que les dérivés : un cliché retouché
# dont on OUBLIE de régénérer les vignettes passait. Plus maintenant.
# R1.8 : les workflows installés doivent être l'octet de leurs modèles — un
# `.github/workflows/*.yml` retouché à la main désaligne la chaîne de son contrat,
# en silence (classe E-09/C-01). La parité est un gel comme les autres : elle se vérifie.
scelle: ## gel des archives G et H, des maîtres, de la galerie (R1.9) + parité des workflows (R1.8)
	@sha256sum --check --quiet gouvernance/ARCHIVE.sha256 \
	  && echo "archives 2026-G et 2026-H intactes"
	@test -f gouvernance/ICONOGRAPHIE.sha256 || (echo "aucun scellé des maîtres : lancer « make iconographie »" && exit 1)
	@sha256sum --check --quiet gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "maîtres d'illustration conformes au scellé ($$(grep -c . gouvernance/ICONOGRAPHIE.sha256) lignes)"
	@test -f gouvernance/GALERIE.sha256 || (echo "aucun scellé de la galerie : lancer « make galerie »" && exit 1)
	@sha256sum --check --quiet gouvernance/GALERIE.sha256 \
	  && echo "galerie photoréaliste conforme au scellé ($$(grep -c . gouvernance/GALERIE.sha256) lignes)"
	@cmp -s sources/github_actions_continuite.yml .github/workflows/continuite.yml \
	  && cmp -s sources/github_actions_batterie.yml .github/workflows/batterie.yml \
	  && echo "workflows installés fidèles à leurs modèles (2 comparaisons octet à octet)" \
	  || (echo "workflow installé désaligné de son modèle : relancer « make workflows » et committer (R1.8)" && exit 1)

controle: ## continuité, parité des données, chroniques, portail, artéfact, fraîcheur, manifeste (R1.3), géographie, quatre sceaux d'artéfacts, archives
	$(PY) -m py_compile sources/*.py
	$(PY) sources/check_continuity.py
	$(PY) sources/check_canon.py
	$(PY) sources/check_chroniques.py
	$(PY) sources/check_pdf.py
	$(PY) sources/pdf_fingerprint.py --check
	$(PY) sources/check_manifest.py --check
	$(PY) sources/check_geography.py
	$(PY) sources/check_portal.py
	$(PY) sources/empreinte_atlas.py --check
	$(PY) sources/empreinte_arbre.py --check
	$(PY) sources/empreinte_hymne.py --check
	$(PY) sources/empreinte_vignettes.py --check
	$(MAKE) --no-print-directory scelle

# L'ordre est un contrôle, pas une commodité (constat E-21) : graver l'empreinte AVANT
# de la vérifier rend `--check` infaillible par construction. `empreinte` reste donc
# l'acte d'assentiment qui TERMINE la chaîne — jamais celui qui l'ouvre.
# La batterie casse des COPIES du dépôt : la référence n'est jamais touchée — et le
# workflow `batterie.yml` le vérifie (`git diff --quiet` après la course), au lieu de
# le promettre. Volontairement hors de `controle` : elle coûte 2 min 26 s (mesure du
# 1ᵉʳ sept. 2026, 24 scénarios) et réécrit
# des scellés dans ses laboratoires. Elle court à HORAIRES en CI (lundi 03:17 UTC,
# plus `workflow_dispatch`) — pas à chaque push, mais assez souvent pour qu'un
# contrôle émasculé ne survive pas une semaine (classe de défaut C-01).
batterie: env
	$(PY) sources/test_mutations.py

tout: arbre hymne vignettes pdf controle empreinte ## la chaîne complète
	@echo "2026-I régénérée et contrôlée."

propre: ## nettoyages mineurs
	rm -rf sources/__pycache__
