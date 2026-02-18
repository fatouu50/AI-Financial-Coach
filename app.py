from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulation", methods=["GET", "POST"])
def simulation():
    if request.method == "POST":
        bank = request.form["bank"]
        salary = float(request.form["salary"])
        savings = float(request.form["savings"])
        expenses = float(request.form["expenses"])

        debt_ratio = (expenses / salary) * 100
        remaining = salary - expenses

        # Score financier simple
        score = 100 - debt_ratio

        # Recommandation intelligente
        if debt_ratio > 50:
            recommendation = "⚠️ Situation risquée. Priorité : stabiliser vos finances."
        elif remaining > 1000 and savings > 5000:
            recommendation = "🏠 Vous pouvez envisager un investissement immobilier."
        elif remaining > 500:
            recommendation = "🚗 Un investissement modéré comme un véhicule est envisageable."
        else:
            recommendation = "💡 Recommandation : renforcer votre épargne avant d’investir."

        return render_template(
            "result.html",
            bank=bank,
            salary=salary,
            savings=savings,
            expenses=expenses,
            debt_ratio=round(debt_ratio, 2),
            remaining=remaining,
            score=round(score, 2),
            recommendation=recommendation
        )

    return render_template("simulation.html")

if __name__ == "__main__":
    app.run(debug=True)
