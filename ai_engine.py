"""
Moteur d'analyse financière — AI Inclusive Finance
═══════════════════════════════════════════════════

Corrections & améliorations apportées :
────────────────────────────────────────────────────────────────
1. SCORE SUR 1000 (et non plus sur 100)
   L'ancien score sur 100 était incohérent avec l'affichage
   front-end qui attendait une valeur sur 1000.

2. SCORING MULTIDIMENSIONNEL (5 composantes)
   L'ancien score n'avait que 2 variables (ratio_epargne et
   ratio_depenses), ce qui créait des anomalies : quelqu'un
   avec 0 dépenses sur 1 € de revenu obtenait 100.
   Maintenant 5 dimensions indépendantes :
     • Taux d'épargne          (200 pts)
     • Ratio d'endettement     (200 pts)
     • Coussin de sécurité     (200 pts)
     • Solidité du solde net   (200 pts)
     • Bonus contextuel        (200 pts)

3. PROFILS ENRICHIS (5 niveaux au lieu de 3)
   Granularité plus fine pour des recommandations
   plus personnalisées.

4. CONSEILS MULTIPLES
   On retourne une liste de conseils prioritisés
   au lieu d'une seule phrase générique.

5. ALIGNEMENT ODD CALCULÉ
   On détermine quels Objectifs de Développement
   Durable sont atteints selon le profil.

6. PLUS DE DÉPENDANCE NUMPY
   np.clip remplacé par min/max natif Python.
   numpy n'est pas nécessaire pour des calculs scalaires.
"""


# ── Constantes ────────────────────────────────────────────────
SCORE_MAX = 1000

# Seuils de profil (sur 1000)
SEUIL_EXCELLENT  = 750
SEUIL_BON        = 550
SEUIL_EQUILIBRE  = 350
SEUIL_FRAGILE    = 150


def _score_taux_epargne(taux: float) -> float:
    """
    Composante 1 — Taux d'épargne (0 à 200 pts)
    taux : fraction du revenu épargnée (0.0 à 1.0)

    Barème :
      >= 30%  → 200 pts  (excellent)
      >= 20%  → 160 pts
      >= 10%  → 110 pts
      >= 5%   →  60 pts
      > 0%    →  20 pts
      = 0%    →   0 pts
    """
    if taux >= 0.30: return 200
    if taux >= 0.20: return 160
    if taux >= 0.10: return 110
    if taux >= 0.05: return  60
    if taux >  0.00: return  20
    return 0


def _score_ratio_depenses(ratio: float) -> float:
    """
    Composante 2 — Ratio d'endettement (0 à 200 pts)
    ratio : part des charges dans le revenu (0.0 à 1.0)

    Barème :
      <= 40%  → 200 pts  (sain)
      <= 55%  → 150 pts
      <= 70%  → 100 pts
      <= 85%  →  50 pts
      > 85%   →   0 pts  (danger)
    """
    if ratio <= 0.40: return 200
    if ratio <= 0.55: return 150
    if ratio <= 0.70: return 100
    if ratio <= 0.85: return  50
    return 0


def _score_coussin(mois: float) -> float:
    """
    Composante 3 — Coussin de sécurité (0 à 200 pts)
    mois : nombre de mois de charges couverts par l'épargne

    Barème :
      >= 6 mois → 200 pts  (recommandation internationale)
      >= 3 mois → 140 pts
      >= 1 mois →  70 pts
      < 1 mois  →  20 pts
      = 0       →   0 pts
    """
    if mois >= 6: return 200
    if mois >= 3: return 140
    if mois >= 1: return  70
    if mois >  0: return  20
    return 0


def _score_solde_net(solde: float, revenu: float) -> float:
    """
    Composante 4 — Solidité du solde net (0 à 200 pts)
    Mesure la valeur absolue du surplus, normalisée par le revenu.
    Corrige l'anomalie de l'ancien modèle qui ignorait les montants absolus.

    Barème :
      solde >= 30% du revenu → 200 pts
      solde >= 15% du revenu → 140 pts
      solde >= 5%  du revenu → 80  pts
      solde > 0              → 30  pts
      solde <= 0             →  0  pts
    """
    if revenu <= 0:
        return 0
    ratio = solde / revenu
    if ratio >= 0.30: return 200
    if ratio >= 0.15: return 140
    if ratio >= 0.05: return  80
    if ratio >  0:    return  30
    return 0


