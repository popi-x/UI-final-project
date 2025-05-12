/*$(document).ready(function () {
    $('.mcq-btn').on('click', function () {
      const $btn = $(this);
      const $slot = $btn.closest('[data-slot]');
      const currentValue = $slot.data('value');
      const newValue = (currentValue === $btn.data('value')) ? 'unselected' : $btn.data('value');
  
      $slot.attr('data-value', newValue);
      $btn.toggleClass('active', newValue !== 'unselected');
    });
  });
*/
$(document).ready(function () {
    $('.mcq-btn').on('click', function () {
      const $btn = $(this);
      const $slot = $btn.closest('[data-slot]');
      const currentValue = $slot.attr('data-value');
      const btnValue = $btn.data('value');
  
      // Unselect if already selected when clicked
      if (currentValue === btnValue) {
        $slot.attr('data-value', 'unselected');
        $btn.removeClass('active');
      } 
      // select when clicked
      else {
        $slot.attr('data-value', btnValue);
        $slot.find('.mcq-btn').removeClass('active'); // 清除同组其他按钮的选中状态
        $btn.addClass('active');
      }
    });
  });