from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS

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

@app.route("/quiz/<int:question_id>")
def quiz_view(question_id):
    draggable_values = correct_answers.get(question_id, [])
    template_name = f"quiz_{question_id}.html"
    return render_template(template_name, draggable_values=draggable_values, question_id=question_id)


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

    # Build aligned lists for frontend
    user_answers = [user_data.get(f"slot_{i}") for i in range(len(correct))]
    correctness = [user_answers[i] == correct[i] for i in range(len(correct))]
    is_correct = all(correctness)

    # Store score
    session[f"score_{question_id}"] = sum(correctness)

    return render_template(
        "quiz_answer.html",
        question_id=question_id,
        user_answers=user_answers,
        correct_answers=correct,
        correctness=correctness,
        is_correct=is_correct
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
