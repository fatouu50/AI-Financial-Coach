"""
Moteur Coach Financier — AI Inclusive Finance · Djibouti
═══════════════════════════════════════════════════════════

Ce module est le cœur de la simulation.
Il reçoit un profil UserData + score et génère :

  1. Un catalogue d'opportunités réelles à Djibouti
     (immobilier, auto, terrain, investissement, épargne)

  2. Pour chaque opportunité : faisable / risqué / déconseillé
     avec calcul de mensualité, durée, apport requis

  3. Un projet personnalisé si l'utilisateur entre le sien

  4. Un plan d'action mensuel chiffré

Tous les prix sont en FDJ (Franc Djiboutien).
1 EUR ≈ 200 FDJ (taux approximatif 2024)
"""

# ─────────────────────────────────────────────────────────────
# CATALOGUE DES OPPORTUNITÉS — Prix réels Djibouti 2024
# Source : marché immobilier djiboutien, concessionnaires locaux
# ─────────────────────────────────────────────────────────────

OPPORTUNITES = {

    # ── IMMOBILIER ────────────────────────────────────────────
    "immobilier": [
        {
            "id":          "maison_balbala",
            "nom":         "Maison F3 — Balbala",
            "description": "Maison 3 pièces dans le quartier de Balbala, "
                           "proche des commodités. Idéal pour une première acquisition.",
            "prix":        8_000_000,   # FDJ
            "apport_min":  0.15,        # 15% d'apport minimum
            "duree_max":   20,          # ans
            "taux_interet": 0.07,       # 7% annuel (taux moyen Djibouti)
            "type":        "immobilier",
            "emoji":       "🏠",
            "quartier":    "Balbala",
            "surface":     "65 m²",
        },
        {
            "id":          "appartement_centre",
            "nom":         "Appartement F2 — Centre-ville",
            "description": "Appartement moderne en plein centre de Djibouti-Ville. "
                           "Proche des banques, commerces et administration.",
            "prix":        12_000_000,
            "apport_min":  0.20,
            "duree_max":   20,
            "taux_interet": 0.07,
            "type":        "immobilier",
            "emoji":       "🏢",
            "quartier":    "Centre-ville",
            "surface":     "55 m²",
        },
        {
            "id":          "villa_plateau",
            "nom":         "Villa F4 — Plateau du Serpent",
            "description": "Belle villa familiale dans un quartier résidentiel calme. "
                           "Jardin, parking, vue dégagée.",
            "prix":        25_000_000,
            "apport_min":  0.20,
            "duree_max":   25,
            "taux_interet": 0.075,
            "type":        "immobilier",
            "emoji":       "🏡",
            "quartier":    "Plateau du Serpent",
            "surface":     "120 m²",
        },
    ],

    # ── TERRAIN ───────────────────────────────────────────────
    "terrain": [
        {
            "id":          "terrain_pk12",
            "nom":         "Terrain 200 m² — PK 12",
            "description": "Terrain constructible à PK 12, viabilisé, "
                           "titre foncier disponible. Excellent pour construire.",
            "prix":        3_500_000,
            "apport_min":  0.30,
            "duree_max":   10,
            "taux_interet": 0.08,
            "type":        "terrain",
            "emoji":       "🗺️",
            "quartier":    "PK 12",
            "surface":     "200 m²",
        },
        {
            "id":          "terrain_arta",
            "nom":         "Terrain 500 m² — Arta",
            "description": "Grand terrain dans la région d'Arta, "
                           "air frais, potentiel agricole ou résidentiel.",
            "prix":        2_000_000,
            "apport_min":  0.25,
            "duree_max":   10,
            "taux_interet": 0.08,
            "type":        "terrain",
            "emoji":       "🌿",
            "quartier":    "Arta",
            "surface":     "500 m²",
        },
    ],

    # ── VÉHICULES ─────────────────────────────────────────────
    "auto": [
        {
            "id":          "moto_commute",
            "nom":         "Moto 125cc — Déplacement quotidien",
            "description": "Moto économique pour les trajets domicile-travail. "
                           "Faible consommation, entretien accessible.",
            "prix":        400_000,
            "apport_min":  0.20,
            "duree_max":   3,
            "taux_interet": 0.10,
            "type":        "auto",
            "emoji":       "🛵",
            "marque":      "Honda / Yamaha",
            "annee":       2024,
        },
        {
            "id":          "voiture_occasion",
            "nom":         "Voiture d'occasion — Toyota Corolla",
            "description": "Berline fiable et répandue à Djibouti. "
                           "Pièces détachées disponibles localement.",
            "prix":        1_800_000,
            "apport_min":  0.25,
            "duree_max":   5,
            "taux_interet": 0.10,
            "type":        "auto",
            "emoji":       "🚗",
            "marque":      "Toyota Corolla",
            "annee":       2019,
        },
        {
            "id":          "4x4_professionnel",
            "nom":         "4x4 Pick-up — Usage professionnel",
            "description": "Véhicule utilitaire pour activité commerciale "
                           "ou transport. Idéal pour entrepreneurs.",
            "prix":        4_500_000,
            "apport_min":  0.30,
            "duree_max":   5,
            "taux_interet": 0.10,
            "type":        "auto",
            "emoji":       "🚙",
            "marque":      "Toyota Hilux",
            "annee":       2022,
        },
    ],

    # ── INVESTISSEMENT LOCATIF ────────────────────────────────
    "locatif": [
        {
            "id":          "studio_locatif",
            "nom":         "Studio locatif — Centre-ville",
            "description": "Petit studio à louer à des expatriés ou fonctionnaires. "
                           "Loyer estimé : 80 000 FDJ/mois. Rentabilité ~8%/an.",
            "prix":        10_000_000,
            "apport_min":  0.30,
            "duree_max":   15,
            "taux_interet": 0.075,
            "loyer_estime": 80_000,     # FDJ/mois
            "rendement":   0.08,        # 8% brut annuel
            "type":        "locatif",
            "emoji":       "🏘️",
            "quartier":    "Centre-ville",
        },
        {
            "id":          "local_commercial",
            "nom":         "Local commercial — Marché central",
            "description": "Local à louer pour activité commerciale. "
                           "Loyer estimé : 120 000 FDJ/mois. Emplacement stratégique.",
            "prix":        15_000_000,
            "apport_min":  0.35,
            "duree_max":   15,
            "taux_interet": 0.08,
            "loyer_estime": 120_000,
            "rendement":   0.096,
            "type":        "locatif",
            "emoji":       "🏪",
            "quartier":    "Marché central",
        },
    ],

    # ── ÉPARGNE / PLACEMENT ───────────────────────────────────
    "epargne": [
        {
            "id":          "epargne_progressive",
            "nom":         "Plan épargne progressif — 12 mois",
            "description": "Versement mensuel fixe sur un compte épargne IMF. "
                           "Taux garanti 4.5%/an. Idéal pour constituer un apport.",
            "versement_mensuel": None,  # calculé dynamiquement
            "taux":        0.045,
            "duree":       12,
            "type":        "epargne",
            "emoji":       "🏦",
            "objectif":    "Constituer un apport immobilier",
        },
        {
            "id":          "fonds_impact",
            "nom":         "Fonds d'investissement à impact — ODD",
            "description": "Placement collectif dans des PME locales djiboutiennes. "
                           "Rendement estimé 7-9%/an. Aligné sur les ODD 8 et 10.",
            "versement_mensuel": None,
            "taux":        0.08,
            "duree":       36,
            "type":        "epargne",
            "emoji":       "🌍",
            "objectif":    "Investissement à impact social",
        },
        {
            "id":          "tontine_digitale",
            "nom":         "Tontine digitale — Groupe de 10",
            "description": "Épargne collective entre pairs via mobile money. "
                           "Cycle de 10 mois, mise mensuelle flexible.",
            "versement_mensuel": None,
            "taux":        0.0,         # pas d'intérêt, épargne forcée
            "duree":       10,
            "type":        "epargne",
            "emoji":       "🤝",
            "objectif":    "Épargne disciplinée sans banque",
        },
    ],
}


