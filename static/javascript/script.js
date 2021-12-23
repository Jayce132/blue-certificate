$(function () {
    var availableTags = countries;
    $("#country_name_input").autocomplete({
        position: {
            my: "left+0 top+10",
        },
        source: function (request, response) {
            var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(request.term), "i");
            response($.grep(availableTags, function (item) {
                return matcher.test(item);
            })); //.slice(0, 20)
        }
    });
});

