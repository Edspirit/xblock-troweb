function TrowebEditBlock(runtime, element) {
    $(element).find('.save-button').bind('click', function() {
      var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
      var data = {
        href: $(element).find('input[name=href]').val(),
        maxwidth: $(element).find('input[name=maxwidth]').val(),
        maxheight: $(element).find('input[name=maxheight]').val()
      };
      runtime.notify('save', {state: 'start'});
      $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
        runtime.notify('save', {state: 'end'});
      });
    });

    $(element).find('.cancel-button').bind('click', function() {
      runtime.notify('cancel', {});
    });
    function saveItem(form_data) {
        runtime.notify('save', {state: 'start'});
        // Bind the FormData object and the form element
        $.ajax({
            url: 'http://127.0.0.1:5000',
            type: 'POST',
            data: form_data,
            success: function(result) {
                runtime.notify('save', {state: 'end'});
            },
            error: function(result){
                runtime.notify('save', {state: 'fail'});
            }
        });
    };
    // Get the form element
    $("form").submit(function(event) {
        event.preventDefault();
        form_data = $(this).serialize()
        saveItem(form_data);
        });
    $("a#delete-trowebitem").click(function(){
        pk = $(this).attr('pk')
        endpoint = "http://127.0.0.1:5000" + "/" + pk + "/"
        runtime.notify('save', {state: 'start'});
        $.ajax({
            url: endpoint,
            type: 'DELETE',
            success: function(result) {
                $("tr" + "#" + pk).hide() //hide the row
                runtime.notify('save', {state: 'end'});
            },
            error: function(result){
                runtime.notify('save', {state: 'fail'});
            }
        });
    });
}
