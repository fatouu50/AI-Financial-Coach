# AI Inclusive Finance

> **Plateforme d'analyse financière intelligente et explicable, conçue pour les marchés à données limitées.**

L'IA ne vous dit pas quoi acheter — elle vous montre **quand une décision devient réellement sûre.**

---

## Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Installation](#installation)
- [Lancement](#lancement)
- [Structure du projet](#structure-du-projet)
- [Moteur IA — Scoring](#moteur-ia--scoring)
- [Parcours utilisateur](#parcours-utilisateur)
- [Alignement ODD](#alignement-odd)
- [Variables d'environnement](#variables-denvironnement)
- [Déploiement](#déploiement)
- [Contribuer](#contribuer)

---

## Vue d'ensemble

**AI Inclusive Finance** est une application web Flask qui permet à toute personne — avec seulement 3 données financières — d'obtenir une analyse complète de sa stabilité financière, une simulation de scénarios d'imprévus, et des recommandations personnalisées adaptées au contexte local (Djibouti et zone MENA).

Le projet répond à un constat simple : la majorité des décisions d'investissement (achat immobilier, véhicule, terrain) sont prises sans aucune projection future, faute d'accès à un conseiller financier. Cette application démocratise ce conseil grâce à une IA légère, transparente et déployable sans connexion bancaire.

---

## Fonctionnalités

### Analyse financière en temps réel
- Score de stabilité financière sur **1 000 points** calculé selon 5 dimensions indépendantes
- Mise à jour instantanée du tableau de bord à chaque saisie
- Indicateurs clés : taux d'épargne, ratio d'endettement, coussin de sécurité, solde net

### Simulation d'imprévus
- 3 scénarios activables en un clic : baisse de revenu −30%, dépense inattendue +50%, perte d'emploi
- Verdict automatique post-simulation : *"Dans ce scénario, l'achat devient risqué. L'IA recommande d'attendre 8 mois supplémentaires."*
- Réinitialisation instantanée vers la situation réelle

### IA explicable
- Justification systématique de chaque score et recommandation
- Décomposition visuelle des 5 composantes du score
- Phrase de décision adaptative : la page dit immédiatement si une décision est sûre, à surveiller, ou déconseillée

### Coach financier
- Opportunités d'investissement filtrables (immobilier, terrain, auto, locatif, épargne)
- Simulation personnalisée d'un projet (prix, durée, apport, loyer estimé)
- Plan d'action mensuel priorisé
- Calcul du cash-flow locatif

### GPS Financier
- Projection prédictive sur 36 mois
- Simulation de mode crise
- Visualisation de l'évolution du patrimoine dans le temps

---

## Architecture

```
Utilisateur
    │
    ▼
Interface Web (Flask + Jinja2)
    │  dashboard.html  ← saisie + aperçu temps réel
    │  result.html     ← score + conseil IA explicable
    │  coach.html      ← opportunités + plan d'action
    │  forecast.html   ← projection 36 mois
    │
    ▼
Moteur d'analyse IA  [ai_engine.py]
    │  5 composantes de scoring
    │  Profils (5 niveaux)
    │  Conseils priorisés
    │
    ├──▶  Module de recommandation  [recommendation.py]
    │        Opportunités filtrées par profil et pays
    │
    └──▶  Générateur de coaching    [coach.py]
             Plan d'action mensuel
             Simulation projet personnel
             Calcul mensualités / apport / cash-flow
```

Aucune base de données. Aucune connexion bancaire. Stateless par conception.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | Python 3.10+ · Flask 3.x |
| Templating | Jinja2 |
| Frontend | HTML5 · CSS3 custom (variables CSS) · Vanilla JS |
| Typographie | Cormorant Garamond · DM Mono · Syne (Google Fonts) |
| Déploiement | Gunicorn · compatible Render / Railway / VPS |
| Dépendances Python | `flask` uniquement — pas de NumPy, pas de Pandas |

---

## Installation

### Prérequis

- Python **3.10** ou supérieur
- `pip`

### Cloner et installer

```bash
git clone https://github.com/fatouu50/finance-ai.git
cd finance-ai

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### `requirements.txt`

```
flask>=3.0.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
```

---

## Lancement

### Mode développement

```bash
python app.py
```

L'application tourne sur `http://localhost:5000`

### Mode production (Gunicorn)

```bash
gunicorn app:app --bind 0.0.0.0:5000 --workers 2 --threads 4
```

---

## Structure du projet

```
ai-inclusive-finance/
│
├── app.py                  # Point d'entrée Flask — routes et orchestration
├── ai_engine.py            # Moteur de scoring financier (5 composantes)
├── models.py               # UserData — modèle de données avec propriétés calculées
├── coach.py                # Générateur de coaching et plan d'action
├── recommendation.py       # Moteur de recommandation d'opportunités
├── config.py               # Configuration (clé secrète, debug, etc.)
│
├── templates/
│   ├── base.html           # Layout global — tokens CSS, navigation
│   ├── index.html          # Page d'accueil
│   ├── banks.html          # Sélection de la banque — étape 1
│   ├── dashboard.html      # Formulaire + aperçu temps réel — étape 2
│   ├── result.html         # Score IA + conseil explicable — étape 3
│   ├── coach.html          # Coach financier + opportunités — étape 4
│   ├── forecast.html       # GPS Financier — projection 36 mois
│   ├── opportunities.html  # Catalogue d'opportunités
│   └── about.html          # À propos du projet
│
├── static/
│   └── style.css           # Styles globaux (reset, composants partagés)
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Moteur IA — Scoring

Le score de stabilité financière est calculé sur **1 000 points** selon 5 composantes indépendantes, chacune plafonnée à 200 points.

### Composante 1 — Taux d'épargne (200 pts)

| Taux d'épargne | Points |
|---|---|
| ≥ 30% | 200 |
| ≥ 20% | 160 |
| ≥ 10% | 110 |
| ≥ 5% | 60 |
| > 0% | 20 |
| 0% | 0 |

### Composante 2 — Ratio d'endettement (200 pts)

| Part des charges | Points |
|---|---|
| ≤ 40% | 200 |
| ≤ 55% | 150 |
| ≤ 70% | 100 |
| ≤ 85% | 50 |
| > 85% | 0 |

### Composante 3 — Coussin de sécurité (200 pts)

| Mois de réserve | Points |
|---|---|
| ≥ 6 mois | 200 |
| ≥ 3 mois | 140 |
| ≥ 1 mois | 70 |
| < 1 mois | 20 |
| 0 | 0 |

### Composante 4 — Solidité du solde net (200 pts)

Mesure le surplus mensuel normalisé par le revenu.

| Surplus / Revenu | Points |
|---|---|
| ≥ 30% | 200 |
| ≥ 15% | 140 |
| ≥ 5% | 80 |
| > 0% | 30 |
| ≤ 0% | 0 |

### Composante 5 — Bonus contextuel (200 pts)

| Comportement | Bonus |
|---|---|
| Objectif d'épargne défini | +50 |
| Revenu > dépenses × 1,5 | +50 |
| Horizon ≥ 12 mois | +50 |
| Revenus diversifiés | +50 |

### Profils

| Score | Profil | Signification |
|---|---|---|
| ≥ 750 | Investisseur actif | Prêt pour un engagement financier majeur |
| 550–749 | Épargnant prudent | Bonne base, ajustements mineurs recommandés |
| 350–549 | Profil équilibré | Viable mais marges de progression significatives |
| 150–349 | Profil fragile | Stabilisation prioritaire avant tout investissement |
| < 150 | Profil précaire | Restructuration financière recommandée |

---

## Parcours utilisateur

```
[Accueil]
    │
    ▼
[Sélection banque]  ←  Étape 1
    │
    ▼
[Saisie financière + aperçu temps réel]  ←  Étape 2
    │  · Revenus, dépenses, épargne, objectif
    │  · Score mis à jour à chaque frappe
    │  · Simulation d'imprévu disponible
    │
    ▼
[Résultat IA + score explicable]  ←  Étape 3
    │  · Score /1000 avec décomposition
    │  · Conseil personnalisé justifié
    │  · Bannière de décision responsable
    │
    ▼
[Coach financier]  ←  Étape 4
    │  · Opportunités filtrées par profil
    │  · Simulation projet personnel
    │  · Plan d'action mensuel
    │
    ▼
[GPS Financier]  ←  Optionnel
       · Projection 36 mois
       · Mode crise
```

---

## Alignement ODD

L'application mesure sa contribution aux Objectifs de Développement Durable de l'ONU :

| ODD | Intitulé | Déclencheur |
|---|---|---|
| ODD 1 | Fin de la pauvreté | Score ≥ 150 |
| ODD 8 | Travail décent et croissance économique | Solde mensuel positif |
| ODD 10 | Réduction des inégalités | Taux d'épargne ≥ 10% |
| ODD 17 | Partenariats pour la réalisation des objectifs | Score ≥ 550 |

---

## Variables d'environnement

Créer un fichier `.env` à la racine (voir `.env.example`) :

```env
# Obligatoire en production
SECRET_KEY=votre_cle_secrete_tres_longue

# Optionnel
FLASK_ENV=production
PORT=5000
DEBUG=False
```

---

## Déploiement

### Render.com

1. Connecter le dépôt GitHub
2. **Build command** : `pip install -r requirements.txt`
3. **Start command** : `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Ajouter la variable `SECRET_KEY` dans les paramètres d'environnement

### Railway

```bash
railway login
railway init
railway up
```

### VPS (Ubuntu/Debian)

```bash
# Installer les dépendances système
sudo apt update && sudo apt install python3-pip python3-venv nginx -y

# Configurer le service systemd
sudo nano /etc/systemd/system/ai-finance.service

# Démarrer
sudo systemctl enable ai-finance && sudo systemctl start ai-finance
```

---

## Contribuer

Les contributions sont les bienvenues. Pour proposer une modification :

1. Forker le dépôt
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. Committer les changements : `git commit -m "feat: description claire"`
4. Pousser la branche : `git push origin feature/ma-fonctionnalite`
5. Ouvrir une Pull Request

---

## Philosophie du projet

> *"Beaucoup d'outils poussent à consommer. Celui-ci montre comment éviter une mauvaise décision."*

AI Inclusive Finance ne recommande pas des produits financiers. Il **protège** l'utilisateur en rendant visible ce que les simulateurs classiques cachent : le risque réel d'un engagement face à un imprévu.

---

*Construit pour le hackathon IA & Inclusion Économique · Djibouti 2025*
