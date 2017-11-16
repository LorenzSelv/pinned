$(".event-card").mouseover(function() {
    $(".event-card").not(this).each(function() {
        $(this).addClass("card-blurred")
    })
}).mouseout(function() {
    $(".event-card").not(this).each(function() {
        $(this).removeClass("card-blurred")
    })
})