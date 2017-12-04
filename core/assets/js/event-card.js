// Blur other cards when hovering over one and remove blurring after leaving it
$(".event-card").mouseover(function() {
    $(".event-card").not(this).each(function() {
        $(this).addClass("card-blurred")
    })
}).mouseout(function() {
    $(".event-card").not(this).each(function() {
        $(this).removeClass("card-blurred")
    })
})