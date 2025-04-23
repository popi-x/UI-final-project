$(document).ready(function(){
    console.log("test drag_drop loaded");

    $(".draggable").draggable({
        revert: "invalid",
        helper: "clone"
      });
    
      $(".dropzone").droppable({
        accept: ".draggable",
        drop: function (event, ui) {
          const droppedValue = ui.draggable.data("value");
          const $this = $(this);
          $this.data("value", droppedValue);
          $this.text(droppedValue);
    
          ui.draggable.draggable("disable");
          ui.draggable.addClass("used");
        }
      });
    /*
      $("#submit-btn").on("click", function () {
        let userAnswers = {};
        $(".dropzone").each(function (i) {
          userAnswers[`slot_${i}`] = $(this).data("value") || null;
        });
    
        const dataToSend = {
          question_id: 1,
          user_answers: userAnswers
        };
    
        $.ajax({
          url: "/quiz/1/answer",
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify(dataToSend),
          success: function () {
            window.location.href = "/quiz/1/answer";
          }
        });
      });
      */
})
