// --- Register ---
var doRegister = function(name, email, password) {
    $.ajax({
        method: 'PUT',
        url: '/api/user',
        dataType: 'json',
        data: { name: name, email: email, password: password },
        success: function(data) {
            console.log('success!');
            console.log(data);

            if (data == email) {
                doLogin(email, password);
            } else {
                $('#error').show().text('Cannot create user');
            }
        },
        error: onError
    });
};

$(document).on('submit', '#register', null, function() {
    var name = $('#register input[name="name"]').val();
    var email = $('#register input[name="email"]').val();
    var password = $('#register input[name="password"]').val();

    doRegister(name, email, password);

    return false;
});
