$(function() {
    var source = $("#template").html();
    var template = Handlebars.compile(source);

    // Make an item editable
    var makeEditable = function() {
        var field = $(this).attr('data-field');
        var url = $(this).attr('data-url');

        $(this).editable({
            title: 'Enter new ' + field,
            type: 'text',
            pk: 1,
            url: url,
            ajaxOptions: { type: 'POST' },
            /* params: function(params) {
                var result = {};
                result[field] = params.value;
                return result;
            } */
        });
    };

    // Render templates
    if (window.location.pathname.length > 1) {
        $.ajax({
            url: '/api' + window.location.pathname,
            dataType: 'json',
            success: function(data) {
                $("#content").html(template(data));
                $("#content .editable").each(makeEditable);
            },
            error: function(err) {
                window.location.assign('/');
            },
        });
    } else {
        // At the home page, don't show logout
        $("#content").html(template());
        $('a#logout').hide();
    }

    var onError = function(err, msg) {
        $('#error').show().text(msg);
    };

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

    $('#register').submit(function() {
        var name = $('#register input[name="name"]').val();
        var email = $('#register input[name="email"]').val();
        var password = $('#register input[name="password"]').val();

        doRegister(name, email, password);

        return false;
    });

    // --- Create a questionset ---
    var doCreateQuestionSet = function(title, startDate, frequency) {
        $.ajax({
            method: 'PUT',
            url: '/api/questionset',
            dataType: 'json',
            data: { title: title, 'start-date': startDate, frequency: frequency },
            success: function(id) {
                window.location.assign('/api/questionset/' + id);
            },
            error: onError
        });
    };

    $('#create-questionset').submit(function() {
        var title = $('#create-questionset input[name="title"]').val();
        var startDate = $('#create-questionset input[name="start-date"]').val();
        var frequency = $('#create-questionset input[name="frequency"]').val();

        doCreateQuestionSet(title, startDate, frequency);

        return false;
    });

});
