from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)

# Sample correct answers for quiz 1
correct_answers = {
    1: {
        "slot_0": "-4",
        "slot_1": "-3",
        "slot_2": "-1",
        "slot_3": "0",
        "slot_4": "+2",
        "slot_5": "+3"
    }
}

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/quiz/<int:question_num>')
def quiz_page(question_num):
    return render_template("quiz.html", question_num=question_num)

@app.route('/quiz/<int:question_num>/answer', methods=['POST', 'GET'])
def quiz_answer(question_num):
    if request.method == 'POST':
        data = request.get_json()
        user_answers = data.get('user_answers', {})
        correct = correct_answers.get(question_num, {})

        correctness = []
        score = 0
        for i in range(len(correct)):
            correct_value = correct.get(f"slot_{i}")
            user_value = user_answers.get(f"slot_{i}")
            is_correct = user_value == correct_value
            correctness.append(is_correct)
            if is_correct:
                score += 1

        session[f"quiz_{question_num}_score"] = score
        session[f"quiz_{question_num}_user_answers"] = user_answers
        return jsonify(success=True)

    # For GET: render feedback page
    user_answers = session.get(f"quiz_{question_num}_user_answers", {})
    correct = correct_answers.get(question_num, {})
    correctness = [user_answers.get(f"slot_{i}") == correct.get(f"slot_{i}") for i in range(len(correct))]
    is_correct = all(correctness)

    return render_template("quiz_answer.html",
                           question_num=question_num,
                           user_answers=[user_answers.get(f"slot_{i}", "") for i in range(len(correct))],
                           correct_answers=[correct.get(f"slot_{i}", "") for i in range(len(correct))],
                           correctness=correctness,
                           is_correct=is_correct)

@app.route('/quiz/results')
def quiz_results():
    total_score = sum(session.get(key, 0) for key in session if key.endswith('_score'))
    return f"<h1>Your final score: {total_score}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
