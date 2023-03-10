$(function(){
	$('.menu-ac').click(function(){
		$(this).next('.ac').slideToggle(500);
	});
	$('.fa-search').click(function(){
	       	 $(".search").animate({
                width: "toggle"
            });
	});
});