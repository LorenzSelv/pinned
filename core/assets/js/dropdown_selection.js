$(".dropdown-menu .dropdown-item").click(function() {
    var selText = $(this).text();
    var selColor = $(this).css("background-color")
    $(this).parents('.input-group').find('#dropdownMenuButton').html(selText + ' <span class="caret"></span>').css("background-color", selColor);
});