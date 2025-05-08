$(document).ready(function () {
  const qid = getQuestionId();
  const LAST_QUESTION_ID = 5; // ← ID of the last question

  // 1. get quiz ID from current page
  function getQuestionId() {
    const container = document.getElementById("quiz-container");
    return container ? parseInt(container.dataset.questionId) : null;
  }

  // 2. hide submit button on answer/feedback pages
  const path = window.location.pathname;
  if (path.includes("/answer")) {
    $("#submit-btn").hide();
  }

  // 3. submit button
  function submitQuiz(questionId) {
    let userAnswers = {};
    let isComplete = true;
  
    document.querySelectorAll('[data-slot]').forEach((el) => {
      const slot = el.dataset.slot;
      const val = el.dataset.value || null; // get container's data-value
      userAnswers[slot] = val;
  
      if (!val) {
        isComplete = false;
      }
    });
  
    if (!isComplete) {
      alert("Please complete all parts of the question before submitting!");
      return;
    }
  

    fetch(`/quiz/${questionId}/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: questionId,
        user_answers: userAnswers
      })
    }).then(() => {
      window.location.href = `/quiz/${questionId}/answer`;
    });
  }

  // 4. nextpage
  function nextPage(questionId) {
    if (questionId >= LAST_QUESTION_ID) {
      window.location.href = "/quiz/results";
    } else {
      window.location.href = `/quiz/${questionId + 1}`;
    }
  }

  // 5. events
  $('#submit-btn').on('click', function () {
    if (qid) {
      submitQuiz(qid);
    } else {
      alert("Cannot determine quiz ID.");
    }
  });

  $('#show-answer-btn').on('click', function () {
    $('#correct-answers').removeClass('d-none');
  });

  $('#next-btn').on('click', function () {
    if (qid) {
      nextPage(qid);
    }
  });

  //6. Proress Bar
  function renderProgressBar(questionId, totalQuestions = 5) {
    const percent = Math.floor((questionId / totalQuestions) * 100);
    const $bar = $("#quizProgress");
  
    $bar.css("width", `${percent}%`);
    $bar.text(`${percent}%`);
  }
  //renderProgressBar(qid);
  //Function disabled because now it's rendered directly in HTML using server data
  //You can revert this if we want to restore the loading client-side animation later
});
