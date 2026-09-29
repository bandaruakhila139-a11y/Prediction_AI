from flask import Flask, render_template, request, redirect, url_for, flash
from database import save_project, get_latest_project
from market_analysis import get_market_summary

app = Flask(__name__)
app.secret_key = "ml-project-secret-key"


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    summary = get_market_summary()

    latest_project = None
    try:
        p = get_latest_project()
        if p:
            latest_project = [
                p.get("startup_name"),
                p.get("industry"),
                p.get("business_model"),
                p.get("target_market"),
                p.get("budget"),
                p.get("project_description")
            ]
    except Exception as e:
        print("Database error:", e)

    return render_template(
        "dashboard.html",
        summary=summary,
        latest_project=latest_project
    )


@app.route("/project", methods=["GET", "POST"])
def project():

    if request.method == "POST":
        startup_name = request.form.get("startup_name", "").strip()
        industry = request.form.get("industry", "").strip()
        business_model = request.form.get("business_model", "").strip()
        target_market = request.form.get("target_market", "").strip()
        budget = request.form.get("budget", "0").strip()
        description = request.form.get("description", "").strip()

        if not startup_name or not industry or not business_model:
            flash("Please fill all required fields.", "error")
            return redirect(url_for("project"))

        try:
            save_project({
                "startup_name": startup_name,
                "industry": industry,
                "business_model": business_model,
                "target_market": target_market,
                "budget": budget or 0,
                "project_description": description
            })

            flash("Project submitted successfully!", "success")
            return redirect(url_for("dashboard"))

        except Exception as e:
            print("Database error:", e)
            flash("Database connection failed. Check PostgreSQL settings.", "error")
            return redirect(url_for("project"))

    return render_template("project.html")


@app.route("/risk")
def risk():
    return render_template("placeholder.html", title="Risk Assessment")


@app.route("/recommendations")
def recommendations():
    return render_template("placeholder.html", title="Recommendations")


if __name__ == "__main__":
    app.run(debug=True)
