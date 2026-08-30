# Chancellerie royale — chaîne de production du volume 2026-I.
# Buts : env · arbre · carte · hymne · pdf · empreinte · controle · scelle · iconographie · tout · propre
# Hors venv, remplacer PY=.venv/bin/python par PY=python3 (make PY=python3).

PY      ?= .venv/bin/python
VENV    ?= .venv
PDF     := Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf

.DEFAULT_GOAL := tout
.PHONY: env arbre carte hymne pdf empreinte controle scelle iconographie batterie workflows tout propre

env: ## crée le venv et y épingle les dépendances (contournement PEP 668, constat E-11)
	@test -x $(PY) || python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -r requirements.txt
	@echo "environnement prêt : $(PY)"

arbre: ## régénère l'arbre généalogique (déterministe au bit près)
	$(PY) sources/generate_genealogy.py

carte: ## atlas géographique (proposé, non décrété) : SVG, PNG, HTML
	$(PY) sources/generate_map.py

hymne: ## hymne national (décrété, Avis royal n° 8) : enregistrement de référence du refrain
	$(PY) sources/generate_hymne.py

pdf: $(PDF) ## régénère l'encyclopédie PDF 2026-I

$(PDF): ENCYCLOPEDIE_CONSOLIDEE_2026_I.md sources/generate_encyclopedie_2026_i.py sources/babberland_images.py $(wildcard images/*.png)
	$(PY) sources/generate_encyclopedie_2026_i.py

empreinte: ## grave l'empreinte sémantique du PDF publié — acte d'assentiment, pas un contrôle
	$(PY) sources/pdf_fingerprint.py --write

workflows: ## installe le modèle de CI dans .github/workflows/ (à committer avec un jeton tenant « workflows »)
	@mkdir -p .github/workflows && cp sources/github_actions_continuite.yml .github/workflows/continuite.yml \
	  && rm -f .github/workflows/main.yml \
	  && echo ".github/workflows/continuite.yml installé, talon main.yml retiré — le pousser nécessite la permission « workflows » pour l'App."

iconographie: ## scelle les maîtres d'illustration par leur nom (gouvernance/ICONOGRAPHIE.sha256)
	@cd $(CURDIR) && sha256sum images/*.png > gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "gouvernance/ICONOGRAPHIE.sha256 regreffé — $(words $(wildcard images/*.png)) maîtres scellés"

scelle: ## vérifie le gel des archives G et H et des maîtres d'illustration (E-18, E-23)
	@sha256sum --check --quiet gouvernance/ARCHIVE.sha256 \
	  && echo "archives 2026-G et 2026-H intactes"
	@test -f gouvernance/ICONOGRAPHIE.sha256 || (echo "aucun scellé des maîtres : lancer « make iconographie »" && exit 1)
	@sha256sum --check --quiet gouvernance/ICONOGRAPHIE.sha256 \
	  && echo "maîtres d'illustration conformes au scellé ($$(grep -c . gouvernance/ICONOGRAPHIE.sha256) lignes)"

controle: ## continuité, parité des données, parité du portail, artéfact, fraîcheur, géographie, archives
	$(PY) -m py_compile sources/*.py
	$(PY) sources/check_continuity.py
	$(PY) sources/check_canon.py
	$(PY) sources/check_pdf.py
	$(PY) sources/pdf_fingerprint.py --check
	$(PY) sources/check_geography.py
	$(PY) sources/check_portal.py
	$(MAKE) --no-print-directory scelle

# L'ordre est un contrôle, pas une commodité (constat E-21) : graver l'empreinte AVANT
# de la vérifier rend `--check` infaillible par construction. `empreinte` reste donc
# l'acte d'assentiment qui TERMINE la chaîne — jamais celui qui l'ouvre.
# La batterie casse des COPIES du dépôt : la référence n'est jamais touchée.
# Volontairement hors de `controle` et hors de la CI — elle coûte une minute et réécrit des scellés.
batterie: env
	$(PY) sources/test_mutations.py

tout: arbre hymne pdf controle empreinte ## la chaîne complète
	@echo "2026-I régénérée et contrôlée."

propre: ## nettoyages mineurs
	rm -rf sources/__pycache__
