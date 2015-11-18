/**
 * Created by stanley on 10/14/14.
 */
$(document).ready(function() {

    var cache = {};
    $("#query").autocomplete({
        minLength: 1,
        source: function(request, response) {
            var term = request.term;
            if (term.trim() == '')
                return;
            if (term in cache) {
                response(cache[term]);
                return;
            }
            $.getJSON("/autocomplete", function(data) {
                cache[term] = data;
                response(data);
            });
        }
    });

});