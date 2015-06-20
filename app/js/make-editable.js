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
