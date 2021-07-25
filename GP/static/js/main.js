$('.carousel').carousel({
    interval:3000 
});

$(function(){
    'use strict';
    // Adjust slider height
    var winH = $(window).height(),
        navH = $('.navbar').innerHeight(),
        conH = 150;
    
    $('.testmonials, .item').height((winH - navH) - conH);
    });
$("#img1").click(function() {
    $("#modal1").toggle();
    })
$("#img2").click(function() {
    $("#modal2").show();
    })
$("#img3").click(function() {
    $("#modal3").show();
    })  
$("#img4").click(function() {
    $("#modal4").show();
    })