# ─────────────────────────────────────────────────────────────
# CALCULS FINANCIERS
# ─────────────────────────────────────────────────────────────

def calculer_mensualite(prix: float, apport_pct: float,
                        taux_annuel: float, duree_ans: int) -> dict:
    """
    Calcule la mensualité d'un crédit par la formule bancaire standard.

    Formule : M = K × (t/12) / (1 - (1 + t/12)^-n)
    Où :
        K = capital emprunté (prix - apport)
        t = taux annuel
        n = nombre de mensualités

    Retourne un dict complet avec tous les chiffres utiles.
    """
    apport      = prix * apport_pct
    capital     = prix - apport
    t_mensuel   = taux_annuel / 12
    n           = duree_ans * 12

    if t_mensuel == 0:
        mensualite = capital / n
    else:
        mensualite = capital * t_mensuel / (1 - (1 + t_mensuel) ** -n)

    cout_total  = mensualite * n
    cout_credit = cout_total - capital

    return {
        "apport":       round(apport),
        "capital":      round(capital),
        "mensualite":   round(mensualite),
        "cout_total":   round(cout_total),
        "cout_credit":  round(cout_credit),
        "n_mois":       n,
        "duree_ans":    duree_ans,
        "taux_annuel":  round(taux_annuel * 100, 2),
    }


