// --- Logout ---
var doLogout = function() {
    $.ajax({
        method: 'POST',
        url: '/api/user/logout',
        dataType: 'json',
        success: function(data) {
            if (data) {
                window.location.assign('/');
            } else {
                $('#error').show().text('Cannot log out');
            }
        },
        error: onError
    });
};

$(document).on('click', 'a#logout', null, function() {
    doLogout();
});
