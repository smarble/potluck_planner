"use strict";

function replaceDishIdea(results) {
    // this below is an ajax call
    $("#ideas_text").html(results);
}

function showDishIdeas(evt) {
    $.get('/dish_ideas', replaceDishIdea);
}

$('#ideas_button').on('click', showDishIdeas);

