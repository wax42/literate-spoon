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
		this.current_len = 0; // TODO 
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
	check_correct_puzzle() {
		let tmp_puzzle = []
		for(let i=0; i<puzzle.size_puzzle; i++) {
			tmp_puzzle[i] = [];
			for(let j=0; j<puzzle.size_puzzle; j++) {
				tmp_puzzle[i][j] = ui.input_puzzle[i][j].value();
			}
		}
		// Create JSON string with 1 in start
		var obj = '{ "1" : { "puzzle":'
		+ JSON.stringify(tmp_puzzle)
		+ '}}'
		
		console.log(obj);
		ws.send(obj)
		// Check  
	}

	// TO DELETE
	// ajouter function de check de validite
	// ou autre calcule chinois pour avoir des stats
}

var puzzle = new Puzzle();
var ui = new UI();

// Variable WebSocket declaration
var ws = null;


// TO DELETE Slider declaration
let input, button, greeting;
var button_algo;



/*
 Function of the main programm definition
	- draw()
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
	redraw();
}

function setup() {
	// loop();
	noLoop(); // redraw and noLoop don't work 
	canvas_resize();
	ws = new WebSocket("ws://127.0.0.1:8082");
	ws.onopen = ()=> {
		ws.send('{ "3":"hello from client"}');
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

	initialize_input_puzzle();


	// button creation	

	let x = ui.middle_width + 150;
	let y = 250;




	button = createButton('submit');
	button.position(input.x + input.width, 65);
	button.mousePressed(function_test_greet);
	
	button_edit = createButton('edit');
	button_edit.position(ui.full_width - 200, 100);
	button_edit.mousePressed(event_button_edit);

	button_algo = createButton('algo');
	button_algo.position(ui.middle_width + 50, 100);
	button_algo.mousePressed(algo);


	greeting = createElement('h2', 'what is your name?');
	greeting.position(ui.middle_width, 5);

	initialize_mode_normal();

  
}



// TO ADD maybe in other place WHERE i don't know

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
				ui.input_puzzle[y][x].size(30, 20); // size of the input

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
	// puzzle.check_correct_puzzle();
	console.log("Mouse pressed", mouseX, mouseY);
	ws.send('{ "0": { "heuristics": "", "puzzle": "", "size_puzzle": "", "factor": "", }}');
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