def evaluer_faisabilite(mensualite: float, user) -> dict:
    """
    Évalue si une mensualité est supportable pour ce profil.

    Règle bancaire universelle :
        mensualité ≤ 33% du revenu net → VERT (faisable)
        mensualité ≤ 40% du revenu net → ORANGE (tendu)
        mensualité > 40% du revenu net → ROUGE (déconseillé)

    On tient aussi compte du coussin de sécurité :
        si mois_securite < 3 → on rétrograde d'un niveau
    """
    revenu = user.revenu_total
    if revenu <= 0:
        return {"statut": "impossible", "couleur": "red",
                "ratio": 0, "message": "Revenu insuffisant"}

    ratio = mensualite / revenu

    if ratio <= 0.33:
        statut, couleur = "faisable", "green"
        message = f"Mensualité raisonnable ({round(ratio*100)}% de vos revenus)"
    elif ratio <= 0.40:
        statut, couleur = "tendu", "orange"
        message = f"Budget serré ({round(ratio*100)}% de vos revenus — limite recommandée : 33%)"
    else:
        statut, couleur = "deconseille", "red"
        message = f"Trop élevé ({round(ratio*100)}% de vos revenus — max recommandé : 33%)"

    # Rétrogradation si coussin insuffisant
    if user.mois_securite < 3 and statut == "faisable":
        statut, couleur = "tendu", "orange"
        message += f" — mais réserve faible ({user.mois_securite:.1f} mois)"

    # Impossible si solde négatif
    if user.solde <= 0:
        statut, couleur = "impossible", "red"
        message = "Solde mensuel négatif — crédit impossible"

    return {
        "statut":  statut,
        "couleur": couleur,
        "ratio":   round(ratio * 100, 1),
        "message": message,
    }


def calculer_epargne(versement: float, taux_annuel: float,
                     duree_mois: int) -> dict:
    """
    Calcule la capitalisation d'une épargne mensuelle.
    Formule des intérêts composés mensuels.
    """
    t = taux_annuel / 12
    if t == 0:
        total = versement * duree_mois
    else:
        total = versement * ((1 + t) ** duree_mois - 1) / t

    interets = total - (versement * duree_mois)
    return {
        "versement":  round(versement),
        "total":      round(total),
        "interets":   round(interets),
        "duree_mois": duree_mois,
    }


# ─────────────────────────────────────────────────────────────
# MOTEUR PRINCIPAL DU COACH
# ─────────────────────────────────────────────────────────────

