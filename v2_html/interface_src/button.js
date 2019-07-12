"use strict";



// Declare 4 button [ next, previous, first, last]

// TODO maybe in array ?
var button_next, button_previous, button_first, button_last, button_random

// TO DELETE or NOT
var button_algo;

// Declare Stats
var elem_stats
// Declare elem to put the number all_node, node_open, node_close, time_duration
var elem_all_node, elem_node_open, elem_node_close, elem_time_duration, elem_number_of_move;

// Declare elem title and signature
var elem_title, elem_signature;

// Declare 3 button [ mahanttan, gaschnig, hamming ]
var buttons_heuristics = new Array(3).fill;

// Declare array[2] [0] = Slider   [1] = Element
var slider_factor;
var elem_factor;

var slider_size;
var elem_size;


function initialize_mode_normal() {
    // Initialize button next previous first last

    slider_factor = createSlider(0, 100, 0, 1);
    elem_factor = createElement('h2',"factor:" + 0);
 
    slider_factor.style('width', '80px');
    slider_factor.mouseReleased( () => {
        puzzle.factor = slider_factor.value();
        elem_factor.html("factor:" + puzzle.factor);
    });

    initialize_slider_size();
    initialize_div_titles();
    initialize_text_puzzle();
    initialize_button_heuristique();

    elem_stats = createElement('h4', "Total number of state ever selected in the 'opened' set (Complexity in time): " + puzzle.all_node
        + "</br>Maximum numbere of states ever represented in memory at the same time during the search (Complexity in time): "  + puzzle.node_close 
        + "</br>Number of moves required to transition from the initial state to the final state, according to the search: " + puzzle.len_path 
        + "</br>Time duration:" +  puzzle.time_duration)


    // button creation	

    button_algo = createButton('algo');
	button_algo.mousePressed(algo);
    button_algo.size(60, 20);

    button_next = createButton('next');
    button_next.mousePressed(event_button_next);
    button_next.size(60, 20);


    button_previous = createButton('previous');
    button_previous.mousePressed(event_button_previous);
    button_previous.size(60, 20);

    button_first = createButton('first');
    button_first.mousePressed(event_button_first);
    button_first.size(60, 20);

    button_last = createButton('last');
    button_last.mousePressed(event_button_last); 
    button_last.size(60, 20);


}

function initialize_div_titles(len = puzzle.size_puzzle) {
    ui.div_titles = [];
    for (let i=0; i<len; i++) {
        ui.div_titles[i] = [];
        for (let j=0; j<len; j++) {
            ui.div_titles[i][j] = createDiv();
            ui.div_titles[i][j].addClass("title_puzzle");
        }
    }
}

function initialize_text_puzzle() {
    ui.text_puzzles = [];
    for (let i=0; i<puzzle.size_puzzle; i++) {
        ui.text_puzzles[i] = [];
        for (let j=0; j<puzzle.size_puzzle; j++) {
            ui.text_puzzles[i][j] = createElement('h6', puzzle.current_puzzle[i][j]);
        }
    }
}





function initialize_button_heuristique() {        
    
    puzzle.heuristics.forEach((value, i) => {

        // button creation
		buttons_heuristics[i] = createButton(value);
        buttons_heuristics[i].size(60, 20);
        if (puzzle.index_heuristics == i)
            buttons_heuristics[i].addClass('active_button'); 

        // event button heuristics
		buttons_heuristics[i].mousePressed( () => {
            // save index of heuristics in puzzle obj
            puzzle.index_heuristics = i;
            // disable the button of the selected heuristics
            buttons_heuristics[i].addClass('active_button'); 
            puzzle.heuristics.forEach((value, e) => {
                if (i != e) {
                    buttons_heuristics[e].removeClass('active_button'); // activate the button for the other button
                }
			    console.log(value);
            });
        });
    });
}

function initialize_input_puzzle() {
    // Initialize input puzzle
    let n = 0;
    ui.input_puzzle = [];
    for(let i=0; i<puzzle.size_puzzle; i++) {
		ui.input_puzzle[i] = [];
		for(let j=0; j<puzzle.size_puzzle; j++) {
            ui.input_puzzle[i][j] = createInput();
            ui.input_puzzle[i][j].attribute("type", "number");
            // ui.input_puzzle[i][j].attribute("pattern", "[0-9]");
            // ui.input_puzzle[i][j].attribute("title", "Put a fucking number");
            ui.input_puzzle[i][j].attribute("min", 0);
            ui.input_puzzle[i][j].attribute("max", 99);
            ui.input_puzzle[i][j].addClass("input_puzzle")
            ui.input_puzzle[i][j].value(n);
            n++;

		}
	}
}


function fill_input_puzzle() {
    // FIll the input_puzzle with the current_puzzle
    for(let i=0; i<puzzle.size_puzzle; i++) {
		for(let j=0; j<puzzle.size_puzzle; j++) {
            ui.input_puzzle[i][j].value(puzzle.current_puzzle[i][j]);
        }
    }
}




function initialize_slider_size() {
    // createSlider(min, max, [value], [step])
    // create elem for write the value of the slider
    
    // Manager of the size slider
    slider_size = createSlider(3, 10, puzzle.size_puzzle, 1);
    elem_size = createElement('h2', "size:" + puzzle.size_puzzle);

    // initialize slider slide    
    slider_size.style('width', '80px');
    slider_size.mouseReleased( () => {
        ui.random_size = slider_size.value();
        elem_size.html("size: " + ui.random_size);
    });
}

function destroy_mode_normal() {
    // destroy button next previous first last
    destroy_text_puzzle();
    destroy_button_heuristique();
    slider_factor.remove();
    elem_factor.remove();

    slider_size.remove();
    elem_size.remove();

    elem_stats.remove();
    
    button_next.remove();
    button_previous.remove();
    button_first.remove();
    button_last.remove();
    button_algo.remove();
}

function destroy_button_heuristique() {
    for (let i=0; i<3; i++) {
        buttons_heuristics[i].remove();
    }
}


function destroy_div_titles(len = puzzle.size_puzzle) {
    for (let i=0; i<len; i++) {
        for (let j=0; j<len; j++) {
            ui.div_titles[i][j].remove();
        }
    }
}

function destroy_text_puzzle() {
    for (let i=0; i<puzzle.size_puzzle; i++) {
        for (let j=0; j<puzzle.size_puzzle; j++) {
            ui.text_puzzles[i][j].remove();
        }
    }
}


function animate_title() {
    ui.last_position0 = ui.position0yx
    ui.findpos0();
    ui.div_titles[ui.position0yx[0]][ui.position0yx[1]].removeClass('empty_title_puzzle')
}


function event_button_next() {
    puzzle.turn = (puzzle.turn + 1);
    if (puzzle.turn >= puzzle.len_path) {
        puzzle.turn = puzzle.len_path - 1;
    }
    animate_title();
    // redraw();
}


function event_button_previous() {
    puzzle.turn -= 1;
    if (puzzle.turn < 0)
    {
		puzzle.turn = 0;
    }
    animate_title();

    // redraw();
}


function event_button_first() {
    puzzle.turn = 0;
    // redraw();
    animate_title();

}


function event_button_last() {
    puzzle.turn = puzzle.len_path - 1;
    animate_title();
    
    // redraw();

}


function event_button_random() {
    let obj = {};
    obj.random_puzzle = ui.random_size;
    ws.send(JSON.stringify(obj));
}
  