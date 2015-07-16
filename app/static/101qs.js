$(function() {
    var alternateMethod = function(method) {
        return function(evt) {
            evt.preventDefault();

            console.log(evt);
            console.log(method + ' ' + evt.currentTarget.href);

            $.ajax({ type: method, url: evt.currentTarget.href, success: function() { location.reload() } });
        };
    };

    $('.as-delete').click(alternateMethod('delete'));
    $('.as-post').click(alternateMethod('post'));

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