def _score_bonus_contextuel(user) -> float:
    """
    Composante 5 — Bonus contextuel (0 à 200 pts)
    Récompense les comportements positifs :
      • Objectif d'épargne défini    → +50 pts
      • Revenu > dépenses * 1.5     → +50 pts  (marge confortable)
      • Horizon long (>= 12 mois)   → +50 pts
      • Autres revenus diversifiés  → +50 pts
    """
    bonus = 0
    if getattr(user, 'objectif_epargne', 0) > 0:
        bonus += 50
    if user.depenses > 0 and user.revenu_total > user.depenses * 1.5:
        bonus += 50
    if getattr(user, 'horizon', 0) >= 12:
        bonus += 50
    if getattr(user, 'autres_revenus', 0) > 0:
        bonus += 50
    return bonus


def _determiner_profil(score: float) -> dict:
    """
    Retourne le profil, l'emoji, la couleur CSS et une description
    en fonction du score sur 1000.
    """
    if score >= SEUIL_EXCELLENT:
        return {
            "nom":         "Investisseur actif",
            "emoji":       "🏆",
            "couleur":     "green",
            "description": "Votre situation financière est excellente. Vous êtes prêt pour des investissements durables."
        }
    if score >= SEUIL_BON:
        return {
            "nom":         "Épargnant prudent",
            "emoji":       "📈",
            "couleur":     "teal",
            "description": "Bonne base financière. Quelques ajustements permettront d'accéder à l'investissement."
        }
    if score >= SEUIL_EQUILIBRE:
        return {
            "nom":         "Profil équilibré",
            "emoji":       "⚖️",
            "couleur":     "gold",
            "description": "Situation correcte mais des marges de progression significatives existent."
        }
    if score >= SEUIL_FRAGILE:
        return {
            "nom":         "Profil fragile",
            "emoji":       "⚠️",
            "couleur":     "orange",
            "description": "Votre situation nécessite une stabilisation avant tout investissement."
        }
    return {
        "nom":         "Profil précaire",
        "emoji":       "🆘",
        "couleur":     "red",
        "description": "Une restructuration financière est prioritaire. Un accompagnement est recommandé."
    }


def _generer_conseils(user, score: float) -> list:
    """
    Génère une liste ordonnée de conseils personnalisés
    en fonction des points faibles détectés.
    Retourne une liste de dicts {priorite, titre, texte, type}.
    """
    conseils = []
    priorite = 1

    # Solde négatif — urgence absolue
    if user.solde < 0:
        conseils.append({
            "priorite": priorite,
            "titre": "Déficit mensuel détecté",
            "texte": f"Vos dépenses dépassent vos revenus de {abs(user.solde):,.0f} €/mois. "
                     "Identifiez et réduisez les charges non essentielles immédiatement.",
            "type": "danger"
        })
        priorite += 1

    # Ratio de charges élevé
    if user.ratio_depenses > 0.70:
        conseils.append({
            "priorite": priorite,
            "titre": "Taux d'endettement critique",
            "texte": f"{round(user.ratio_depenses * 100)}% de vos revenus partent en charges. "
                     "Le seuil sain est 40-55%. Renégociez loyer et abonnements en priorité.",
            "type": "danger" if user.ratio_depenses > 0.85 else "warning"
        })
        priorite += 1
    elif user.ratio_depenses > 0.55:
        conseils.append({
            "priorite": priorite,
            "titre": "Ratio de charges à surveiller",
            "texte": f"{round(user.ratio_depenses * 100)}% de vos revenus sont absorbés par les charges. "
                     "Objectif : descendre sous 55%.",
            "type": "warning"
        })
        priorite += 1

    # Coussin de sécurité insuffisant
    if user.mois_securite < 3:
        conseils.append({
            "priorite": priorite,
            "titre": "Coussin de sécurité insuffisant",
            "texte": f"Vous avez {user.mois_securite:.1f} mois de réserve. "
                     "L'objectif international est 6 mois. "
                     f"Il vous manque {max(0, 6 - user.mois_securite):.1f} mois d'épargne de précaution.",
            "type": "warning"
        })
        priorite += 1
    elif user.mois_securite >= 6:
        conseils.append({
            "priorite": priorite,
            "titre": "Coussin de sécurité solide",
            "texte": f"Excellent : {user.mois_securite:.1f} mois de réserve. "
                     "Vous pouvez envisager de placer l'excédent dans un produit rémunéré.",
            "type": "positive"
        })
        priorite += 1

    # Taux d'épargne faible
    if 0 < user.taux_epargne < 0.10:
        conseils.append({
            "priorite": priorite,
            "titre": "Taux d'épargne à améliorer",
            "texte": f"Vous épargnez {round(user.taux_epargne * 100)}% de vos revenus. "
                     "Essayez d'atteindre 10% avec la méthode 'pay yourself first' : "
                     "virer automatiquement 10% en début de mois.",
            "type": "warning"
        })
        priorite += 1
    elif user.taux_epargne >= 0.20:
        conseils.append({
            "priorite": priorite,
            "titre": "Excellent taux d'épargne",
            "texte": f"{round(user.taux_epargne * 100)}% de vos revenus sont épargnés. "
                     "Vous êtes éligible aux produits de microcrédit et d'investissement à impact local.",
            "type": "positive"
        })
        priorite += 1

    # Capacité d'emprunt
    if user.capacite_emprunt > 0 and score >= SEUIL_EQUILIBRE:
        conseils.append({
            "priorite": priorite,
            "titre": "Capacité d'emprunt estimée",
            "texte": f"Selon la règle du tiers, vous pouvez emprunter jusqu'à "
                     f"{user.capacite_emprunt:,.0f} € sur 10 ans. "
                     "Consultez votre IMF partenaire pour valider cette estimation.",
            "type": "info"
        })
        priorite += 1

    # Conseil générique si rien de spécifique
    if not conseils:
        conseils.append({
            "priorite": 1,
            "titre": "Situation stable",
            "texte": "Votre situation financière de base est saine. "
                     "Définissez un objectif d'épargne mensuel pour progresser davantage.",
            "type": "info"
        })

    return conseils


