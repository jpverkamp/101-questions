$(function() {
    $('.view#landing').show();

    var editableText = function(qsid, id, field) {
        $(id + ' .item').editable({
            title: 'Enter new ' + field,
            type: 'text',
            pk: 1,
            url: '/questionset/' + qsid + '/' + field,
            ajaxOptions: { type: 'put' },
            params: function(params) {
                var result = {};
                result[field] = params.value;
                return result;
            }
        });
    };

    var editableList = function(qsid, id, field) {
        $(id + ' .new').click(function() {
            var postData = {};
            postData[field] = '';

            $.ajax({
                type: 'POST',
                url: '/questionset/' + qsid + '/' + field,
                data: postData,
                dataType: 'json',
                success: renderQuestionSet
            });
        });

        $(id + ' .import').click(function() {
            console.log('hello word');

            var postData = {};
            postData[field] = '';

            $('#import-dialog .field-name').text(field + 's');
            $('#import-dialog-values').val('')
            $('#import-dialog').modal('show');

            $('#import-dialog-save').unbind('click').click(function() {
                $('#import-dialog').modal('hide');

                var postData = {};
                postData[field + 's'] = JSON.stringify($('#import-dialog-values').val().split(/\n/g));
                $.ajax({
                    type: 'POST',
                    url: '/questionset/' + qsid + '/' + field + 's',
                    data: postData,
                    dataType: 'json',
                    success: renderQuestionSet
                });
            });
        });

        $(id + ' li').each(function(i, el) {
            $(el).find('.delete').click(function() {
                $.ajax({
                    type: 'DELETE',
                    url: '/questionset/' + qsid + '/' + field + '/' + i,
                    dataType: 'json',
                    success: renderQuestionSet
                });
                return false;
            });

            $(el).find('.send').click(function() {
                $.ajax({
                    type: 'POST',
                    url: '/questionset/' + qsid + '/send-next',
                    dataType: 'json',
                    success: renderQuestionSet
                });
            });

            $(el).find('.item').editable({
                title: 'Enter new ' + field,
                type: 'text',
                pk: 1,
                url: '/questionset/' + qsid + '/' + field + '/' + i,
                ajaxOptions: { type: 'put' },
                params: function(params) {
                    var result = {};
                    result[field] = params.value;
                    return result;
                }
            });
        });
    };

    var renderQuestionSet = function(data) {
        $.ajax({
            url: '/static/questionset.template.htm',
            cache: true,
            dataType: 'html',
            success: function(template) {
                var compiledTemplate = Handlebars.compile(template);
                var html = compiledTemplate(data);

                $('.container').hide();
                $('#questionset').html(html).show();

                editableText(data.id, '#viewTitle', 'title');
                editableText(data.id, '#viewFrequency', 'frequency');

                editableList(data.id, '#viewEmails', 'email');
                editableList(data.id, '#viewQuestions', 'question');

                var $next = $($('#viewQuestions li')[data.nextQuestion]);
                $next.css('font-weight', 'bold');
                $next.find('.send').show();
            }
        });
    };


    $('#loadButton').click(function() {
        var id = $('input[name="loadID"]').val();

        $.ajax({
            type: 'GET',
            url: '/questionset/' + id,
            dataType: 'json',
            success: renderQuestionSet
        });

        return false;
    });

    $('#createButton').click(function() {
        var title = $('input[name="createTitle"]').val();
        var frequency = $('input[name="createFrequency"]').val();
        var email = $('input[name="createEmail"]').val();

        $.ajax({
            type: 'POST',
            url: '/questionset',
            data: {
                title: title,
                frequency: frequency,
                email: email
            },
            dataType: 'json',
            success: renderQuestionSet
        });

        return false;
    });
});
