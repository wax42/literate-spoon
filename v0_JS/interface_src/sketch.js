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


	// TO DELETE
	// ajouter function de check de validite
	// ou autre calcule chinois pour avoir des stats
}

var puzzle = new Puzzle();
var ui = new UI();

// Variable WebSocket declaration
var ws = null;

var loadingAnimation;




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


	// test for loading
	loadingAnimation = select('.bubbles-wrapper');

	ws = new WebSocket("ws://127.0.0.1:8082");
	ws.onopen = ()=> {
		ws.send('{ "logs":"hello from client"}');
		// Just some log for the back
	}

	// listenner a mettre dans une fonction en dehors

	ws.onmessage = (e) => {
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
			result = result.algo;
			puzzle.path = result.path;
			puzzle.len_path = result.len_path;
			puzzle.size_puzzle = result.size_puzzle;
			puzzle.all_node = result.all_node;
			puzzle.node_open = result.node_open;
			puzzle.node_close = result.node_close;
			elem_all_node.html("all node:" + puzzle.all_node);
			elem_node_close.html("node open:" + puzzle.node_close);
			elem_node_open.html("node close:" + puzzle.node_open);
			elem_time_duration.html("time duration:" + puzzle.time_duration);
			// elem_time_duration.style(, 100);
		} else if ("logs" in result ) {
			console.log("Somes logs from the back", result.logs);
		} else if ("validate_puzzle" in result ) {
			//  Que faire quand le puzzle est valide
			// C'est le mauvais puzzle qui est envoyer pour l'instant ou plutot pas celui d'edit
			// euh enfet si mais c'est buguer
			if (result.validate_puzzle) {
				console.log("Puzzle valide")
				puzzle.current_puzzle = ui.tmp_validate_puzzle;
			} else {
				console.log("invalide Puzzle");
				// lauch small animation
				event_button_edit(); // Rego to edit the puzzle
			}
		}
		else {
			console.log("que des suces putes");
		}
		// TODO REMETTRE LA LIGNE EN BAS OU LA DESACTIVER POUR TESTER LE CHARGEMENT!!!
		ui.loading = false;
	}

	// initialize input for the puzzle

	// gestion current_len a revoir TODO
	ui.current_len = puzzle.size_puzzle;


	// The button is always in the same place

	// maybe with the responsive recalculate this position

	button_edit = createButton('edit');
	button_edit.mousePressed(event_button_edit);
	button_edit.size(60, 20);

	elem_title = createElement('h1', "42 N_PUZZLE");
	elem_signature = createElement("h5", "by vguerand and alhelson");
	// greeting = createElement('h2', 'what is your name?');
	// greeting.position(ui.middle_width, 5);

	initialize_mode_normal();

  
}



// TO ADD maybe in other place WHERE i don't know

function draw_edit_puzzle() {
	// console.log("draw puzzle() puzzle.turn :", puzzle.turn);
	push(); // The push() function saves the current drawing style settings and transformations

	let w = ui.full_width * 0.4 / puzzle.size_puzzle;
	let h = ui.full_height * 0.8  / puzzle.size_puzzle;

	let start_x = 0.05 * ui.full_width;
	let start_y = 0.20 *  ui.full_height

	// TODO After delete the size of the button  remplace 20 with a variable
	h = h - 20;

	// console.log(" DEBUG ", puzzle.size_puzzle, ui.current_len, puzzle.current_puzzle)

	let data;
	for (var y = 0; y < puzzle.size_puzzle; y++) {
		for (var x = 0; x < puzzle.size_puzzle; x++) {

				ui.div_titles[y][x].position(start_x + x * w, start_y + y * h);
				ui.div_titles[y][x].size(w - 10, h - 10);
				
				ui.input_puzzle[y][x].position(start_x + x * w + w * 0.25, start_y + y * h + h * 0.25);

		}
	}
	//  pop() restores these settings of push()
}



function draw_puzzle() {

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
				data = puzzle.current_puzzle[y][x];
				if (data == '0') {
					ui.div_titles[y][x].addClass("empty_title_puzzle");

				}
				ui.div_titles[y][x].position(start_x + x * w, start_y + y * h);
				ui.div_titles[y][x].size(w - 10, h - 10);
				ui.text_puzzles[y][x].position(start_x + x * w + w * 0.25, start_y + y * h + h * 0.25);
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

	height = ui.full_height * 0.5;
	width_interval = 80;

	elem_all_node.position(ui.full_width * 0.5 + width_interval * 0, height);
	elem_node_close.position(ui.full_width * 0.5 + width_interval * 1, height);
	elem_node_open.position(ui.full_width * 0.5 + width_interval * 2, height);
	elem_time_duration.position(ui.full_width * 0.5 + width_interval * 3, height);

	draw_puzzle();
	console.log("draw mode normal");
}

function draw() {
	console.log("draw");

	frameRate(2); // to regulate fps
	button_edit.position(ui.full_width * 0.05, ui.full_height * 0.05);

	elem_title.position(ui.full_width * 0.25, ui.full_height * 0.05);
	elem_signature.position(ui.full_width * 0.15, ui.full_height * 0.92);
	
	if (ui.loading) {
		console.log(" Ouii");
		image(ui.images[ui.index], ui.full_width / 2, ui.full_height / 2);
		ui.index = (ui.index + 1) % ui.images.length; 
		// clear();
		// loadingAnimation.addClass('display-none');
		// textAlign(CENTER, CENTER);
		// textSize(120);
		// textStyle(BOLD);
		// fill("#8861A4");
		// text("SUCCESS!!", width / 2, height / 2);
		// ui.loading = false;
		// faire des bails de chargements
	} else if (ui.edit) {
		draw_mode_edit();
	} else {
		draw_mode_normal();
	}
}

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
	initialize_mode_normal();
	ui.loading = true;
}