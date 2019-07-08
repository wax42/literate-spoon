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
			- tmp_validate_puzzle
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

		// normal mode
		this.div_titles = []; // Will contain the Div elem of the titles
		this.text_puzzles = []; // Will contain the Text elem of the titles


		// edit mode
		this.edit = false;
		this.input_puzzle = [];
		this.tmp_validate_puzzle;
		this.loading = false;
		// this.current_len = 0; // TODO 
		// Fix the current len 

		// loading mode
		this.images = [];
		this.index = 0;
		this.counter_image = 0;
		this.total_image = 40;
		this.loading_image = false;

		// animate title
		this.animed_title = false;
		this.position0yx = [0, 0];
		this.last_position0 = [0, 0];

	}
	findpos0 () {
		for (let i=0; i<puzzle.size_puzzle; i++) {
			for (let j=0; j<puzzle.size_puzzle; j++) {
					if (puzzle.current_puzzle[i][j]  == '0')
						this.position0yx = [i, j]
			}
		}
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
		this.all_node = 0;
		this.node_open = 0;
		this.node_close = 0;
		this.time_duration = 0; 

		this.heuristics = ['manhatan', 'gaschnig', 'hamming'];
		this.index_heuristics = 0;
	}

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

function loadImageElement(filename) {
	loadImage(filename, imageLoaded);
  
	function imageLoaded(image) {
	  console.log(filename);
	  ui.images.push(image);
	  ui.counter_image++;
	  if (ui.counter_image == ui.total_image) {
		ui.loading_image = true;
		ui.loading = true;
	  }
	}
  }

function preload() {
	/*
	Called directly before setup(),  the preload() function is used 
	to handle asynchronous loading of external files in a blocking way.
	*/
	for (var i = 1; i <= ui.total_image; i++) {
		loadImageElement("img/anim" + i + ".png");
	}

}


function setup() {

	// noLoop(); //  
	canvas_resize();

	// Wait for the back response
	ui.loading = true;


	// Initialize the websocket
	ws = new WebSocket("ws://127.0.0.1:8082");
	
	// TODO launch a first time a random puzzle in the back
	ws.onopen = ()=> {
		// Just sends some random logs to test the back
		// ws.send('{ "logs":"hello from client"}');
		var obj = {}
		obj.algo = {
			"heuristics": puzzle.heuristics[1],
			"puzzle": puzzle.current_puzzle, // checker le puzzle qu'on envoie la gestion est pas encore reglo
			"size_puzzle": puzzle.size_puzzle,
			"factor": puzzle.factor
		}
		ws.send(JSON.stringify(obj));
	}

	// listenner of the websocket
	ws.onmessage = (e) => {
		event_onmessage(e); 
	}

	// ??? Initialize current_len TODO check the obligation of this shit
	ui.current_len = puzzle.size_puzzle;
	ui.findpos0();



	button_edit = createButton('edit');
	button_edit.mousePressed(event_button_edit);
	button_edit.size(60, 20);

	elem_title = createElement('h1', "N-Puzzle");
	elem_signature = createElement("h5", "by vguerand and alhelson");

}

// When the back send a message 
function event_onmessage(e) {
		let result;

		console.log(e);
		if (e == undefined) {
			// TODO delete
			console.log("Suce tes morts");
			return ;
		}
		result = JSON.parse(e.data);
		// TODO gestion of which message
		console.log("Back send a new message", result);
		if ("algo" in result) {
			initialize_mode_normal();
			result = result.algo;
			puzzle.path = result.path;
			puzzle.len_path = result.len_path;
			puzzle.size_puzzle = result.size_puzzle;
			puzzle.all_node = result.all_node;
			puzzle.node_open = result.node_open;
			puzzle.node_close = result.node_close;
			elem_all_node.html("Total number of state ever selected in the 'opened' set (Complexity in time)" + puzzle.all_node);
			elem_node_close.html("Maximum numbere of states ever represented in memory at the same time during the search (Complexity in time)"  + puzzle.node_close);
			elem_number_of_move.html("Number of moves required to transition from the initial state to the final state, according to the search" + puzzle.len_path);
			elem_node_open.html("node close:" + puzzle.node_open);
			elem_time_duration.html("time duration:" + puzzle.time_duration);
			console.log(puzzle.path);

		} else if ("logs" in result ) {
			console.log("Somes logs from the back", result.logs);
		} else if ("validate_puzzle" in result ) {
			//  Que faire quand le puzzle est valide
			// C'est le mauvais puzzle qui est envoyer pour l'instant ou plutot pas celui d'edit
			// euh enfet si mais c'est buguer
			if (result.validate_puzzle) {
				console.log("Puzzle valide")
				puzzle.current_puzzle = ui.tmp_validate_puzzle;
				destroy_div_titles();
				initialize_mode_normal();
			} else {
				console.log("invalide Puzzle");
				ui.edit = true;
				initialize_mode_edit(); // Rego to edit the puzzle

				// lauch small animation
			}
		} else if ("random_puzzle" in result) {
			puzzle.current_puzzle = result['random_puzzle'];
		}
		else {
			console.log("que des suces putes");
		}
		// TODO REMETTRE LA LIGNE EN BAS OU LA DESACTIVER POUR TESTER LE CHARGEMENT!!!
		ui.loading = false;
	}



