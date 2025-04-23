from flask import Flask, render_template, request, redirect, session, url_for
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/triangle")
def triangle_redirect():
    return redirect(url_for("triangle", step_id=1))

@app.route("/learn/<int:step_id>", methods=["GET", "POST"])
def triangle(step_id):
    session["step"] = step_id
    feedback = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "next":
            # Handle logic for step 3 with feedback
            if step_id == 3:
                choice = request.form.get("choice1")
                session["choice1"] = choice
                if choice != "Shutter Speed":
                    feedback = "❌ Remember the exposure triangle: once you pick one setting, the other two need to adjust accordingly. Is what you chose the most important setting for this shot? Try again."
                    return render_template("triangle_step.html", step=step_id, feedback=feedback)
            return redirect(url_for("triangle", step_id=step_id + 1))

        elif action == "prev":
            return redirect(url_for("triangle", step_id=step_id - 1))

        elif action == "restart":
            session.clear()
            return redirect(url_for("triangle", step_id=1))

    return render_template("triangle_step.html", step=step_id)

# ✅ ADD THIS to make it run properly at port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
