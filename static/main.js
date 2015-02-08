$(function() {
  $('.view#landing').show();

  var renderQuestionSet = function(data) {
    $.ajax({
      url: '/static/questionset.template.htm',
      cache: true,
      dataType: 'html',
      success: function(template) {
        var compiledTemplate = Handlebars.compile(template);
        var html = compiledTemplate(data);

        $('.container').hide();
        $('#questionset').html(html).show();
      }
    });
  };

  $('#loadButton').click(function() {
    var id = $('input[name="loadID"]').val();

    $.ajax({
      type: 'GET',
      url: '/questionset/' + id,
      dataType: 'json',
      success: renderQuestionSet
    });

    return false;
  });

  $('#createButton').click(function() {
    var title = $('input[name="createTitle"]').val();
    var frequency = $('input[name="createFrequency"]').val();
    var email = $('input[name="createEmail"]').val();

    $.ajax({
      type: 'POST',
      url: '/questionset',
      data: {
        title: title,
        frequency: frequency,
        email: email
      },
      dataType: 'json',
      success: renderQuestionSet
    });

    return false;
  });

});
