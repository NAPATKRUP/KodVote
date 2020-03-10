$(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
  });

$(function () {
  $('#datetimepicker1').datetimepicker({
      locale: 'th',
      minDate : new Date(),
      defaultDate: new Date()
  });
  $('#datetimepicker2').datetimepicker({
      locale: 'th',
      minDate : new Date()
  });
});

$('#myModal').modal({
  backdrop: 'static',
  keyboard: false
});