import os

class Config:
    # ── Sécurité ────────────────────────────────────────────────
    # La SECRET_KEY ne doit JAMAIS être en dur dans le code.
    # On la lit depuis une variable d'environnement.
    # Si elle n'existe pas (dev local), on utilise un fallback.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-change-in-production")

    # ── Mode debug ──────────────────────────────────────────────
    # En production, mettre DEBUG=False dans les variables d'env.
    DEBUG = os.environ.get("DEBUG", "true").lower() == "true"

    # ── Métadonnées de l'app ────────────────────────────────────
    APP_NAME    = "AI Inclusive Finance"
    APP_VERSION = "2.0.0"
    APP_LOCALE  = "fr_DJ"  # Djibouti