"use strict";
// Slider declaration
let rSlider, gSlider, bSlider;
let input, button, greeting;

var ws = null;


// Size declaration
var GetSize = ()=> {
	return ([Math.max(window.innerWidth || 0),
			Math.max(window.innerHeight || 0)]);
}

var full_width = GetSize()[0];
var full_height = GetSize()[1];

var middle_width = full_width / 2;

// Declaration of n_puzzle variable

var path = null;
var current_puzzle = [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]];
var turn = 0;
var len_path = 0;
var size_puzzle = 5;



//canvas resize on viewport change
function canvas_resize() {
    var win_size = GetSize();
    resizeCanvas(win_size[0], win_size[1], true);
}

//window resize on viewport change >> hook
function windowResized() {
	full_width = GetSize()[0];
	full_height = GetSize()[1];
	canvas_resize();
	redraw();
}

function setup() {
	// loop();
	noLoop();
	canvas_resize();
	ws = new WebSocket("ws://127.0.0.1:8082");
	ws.onopen = ()=> {
		ws.send("hello from client");
	}
	ws.onmessage = (e)=>{
		console.log("received:", e);
		redraw();
	}

	rSlider = createSlider(0, 255, 100);
	rSlider.position(middle_width, 20);
	gSlider = createSlider(0, 255, 0);
	gSlider.position(middle_width, 50);
	bSlider = createSlider(0, 255, 255);
	bSlider.position(middle_width, 80);
}

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
  


function draw_puzzle() {
	let w = middle_width / size_puzzle;
	let h = full_height / size_puzzle;

	// TODO After delete the size of the button 
	h = h - 20;
	
	if (path) {
		current_puzzle = path[turn]
	}
	let data;
	for (var y = 0; y < size_puzzle; y++) {
		for (var x = 0; x < size_puzzle; x++) {
				data = current_puzzle[y][x];
				rect(x * w, y * h, w, h);
				text(data, x * w + w / 2, y * h + h / 2);
		}
	}
}

function draw() {
	console.log("draw");

	input = createInput();
	input.position(middle_width, 65);

	button = createButton('submit');
	button.position(input.x + input.width, 65);
	button.mousePressed(function_test_greet);


	greeting = createElement('h2', 'what is your name?');
	greeting.position(middle_width, 5);
  

	// Test slider
	const r = rSlider.value();
	const g = gSlider.value();
	const b = bSlider.value();
	background(r, g, b);
	text('red', rSlider.x * 2 + rSlider.width, 35);
	text('green', gSlider.x * 2 + gSlider.width, 65);
	text('blue', bSlider.x * 2 + bSlider.width, 95);

	draw_puzzle();
}

// function mousePressed() {
// 	console.log("Mouse pressed", mouseX, mouseY);
// 	ws.send("mousePressed");
// 	ws.onmessage = (e)=>{
// 		path = JSON.parse(e.data);
// 		len_path = path.length;
// 		console.log('len_path', len_path);
// 		if (path) {
// 			size_puzzle = path[0].length
// 			console.log('size_puzzle', size_puzzle);
// 		}
// 		console.log('parse', path);
// 		redraw();
// 	}
// }

function mouseClicked() {
	console.log("Mouse clicked", mouseX, mouseY);
	//  Allons nous faire les bouttons ici ??
	// ça risque d'etre chiant ! Esperons qu'il y a une lib

}