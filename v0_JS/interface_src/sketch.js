"use strict";

/*
 class for the interface
	UI: 
		Variable
			// Size 

			- full_width
			- full_height
			- middle_with
			
			# Color
			- color_black
			- color_white
			// Mode edit
			
			- edit 
			- input_puzzle
			- factor
			- loading

		Function

			- GetSize()
		
	
	Puzzle:
		Variable
			// 
			- path
			- turn
			- len_path
			- current_puzzle
			- size_puzzle
			- all_nodes
			- node_open
			- node_close
		
		Function
			pass


 */

// Interface declaration
class UI {
	constructor(name) {
		// Size declaration
		this.full_width = this.GetSize()[0];
		this.full_height = this.GetSize()[1];
		this.middle_width = this.full_width / 2;

		// color declaration
		this.color_black = ( 0, 0, 0);
		this.color_white = (255, 255, 255);

		// edit mode
		this.edit = false;
		this.input_puzzle = [];
		this.loading = false;
		// this.current_len = 0; // TODO 
		// Fix the current len 
	}
	// get size of windows
	GetSize(){
		return ([Math.max(window.innerWidth || 0),
				Math.max(window.innerHeight || 0)]);
	}


}

// Puzzle declaration
class Puzzle {
	constructor(name) {
		this.path = null;
		this.factor = 0;
		this.turn = 0;
		this.len_path = 0;
		this.current_puzzle = [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]];
		this.size_puzzle = 5;
		this.all_node;
		this.node_open;
		this.node_close;

		this.heuristics = ['manhatan', 'gaschnig', 'hamming'];
		this.index_heuristics = 0;
	}


	// TO DELETE
	// ajouter function de check de validite
	// ou autre calcule chinois pour avoir des stats
}

var puzzle = new Puzzle();
var ui = new UI();

// Variable WebSocket declaration
var ws = null;






/*
 Function of the main programm definition
	- draw()
	- preload()
	- setup()
	- canvas_resize()
	- windowResized()


Function to moves in another places
	- draw_puzzle
	- draw_edit_puzzle
	- draw_mode_edit


Function to delete
	- algo

 */

//canvas resize on viewport change
function canvas_resize() {
    var win_size = ui.GetSize();
    resizeCanvas(win_size[0], win_size[1], true);
}

//window resize on viewport change >> hook
function windowResized() {
	ui.full_width = ui.GetSize()[0];
	ui.full_height = ui.GetSize()[1];
	ui.middle_width = ui.full_width / 2;
	canvas_resize();
	// redraw();
}

function preload() {
	/*
	Called directly before setup(),  the preload() function is used 
	to handle asynchronous loading of external files in a blocking way.
	*/

	// TODO the first launch 

}

function setup() {
	// noLoop(); //  
	canvas_resize();
	ws = new WebSocket("ws://127.0.0.1:8082");
	ws.onopen = ()=> {
		ws.send('{ "logs":"hello from client"}');
		// Just some log for the back
	}

	// listenner
	ws.onmessage = (e) => {

		var back_response = JSON.stringify(e);
		console.log(back_response);


		// virer cette merde ou justement mettre a jour 
		// correctement ici en fonction de ce qu'on recoit
		// console.log("received:", e);
		// redraw();
	}

	// initialize input for the puzzle

	// gestion current_len a revoir TODO
	ui.current_len = puzzle.size_puzzle;


	// The button is always in the same place

	// maybe with the responsive recalculate this position

	button_edit = createButton('edit');
	button_edit.mousePressed(event_button_edit);

	// greeting = createElement('h2', 'what is your name?');
	// greeting.position(ui.middle_width, 5);

	initialize_mode_normal();

  
}



// TO ADD maybe in other place WHERE i don't know

