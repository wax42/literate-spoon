"use strict";
var button_next, button_previous, button_first, button_last, button_edit

function function_button_edit() {
    ui.edit = !ui.edit;
}


function function_button_next() {
    // console.log("debut puzzle.turn :", puzzle.turn, puzzle.len_path);
    puzzle.turn = (puzzle.turn + 1);
    if (puzzle.turn >= puzzle.len_path) {
        // console.log(" Function next END");
        puzzle.turn = puzzle.len_path - 1;
    }
    redraw();
    // console.log("NEXT puzzle.turn :", puzzle.turn);
}


function function_button_previous() {
    puzzle.turn -= 1;
    if (puzzle.turn < 0)
    {
		puzzle.turn = 0;
    }
    redraw();
}


function function_button_first() {
    puzzle.turn = 0;
    redraw();
}


function function_button_last() {
	puzzle.turn = puzzle.len_path - 1;
    redraw();
}

