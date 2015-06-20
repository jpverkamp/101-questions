// --- Login ---
var doLogin = function(email, password) {
    $.ajax({
        method: 'POST',
        url: '/api/user/login',
        dataType: 'json',
        data: { email: email, password: password },
        success: function(data) {
            if (data) {
                window.location.assign('/user/me');
            } else {
                $('#error').show().text('Cannot log in');
            }
        },
        error: onError
    });
};

$(document).on('submit', '#login', null, function() {
    var email = $('#login input[name="email"]').val();
    var password = $('#login input[name="password"]').val();

    doLogin(email, password);

    return false;
});
