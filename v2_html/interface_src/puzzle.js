

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



function initialize_div_titles(len = 3) {
    div_titles = [];
    let n = 1;

    for (let i=0; i<len; i++) {
        div_titles[i] = [];
        let new_row = document.createElement("div");
        new_row.setAttribute("id", "row"+ i);
        new_row.classList.add("row");

        row.push(new_row);
        document.getElementById("puzzle").appendChild(new_row);
        for (let j=0; j<len; j++) {
            div_titles[i][j] = document.createElement("div");
            div_titles[i][j].classList.add("title_puzzle");
            div_titles[i][j].classList.add("col");
            text = document.createTextNode('1');
            div_titles[i][j].appendChild(text);

            document.getElementById("row" + i).appendChild(div_titles[i][j])
        }
    }
}

function initialize_text_puzzle(len = 3) {
    text_puzzles = [];
    for (let i=0; i<len; i++) {
        text_puzzles[i] = [];
        for (let j=0; j<len; j++) {
            text_puzzles[i][j] = createElement("button");
            text_puzzles[i][j].classList.add("btn btn-default puzzle_button");
            text_puzzles[i][j].innerHTML= "1"
            document.getElementById("puzzle").appendChild(puzzle.text_puzzles[i][j])
        }
    }
}

var ws = null;

var text_puzzles, div_titles;



// Initialize the websocket
ws = new WebSocket("ws://127.0.0.1:8082");
puzzle = new Puzzle();

ws.onopen = ()=> {
    var obj = {}
    obj.algo = {
        "heuristics": puzzle.heuristics[1],
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
    if ("algo" in result) {
        result = result.algo;
        puzzle.path = result.path;
        puzzle.len_path = result.len_path;
        puzzle.size_puzzle = result.size_puzzle;
        puzzle.all_node = result.all_node;
        puzzle.node_open = result.node_open;
        puzzle.node_close = result.node_close;
        console.log(puzzle.path);
    } else if ("logs" in result ) {

        // TODO put all of the errors here and put it on modal
        console.log("Somes logs from the back", result.logs);
    }  
    else if ("random_puzzle" in result) {
        puzzle.initialize_puzzle();
        puzzle.current_puzzle = result['random_puzzle']['puzzle'];
        puzzle.size_puzzle = result['random_puzzle']['size_puzzle'];
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

row = []


initialize_div_titles();