# Chancellerie royale — chaîne de production du volume 2026-I.
# Buts : env · arbre · pdf · empreinte · controle · tout · propre
# Hors venv, remplacer PY=.venv/bin/python par PY=python3 (make PY=python3).

PY      ?= .venv/bin/python
VENV    ?= .venv
PDF     := Royaume_du_Babberland_Encyclopedie_Consolidee_2026_I.pdf

.DEFAULT_GOAL := tout
.PHONY: env arbre pdf empreinte controle workflows tout propre

env: ## crée le venv et y épingle les dépendances (contournement PEP 668, constat E-11)
	@test -x $(PY) || python3 -m venv $(VENV)
	$(PY) -m pip install --quiet --upgrade pip
	$(PY) -m pip install --quiet -r requirements.txt
	@echo "environnement prêt : $(PY)"

arbre: ## régénère l'arbre généalogique (déterministe au bit près)
	$(PY) sources/generate_genealogy.py

pdf: $(PDF) ## régénère l'encyclopédie PDF 2026-I

$(PDF): ENCYCLOPEDIE_CONSOLIDEE_2026_I.md sources/generate_encyclopedie_2026_i.py $(wildcard images/*.png)
	$(PY) sources/generate_encyclopedie_2026_i.py

empreinte: ## grave l'empreinte sémantique du PDF publié (contrat de la CI)
	$(PY) sources/pdf_fingerprint.py --write

workflows: ## installe le modèle de CI dans .github/workflows/ (à committer avec un jeton tenant « workflows »)
	@mkdir -p .github/workflows && cp sources/github_actions_continuite.yml .github/workflows/continuite.yml \
	  && echo ".github/workflows/continuite.yml prêt — le pousser nécessite la permission « workflows » pour l'App."

controle: ## continuité des sources, artefact publié, fraîcheur de l'empreinte
	$(PY) sources/check_continuity.py
	$(PY) sources/check_pdf.py
	$(PY) sources/pdf_fingerprint.py --check

tout: arbre pdf empreinte controle ## la chaîne complète
	@echo "2026-I régénérée et contrôlée."

propre: ## nettoyages mineurs
	rm -rf sources/__pycache__
