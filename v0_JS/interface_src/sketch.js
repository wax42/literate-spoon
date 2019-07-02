"use strict";
// Slider declaration
let input, button, greeting;

let button_algo;


// WebSocket declaration
var ws = null;

// get size of windows
var GetSize = () => {
	return ([Math.max(window.innerWidth || 0),
			Math.max(window.innerHeight || 0)]);
}


// Interface declaration

class UI {
	constructor(name) {
		// Size declaration
		this.full_width = GetSize()[0];
		this.full_height = GetSize()[1];
		this.middle_width = this.full_width / 2;

		// color declaration
		this.color_black = ( 0, 0, 0);
		this.color_white = (255, 255, 255);

		this.edit = false;
		this.input_puzzle= [];

		// button declaration
		// button_next, button_previous, button_right, button_left, button_first, button_last




	}
}

var ui = new UI();

// Color declaration

var color_black = (0, 0, 0);
var color_white = (255, 255, 255);




// Declaration of n_puzzle variable in Obj
class Puzzle {
	constructor(name) {
		this.path = null;
		this.turn = 0;
		this.len_path = 0;
		this.current_puzzle = [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]];
		this.size_puzzle = 5;
		this.all_node;
		this.node_open;
		this.node_close;

		this.heuristique = ['manhatan', 'gaschnig', 'hamming'];
		this.index_heuristique = 0;
	}
}

var puzzle = new Puzzle();

/*
 Function of the main programm definition
	- draw()
	- setup()
	- canvas_resize()
	- windowResized()

 */

//canvas resize on viewport change
function canvas_resize() {
    var win_size = GetSize();
    resizeCanvas(win_size[0], win_size[1], true);
}

//window resize on viewport change >> hook
function windowResized() {
	ui.full_width = GetSize()[0];
	ui.full_height = GetSize()[1];
	ui.middle_width = ui.full_width / 2;
	canvas_resize();
	redraw();
}

function setup() {
	// loop();
	noLoop(); // redraw and noLoop don't work 
	canvas_resize();
	ws = new WebSocket("ws://127.0.0.1:8082");
	ws.onopen = ()=> {
		ws.send("hello from client");
	}

	// listenner
	ws.onmessage = (e)=>{
		// virer cette merde ou justement mettre a jour 
		// correctement ici en fonction de ce qu'on recoit
		// console.log("received:", e);
		// redraw();
	}



	input = createInput();
	input.position(ui.middle_width, 65);

	// initialize input for the puzzle

	initialise_input_puzzle();


	// button creation	

	let x = ui.middle_width + 150;
	let y = 250;




	button = createButton('submit');
	button.position(input.x + input.width, 65);
	button.mousePressed(function_test_greet);
	
	button_edit = createButton('edit');
	button_edit.position(ui.full_width - 200, 100);
	button_edit.mousePressed(function_button_edit);

	button_algo = createButton('algo');
	button_algo.position(ui.middle_width + 50, 100);
	button_algo.mousePressed(algo);


	greeting = createElement('h2', 'what is your name?');
	greeting.position(ui.middle_width, 5);

	initialise_button();

  
}



function draw_edit_puzzle() {
	console.log("draw puzzle() puzzle.turn :", puzzle.turn);
	push(); // The push() function saves the current drawing style settings and transformations

	let w = ui.middle_width / puzzle.size_puzzle;
	let h = ui.full_height / puzzle.size_puzzle;

	// TODO After delete the size of the button  remplace 20 with a variable
	h = h - 20;

	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {
				data = puzzle.current_puzzle[y][x];
				ui.input_puzzle[y][x].value(data);
				ui.input_puzzle[y][x].position(x * w + w / 2, y * h + h / 2);
				ui.input_puzzle[y][x].size(20, 20); // size of the input

				rect(x * w, y * h, w, h, 20);
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

	let w = ui.middle_width / puzzle.size_puzzle;
	let h = ui.full_height / puzzle.size_puzzle;

	// TODO After delete the size of the button 
	h = h - 20;
	
	if (puzzle.path) {
		puzzle.current_puzzle = puzzle.path[puzzle.turn]
	}
	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {
				data = puzzle.current_puzzle[y][x];
				// position_x, position_y, witdth, height, rounded_corners
				if (data == '0') {
					fill(ui.color_black); // black square 
				}
				else {
					fill(ui.color_white); // white square
				}
				rect(x * w, y * h, w, h, 20);
				push();
				fill(0, 0, 0);
				text(data, x * w + w / 2, y * h + h / 2);
				pop();

		}
	}
	pop();
	//  pop() restores these settings of push()

}

function draw_mode_edit() {
	draw_edit_puzzle();
	console.log("draw mode edit");
}

function draw() {
	console.log("draw");

	background(210, 190, 80);
	
	if (ui.edit) {
		draw_mode_edit();
	}
	else {
		draw_puzzle();
	}
}

function algo() {
	console.log("Mouse pressed", mouseX, mouseY);
	ws.send("mousePressed");
	ws.onmessage = (e) => {
		let result;
		result = JSON.parse(e.data);
		console.log(result);
		puzzle.path = result.path
		puzzle.len_path = result.len_path
		puzzle.size_puzzle = result.size_puzzle
		redraw();
	}
}

function mouseClicked() {
	console.log("Mouse clicked", mouseX, mouseY);
	// remove();
	// setup();
	// redraw();
	//  Allons nous faire les bouttons ici ??
	// ça risque d'etre chiant ! Esperons qu'il y a une lib

}