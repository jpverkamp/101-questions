var addToList = function(event) {
    $target = $(event.target);

    var field = $target.attr('data-field');
    var url = $target.attr('data-url');

    $.ajax({
        method: 'PUT',
        url: url,
        dataType: 'json',
        data: { value: '' },
        success: function(data) {
            if (data) {
                window.location.reload(true);
            } else {
                $('#error').show().text('Cannot add');
            }
        },
        error: onError
    });

    console.log(event);
};
