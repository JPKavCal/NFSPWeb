var $root = $('html, body');

$(document).on('shown.bs.collapse', function(event){
    console.log()
    $root.animate({
        scrollTop: $("#" + event.currentTarget.activeElement.id.substring(0,3)).offset().top - 55
    }, 500);
});