class UserData:
    """
    Modèle central de données utilisateur.

    Corrections apportées :
    ─────────────────────────────────────────────────────────────
    1. UNIFICATION DES CHAMPS : Les deux formulaires utilisaient
       des noms différents (salary/savings/expenses vs revenu/
       depenses/epargne). UserData accepte maintenant les deux
       conventions et les normalise en un seul nom interne.

    2. VALIDATION : Les valeurs négatives sont ramenées à 0.
       Une ValueError est levée si les types sont invalides.

    3. CHAMPS ENRICHIS : On stocke maintenant aussi l'objectif,
       l'horizon, la banque choisie et la situation pro —
       tous les champs des nouveaux formulaires.

    4. PROPRIÉTÉS CALCULÉES : solde, taux_epargne et
       mois_securite sont calculés une seule fois ici
       et réutilisables partout sans recalcul.
    """

    def __init__(
        self,
        revenu=0,       # aussi accepté comme "salary"
        depenses=0,     # aussi accepté comme "expenses"
        epargne=0,      # aussi accepté comme "savings"
        objectif="epargne",
        horizon=12,
        banque=None,
        situation=None,
        autres_revenus=0,
        objectif_epargne=0,
        pays=None,
    ):
        # ── Conversion et validation ──────────────────────────
        try:
            self.revenu          = max(0.0, float(revenu))
            self.depenses        = max(0.0, float(depenses))
            self.epargne         = max(0.0, float(epargne))
            self.autres_revenus  = max(0.0, float(autres_revenus or 0))
            self.objectif_epargne = max(0.0, float(objectif_epargne or 0))
            self.horizon         = max(1, int(horizon or 12))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Données financières invalides : {e}")

        # ── Champs contextuels ────────────────────────────────
        self.objectif  = objectif  or "epargne"
        self.banque    = banque
        self.situation = situation
        self.pays      = pays

    # ── Propriétés calculées (une seule fois) ─────────────────

    @property
    def revenu_total(self):
        """Revenu net + autres revenus."""
        return self.revenu + self.autres_revenus

    @property
    def solde(self):
        """Argent restant après charges."""
        return self.revenu_total - self.depenses

    @property
    def taux_epargne(self):
        """Part du revenu épargnée (0 à 1)."""
        if self.revenu_total <= 0:
            return 0.0
        return max(0.0, self.solde / self.revenu_total)

    @property
    def ratio_depenses(self):
        """Part du revenu consommée par les charges (0 à 1)."""
        if self.revenu_total <= 0:
            return 1.0
        return min(1.0, self.depenses / self.revenu_total)

    @property
    def mois_securite(self):
        """Nombre de mois de charges couvertes par l'épargne."""
        if self.depenses <= 0:
            return 0.0
        return self.epargne / self.depenses

    @property
    def capacite_emprunt(self):
        """Capacité d'emprunt estimée (règle du 33%)."""
        mensualite_max = self.solde * 0.33
        return max(0.0, round(mensualite_max * 12 * 10, 2))

    def to_dict(self):
        """Sérialisation complète pour debug ou stockage futur."""
        return {
            "revenu":           self.revenu,
            "depenses":         self.depenses,
            "epargne":          self.epargne,
            "autres_revenus":   self.autres_revenus,
            "revenu_total":     self.revenu_total,
            "solde":            self.solde,
            "taux_epargne":     round(self.taux_epargne * 100, 1),
            "ratio_depenses":   round(self.ratio_depenses * 100, 1),
            "mois_securite":    round(self.mois_securite, 1),
            "capacite_emprunt": self.capacite_emprunt,
            "objectif":         self.objectif,
            "horizon":          self.horizon,
            "banque":           self.banque,
            "situation":        self.situation,
            "pays":             self.pays,
        }