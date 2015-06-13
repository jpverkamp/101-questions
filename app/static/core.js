$(function() {
    // Render templates
    if (window.location.pathname.length > 1) {
        var source = $("#content").html();
        var template = Handlebars.compile(source);

        console.log('fetching'); // DEBUG
        $.ajax({
            url: '/api' + window.location.pathname,
            dataType: 'json',
            success: function(data) {
                console.log(data); // DEBUG
                $("#content").html(template(data));
            },
            error: function(err) {
                console.log(err);
                window.location.assign('/');
            },
        });
    } else {
        console.log('ignoring, pathname too short'); // DEBUG

        // At the home page, don't show logout
        $('a#logout').hide();
    }

    var onError = function(err, msg) {
        console.log(err); // DEBUG
        $('#error').show().text(msg);
    };

    // --- Login ---
    var doLogin = function(email, password) {
        console.log('trying to login ' + email); // DEBUG

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


    $('#login').submit(function() {
        var email = $('#login input[name="email"]').val();
        var password = $('#login input[name="password"]').val();

        doLogin(email, password);

        return false;
    });

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

    $('a#logout').click(function() {
        doLogout();
    });

    // --- Register ---
    var doRegister = function(name, email, password) {
        console.log('trying to register ' + email); // DEBUG

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
    }

    $('#register').submit(function() {
        var name = $('#register input[name="name"]').val();
        var email = $('#register input[name="email"]').val();
        var password = $('#register input[name="password"]').val();

        doRegister(name, email, password);

        return false;
    });
});
