from flask import Flask, render_template, request
from rules import rule_based_score
from hf_model import hf_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        text = request.form["message"]

        rule_s, reasons = rule_based_score(text)

        if rule_s < 50:
            hf_s, hf_reason = hf_score(text)
        else:
            hf_s, hf_reason = 0, "AI model skipped (rule-based confidence high)"

        final_score = (0.7 * rule_s) + (0.3 * hf_s)

        if rule_s > 60:
            final_score = max(final_score, 75)
            reasons.append("Strong scam indicators from rule-based system")

        if hf_s != 0:
            reasons.append(hf_reason)

        final_score = min(final_score, 100)

        # Risk level
        if final_score >= 75:
            risk = "High"
        elif final_score >= 45:
            risk = "Medium"
        else:
            risk = "Low"

        result = {
            "score": round(final_score, 2),
            "risk": risk,
            "reasons": list(set(reasons))
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
