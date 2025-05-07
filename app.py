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

@app.route("/learn/exposure/cover")
def exposure():
    return render_template("exposure_cover.html")

@app.route("/learn/exposure/1")
def exposure_1():
    return render_template("exposure_1.html")

@app.route("/learn/iso/cover")
def iso_cover():
    return render_template("iso_cover.html")

@app.route("/learn/iso/1")
def iso_1():
    return render_template("iso_1.html")


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
            return redirect(url_for("quiz_view", question_id=1))

    return render_template("triangle_step.html", step=step_id)


@app.route("/aperture/<int:step>", methods=["GET", "POST"])
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

@app.route("/shutter_speed/<int:step>", methods=["GET", "POST"])
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

    # Define image files per quiz
    image_sets = {
        1: ["quiz1_img1.png", "quiz1_img2.png", "quiz1_img3.png", "quiz1_img4.png", "quiz1_img5.png", "quiz1_img6.png"],
        2: ["quiz2_img1.png", "quiz2_img2.png", "quiz2_img3.png", "quiz2_img4.png"],
        3: ["quiz3_img1.png"],
        4: ["quiz4_img1.png", "quiz4_img2.png", "quiz4_img3.png"],
        5: ["quiz5_img1.png", "quiz5_img2.png", "quiz5_img3.png"]
    }

    image_files = image_sets.get(question_id, [])

    return render_template(template_name,
                           draggable_values=draggable_values,
                           image_files=image_files,
                           question_id=question_id,
                           progress_percent=percent)


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


if __name__ == "__main__":
    app.run(debug=True, port=5001)
