// --- Create a questionset ---
var doCreateQuestionSet = function(title, startDate, frequency) {
    $.ajax({
        method: 'PUT',
        url: '/api/user/me/questionsets',
        dataType: 'json',
        data: {
            title: title,
            'start-date': startDate,
            frequency: frequency,
            'current-question': 0
        },
        success: function(id) {
            window.location.assign('/questionset/' + id);
        },
        error: onError
    });
};

$(document).on('submit', '#create-questionset', null, function() {
    var title = $('#create-questionset input[name="title"]').val();
    var startDate = $('#create-questionset input[name="start-date"]').val();
    var frequency = $('#create-questionset input[name="frequency"]').val();

    doCreateQuestionSet(title, startDate, frequency);

    return false;
});
