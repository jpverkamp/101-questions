
$(function() {
    var alternateMethod = function(method) {
        return function(evt) {
            evt.preventDefault();

            if (method == 'delete' && !confirm('Are you sure you wish to delete this item?')) {
                return;
            }

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

    $('.toggleable').each(function(i, el) {
        var url = $(el).attr('data-url');
        var name = $(el).attr('name');
        var value = $(el).attr('value');

        $(this).click(function() {
            $.ajax({
                url: url,
                method: 'POST',
                data: {
                    name: name,
                    value: value,
                    state: $(el).is(':checked')
                }
            });
        });
    });

    $('.selectable').each(function(i, el) {
        var url = $(el).attr('data-url');
        var name = $(el).attr('name');

        $(this).change(function() {
            $.ajax({
                url: url,
                method: 'POST',
                data: {
                    name: name,
                    value: $(el).val()
                }
            });
        });
    });

    $('#page-list-toggle').click(function() {
        console.log('hello');
        $('#page-list-short').hide();
        $('#page-list-all').show();
        return false;
    });
});
