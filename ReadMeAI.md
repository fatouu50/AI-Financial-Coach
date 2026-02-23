# AI Inclusive Finance

Plateforme d'analyse financière inclusive propulsée par IA — conçue pour Djibouti et l'Afrique de l'Est.

---

## Structure du projet

```
ai-inclusive-finance/
│
├── app.py               ← Serveur Flask, routes, gestion d'erreurs
├── config.py            ← Configuration (clé secrète, debug…)
├── models.py            ← Modèle UserData (validation + propriétés calculées)
├── ai_engine.py         ← Moteur de scoring IA multidimensionnel
├── recommendation.py    ← Recommandations produits et décision investissement
├── requirements.txt     ← Dépendances Python
├── .env.example         ← Variables d'environnement à copier
│
└── templates/
    ├── base.html        ← Layout principal (nav, ticker, footer)
    ├── index.html       ← Page d'accueil
    ├── about.html       ← Page vision
    ├── dashboard.html   ← Formulaire simulation principal
    ├── situation.html   ← Formulaire situation financière
    ├── bank_select.html ← Sélection de banque
    ├── result.html      ← Page de résultat IA
    ├── 404.html         ← Page d'erreur 404
    └── 500.html         ← Page d'erreur 500
```

---

## Installation

```bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/ai-inclusive-finance
cd ai-inclusive-finance

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et renseigner SECRET_KEY

# 5. Lancer l'application
python app.py
```

L'application est disponible sur `http://localhost:5000`

---

## Variables d'environnement

Créer un fichier `.env` à la racine :

```env
SECRET_KEY=votre-cle-secrete-longue-et-aleatoire
DEBUG=false
PORT=5000
```

**Ne jamais commiter `.env` dans git.**

---

## Routes disponibles

| Route        | Méthode | Description                              |
|--------------|---------|------------------------------------------|
| `/`          | GET     | Page d'accueil                           |
| `/about`     | GET     | Page vision                              |
| `/form`      | GET     | Sélection de banque                      |
| `/situation` | GET     | Formulaire situation financière          |
| `/dashboard` | GET     | Formulaire simulation principal          |
| `/analyse`   | POST    | Analyse depuis dashboard (revenu/…)      |
| `/result`    | POST    | Analyse depuis situation (salary/…)      |

---

## Moteur de scoring

Le score est calculé sur **1000 points** via 5 composantes indépendantes :

| Composante           | Max   | Critère                          |
|----------------------|-------|----------------------------------|
| Taux d'épargne       | 200 pts | ≥ 30% du revenu = 200 pts      |
| Ratio d'endettement  | 200 pts | ≤ 40% du revenu = 200 pts      |
| Coussin de sécurité  | 200 pts | ≥ 6 mois de charges = 200 pts  |
| Solidité du solde    | 200 pts | Solde ≥ 30% du revenu = 200 pts|
| Bonus contextuel     | 200 pts | Objectif + horizon + diversif. |

### Niveaux de profil

| Score      | Profil              |
|------------|---------------------|
| 750–1000   | Investisseur actif  |
| 550–749    | Épargnant prudent   |
| 350–549    | Profil équilibré    |
| 150–349    | Profil fragile      |
| 0–149      | Profil précaire     |

---

## Banques partenaires (Djibouti)

- **Salaam Bank** — Finance islamique (Murabaha)
- **CAC Bank** — Banque commerciale, microcrédit
- **Saba Bank** — Transferts, diaspora
- **BCIMR** — Immobilier, habitat social
- **Banque de Djibouti** — Secteur public, fonctionnaires

---

## Corrections apportées (v2.0)

1. **SECRET_KEY** sortie du code source → variable d'environnement
2. **Score sur 1000** cohérent avec le front-end (était sur 100)
3. **Scoring multidimensionnel** (5 composantes vs 2 avant)
4. **Noms de champs unifiés** (`salary`/`revenu` acceptés partout)
5. **recommendation.py connecté** à app.py (était orphelin)
6. **Gestion d'erreurs** sur toutes les routes POST
7. **Route `/form`** et **`/situation`** ajoutées (manquantes)
8. **numpy supprimé** (remplacé par min/max natif)
9. **UserData enrichi** avec propriétés calculées réutilisables
10. **Pages d'erreur** 404 et 500 personnalisées
