$(function() {
    $('.sidebar a').removeClass('active');
    $('.sidebar a').each(function(){
        if ($(this).attr('href') === window.location.pathname){
            $(this).addClass('active');
        }
    });
});