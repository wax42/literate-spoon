"use strict";
// Slider declaration
let rSlider, gSlider, bSlider;


var ws = null;

// Size declaration
var GetSize = ()=> {
	return ([Math.max(window.innerWidth || 0),
			Math.max(window.innerHeight || 0)]);
}


let full_width = GetSize()[0];
let full_height = GetSize()[1];

let middle_width = full_width / 2;



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

function draw() {
	console.log("draw");

	// square(0, 0, 200);
	// text('1', 20, 20);
	// ellipse(GetSize()[0]/2, GetSize()[1]/2, GetSize()[0], GetSize()[1]);

	const r = rSlider.value();
	const g = gSlider.value();
	const b = bSlider.value();
	background(r, g, b);
	text('red', rSlider.x * 2 + rSlider.width, 35);
	text('green', gSlider.x * 2 + gSlider.width, 65);
	text('blue', bSlider.x * 2 + bSlider.width, 95);


	
	let h_case = 5;
	let w_case = 5;
	let w = middle_width / w_case;
	let h = full_height / h_case;
	// let w = 50;
	// let h = 50;
	var tableau = [[1, 2, 3, 4, 5], [16, 17, 18, 19, 6], [15, 24, 0, 20, 7], [14, 23, 22, 21, 8], [13, 12, 11, 10, 9]];
	let data;

	for (var y = 0; y < h_case; y++) {
		for (var x = 0; x < w_case; x++) {
				data = tableau[y][x];
				rect(x * w, y * h, w, h);
				text(data, x * w + w / 2, y * h + h / 2);
		}
	}
}

function mousePressed() {
	console.log("Mouse pressed", mouseX, mouseY);
	ws.send("mousePressed");
	ws.onmessage = (e)=>{
		console.log("received:", e);
		redraw();
	}
}

function mouseClicked() {
	console.log("Mouse clicked", mouseX, mouseY);
}