$(document).ready(function () {
  const qid = getQuestionId();
  const LAST_QUESTION_ID = 8;

  function getQuestionId() {
    const container = document.getElementById("quiz-container");
    return container ? parseInt(container.dataset.questionId) : null;
  }

  const path = window.location.pathname;
  if (path.includes("/answer")) {
    $("#submit-btn").hide();
  }

  function submitQuiz(questionId) {
    let userAnswers = {};

    if (questionId === 4) {
      const slider = document.getElementById("aperture-slider");
      const idx = parseInt(slider.value);
      const value = window.apertureValues[idx];
      console.log("🎯 Submitting aperture value:", value); // ADD THIS
      userAnswers["slot_0"] = value;
    } else {
      // Handle drag-and-drop quizzes
      let isComplete = true;
    
      document.querySelectorAll('[data-slot]').forEach((el) => {
        const slot = el.dataset.slot;
        const val = el.dataset.value || null; // get container's data-value
        userAnswers[slot] = val;
        console.log("im here")
    
        if (!val) {
          isComplete = false;
        }
      });
    
      if (!isComplete) {
        alert("Please complete all parts of the question before submitting!");
        return;
      }
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

  function nextPage(questionId) {
    if (questionId >= LAST_QUESTION_ID) {
      window.location.href = "/quiz/results";
    } else {
      window.location.href = `/quiz/${questionId + 1}`;
    }
  }

  $('#submit-btn').on('click', function () {
    if (qid) {
      submitQuiz(parseInt(qid));
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
});

// Clear answer functionality
$('#clear-answer-btn').on('click', function () {
  // Reset all dropzones
  $('.dropzone').each(function () {
    $(this).text('').removeAttr('data-value').removeData('value');
  });

  // Re-enable draggable items
  $('.draggable').each(function () {
    $(this).removeClass('used');
    $(this).draggable('enable');
  });

  // T/F
  $('.btn.active').removeClass('active');
  $('input[type=radio]').prop('checked', false);

  // Reset MCQ buttons (like in quiz 7)
  $('.mcq-btn').removeClass('active');
  $('[data-slot]').attr('data-value', 'unselected');


  // Reset slider (if it's a slider question like quiz 3)
  const slider = document.getElementById("aperture-slider");
  const label = document.getElementById("aperture-value");
  if (slider && label && window.apertureValues) {
    slider.value = 0;
    label.textContent = window.apertureValues[0];
  }
});
