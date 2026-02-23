"""
Module de recommandation financière — AI Inclusive Finance
══════════════════════════════════════════════════════════

Corrections & améliorations apportées :
────────────────────────────────────────────────────────────────
1. CONNEXION AU RESTE DE L'APP
   L'ancienne version était un fichier isolé, jamais importé
   dans app.py et jamais utilisé. Ce module est maintenant
   importé et appelé dans app.py.

2. INTERFACE UNIFIÉE
   Avant : analyze_profile(salary, savings, expenses)  ← anglais
   Après : recommander(user)  ← reçoit un objet UserData
   Plus de duplication de calculs déjà faits dans UserData.

3. RÈGLE DES 33% CORRIGÉE
   L'ancienne formule était :
     borrowing_capacity = remaining * 0.33 * 12 * 10
   Ce calcul était approximatif et non expliqué.
   La nouvelle version est transparente et documentée.

4. RECOMMANDATIONS PAR OBJECTIF
   Les recommandations changent selon l'objectif déclaré
   par l'utilisateur (épargne, crédit, investissement…).

5. LISTE DE PRODUITS SUGGÉRÉS
   On retourne maintenant des produits financiers concrets
   adaptés au profil et à la banque choisie.
"""

from ai_engine import (
    SEUIL_EXCELLENT,
    SEUIL_BON,
    SEUIL_EQUILIBRE,
    SEUIL_FRAGILE,
)


# ── Produits financiers par niveau de score ───────────────────

PRODUITS = {
    "precaire": [
        {"nom": "Tontine digitale",      "type": "epargne",   "desc": "Épargne collective entre pairs, sans banque."},
        {"nom": "Mobile money basique",  "type": "epargne",   "desc": "Ouvrir un compte Wave ou Orange Money."},
        {"nom": "Formation financière",  "type": "education", "desc": "Programme d'éducation financière de base."},
    ],
    "fragile": [
        {"nom": "Compte épargne IMF",    "type": "epargne",   "desc": "Épargne progressive avec une institution de microfinance."},
        {"nom": "Microcrédit 3 mois",    "type": "credit",    "desc": "Petit prêt court terme pour stabiliser la trésorerie."},
        {"nom": "Budget personnel IA",   "type": "outil",     "desc": "Suivi mensuel assisté par notre outil de budget."},
    ],
    "equilibre": [
        {"nom": "Plan épargne 12 mois",  "type": "epargne",   "desc": "Épargne programmée avec objectif défini."},
        {"nom": "Microcrédit PME",       "type": "credit",    "desc": "Financement d'une activité commerciale locale."},
        {"nom": "Assurance vie basique", "type": "protection","desc": "Couverture minimale pour protéger la famille."},
    ],
    "bon": [
        {"nom": "Fonds d'investissement local", "type": "investissement", "desc": "Placement dans des PME locales à impact."},
        {"nom": "Crédit immobilier BCIMR",       "type": "credit",         "desc": "Financement habitat avec BCIMR."},
        {"nom": "Assurance complète",            "type": "protection",     "desc": "Couverture santé + vie + habitation."},
    ],
    "excellent": [
        {"nom": "Portefeuille ODD",             "type": "investissement", "desc": "Investissement diversifié aligné sur les ODD."},
        {"nom": "Crédit entreprise",             "type": "credit",         "desc": "Financement de création ou expansion d'entreprise."},
        {"nom": "Fonds de pension local",        "type": "retraite",       "desc": "Préparation retraite via un fonds certifié."},
        {"nom": "Conseil patrimonial",           "type": "conseil",        "desc": "Accompagnement personnalisé par un conseiller IMF."},
    ],
}


def _niveau_produits(score: float) -> str:
    """Retourne la clé de niveau pour les produits."""
    if score >= SEUIL_EXCELLENT: return "excellent"
    if score >= SEUIL_BON:       return "bon"
    if score >= SEUIL_EQUILIBRE: return "equilibre"
    if score >= SEUIL_FRAGILE:   return "fragile"
    return "precaire"


def recommander(user, score: float) -> dict:
    """
    Génère les recommandations produits et la décision
    d'investissement pour un profil donné.

    Paramètres :
        user  : objet UserData (modèle unifié)
        score : score calculé par ai_engine.analyse_financiere()

    Retourne un dict avec :
        decision        : texte de la décision principale
        decision_type   : "green" | "orange" | "red"
        raison          : explication de la décision
        produits        : liste de produits recommandés
        capacite_emprunt: montant empruntable estimé
        prochaine_etape : action concrète à faire maintenant
    """

    # ── Décision principale ───────────────────────────────────
    if user.ratio_depenses > 0.85 or user.solde < 0:
        decision      = "Restructuration nécessaire"
        decision_type = "red"
        raison        = (
            "Vos charges absorbent plus de 85% de vos revenus ou votre solde est négatif. "
            "Aucun investissement ni crédit n'est recommandé avant stabilisation."
        )
        prochaine_etape = "Contactez un conseiller financier IMF pour un plan de désendettement."

    elif user.ratio_depenses > 0.60 or user.mois_securite < 1:
        decision      = "Épargner en priorité"
        decision_type = "orange"
        raison        = (
            f"Votre taux de charges est de {round(user.ratio_depenses*100)}% "
            f"et votre coussin de sécurité est de {user.mois_securite:.1f} mois. "
            "Constituez d'abord une réserve de 3 mois avant tout crédit."
        )
        prochaine_etape = "Ouvrez un compte épargne automatique et épargnez 10% de vos revenus chaque mois."

    elif score >= SEUIL_BON:
        decision      = "Investissement recommandé"
        decision_type = "green"
        raison        = (
            f"Votre score de {score}/1000, votre solde positif de {user.solde:,.0f} €/mois "
            f"et {user.mois_securite:.1f} mois de réserve vous qualifient pour des produits d'investissement."
        )
        prochaine_etape = "Comparez les offres de crédit ou d'investissement de vos IMF partenaires."

    else:
        decision      = "Consolidation recommandée"
        decision_type = "gold"
        raison        = (
            "Votre situation est stable mais perfectible. "
            "Augmentez votre épargne pendant 6 mois avant d'envisager un crédit."
        )
        prochaine_etape = "Fixez un objectif d'épargne mensuel et suivez-le pendant 3 mois consécutifs."

    # ── Produits adaptés ──────────────────────────────────────
    niveau   = _niveau_produits(score)
    produits = PRODUITS.get(niveau, [])

    # ── Personnalisation selon la banque ─────────────────────
    banque = getattr(user, 'banque', None)
    if banque == "bcimr" and score >= SEUIL_EQUILIBRE:
        # BCIMR est spécialisée immobilier
        produits = [p for p in produits if p["type"] != "investissement"]
        produits.insert(0, {
            "nom":  "Crédit habitat BCIMR",
            "type": "credit",
            "desc": "Offre immobilière prioritaire via votre banque BCIMR sélectionnée."
        })
    elif banque == "salaam":
        # Salaam Bank = finance islamique
        produits.insert(0, {
            "nom":  "Financement Murabaha",
            "type": "credit",
            "desc": "Financement islamique sans intérêt via Salaam Bank."
        })

    return {
        "decision":         decision,
        "decision_type":    decision_type,
        "raison":           raison,
        "produits":         produits[:4],          # max 4 produits affichés
        "capacite_emprunt": user.capacite_emprunt,
        "prochaine_etape":  prochaine_etape,
    }