def _alignement_odd(user, score: float) -> list:
    """
    Retourne la liste des ODD (Objectifs Développement Durable)
    atteints ou partiellement atteints selon le profil.
    """
    odds = []

    # ODD 1 — Fin de la pauvreté
    if score >= SEUIL_FRAGILE:
        odds.append({"numero": 1, "nom": "Fin de la pauvreté",
                     "statut": "actif", "classe": "green"})

    # ODD 8 — Travail décent et croissance
    if user.solde > 0:
        odds.append({"numero": 8, "nom": "Travail décent",
                     "statut": "actif", "classe": "blue"})

    # ODD 10 — Réduction des inégalités
    if user.taux_epargne >= 0.10:
        odds.append({"numero": 10, "nom": "Réduction des inégalités",
                     "statut": "actif", "classe": "gold"})

    # ODD 17 — Partenariats
    if score >= SEUIL_BON:
        odds.append({"numero": 17, "nom": "Partenariats",
                     "statut": "actif", "classe": "blue"})

    return odds


# ── Point d'entrée principal ──────────────────────────────────

def analyse_financiere(user) -> dict:
    """
    Analyse financière complète à partir d'un objet UserData.

    Changement d'interface :
    Avant → analyse_financiere(revenu, depenses, epargne)
    Après → analyse_financiere(user)  ← objet UserData complet

    Cela permet d'utiliser toutes les propriétés calculées
    de UserData sans les recalculer ici.

    Retourne un dict complet pour le template result.html.
    """

    # ── Calcul des 5 composantes ──────────────────────────────
    s1 = _score_taux_epargne(user.taux_epargne)
    s2 = _score_ratio_depenses(user.ratio_depenses)
    s3 = _score_coussin(user.mois_securite)
    s4 = _score_solde_net(user.solde, user.revenu_total)
    s5 = _score_bonus_contextuel(user)

    score_brut = s1 + s2 + s3 + s4 + s5
    score = min(SCORE_MAX, max(0, round(score_brut)))

    # ── Profil, conseils, ODD ─────────────────────────────────
    profil_data = _determiner_profil(score)
    conseils    = _generer_conseils(user, score)
    odds        = _alignement_odd(user, score)

    # ── Impact durable (0–100%) ───────────────────────────────
    # Normalisé sur 1000, plafonné à 100%
    impact = round(min(100.0, score / 10.0), 1)

    # ── Score de composantes (pour visualisation radar) ───────
    composantes = {
        "epargne":    round(s1 / 200 * 100),
        "endettement": round(s2 / 200 * 100),
        "securite":   round(s3 / 200 * 100),
        "solde":      round(s4 / 200 * 100),
        "bonus":      round(s5 / 200 * 100),
    }

    return {
        # Données principales (compatibles avec result.html existant)
        "score":   score,
        "profil":  profil_data["nom"],
        "conseil": conseils[0]["texte"] if conseils else "",
        "impact":  impact,

        # Données enrichies
        "profil_data":   profil_data,
        "conseils":      conseils,
        "odds":          odds,
        "composantes":   composantes,

        # Métriques financières (pour l'affichage dans result.html)
        "solde_net":        round(user.solde, 2),
        "taux_epargne":     round(user.taux_epargne * 100, 1),
        "ratio_depenses":   round(user.ratio_depenses * 100, 1),
        "mois_securite":    round(user.mois_securite, 1),
        "capacite_emprunt": user.capacite_emprunt,

        # Détail du score (transparence)
        "score_detail": {
            "taux_epargne":  s1,
            "endettement":   s2,
            "coussin":       s3,
            "solde":         s4,
            "bonus":         s5,
            "total":         score,
            "max":           SCORE_MAX,
        }
    }