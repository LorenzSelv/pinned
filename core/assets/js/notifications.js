// Listen for clicks on the notification dropdown
$('.notifications.dropdown').find(".dropdown-item").on("click", function() {
    if (!$(this).siblings().length) {
        $(this).parent().append("<center>No notifications</center>")
    }
})