from flask import Flask, jsonify, render_template, request, redirect, session, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# Correct answers for each quiz question
correct_answers = {
    1: ['Exposure', 'Shutter Speed', 'ISO', 'Aperture'],
    2: ['-4', '0', '+3', '+2', '-1', '-3'],
    3: ['12800', '800', '1600', '6400'],
    4: ['f1.4'],  # Example — you can add complexity later
    5: ['False', 'False', 'True'],
    6: ['False', 'True', 'True', 'False', 'False'],
    7: ['unselected', 'Shutter Speed', 'Aperture'],
    # 8: ['High', 'Medium', 'Medium'],
    8: ['f4.8 1/15s ISO1600', 'f7.1 1/30s ISO1250', 'f5.6 1/2000s ISO800']
}

draggable_options = {
    1: ['Shutter Speed', 'Aperture', 'ISO', 'Exposure'],
    2: ['-4', '-3', '-1', '0', '+2', '+3'],
    3: ['800', '1600', '6400', '12800'],
    4: ['f0.95', 'f1.4', 'f2.0', 'f2.8', 'f4', 'f5.6', 'f8', 'f11', 'f14', 'f16'],
    8: ['f7.1 1/30s ISO1250', 'f4.8 1/15s ISO1600', 'f5.6 1/2000s ISO800']
}

quiz_questions = {
    1: "Match the terms with the correct concepts",
    2: "Drag and drop the correct exposure value below each photo",
    3: "Drag and drop the correct ISO used in each photo",
    4: "Adjust the aperture slider so that only the desired object appears sharp and in focus",
    5: "Judge if the given shutter speed matches with the scenario",
    6: "Determine if the following statements are true or false",
    7: "Choose the parameter(s) that you need to adjust first in the given scenario",
    # 8: "Choose the parameter(s) that you need to adjust first in the given scenario",
    8: "Match the photos with the correct settings"
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
    with open("data/exposure_triangle.json", encoding="utf8") as f:
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
            if step_id == 4:
                choice = request.form.get("answer")
                if choice:
                    session["choice5"] = choice
                    if choice != "Shutter speed":
                        feedback = "❌ Incorrect! Remember: to freeze motion, Shutter Speed is the key. Try again."
                        return render_template("exposure_triangle.html", step=step_id, total_steps=total_steps, data=content[step_id - 1], feedback=feedback)

            # ---------- Special logic for step 6 ----------
            if step_id == 5:
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
    draggable_values = draggable_options.get(question_id, [])
    template_name = f"quiz_{question_id}.html"
    percent = int((question_id / len(correct_answers)) * 100)

    # Define image files per quiz
    image_sets = {
        2: ["quiz2_img1.png", "quiz2_img2.png", "quiz2_img3.png", "quiz2_img4.png", "quiz2_img5.png", "quiz2_img6.png"],
        3: ["quiz3_img1.png", "quiz3_img2.png", "quiz3_img3.png", "quiz3_img4.png"],
        4: ["quiz4_img1.png"],
        5: ["quiz5_img1.png", "quiz5_img2.png", "quiz5_img3.png"],
        8: ["quiz9_img1.png", "quiz9_img2.png", "quiz9_img3.png"]
    }

    image_files = image_sets.get(question_id, [])

    return render_template(template_name,
                           draggable_values=draggable_values,
                           image_files=image_files,
                           question_id=question_id,
                           progress_percent=percent,
                           quiz_questions=quiz_questions)


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

    user_answers = [user_data.get(f"slot_{i}") for i in range(len(correct))]
    correctness = [user_answers[i] == correct[i] for i in range(len(correct))]
    is_correct = all(correctness)

    session[f"score_{question_id}"] = sum(correctness)
    percent = int((question_id / len(correct_answers)) * 100)

    # Load same images used in quiz
    image_sets = {
        2: ["quiz2_img1.png", "quiz2_img2.png", "quiz2_img3.png", "quiz2_img4.png", "quiz2_img5.png", "quiz2_img6.png"],
        3: ["quiz3_img1.png", "quiz3_img2.png", "quiz3_img3.png", "quiz3_img4.png"],
        4: ["quiz4_img1.png"],
        5: ["quiz5_img1.png", "quiz5_img2.png", "quiz5_img3.png"],
        8: ["quiz9_img1.png", "quiz9_img2.png", "quiz9_img3.png"]
    }

    image_files = image_sets.get(question_id, [])

    is_mcq = question_id == 7

    return render_template(
        "quiz_answer.html",
        is_mcq = is_mcq,
        question_id=question_id,
        user_answers=user_answers,
        correct_answers=correct,
        correctness=correctness,
        is_correct=is_correct,
        progress_percent=percent,
        image_files=image_files,
        quiz_questions=quiz_questions
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

@app.route("/quiz/restart")
def quiz_restart():
    # Clear previous quiz answers and scores
    for key in list(session.keys()):
        if key.startswith("score_") or key.startswith("user_answers_"):
            session.pop(key)
    return redirect(url_for('quiz_view', question_id=1))



if __name__ == "__main__":
    app.run(debug=True, port=5001)
