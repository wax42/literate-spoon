"use strict";
var button_next, button_previous, button_first, button_last, button_edit

// Declare 4 button [ next, previous, first, last]
// var button_navigate_puzzle = new Array(4).fill;
// JSP ENCORE 


// Declare 3 button [ mahanttan, gaschnig, hamming ]
var button_heuristique = new Array(3).fill;

function function_button_edit() {
    if (ui.edit) {
        ui.edit = !ui.edit;
        destroy_mode_edit();

        initialise_button();
    }
    else {
        ui.edit = !ui.edit;
        initialise_mode_edit();
        button_next.remove();
        button_previous.remove();
        button_first.remove();
        button_last.remove();
    }
    redraw();
}


function initialise_input_puzzle() {
    // Initialize input puzzle
    for(let i=0; i<puzzle.size_puzzle; i++) {
		ui.input_puzzle[i] = [];
		for(let j=0; j<puzzle.size_puzzle; j++) {
			ui.input_puzzle[i][j] = createInput();
		}
	}
}


function initialise_mode_edit() {
    // Initialize heuristique button

    let x = ui.middle_width + 250;
    let y = 50
    console.log(" Initialisation mode edit");
    puzzle.heuristique.forEach((value, i) => {
		button_heuristique[i] = createButton(value);
		button_heuristique[i].position(x, y + ( i * 50));
		button_heuristique[i].mousePressed( () => {
			console.log(value);
		});
    });
    
    initialise_input_puzzle();
}

function destroy_mode_edit() {
    // destroy button heuristique
    for (let i=0; i<3; i++) {
        button_heuristique[i].remove();
    }
    for (var y = 0; y < puzzle.size_puzzle; y++) {
        for (var x = 0; x < puzzle.size_puzzle; x++) {
            ui.input_puzzle[y][x].remove();
        }
    }
}


function initialise_button() {
    // Initialize button next previous first last

    /// TODO foutre sa dans un putain d'array
    // PCK c'est moche
    console.log(" go to init button");
    button_next = createButton('next');
    button_next.position(ui.middle_width + 50, 250);
    button_next.mousePressed(function_button_next);

    button_previous = createButton('previous');
    button_previous.position(ui.middle_width + 50, 300);
    button_previous.mousePressed(function_button_previous);

    button_first = createButton('first');
    button_first.position(ui.middle_width + 50, 350);
    button_first.mousePressed(function_button_first);

    button_last = createButton('last');
    button_last.position(input.x + input.width, 400);
    button_last.mousePressed(function_button_last); 
}



function function_button_next() {
    puzzle.turn = (puzzle.turn + 1);
    if (puzzle.turn >= puzzle.len_path) {
        puzzle.turn = puzzle.len_path - 1;
    }
    redraw();
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


// TO DELETE 
// Ici est stocke toute la merde qui va etre supprime


function function_test_greet() {
	const name = input.value();
	greeting.html('hello ' + name + '!');
	input.value('');
  
	for (let i = 0; i < 200; i++) {
	  push();
	  fill(random(255), 255, 255);
	  translate(random(width), random(height));
	  rotate(random(2 * PI));
	  text(name, 0, 0);
	  pop();
	}
}
  