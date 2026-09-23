from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv
import io
import os

app = Flask(__name__)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "digigrow-dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digigrow.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    business = db.Column(db.String(150), nullable=False)
    platform = db.Column(db.String(80), nullable=False)
    confidence = db.Column(db.Integer, nullable=False)
    online_presence = db.Column(db.Integer, nullable=False)
    challenges = db.Column(db.Text, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ModuleProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_slug = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(150), nullable=False)
    views = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


MODULES = {
    "social-media": {
        "title": "Social Media Marketing",
        "icon": "📱",
        "description": "Learn how to use social media platforms to promote your business and connect with customers.",
        "topics": [
            "Instagram Business",
            "Facebook Pages",
            "WhatsApp Business",
            "Creating attractive posts",
            "Using hashtags",
            "Customer engagement",
            "Posting consistently"
        ],
        "activity": "Create one promotional post for your business. Add your product name, price, contact number and a short description."
    },

    "canva": {
        "title": "Canva & Content Creation",
        "icon": "🎨",
        "description": "Learn how to create attractive posters, social media posts and promotional content using Canva.",
        "topics": [
            "Introduction to Canva",
            "Choosing templates",
            "Adding text and images",
            "Business branding",
            "Creating product posters",
            "Instagram post sizes",
            "Design tips"
        ],
        "activity": "Create a simple promotional poster for one product or service using a Canva template."
    },

    "google-business": {
        "title": "Google Business Profile",
        "icon": "📍",
        "description": "Learn how customers can discover your business through Google Search and Google Maps.",
        "topics": [
            "Creating a business profile",
            "Adding business name and address",
            "Adding phone number and working hours",
            "Uploading business photos",
            "Managing customer reviews",
            "Posting business updates",
            "Keeping information updated"
        ],
        "activity": "Prepare the information required for your Google Business Profile, including business name, address, phone number, hours and photos."
    },

    "ecommerce": {
        "title": "E-Commerce & Online Selling",
        "icon": "🛒",
        "description": "Learn how to present products online, receive orders and communicate with customers.",
        "topics": [
            "Introduction to online selling",
            "Creating product listings",
            "Writing product descriptions",
            "Product photography",
            "Setting prices",
            "Managing customer orders",
            "Customer communication"
        ],
        "activity": "Create a sample online product listing with product name, photo, description, price and contact details."
    },

    "digital-payments": {
        "title": "Digital Payment Awareness",
        "icon": "💳",
        "description": "Learn how to accept digital payments safely using UPI and QR codes.",
        "topics": [
            "Understanding UPI",
            "Using QR codes",
            "Accepting digital payments",
            "Checking payment confirmation",
            "Avoiding payment scams",
            "Protecting UPI PIN",
            "Safe digital payment practices"
        ],
        "activity": "Prepare a five-step checklist for safely accepting a digital payment from a customer."
    },

    "resources": {
        "title": "Resources & Tips",
        "icon": "📚",
        "description": "Use these practical tips and checklists to continue improving your digital presence.",
        "topics": [
            "Daily social media checklist",
            "Content planning",
            "Customer response tips",
            "Online presence checklist",
            "Digital payment safety",
            "Product promotion tips",
            "One-week marketing plan"
        ],
        "activity": "Create a one-week digital marketing action plan for your business."
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/training")
def training():
    return render_template("training.html", modules=MODULES)


@app.route("/module/<slug>", methods=["GET", "POST"])
def module(slug):
    data = MODULES.get(slug)
    if not data:
        return render_template("404.html"), 404
    progress = ModuleProgress.query.filter_by(module_slug=slug).first()
    if not progress:
        progress = ModuleProgress(module_slug=slug, title=data["title"], views=1)
        db.session.add(progress)
    else:
        progress.views += 1
    db.session.commit()
    return render_template("module.html", module=data, slug=slug)


@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        try:
            response = SurveyResponse(
                survey_type=request.form["survey_type"],
                name=request.form["name"].strip(),
                business=request.form["business"].strip(),
                platform=request.form["platform"],
                confidence=int(request.form["confidence"]),
                online_presence=int(request.form["online_presence"]),
                challenges=request.form["challenges"].strip(),
                feedback=request.form.get("feedback", "").strip()
            )
            db.session.add(response)
            db.session.commit()
            flash("Thank you! Your survey response has been saved.", "success")
            return redirect(url_for("survey"))
        except (KeyError, ValueError):
            flash("Please complete all required survey fields.", "error")
    return render_template("survey.html")


def average(rows, field):
    return round(sum(getattr(r, field) for r in rows) / len(rows), 1) if rows else 0


@app.route("/results")
def results():
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.asc()).all()
    pre = [r for r in responses if r.survey_type == "pre"]
    post = [r for r in responses if r.survey_type == "post"]
    stats = {
        "total": len(responses),
        "pre": len(pre),
        "post": len(post),
        "pre_confidence": average(pre, "confidence"),
        "post_confidence": average(post, "confidence"),
        "pre_presence": average(pre, "online_presence"),
        "post_presence": average(post, "online_presence")
    }
    stats["confidence_change"] = round(stats["post_confidence"] - stats["pre_confidence"], 1) if pre and post else 0
    stats["presence_change"] = round(stats["post_presence"] - stats["pre_presence"], 1) if pre and post else 0
    return render_template("results.html", stats=stats)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        flash("Invalid username or password.", "error")

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.desc()).all()
    contacts = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    module_rows = ModuleProgress.query.order_by(ModuleProgress.views.desc()).all()

    pre = [r for r in responses if r.survey_type == "pre"]
    post = [r for r in responses if r.survey_type == "post"]

    platforms = ["Instagram", "Facebook", "WhatsApp Business", "Google Business Profile", "None yet", "Other"]
    platform_counts = {platform: sum(r.platform == platform for r in responses) for platform in platforms}

    challenge_counts = {}
    for response in responses:
        challenge = response.challenges.strip() or "Not specified"
        challenge_counts[challenge] = challenge_counts.get(challenge, 0) + 1
    top_challenges = sorted(challenge_counts.items(), key=lambda item: (-item[1], item[0]))[:6]

    stats = {
        "total": len(responses),
        "pre": len(pre),
        "post": len(post),
        "contacts": len(contacts),
        "pre_confidence": average(pre, "confidence"),
        "post_confidence": average(post, "confidence"),
        "pre_presence": average(pre, "online_presence"),
        "post_presence": average(post, "online_presence"),
        "module_views": sum(m.views for m in module_rows)
    }

    chart_data = {
        "confidence": [stats["pre_confidence"], stats["post_confidence"]],
        "presence": [stats["pre_presence"], stats["post_presence"]],
        "platform_labels": list(platform_counts.keys()),
        "platform_values": list(platform_counts.values())
    }

    return render_template(
        "admin.html",
        stats=stats,
        responses=responses,
        contacts=contacts,
        module_rows=module_rows,
        top_challenges=top_challenges,
        chart_data=chart_data
    )