// TO ADD maybe in other place WHERE i don't know

function draw_edit_puzzle() {
	// console.log("draw puzzle() puzzle.turn :", puzzle.turn);

	let w = ui.full_width * 0.4 / puzzle.size_puzzle;
	let h = ui.full_height * 0.8  / puzzle.size_puzzle;

	let start_x = 0.05 * ui.full_width;
	let start_y = 0.20 *  ui.full_height

	// TODO After delete the size of the button  remplace 20 with a variable
	h = h - 20;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {

				ui.div_titles[y][x].position(start_x + x * w, start_y + y * h);
				ui.div_titles[y][x].size(w - 10, h - 10);
				
				ui.input_puzzle[y][x].position(start_x + x * w + w * 0.25, start_y + y * h + h * 0.25);

		}
	}
}



function draw_puzzle() {

	let w = ui.full_width * 0.4 / puzzle.size_puzzle;
	let h = ui.full_height * 0.7  / puzzle.size_puzzle;
	if (w < h) {
			h = w;
	} else {
		w = h;
	}

	let start_x = 0.05 * ui.full_width;
	let start_y = 0.20 *  ui.full_height
	
	if (puzzle.path) {
		puzzle.current_puzzle = puzzle.path[puzzle.turn]
	}

	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {
				data = puzzle.current_puzzle[y][x];
				if (data == '0') {
					ui.div_titles[y][x].addClass("empty_title_puzzle");

				}
				ui.div_titles[y][x].position(start_x + x * w, start_y + y * h);
				ui.div_titles[y][x].size(w - 15, h - 15);
				ui.text_puzzles[y][x].position(start_x + x * w + w * 0.33, start_y + y * h + h * 0.33);
				// Warning if the puzzle size move segmentation fault
				ui.text_puzzles[y][x].html(puzzle.current_puzzle[y][x]);

		}
	}
}

function draw_mode_edit() {
	draw_edit_puzzle();
	
	let height = ui.full_height * 0.5;
	elem_size.position(ui.full_width * 0.5, height); 
	slider_size.position(ui.full_width * 0.5, height  + 50);

  elem_factor.position(ui.full_width * 0.5, height + 100);
	slider_factor.position(ui.full_width * 0.5, height + 150);
}

function draw_mode_normal( ) {
	// position of the buttons
	let height = ui.full_height * 0.15;
	let width_interval = 65;

	button_algo.position(ui.full_width * 0.15 + width_interval * 0, height); // TODO mettre  au autre endroit
	button_next.position(ui.full_width * 0.15 + width_interval * 1, height);
	button_previous.position(ui.full_width * 0.15 + width_interval * 2, height);
	button_first.position(ui.full_width * 0.15 + width_interval * 3, height);
	button_last.position(ui.full_width * 0.15 + width_interval * 4, height);

	puzzle.heuristics.forEach((value, i) => {
		buttons_heuristics[i].position(ui.full_width * 0.75, ui.full_height * 0.15  + ( i * 50));
	});


	height = ui.full_height * 0.50;
	let interval = 80;

			
	elem_all_node.position(ui.full_width * 0.50 , height + interval * 0);
	elem_node_close.position(ui.full_width * 0.50 , height + interval * 1);
	elem_node_open.position(ui.full_width * 0.50 , height + interval * 2);
	elem_time_duration.position(ui.full_width * 0.50 , height + interval * 3);
	elem_number_of_move.position(ui.full_width * 0.50 , height + interval * 4);
	


	draw_puzzle();
}

function draw() {
	/*
		Function draw is called in loop.
	*/

	frameRate(20); // to regulate fps
	clear();

	// Recalculate position for responsive app

	button_edit.position(ui.full_width * 0.05, ui.full_height * 0.05);
	elem_title.position(ui.full_width * 0.25, ui.full_height * 0.05);
	elem_signature.position(ui.full_width * 0.15, ui.full_height * 0.92);

	if (ui.loading) {
		// Loading Mode 
		console.log(" Ouii");
		image(ui.images[ui.index], ui.full_width / 2, ui.full_height / 2);
		ui.index = (ui.index + 1) % ui.images.length; 
	} else if (ui.edit) {
		// Edit Mode 
		draw_mode_edit();
	} else {
		// Normal mode
		draw_mode_normal();
	}
}

// Just a function to test the communication with the back for the moment
function algo() {
	// puzzle.check_correct_puzzle();
	console.log("Mouse pressed", mouseX, mouseY);
	destroy_mode_normal();
	destroy_div_titles();
	var obj = {}
	obj.algo = {
		"heuristics": puzzle.heuristics[1],
		"puzzle": puzzle.current_puzzle, // checker le puzzle qu'on envoie la gestion est pas encore reglo
		"size_puzzle": puzzle.size_puzzle,
		"factor": puzzle.factor
	}
	ws.send(JSON.stringify(obj));
	ui.loading = true;
}