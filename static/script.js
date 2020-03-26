"use strict";

function replaceDishIdea(results) {
    $("#ideas_text").html(results);
}

function showDishIdeas(evt) {
    $.get('/dish_ideas', replaceDishIdea);
}

$('#ideas_button').on('click', showDishIdeas);

