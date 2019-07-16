class Puzzle {
	constructor(name) {
		this.path = null;
		this.factor = 1;
		this.turn = 0;
		this.len_path = 0;
		this.current_puzzle = [[4, 5, 1], [0, 3, 8], [6, 2, 7]];
		this.size_puzzle = 3;
		this.all_node = 0;
		this.node_open = 0;
		this.node_close = 0;
		this.time_duration = 0; 
        
        this.random_size = 3;
		this.heuristics = 'manhattan';
	}
	initialize_puzzle() {
        puzzle.path = null;
		puzzle.len_path = 0;
		puzzle.turn = 0;
		puzzle.all_node = 0;
		puzzle.node_open = 0;
		puzzle.node_close = 0;
		puzzle.time_duration = 0; 
	}
}


function animate_title() {
    puzzle.current_puzzle = puzzle.path[puzzle.turn];
    destroy_div_titles();
    initialize_div_titles();

}

function event_button_next() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn = (puzzle.turn + 1);
    if (puzzle.turn >= puzzle.len_path) {
        puzzle.turn = puzzle.len_path - 1;
    }
    animate_title();
}


function event_button_previous() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn -= 1;
    if (puzzle.turn < 0)
    {
		puzzle.turn = 0;
    }
    animate_title();
}

function event_heuristics(value) {
    puzzle.heuristics = value;
}




function event_random() {
    let obj = {};
    obj.random_puzzle = puzzle.random_size;
    ws.send(JSON.stringify(obj));
}

function event_resolve() {
    console.log(elem_load)
    if (elem_load != undefined)
        return ;
    destroy_div_titles();
    initialize_loading();
	var obj = {}
	obj.algo = {
		"heuristics": puzzle.heuristics,
		"puzzle": puzzle.current_puzzle, // checker le puzzle qu'on envoie la gestion est pas encore reglo
		"size_puzzle": puzzle.size_puzzle,
		"factor": puzzle.factor
    }
    console.log(JSON.stringify(obj));
	ws.send(JSON.stringify(obj));
}


function event_factor(value) {
    puzzle.factor = value; 
}

function event_size(value) {
    puzzle.random_size = value;
    let size_elem = document.getElementById("size");
    size_elem.innerHTML = value;
}

function event_button_first() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn = 0;
    animate_title();

}


function event_button_last() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn = puzzle.len_path - 1;
    animate_title();
}


function destroy_div_titles(len = puzzle.size_puzzle) {

    for (let i=0; i<len; i++) {
        for (let j=0; j<len; j++) {
            div_titles[i][j].remove();
        }
        row[i].remove();
    }
}


function initialize_timeout() {
    document.getElementById("msg").innerHTML = "Time out";
    elem_timeout = document.createElement('i');
    elem_timeout.classList.add('fa');
    elem_timeout.classList.add('fa-clock-o');
    elem_timeout.classList.add('fa-5x');
    elem_timeout.classList.add('fa-pulse');

    document.getElementById('loading').appendChild(elem_timeout);
}

function destroy_timeout() {
    elem_timeout.remove();
    elem_timeout = undefined;
}


function initialize_loading() {
    if (elem_timeout != undefined) {
        destroy_timeout();
    }

    elem_load = document.createElement('i');
    elem_load.classList.add('fa');
    elem_load.classList.add('fa-spinner');
    elem_load.classList.add('fa-5x');
    elem_load.classList.add('fa-pulse');

    document.getElementById('loading').appendChild(elem_load);
    document.getElementById("msg").innerHTML = "loading ...";
}

function destroy_loading() {
    elem_load.remove();
    elem_load = undefined;
}


function initialize_div_titles(len = puzzle.size_puzzle) {
    document.getElementById("msg").innerHTML = "";

    div_titles = [];
    row = [];

    for (let i=0; i<len; i++) {
        div_titles[i] = [];
        let new_row = document.createElement("tr");
        new_row.setAttribute("id", "tr"+ i);
        row.push(new_row);

        document.getElementById("puzzle").appendChild(new_row);
        for (let j=0; j<len; j++) {

            div_titles[i][j] = document.createElement("th");
            div_titles[i][j].classList.add("title_puzzle");
            div_titles[i][j].setAttribute("id", "th"+ i);
            if (puzzle.current_puzzle[i][j] != 0) {
         
                text = document.createTextNode(puzzle.current_puzzle[i][j]);
                div_titles[i][j].appendChild(text);
            }
            else {
                div_titles[i][j].classList.add("empty_title_puzzle");
            }
            document.getElementById("tr" + i).appendChild(div_titles[i][j])
        }
    }
}


function initialize_html() {
    document.getElementById("time_duration").innerHTML = parseFloat(puzzle.time_duration).toFixed(3);
    document.getElementById("all_node").innerHTML = puzzle.all_node;
    document.getElementById("node_open").innerHTML = puzzle.node_open;
    document.getElementById("len_path").innerHTML = puzzle.len_path;
    // document.getElementById("path").innerHTML = JSON.stringify(puzzle.path, null, 2);
}


var ws = null;

var text_puzzles, div_titles, row, elem_load, elem_timeout;

// Initialize the websocket
ws = new WebSocket("ws://127.0.0.1:8082");
puzzle = new Puzzle();

ws.onopen = ()=> {
    var obj = {}
    obj.algo = {
        "heuristics": puzzle.heuristics,
        "puzzle": puzzle.current_puzzle,
        "size_puzzle": puzzle.size_puzzle,
        "factor": puzzle.factor
    }
    ws.send(JSON.stringify(obj));
}

ws.onmessage = (e) => {
    let result;
    // Parse the result in object
    result = JSON.parse(e.data);
    if ("algo" in result) {
        result = result.algo;
        destroy_loading();
        if (result.path == -1) {
            console.log("TimeOut")
            initialize_timeout();
            puzzle.initialize_puzzle();
        } else {
            puzzle.path = result.path;
            puzzle.len_path = result.len_path;
            puzzle.size_puzzle = result.size_puzzle;
            puzzle.all_node = result.all_node;
            puzzle.node_open = result.node_open;
            puzzle.node_close = result.node_close;
            puzzle.time_duration = result.time_duration;
            initialize_div_titles();
            initialize_html();
        }
        console.log(puzzle.path);
    } else if ("logs" in result ) {
        console.log("Somes logs from the back", result.logs);
    }  
    else if ("random_puzzle" in result) {
        if (elem_timeout != undefined) {
            destroy_timeout();
        }
        puzzle.initialize_puzzle();
        destroy_div_titles();
        puzzle.current_puzzle = result['random_puzzle']['puzzle'];
        puzzle.size_puzzle = result['random_puzzle']['size_puzzle'];
        initialize_div_titles();
    }
    else {
        console.log("Error websocket invalid", result);
    }
}



/*
Start of the programm :)
*/
initialize_loading();