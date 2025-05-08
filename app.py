from flask import Flask, jsonify, render_template, request, redirect, session, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# Correct answers for each quiz question
correct_answers = {
    1: ['-4', '-3', '-1', '0', '+2', '+3'],
    2: ['800', '1600', '6400', '12800'],
    3: ['f/1.4'],  # Example — you can add complexity later
    4: ['1/1000s', '1/500s'],
    5: ['f7.1 1/30s ISO1250', 'f4.8 1/15s ISO1600', 'f5.6 1/2000s ISO800']
}

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/learn/overview")
def overview():
    return render_template("overview.html")

@app.route("/learn/<string:section>/cover")
def exposure(section):
    with open("data/cover_data.json") as f:
        data = json.load(f)
    return render_template("cover.html", section=section, data=data)


@app.route("/learn/exposure/1")
def exposure_1():
    return render_template("exposure_1.html")


@app.route("/learn/iso/1")
def iso_1():
    return render_template("iso_1.html")


@app.route("/triangle")
def triangle_redirect():
    return redirect(url_for("exposure_triangle", step_id=1))

@app.route("/learn/exposure_triangle/<int:step_id>", methods=["GET", "POST"], endpoint="exposure_triangle")
def triangle(step_id):
    with open("data/exposure_triangle.json") as f:
        content = json.load(f)

    total_steps = len(content)
    session["step"] = step_id
    feedback = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "next":

            # ---------- Special logic for step 3 ----------
            if step_id == 3:
                choice = request.form.get("choice1")
                if choice:
                    session["choice1"] = choice
                    if choice != "Shutter Speed":
                        feedback = "❌ Remember the exposure triangle: once you pick one setting, the other two need to adjust accordingly. Is what you chose the most important setting for this shot? Try again."
                        return render_template("exposure_triangle.html", step=step_id, total_steps=total_steps, data=content[step_id - 1], feedback=feedback)

            # ---------- Special logic for step 5 ----------
            if step_id == 5:
                choice = request.form.get("answer")
                if choice:
                    session["choice5"] = choice
                    if choice != "Shutter speed":
                        feedback = "❌ Incorrect! Remember: to freeze motion, Shutter Speed is the key. Try again."
                        return render_template("exposure_triangle.html", step=step_id, total_steps=total_steps, data=content[step_id - 1], feedback=feedback)

            # ---------- Special logic for step 6 ----------
            if step_id == 6:
                choice = request.form.get("answer")
                if choice:
                    session["choice6"] = choice
                    if choice != "Aperture":
                        feedback = "❌ Not quite! After using fast shutter speed, the next thing to adjust to let in more light is Aperture. Try again."
                        return render_template("exposure_triangle.html", step=step_id, total_steps=total_steps, data=content[step_id - 1], feedback=feedback)

            # ✅ Move to next step
            return redirect(url_for("exposure_triangle", step_id=min(step_id + 1, total_steps)))

        elif action == "prev":
            return redirect(url_for("exposure_triangle", step_id=max(step_id - 1, 1)))

        elif action == "restart":
            session.clear()
            return redirect(url_for("quiz_view", question_id=1))

    return render_template("exposure_triangle.html", step=step_id, total_steps=total_steps, data=content[step_id - 1], feedback=feedback)

@app.route("/learn/aperture/<int:step>", methods=["GET", "POST"])
def aperture(step):
    import json
    from flask import render_template, request, session, redirect, url_for

    with open("data/aperture_data.json") as f:
        content = json.load(f)

    if step < 1 or step > len(content):
        return redirect(url_for("aperture", step=1))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "next" and step < len(content):
            return redirect(url_for("aperture", step=step + 1))
        elif action == "prev" and step > 1:
            return redirect(url_for("aperture", step=step - 1))
        elif action == "restart":
            return redirect(url_for("shutter_speed", step=1))

    data = content[step - 1]
    return render_template("aperture_step.html", step=step, total_steps=len(content), data=data)

@app.route("/learn/shutter_speed/<int:step>", methods=["GET", "POST"])
def shutter_speed(step):
    with open("data/shutter_speed_data.json") as f:
        content = json.load(f)

    if step < 1 or step > len(content):
        return redirect(url_for("shutter_speed", step=1))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "next" and step < len(content):
            return redirect(url_for("shutter_speed", step=step + 1))
        elif action == "prev" and step > 1:
            return redirect(url_for("shutter_speed", step=step - 1))
        elif action == "restart":
            return redirect(url_for("shutter_speed", step=1))

    data = content[step - 1]
    return render_template("shutter_speed_step.html", step=step, total_steps=len(content), data=data)


@app.route("/quiz/<int:question_id>")
def quiz_view(question_id):
    draggable_values = correct_answers.get(question_id, [])
    template_name = f"quiz_{question_id}.html"
    percent = int((question_id / len(correct_answers)) * 100)
    return render_template(template_name, draggable_values=draggable_values, question_id=question_id, progress_percent=percent)


@app.route("/quiz/<int:question_id>/answer", methods=["POST"])
def quiz_post(question_id):
    data = request.get_json()
    user_answers = data.get("user_answers", {})

    # Store answers temporarily in session
    session[f"user_answers_{question_id}"] = user_answers

    return jsonify({"status": "received"})

@app.route("/quiz/<int:question_id>/answer")
def quiz_feedback(question_id):
    correct = correct_answers.get(question_id, [])
    user_data = session.get(f"user_answers_{question_id}", {})
    #DEBUG
    print(f"[DEBUG] Received answers for Quiz {question_id}: {user_data}")

    # Build aligned lists for frontend
    user_answers = [user_data.get(f"slot_{i}") for i in range(len(correct))]
    correctness = [user_answers[i] == correct[i] for i in range(len(correct))]
    is_correct = all(correctness)

    # Store score
    session[f"score_{question_id}"] = sum(correctness)

    # [EDIT]Calculate progress bar width
    percent = int((question_id / len(correct_answers)) * 100)
    return render_template(
        "quiz_answer.html",
        question_id=question_id,
        user_answers=user_answers,
        correct_answers=correct,
        correctness=correctness,
        is_correct=is_correct,
        progress_percent=percent
    )

@app.route("/quiz/results")
def results():
    total_score = 0
    total_possible = 0

    for qid, answers in correct_answers.items():
        score = session.get(f"score_{qid}", 0)
        total_score += score
        total_possible += len(answers)

    return render_template(
        "quiz_results.html",
        score=total_score,
        total=total_possible
    )



# ✅ ADD THIS to make it run properly at port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
