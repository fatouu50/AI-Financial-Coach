from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import UserData
from ai_engine import analyse_financiere
from recommendation import recommander
from coach import generer_coaching

app = Flask(__name__)
app.config.from_object(Config)

def _extraire_user(form):
    def get_float(keys, default=0):
        for key in keys:
            val = form.get(key, "").strip()
            if val:
                try:
                    return float(val)
                except ValueError:
                    raise ValueError(f"Le champ '{key}' doit être un nombre.")
        return float(default)
    def get_int(keys, default=0):
        for key in keys:
            val = form.get(key, "").strip()
            if val:
                try: return int(val)
                except ValueError: return default
        return default

    revenu   = get_float(["revenu","salary"], default=0)
    depenses = get_float(["depenses","expenses"], default=0)
    epargne  = get_float(["epargne","savings"], default=0)
    if revenu   <= 0: raise ValueError("Le revenu mensuel doit être supérieur à 0.")
    if depenses <= 0: raise ValueError("Les dépenses mensuelles doivent être supérieures à 0.")
    return UserData(
        revenu=revenu, depenses=depenses, epargne=epargne,
        autres_revenus=get_float(["autres_revenus"], default=0),
        objectif_epargne=get_float(["objectif_epargne"], default=0),
        horizon=get_int(["horizon"], default=12),
        banque=form.get("banque","").strip() or None,
        situation=form.get("situation","").strip() or None,
        pays=form.get("pays","").strip() or None,
        objectif=form.get("objectif","epargne"),
    )

def _extraire_projet_perso(form):
    prix = form.get("projet_prix","").strip()
    if not prix: return None
    try:
        return {
            "nom":   form.get("projet_nom","Mon projet").strip() or "Mon projet",
            "prix":  float(prix),
            "type":  form.get("projet_type","immobilier"),
            "duree": int(form.get("projet_duree",10)),
            "apport":float(form.get("projet_apport",0.20)),
            "loyer_estime": float(form.get("projet_loyer",0) or 0),
        }
    except: return None

def _analyser_complet(user):
    resultat = analyse_financiere(user)
    reco     = recommander(user, resultat["score"])
    coaching = generer_coaching(user, resultat["score"])
    return resultat, reco, coaching

@app.route("/")
def home(): return render_template("index.html")

@app.route("/banks")
def banks(): return render_template("banks.html")

@app.route("/about")
def about(): return render_template("about.html")

@app.route("/form")
def form():
    banque = request.args.get("banque", "")
    return redirect(url_for("dashboard", banque=banque))

@app.route("/dashboard")
def dashboard():
    if not request.args.get("banque"):
        return redirect(url_for("banks"))
    return render_template("dashboard.html")

@app.route("/situation")
def situation():
    banque = request.args.get("banque","")
    return render_template("situation.html", banque=banque)

@app.route("/analyse", methods=["POST"])
def analyse():
    try:
        user = _extraire_user(request.form)
        resultat, reco, coaching = _analyser_complet(user)
        return render_template("result.html", data=resultat, reco=reco,
                               coaching=coaching, user=user.to_dict())
    except ValueError as e:
        flash(str(e), "error"); return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"Erreur : {e}", "error"); return redirect(url_for("dashboard"))

@app.route("/result", methods=["POST"])
def result():
    try:
        user = _extraire_user(request.form)
        resultat, reco, coaching = _analyser_complet(user)
        return render_template("result.html", data=resultat, reco=reco,
                               coaching=coaching, user=user.to_dict())
    except ValueError as e:
        flash(str(e), "error"); return redirect(url_for("situation"))
    except Exception as e:
        flash(f"Erreur : {e}", "error"); return redirect(url_for("situation"))

@app.route("/forecast", methods=["POST"])
def forecast():
    """GPS Financier — simulation prédictive 3 ans + mode crise."""
    try:
        user    = _extraire_user(request.form)
        resultat = analyse_financiere(user)
        reco     = recommander(user, resultat["score"])
        return render_template("forecast.html", data=resultat, reco=reco, user=user.to_dict())
    except ValueError as e:
        flash(str(e), "error"); return redirect(url_for("banks"))
    except Exception as e:
        flash(f"Erreur : {e}", "error"); return redirect(url_for("banks"))

@app.route("/opportunities", methods=["POST"])
def opportunities():
    """Étape 3 — Affiche les opportunités IA selon le profil."""
    try:
        user    = _extraire_user(request.form)
        resultat = analyse_financiere(user)
        reco     = recommander(user, resultat["score"])
        return render_template("opportunities.html", data=resultat, reco=reco, user=user.to_dict())
    except ValueError as e:
        flash(str(e), "error"); return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"Erreur : {e}", "error"); return redirect(url_for("dashboard"))

@app.route("/coach", methods=["POST"])
def coach():
    try:
        user         = _extraire_user(request.form)
        projet_perso = _extraire_projet_perso(request.form)
        resultat     = analyse_financiere(user)
        coaching     = generer_coaching(user, resultat["score"], projet_perso)
        return render_template("coach.html", data=resultat, coaching=coaching,
                               user=user.to_dict(), projet_perso=projet_perso)
    except ValueError as e:
        flash(str(e), "error"); return redirect(url_for("dashboard"))
    except Exception as e:
        flash(f"Erreur coach : {e}", "error"); return redirect(url_for("dashboard"))

@app.errorhandler(404)
def page_not_found(e): return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e): return render_template("500.html"), 500

if __name__ == "__main__":
    import os
    app.run(debug=app.config["DEBUG"], host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000)))