function draw_edit_puzzle() {
	console.log("draw puzzle() puzzle.turn :", puzzle.turn);
	push(); // The push() function saves the current drawing style settings and transformations

	let w = ui.full_width * 0.4 / puzzle.size_puzzle;
	let h = ui.full_height * 0.8  / puzzle.size_puzzle;

	let start_x = 0.05 * ui.full_width;
	let start_y = 0.20 *  ui.full_height

	// TODO After delete the size of the button  remplace 20 with a variable
	h = h - 20;

	console.log(" DEBUG ", puzzle.size_puzzle, ui.current_len, puzzle.current_puzzle)

	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {
				// if (x >= puzzle.current_puzzle.length || y >= puzzle.current_puzzle.length) {
				// 	data = '';
				// }
				// else {
				// 	data = puzzle.current_puzzle[y][x];
				// }
				// // data = '';
				// ui.input_puzzle[y][x].value(data);
				ui.input_puzzle[y][x].position(start_x + x * w + w / 2, start_y + y * h + h / 2);
				ui.input_puzzle[y][x].size(30, 20); // size of the input

				rect(start_x + x * w, start_y + y * h, w, h, 20);
				push();
				fill(0, 0, 0);
				pop();

		}
	}
	//  pop() restores these settings of push()
}



function draw_puzzle() {
	console.log("draw puzzle() puzzle.turn :", puzzle.turn);
	push(); // The push() function saves the current drawing style settings and transformations

	let w = ui.full_width * 0.4 / puzzle.size_puzzle;
	let h = ui.full_height * 0.8  / puzzle.size_puzzle;

	let start_x = 0.05 * ui.full_width;
	let start_y = 0.20 *  ui.full_height
	// TODO After delete the size of the button 
	h = h - 20;
	
	if (puzzle.path) {
		puzzle.current_puzzle = puzzle.path[puzzle.turn]
	}

	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {
				if (x >= puzzle.current_puzzle.length || y >= puzzle.current_puzzle.length) {
					data = '';
				}
				else {
					data = puzzle.current_puzzle[y][x];
				}
				// if (puzzle.size_puzzle < puzzle.current_len)
				// data = puzzle.current_puzzle[y][x];
				// position_x, position_y, witdth, height, rounded_corners
				if (data == '0') {
					fill(ui.color_black); // black square 
				}
				else {
					fill(ui.color_white); // white square
				}
				rect(start_x + x * w, start_y + y * h, w, h, 20);
				push();
				fill(0, 0, 0);
				text(data, start_x + x * w + w / 2, start_y + y * h + h / 2);
				pop();

		}
	}
	pop();
	//  pop() restores these settings of push()

}

function draw_mode_edit() {
	draw_edit_puzzle();

	let height = ui.full_height * 0.5;
	elem_size.position(ui.full_width * 0.5, height); 
	slider_size.position(ui.full_width * 0.5, height  + 50);

    elem_factor.position(ui.full_width * 0.5, height + 100);
	slider_factor.position(ui.full_width * 0.5, height + 150);


	console.log("draw mode edit");
}

function draw_mode_normal( ) {
	// position of the buttons
	let height = ui.full_height * 0.25;
	let width_interval = 65;
	
    button_algo.position(ui.full_width * 0.5 + width_interval * 0, height);
    button_next.position(ui.full_width * 0.5 + width_interval * 1, height);
	button_previous.position(ui.full_width * 0.5 + width_interval * 2, height);
	button_first.position(ui.full_width * 0.5 + width_interval * 3, height);
    button_last.position(ui.full_width * 0.5 + width_interval * 4, height);

	draw_puzzle();
	console.log("draw mode normal");
}

function draw() {
	console.log("draw");

	background(210, 190, 80);
	frameRate(2); // to regulate fps
	button_edit.position(ui.full_width * 0.05, ui.full_height * 0.05);

	
	// if (ui.loading) {
	// 	// faire des bails de chargements
	// } else if (ui.edit)
	if (ui.edit) {
		draw_mode_edit();
	}
	else {
		draw_mode_normal();
	}
}

function algo() {
	// puzzle.check_correct_puzzle();
	console.log("Mouse pressed", mouseX, mouseY);
	ws.send('{ "algo": { "heuristics": "", "puzzle": "", "size_puzzle": "", "factor": "", }}');
	ws.onmessage = (e) => {
		let result;
		result = JSON.parse(e.data);
		console.log(result);
		puzzle.path = result.path
		puzzle.len_path = result.len_path
		puzzle.size_puzzle = result.size_puzzle
		// redraw();
	}
}