from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

# Temporary in-memory store for quiz results (reset each time the server restarts)
quiz_results = {}

@app.route("/quiz/1")
def quiz_1():
    draggable_values = ['-4', '-3', '-1', '0', '+2', '+3']
    return render_template("quiz.html", draggable_values=draggable_values)

@app.route("/quiz/1/answer", methods=["POST"])
def quiz_1_answer_post():
    data = request.get_json()
    question_id = data.get("question_id")
    user_answers = data.get("user_answers")

    # Store the result
    quiz_results[question_id] = {
        "user_answers": user_answers
    }

    return jsonify({"status": "received"})

@app.route("/quiz/1/answer")
def quiz_1_answer_view():
    question_id = 1
    correct_answers = ['-4', '-3', '-1', '0', '+2', '+3']
    user_data = quiz_results.get(question_id, {}).get("user_answers", {})

    user_answers = [user_data.get(f"slot_{i}") for i in range(6)]
    correctness = [user_answers[i] == correct_answers[i] for i in range(6)]
    is_correct = all(correctness)

    return render_template(
        "quiz_answer.html",
        user_answers=user_answers,
        correct_answers=correct_answers,
        correctness=correctness,
        is_correct=is_correct
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)
