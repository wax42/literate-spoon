"use strict";

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

		// size to generate random puzzle
		this.random_size = 3;
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
		this.current_puzzle = [[4, 5, 1], [0, 3, 8], [6, 2, 7]];
		this.size_puzzle = 3;
		this.all_node = 0;
		this.node_open = 0;
		this.node_close = 0;
		this.time_duration = 0; 

		this.heuristics = ['manhatan', 'gaschnig', 'hamming'];
		this.index_heuristics = 0;
	}
	initialize_puzzle() {
		puzzle.path = null;
		puzzle.turn = 0;
		puzzle.current_puzzle = [[4, 5, 1], [0, 3, 8], [6, 2, 7]];
		puzzle.size_puzzle = 3;
		puzzle.all_node = 0;
		puzzle.node_open = 0;
		puzzle.node_close = 0;
		puzzle.time_duration = 0; 
	}
}

var puzzle = new Puzzle();
var ui = new UI();

// Variable WebSocket declaration
var ws = null;


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


	button_random = createButton('random');
	button_random.mousePressed(event_button_random);
	button_random.size(60, 20);


	elem_title = createElement('h1', "N-Puzzle");
	elem_signature = createElement("h5", "by vguerand and alhelson");

}

// When the back send a message 
function event_onmessage(e) {
		let result;

		// Parse the result in obj
		result = JSON.parse(e.data);
		if ("algo" in result) {
			initialize_mode_normal(); // TODO fix this
			result = result.algo;
			puzzle.path = result.path;
			puzzle.len_path = result.len_path;
			puzzle.size_puzzle = result.size_puzzle;
			puzzle.all_node = result.all_node;
			puzzle.node_open = result.node_open;
			puzzle.node_close = result.node_close;
			destroy_mode_normal();
			initialize_mode_normal();
			console.log(puzzle.path);
		} else if ("logs" in result ) {

			// TODO put all of the errors here
			console.log("Somes logs from the back", result.logs);
		}  
		else if ("random_puzzle" in result) {
			destroy_div_titles();
			destroy_text_puzzle();
			puzzle.initialize_puzzle();
			puzzle.current_puzzle = result['random_puzzle']['puzzle'];
			puzzle.size_puzzle = result['random_puzzle']['size_puzzle'];
			initialize_div_titles();
			initialize_text_puzzle();
		// TODO GEERE MIEUX sa
		}
		else {
			console.log("que des suces putes");
		}
		// TODO REMETTRE LA LIGNE EN BAS OU LA DESACTIVER POUR TESTER LE CHARGEMENT!!!
		ui.loading = false;
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
	else if (puzzle.path == -1) {
		// TODO fix this shit
		console.log("Algo fail")
		return ;
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


function draw_mode_normal( ) {
	// position of the buttons
	let height = ui.full_height * 0.15;
	let width_interval = 65;

	button_algo.position(ui.full_width * 0.5, height); // TODO mettre  au autre endroit


  elem_factor.position(ui.full_width * 0.5, height + 100);
	slider_factor.position(ui.full_width * 0.5, height + 150);

	elem_size.position(ui.full_width * 0.2, height - 100);
	slider_size.position(ui.full_width * 0.2, height - 150);

	button_next.position(ui.full_width * 0.10 + width_interval * 0, height);
	button_previous.position(ui.full_width * 0.10 + width_interval * 1, height);
	button_first.position(ui.full_width * 0.10 + width_interval * 2, height);
	button_last.position(ui.full_width * 0.10 + width_interval * 3, height);

	puzzle.heuristics.forEach((value, i) => {
		buttons_heuristics[i].position(ui.full_width * 0.75, ui.full_height * 0.15  + ( i * 50));
	});


	elem_stats.position(ui.full_width * 0.10 , ui.full_height * 0.50);

	draw_puzzle();
}

function draw() {
	/*
		Function draw is called in loop.
	*/

	frameRate(20); // to regulate fps
	clear();

	// Recalculate position for responsive app

	button_random.position(ui.full_width * 0.05 + 70, ui.full_height * 0.05);

	elem_title.position(ui.full_width * 0.5, ui.full_height * 0.05);
	elem_signature.position(ui.full_width * 0.15, ui.full_height * 0.92);

	if (ui.loading) {
		// Loading Mode 
		console.log(" Ouii");
		image(ui.images[ui.index], ui.full_width / 2, ui.full_height / 2);
		ui.index = (ui.index + 1) % ui.images.length; 
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