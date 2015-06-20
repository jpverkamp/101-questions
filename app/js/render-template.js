var source = $("#template").html();
var template = Handlebars.compile(source);

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
