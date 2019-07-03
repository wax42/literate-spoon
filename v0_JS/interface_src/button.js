"use strict";
// var button_navigate_puzzle = new Array(4).fill;
// JSP ENCORE 

/*

Button, Slider and Input Management

Declaration Variable
    - buttons_heuristics  // array
    - button_next
    - button_previous
    - button_first
    - button_last
    - button_edit


Function Initialization
    -  initialize_mode_normal
    -  initialize_mode_edit
    -  initialize_input_puzzle
   

Function Destruction
    - destroy_mode_edit
    - destroy_mode_normal

Function Event
    - event_button_edit
    - event_button_next
    - event_button_previous
    - event_button_first
    - event_button_last



Function of Bullshit to RENAME or WORK 

    - event_button_edit


Function to delete

    - function_test_greet


*/


// Declare 4 button [ next, previous, first, last]

// TODO maybe in array ?
var button_next, button_previous, button_first, button_last, button_edit



// Declare 3 button [ mahanttan, gaschnig, hamming ]
var buttons_heuristics = new Array(3).fill;

// Declare array[2] [0] = Slider   [1] = Element
var slider_factor;
var elem_factor;

var slider_size;
var elem_size;


function initialize_mode_normal() {
    // Initialize button next previous first last

    button_next = createButton('next');
    button_next.position(ui.middle_width + 50, 250);
    button_next.mousePressed(event_button_next);

    button_previous = createButton('previous');
    button_previous.position(ui.middle_width + 50, 300);
    button_previous.mousePressed(event_button_previous);

    button_first = createButton('first');
    button_first.position(ui.middle_width + 50, 350);
    button_first.mousePressed(event_button_first);

    button_last = createButton('last');
    button_last.position(input.x + input.width, 400);
    button_last.mousePressed(event_button_last); 
}


function initialize_mode_edit() {
    // Initialize heuristics button

    let x = ui.middle_width + 250;
    let y = 50
    
    puzzle.heuristics.forEach((value, i) => {

        // button creation
		buttons_heuristics[i] = createButton(value);
        buttons_heuristics[i].position(x, y + ( i * 50));

        // if the heuristics is already selected
        if (puzzle.index_heuristics == i) {
            buttons_heuristics[i].attribute('disabled', ''); 
        }

        // event button heuristics
		buttons_heuristics[i].mousePressed( () => {
            // save index of heuristics in puzzle obj
            puzzle.index_heuristics = i;
            // disable the button of the selected heuristics
            buttons_heuristics[i].attribute('disabled', ''); 
            puzzle.heuristics.forEach((value, e) => {
                if (i != e) {
                    buttons_heuristics[e].removeAttribute('disabled'); // activate the button for the other button
                }
			    console.log(value);
            });
        });
    });
    
    initialize_input_puzzle();
    initialize_slider_elem();
}

function initialize_input_puzzle() {
    // Initialize input puzzle
    for(let i=0; i<puzzle.size_puzzle; i++) {
		ui.input_puzzle[i] = [];
		for(let j=0; j<puzzle.size_puzzle; j++) {
            ui.input_puzzle[i][j] = createInput();
            ui.input_puzzle[i][j].attribute("type", "number");
            // ui.input_puzzle[i][j].attribute("pattern", "[0-9]");
            // ui.input_puzzle[i][j].attribute("title", "Put a fucking number");
            ui.input_puzzle[i][j].attribute("min", 0);
            ui.input_puzzle[i][j].attribute("max", 99);
            ui.input_puzzle[i][j].addClass("quantity")


		}
	}
}

function initialize_slider_elem() {
    // createSlider(min, max, [value], [step])
    // create elem for write the value of the slider
    slider_factor = createSlider(0, 100, 0, 1);
    elem_factor = createElement('h2', 0);

    slider_factor.position(ui.middle_width + 300, 500);  // TODO make responsive
    elem_factor.position(ui.middle_width + 280, 500);  // TODO make responsive

    slider_factor.style('width', '80px');
    slider_factor.mouseReleased( () => {
        puzzle.factor = slider_factor.value();
        elem_factor.html(puzzle.factor);
    });

    

    slider_size = createSlider(2, 10, puzzle.size_puzzle, 1);
    elem_size = createElement('h2', puzzle.size_puzzle);


    slider_size.position(ui.middle_width + 300, 550); // TODO make responsive
    elem_size.position(ui.middle_width + 280, 550);  // TODO make responsive
    
    slider_size.style('width', '80px');
    slider_size.mouseReleased( () => {
        puzzle.size_puzzle = slider_size.value();
        elem_size.html(puzzle.size_puzzle);
        redraw(); // Create somes bugs 
        // TODO fix the draw --> initialization input / responsive --> and come here 
    });



}

function destroy_mode_edit() {
    // destroy button heuristics
    for (let i=0; i<3; i++) {
        buttons_heuristics[i].remove();
    }
    for (var y = 0; y < puzzle.size_puzzle; y++) {
        for (var x = 0; x < puzzle.size_puzzle; x++) {
            ui.input_puzzle[y][x].remove();
        }
    }
    slider_factor.remove();
    elem_factor.remove();

    slider_size.remove();
    elem_size.remove();
}

function destroy_mode_normal() {
    // destroy button next previous first last
    button_next.remove();
    button_previous.remove();
    button_first.remove();
    button_last.remove();
}

function event_button_edit() {
    // Management of mode

    // if the mode edit is going to close
    if (ui.edit) {
        ui.edit = !ui.edit;
        destroy_mode_edit();

        initialize_mode_normal();
    }
    // if the mode edit is selected
    else { 
        ui.edit = !ui.edit;
        initialize_mode_edit();
        destroy_mode_normal();

    }
    redraw();
}


function event_button_next() {
    puzzle.turn = (puzzle.turn + 1);
    if (puzzle.turn >= puzzle.len_path) {
        puzzle.turn = puzzle.len_path - 1;
    }
    redraw();
}


function event_button_previous() {
    puzzle.turn -= 1;
    if (puzzle.turn < 0)
    {
		puzzle.turn = 0;
    }
    redraw();
}


function event_button_first() {
    puzzle.turn = 0;
    redraw();
}


function event_button_last() {
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
  