@app.route("/admin/export/surveys")
def export_surveys():
    responses = SurveyResponse.query.order_by(SurveyResponse.created_at.asc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Survey Type", "Name", "Business", "Platform",
        "Confidence", "Online Presence", "Challenges", "Feedback", "Created At"
    ])
    for r in responses:
        writer.writerow([
            r.id, r.survey_type, r.name, r.business, r.platform,
            r.confidence, r.online_presence, r.challenges, r.feedback or "",
            r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
        ])
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=digigrow_survey_results.csv"}
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not all(request.form.get(k, "").strip() for k in ["name", "email", "message"]):
            flash("Please fill in all contact fields.", "error")
        else:
            db.session.add(ContactMessage(
                name=request.form["name"].strip(),
                email=request.form["email"].strip(),
                message=request.form["message"].strip()
            ))
            db.session.commit()
            flash("Your message has been received. Thank you!", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")


@app.route("/api/stats")
def api_stats():
    responses = SurveyResponse.query.all()
    return jsonify({
        "survey_responses": len(responses),
        "pre_training": sum(r.survey_type == "pre" for r in responses),
        "post_training": sum(r.survey_type == "post" for r in responses),
        "module_views": sum(m.views for m in ModuleProgress.query.all())
    })


@app.context_processor
def inject_globals():
    return {"year": datetime.now().year, "modules": MODULES}


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DigiGrow database initialized.")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
