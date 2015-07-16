$(function() {
    $('.postit').click(function(evt) {
        evt.preventDefault();

        g = evt;
        console.log(evt.target.href);

        $.ajax({
            type: 'POST',
            url: evt.target.href,
            success: function() { location.reload() }
        });
    });

    $('.editable').each(function(i, el) {
        var field = $(el).attr('data-field');
        var url = $(el).attr('data-url');

        $(this).editable({
            title: 'Enter new ' + field,
            type: 'text',
            pk: 1,
            url: url,
            ajaxOptions: { type: 'POST' },
        });
    });
});
