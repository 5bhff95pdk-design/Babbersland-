# Chancellerie royale — chaîne de production du volume 2026-I.
# Buts : env · arbre · carte · hymne · vignettes · pdf · empreinte · controle · scelle · iconographie · lfs · tout · propre
# Hors venv, remplacer PY=.venv/bin/python par PY=python3 (make PY=python3).

PY      ?= .venv/bin/python
VENV    ?= .venv
PDF     := Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf

.DEFAULT_GOAL := tout
.PHONY: env arbre carte hymne vignettes pdf empreinte controle scelle iconographie lfs batterie workflows tout propre

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

workflows: ## installe le modèle de CI dans .github/workflows/ (à committer avec un jeton tenant « workflows »)
	@mkdir -p .github/workflows && cp sources/github_actions_continuite.yml .github/workflows/continuite.yml \
	  && rm -f .github/workflows/main.yml \
	  && echo ".github/workflows/continuite.yml installé, talon main.yml retiré." \
	  && echo "Pour l'activer (constat E-17/F-01 : une App ne peut pas pousser ce fichier) :" \
	  && echo "    git add .github/workflows/continuite.yml && git commit -m 'CI : installation du workflow' && git push" \
	  && echo "  ou, sans y toucher : github.com/settings/installations → Arena → Workflows : Read and write."

lfs: ## R1.6 : prépare le passage des binaires lourds en Git LFS (variante A′ — gouvernance/LFS_MIGRATION.md)
	@command -v git-lfs >/dev/null 2>&1 || (echo "git-lfs absent : l'installer d'abord, voir gouvernance/LFS_MIGRATION.md" && exit 1)
	git lfs install
	git lfs track "images/realistes/*.png" "images/vignettes/*.webp" "audio/*"
	git add -u .gitattributes
	git commit -m "LFS : galerie 2026-V, vignettes et audio hors Git (R1.6, variante A′)"
	@echo "Puis « git push » — étape qui exige l'accès au CDN GitHub (bloqué dans l'environnement d'agent, gouvernance/LFS_MIGRATION.md § 2)."

iconographie: ## scelle les maîtres d'illustration par leur nom (gouvernance/ICONOGRAPHIE.sha256)
	@cd $(CURDIR) && sha256sum images/*.png > gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "gouvernance/ICONOGRAPHIE.sha256 regreffé — $(words $(wildcard images/*.png)) maîtres scellés"

scelle: ## vérifie le gel des archives G et H et des maîtres d'illustration (E-18, E-23)
	@sha256sum --check --quiet gouvernance/ARCHIVE.sha256 \
	  && echo "archives 2026-G et 2026-H intactes"
	@test -f gouvernance/ICONOGRAPHIE.sha256 || (echo "aucun scellé des maîtres : lancer « make iconographie »" && exit 1)
	@sha256sum --check --quiet gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "maîtres d'illustration conformes au scellé ($$(grep -c . gouvernance/ICONOGRAPHIE.sha256) lignes)"

controle: ## continuité, parité des données, chroniques, parité du portail, artéfact, fraîcheur, géographie, archives
	$(PY) -m py_compile sources/*.py
	$(PY) sources/check_continuity.py
	$(PY) sources/check_canon.py
	$(PY) sources/check_chroniques.py
	$(PY) sources/check_pdf.py
	$(PY) sources/pdf_fingerprint.py --check
	$(PY) sources/check_geography.py
	$(PY) sources/check_portal.py
	$(PY) sources/empreinte_atlas.py --check
	$(MAKE) --no-print-directory scelle

# L'ordre est un contrôle, pas une commodité (constat E-21) : graver l'empreinte AVANT
# de la vérifier rend `--check` infaillible par construction. `empreinte` reste donc
# l'acte d'assentiment qui TERMINE la chaîne — jamais celui qui l'ouvre.
# La batterie casse des COPIES du dépôt : la référence n'est jamais touchée.
# Volontairement hors de `controle` et hors de la CI — elle coûte une minute et réécrit des scellés.
batterie: env
	$(PY) sources/test_mutations.py

tout: arbre hymne vignettes pdf controle empreinte ## la chaîne complète
	@echo "2026-I régénérée et contrôlée."

propre: ## nettoyages mineurs
	rm -rf sources/__pycache__
