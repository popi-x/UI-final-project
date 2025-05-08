/*
$(document).ready(function () {
    console.log("true_false.js loaded");
    
    $('input[type="radio"]').on('change', function () {
      const val = $(this).val();
      const slot = $(this).data('slot');
  
      // Clear selected styles from all options in the same slot
      $(`input[data-slot="${slot}"]`).each(function () {
        $(this).removeAttr("data-value");
        $(this).parent('label').removeClass('active');  // remove highlight
      });
  
      // Mark selected radio with data-value + highlight
      $(this).attr("data-value", val);
      $(this).parent('label').addClass('active');  // green/red button highlight
    });
  });

 $(document).ready(function () {
  console.log("true_false.js loaded");

  $('input[type="radio"]').on('change', function () {
    const val = $(this).val();
    const slot = $(this).data('slot');

    // Clear data-value from all options in this slot
    $(`input[data-slot="${slot}"]`).removeAttr("data-value");
    $(`label[for="${$(this).attr("id")}"]`).removeClass('active');  // optional reset

    // Set data-value ONLY on the selected input
    this.dataset.value = val; // use native JS assignment (safer than jQuery attr)
    $(this).parent('label').addClass('active'); // re-add visual highlight
  });
});
*/
$(document).ready(function () {
  console.log("true_false.js loaded");

  $('input[type="radio"]').on('change', function () {
    const val = $(this).val();
    const container = $(this).closest('[data-slot]'); // find the nearest data-slot container
    const slot = container.data('slot');

    container.attr('data-value', val);

    // Clear other values and add highlights
    container.find('.btn').removeClass('active');
    $(this).closest('.btn').addClass('active');
  });
});
  