def generer_coaching(user, score: float,
                     projet_perso: dict = None) -> dict:
    """
    Génère le rapport complet du coach financier.

    Paramètres :
        user         : objet UserData
        score        : score calculé par ai_engine
        projet_perso : dict optionnel si l'utilisateur entre son propre projet
                       {"nom": "...", "prix": 5000000, "type": "immobilier",
                        "duree": 15, "apport": 0.20}

    Retourne un dict avec :
        opportunites  : liste d'opportunités évaluées (vert/orange/rouge)
        projet_perso  : évaluation du projet personnalisé si fourni
        plan_action   : plan mensuel chiffré
        verdict       : message global du coach
        epargne_cible : combien épargner/mois pour débloquer les opportunités
    """

    opportunites_evaluees = []

    # ── Évaluation de chaque opportunité du catalogue ─────────
    for categorie, items in OPPORTUNITES.items():

        # Filtrer selon le score — ne pas proposer le très haut de gamme
        # à quelqu'un avec un score faible (inutile et décourageant)
        for item in items:
            opp = dict(item)  # copie pour ne pas modifier l'original

            if categorie == "epargne":
                # Pour l'épargne : versement = 10% du solde disponible
                versement = max(5_000, round(user.solde * 0.10))
                opp["versement_mensuel"] = versement
                sim = calculer_epargne(versement, opp["taux"], opp["duree"] * 30 // 10)
                opp["simulation"] = sim
                opp["faisabilite"] = {
                    "statut":  "faisable" if user.solde > 0 else "impossible",
                    "couleur": "green"    if user.solde > 0 else "red",
                    "ratio":   round(versement / user.revenu_total * 100, 1) if user.revenu_total > 0 else 0,
                    "message": f"Versement de {versement:,} FDJ/mois ({round(versement/user.revenu_total*100, 1)}% de vos revenus)" if user.revenu_total > 0 else "Revenu insuffisant",
                }

            else:
                # Pour crédit : chercher la durée optimale
                duree_choisie = _duree_optimale(
                    opp["prix"], opp["apport_min"],
                    opp["taux_interet"], opp["duree_max"], user
                )
                sim = calculer_mensualite(
                    opp["prix"], opp["apport_min"],
                    opp["taux_interet"], duree_choisie
                )
                faisabilite = evaluer_faisabilite(sim["mensualite"], user)

                opp["simulation"]   = sim
                opp["faisabilite"]  = faisabilite
                opp["duree_choisie"] = duree_choisie

                # Ajouter info rendement locatif
                if categorie == "locatif" and "loyer_estime" in opp:
                    cash_flow = opp["loyer_estime"] - sim["mensualite"]
                    opp["cash_flow"] = round(cash_flow)
                    opp["cash_flow_positif"] = cash_flow > 0

            opportunites_evaluees.append(opp)

    # ── Trier : faisable → tendu → déconseillé ────────────────
    ordre = {"faisable": 0, "tendu": 1, "deconseille": 2, "impossible": 3}
    opportunites_evaluees.sort(
        key=lambda x: ordre.get(x["faisabilite"]["statut"], 3)
    )

    # ── Évaluation du projet personnel ────────────────────────
    eval_projet_perso = None
    if projet_perso and projet_perso.get("prix", 0) > 0:
        try:
            prix    = float(projet_perso["prix"])
            apport  = float(projet_perso.get("apport", 0.20))
            duree   = int(projet_perso.get("duree", 10))
            taux    = _taux_par_type(projet_perso.get("type", "immobilier"))

            sim         = calculer_mensualite(prix, apport, taux, duree)
            faisabilite = evaluer_faisabilite(sim["mensualite"], user)

            eval_projet_perso = {
                "nom":          projet_perso.get("nom", "Votre projet"),
                "prix":         prix,
                "type":         projet_perso.get("type", "immobilier"),
                "simulation":   sim,
                "faisabilite":  faisabilite,
                "taux_utilise": round(taux * 100, 2),
                "emoji":        "🎯",
            }

            # Cash flow si locatif
            if projet_perso.get("loyer_estime"):
                loyer = float(projet_perso["loyer_estime"])
                eval_projet_perso["cash_flow"] = round(loyer - sim["mensualite"])
                eval_projet_perso["cash_flow_positif"] = loyer > sim["mensualite"]

        except (ValueError, TypeError):
            pass  # projet perso ignoré si données invalides

    # ── Plan d'action mensuel ──────────────────────────────────
    plan = _generer_plan_action(user, score, opportunites_evaluees)

    # ── Verdict global du coach ────────────────────────────────
    verdict = _generer_verdict(user, score, opportunites_evaluees)

    # ── Épargne cible pour débloquer les opportunités ─────────
    epargne_cible = _calculer_epargne_cible(user, opportunites_evaluees)

    return {
        "opportunites":   opportunites_evaluees,
        "projet_perso":   eval_projet_perso,
        "plan_action":    plan,
        "verdict":        verdict,
        "epargne_cible":  epargne_cible,
        # Stats rapides pour l'affichage
        "nb_faisables":   sum(1 for o in opportunites_evaluees
                              if o["faisabilite"]["statut"] == "faisable"),
        "nb_tendus":      sum(1 for o in opportunites_evaluees
                              if o["faisabilite"]["statut"] == "tendu"),
        "nb_deconseillee":sum(1 for o in opportunites_evaluees
                              if o["faisabilite"]["statut"] in ("deconseille","impossible")),
    }


# ─────────────────────────────────────────────────────────────
# HELPERS INTERNES
# ─────────────────────────────────────────────────────────────

def _taux_par_type(type_bien: str) -> float:
    """Taux d'intérêt moyen par type de bien à Djibouti."""
    taux = {
        "immobilier": 0.070,
        "terrain":    0.080,
        "auto":       0.100,
        "locatif":    0.075,
        "epargne":    0.045,
    }
    return taux.get(type_bien, 0.08)


def _duree_optimale(prix, apport_pct, taux, duree_max, user) -> int:
    """
    Trouve la durée minimale pour que la mensualité soit
    ≤ 33% des revenus. Commence par la durée max et descend.
    Retourne la durée choisie (entre 1 et duree_max ans).
    """
    for duree in range(duree_max, 0, -1):
        sim = calculer_mensualite(prix, apport_pct, taux, duree)
        if sim["mensualite"] <= user.revenu_total * 0.33:
            return duree
    return duree_max  # même si ça dépasse 33%, on retourne le max


def _generer_plan_action(user, score: float, opportunites: list) -> list:
    """
    Génère un plan d'action mensuel personnalisé en 3-5 étapes.
    """
    plan = []

    # Étape 1 — urgence si solde négatif
    if user.solde < 0:
        plan.append({
            "numero": 1,
            "titre":  "Réduire les dépenses ce mois-ci",
            "texte":  f"Vous avez un déficit de {abs(user.solde):,.0f} FDJ/mois. "
                      "Identifiez 2-3 postes de dépenses à couper immédiatement.",
            "montant": abs(user.solde),
            "type":   "urgent",
        })
    else:
        plan.append({
            "numero": 1,
            "titre":  "Automatiser votre épargne",
            "texte":  f"Programmez un virement automatique de "
                      f"{round(user.solde * 0.30):,.0f} FDJ (30% de votre solde) "
                      "le jour de votre paie vers un compte épargne dédié.",
            "montant": round(user.solde * 0.30),
            "type":   "action",
        })

    # Étape 2 — coussin de sécurité
    if user.mois_securite < 6:
        manque    = max(0, user.depenses * 6 - user.epargne)
        mois_pour = round(manque / max(1, user.solde * 0.30)) if user.solde > 0 else 99
        plan.append({
            "numero": 2,
            "titre":  "Constituer votre coussin de sécurité",
            "texte":  f"Objectif : 6 mois de charges = {user.depenses * 6:,.0f} FDJ. "
                      f"Il vous manque {manque:,.0f} FDJ. "
                      f"À ce rythme : {mois_pour} mois pour l'atteindre.",
            "montant": manque,
            "type":   "epargne",
        })

    # Étape 3 — apport pour la première opportunité faisable
    faisables = [o for o in opportunites if o["faisabilite"]["statut"] == "faisable"
                 and o.get("simulation", {}).get("apport", 0) > 0]
    if faisables:
        premiere = faisables[0]
        apport_requis = premiere["simulation"]["apport"]
        if apport_requis > user.epargne:
            diff      = apport_requis - user.epargne
            epargne_m = round(user.solde * 0.20)
            mois      = round(diff / epargne_m) if epargne_m > 0 else 99
            plan.append({
                "numero": 3,
                "titre":  f"Préparer l'apport pour : {premiere['nom']}",
                "texte":  f"Apport requis : {apport_requis:,.0f} FDJ. "
                          f"Vous avez {user.epargne:,.0f} FDJ. "
                          f"En épargnant {epargne_m:,.0f} FDJ/mois → "
                          f"prêt dans {mois} mois.",
                "montant": diff,
                "type":   "objectif",
            })
        else:
            plan.append({
                "numero": 3,
                "titre":  f"Vous pouvez financer : {premiere['nom']}",
                "texte":  f"Votre épargne de {user.epargne:,.0f} FDJ couvre "
                          f"l'apport requis de {apport_requis:,.0f} FDJ. "
                          "Contactez votre banque pour initier le dossier.",
                "montant": apport_requis,
                "type":   "faisable",
            })

    # Étape 4 — diversification
    if score >= 550:
        plan.append({
            "numero": len(plan) + 1,
            "titre":  "Diversifier votre patrimoine",
            "texte":  "Votre score vous qualifie pour un placement dans le "
                      "fonds d'impact local (7-9%/an). "
                      f"Avec {round(user.solde * 0.10):,.0f} FDJ/mois, "
                      "vous construisez un patrimoine durable.",
            "montant": round(user.solde * 0.10),
            "type":   "investissement",
        })

    return plan


def _generer_verdict(user, score: float, opportunites: list) -> dict:
    """
    Génère le verdict global du coach en une phrase forte
    + un message détaillé.
    """
    nb_faisables = sum(1 for o in opportunites
                       if o["faisabilite"]["statut"] == "faisable")

    if user.solde <= 0:
        return {
            "titre":   "⚠️ Stabilisation financière prioritaire",
            "message": "Votre solde mensuel est négatif ou nul. "
                       "Aucun investissement ni crédit n'est recommandé. "
                       "La priorité absolue est de réduire les charges.",
            "couleur": "red",
            "score_verbal": "Situation précaire",
        }
    elif nb_faisables == 0:
        return {
            "titre":   "📈 Continuez à épargner",
            "message": f"Avec un revenu de {user.revenu_total:,.0f} FDJ/mois "
                       f"et {user.mois_securite:.1f} mois de réserve, "
                       "vous n'êtes pas encore prêt pour un crédit. "
                       "Augmentez votre épargne pendant 6 mois pour changer de statut.",
            "couleur": "orange",
            "score_verbal": "En progression",
        }
    elif nb_faisables <= 3:
        return {
            "titre":   "✅ Quelques opportunités accessibles",
            "message": f"{nb_faisables} opportunité(s) sont dans votre portée. "
                       "Concentrez-vous sur la plus adaptée à votre projet de vie "
                       "et constituez l'apport requis.",
            "couleur": "teal",
            "score_verbal": "Profil bancable",
        }
    else:
        return {
            "titre":   "🏆 Large accès aux financements",
            "message": f"Votre profil est solide : {nb_faisables} opportunités "
                       "sont accessibles. Vous avez le choix. "
                       "Priorisez selon votre projet de vie et votre horizon.",
            "couleur": "green",
            "score_verbal": "Profil premium",
        }


def _calculer_epargne_cible(user, opportunites: list) -> dict:
    """
    Calcule combien épargner par mois pour débloquer
    la première opportunité actuellement 'tendue'.
    """
    tendus = [o for o in opportunites
              if o["faisabilite"]["statut"] == "tendu"
              and o.get("simulation")]
    if not tendus:
        return None

    cible = tendus[0]
    mensualite_cible = cible["simulation"]["mensualite"]
    # Combien faut-il gagner de plus pour que ratio <= 33% ?
    revenu_necessaire = mensualite_cible / 0.33
    effort_mensuel    = max(0, revenu_necessaire - user.revenu_total)

    return {
        "opportunite_cible": cible["nom"],
        "mensualite":        mensualite_cible,
        "revenu_necessaire": round(revenu_necessaire),
        "effort_mensuel":    round(effort_mensuel),
        "mois_pour_debloquer": round(effort_mensuel / max(1, user.solde * 0.15)) if user.solde > 0 else 99,
    }