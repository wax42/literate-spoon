

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
    // redraw();
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
    // redraw();

function event_heuristics(value) {
    puzzle.heuristics = value;
}




function event_random() {
    let obj = {};
    obj.random_puzzle = puzzle.random_size;
    ws.send(JSON.stringify(obj));
    console.log("oui")
}

function event_resolve() {
	var obj = {}
	obj.algo = {
		"heuristics": puzzle.heuristics,
		"puzzle": puzzle.current_puzzle, // checker le puzzle qu'on envoie la gestion est pas encore reglo
		"size_puzzle": puzzle.size_puzzle,
		"factor": puzzle.factor
	}
	ws.send(JSON.stringify(obj));
	// ui.loading = true;
}


function event_factor(value) {
    puzzle.factor =  value;
    let factor_elem = document.getElementById("factor");
    factor_elem.innerHTML = "Factor: " + value;
    
}

function event_size(value) {
    //  TODO modify the size in variable
    puzzle.random_size = value;
    let size_elem = document.getElementById("size");
    size_elem.innerHTML = "N: " + value;
}

function event_button_first() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn = 0;
    // redraw();
    animate_title();

}


function event_button_last() {
    if (puzzle.len_path <= 0)
        return ;
    puzzle.turn = puzzle.len_path - 1;
    animate_title();
    
    // redraw();

}


function destroy_div_titles(len = puzzle.size_puzzle) {

    for (let i=0; i<len; i++) {
        for (let j=0; j<len; j++) {
            div_titles[i][j].remove();
        }
        row[i].remove();
    }
}




function initialize_div_titles(len = puzzle.size_puzzle) {
    div_titles = [];
    row = [];

    for (let i=0; i<len; i++) {
        div_titles[i] = [];
        let new_row = document.createElement("tr");
        new_row.setAttribute("id", "tr"+ i);
        // new_row.classList.add("row_puzzle");
        row.push(new_row);

        document.getElementById("puzzle").appendChild(new_row);
        for (let j=0; j<len; j++) {

            div_titles[i][j] = document.createElement("th");
            div_titles[i][j].classList.add("title_puzzle");
            div_titles[i][j].setAttribute("id", "th"+ i);
                // div_titles[i][j].classList.add("col_puzzle");
            if (puzzle.current_puzzle[i][j] != 0) {
         
                text = document.createTextNode(puzzle.current_puzzle[i][j]);
                div_titles[i][j].appendChild(text);
            }
            document.getElementById("tr" + i).appendChild(div_titles[i][j])
        }
    }
}


function initialize_html() {
    document.getElementById("time_duration").innerHTML = puzzle.time_duration
    document.getElementById("all_node").innerHTML = puzzle.all_node 
    document.getElementById("node_close").innerHTML = puzzle.node_close
    document.getElementById("len_path").innerHTML = puzzle.len_path
}


var ws = null;

var text_puzzles, div_titles, row;



// Initialize the websocket
ws = new WebSocket("ws://127.0.0.1:8082");
puzzle = new Puzzle();

ws.onopen = ()=> {
    var obj = {}
    obj.algo = {
        "heuristics": puzzle.heuristics,
        "puzzle": puzzle.current_puzzle, // checker le puzzle qu'on envoie la gestion est pas encore reglo
        "size_puzzle": puzzle.size_puzzle,
        "factor": puzzle.factor
    }
    ws.send(JSON.stringify(obj));
}

ws.onmessage = (e) => {
    let result;
    // Parse the result in object
    result = JSON.parse(e.data);
    console.log("On message", result)
    if ("algo" in result) {
        result = result.algo;
        puzzle.path = result.path;
        puzzle.len_path = result.len_path;
        puzzle.size_puzzle = result.size_puzzle;
        puzzle.all_node = result.all_node;
        puzzle.node_open = result.node_open;
        puzzle.node_close = result.node_close;
        puzzle.time_duration = result.time_duration;
        initialize_html();
        console.log(puzzle.path);
    } else if ("logs" in result ) {

        // TODO put all of the errors here and put it on modal
        console.log("Somes logs from the back", result.logs);
    }  
    else if ("random_puzzle" in result) {
        puzzle.initialize_puzzle();
        destroy_div_titles();
        puzzle.current_puzzle = result['random_puzzle']['puzzle'];
        puzzle.size_puzzle = result['random_puzzle']['size_puzzle'];
        initialize_div_titles();
    // TODO GEERE MIEUX sa
    }
    else {
        console.log("que des suces putes");
    }
    // TODO REMETTRE LA LIGNE EN BAS OU LA DESACTIVER POUR TESTER LE CHARGEMENT!!!
}



/*
Start of the programm :)

*/



initialize_div_titles();