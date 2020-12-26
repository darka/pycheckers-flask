import flask

from flask import request
import pycheckers
import pycheckers.svg

from flask import Flask

app = Flask(__name__)

game = pycheckers.CheckersGame.with_board(
    {
        (3, 6): pycheckers.CheckerPiece(
            pycheckers.CheckerColor.RED, pycheckers.CheckerLevel.MAN
        ),
        (2, 7): pycheckers.CheckerPiece(
            pycheckers.CheckerColor.BLACK, pycheckers.CheckerLevel.MAN
        ),
    }
)

style = """\
<style>
rect.board-square {
  fill: yellow;
  stroke: black;
  stroke-width: 3;
}
rect.board-square-selected {
  fill: #66ff33;
  stroke: #003300;
  stroke-width: 3;
}
circle.checker-red {
  fill: red;
  stroke: black;
  stroke-width: 3;
  pointer-events: none;
}
circle.checker-black {
  fill: black;
  stroke: black;
  stroke-width: 3;
  pointer-events: none;
}
</style>"""

script = """\
<script>

function selectSquare(squareId) {
  var element = document.getElementById(squareId);
  if (element.classList.contains("board-square-selected"))
    return;
  element.classList.add("board-square-selected");
}

function deselectSquare(squareId) {
  var element = document.getElementById(squareId);
  if (!element.classList.contains("board-square-selected"))
    return;
  element.classList.remove("board-square-selected");
}

function extractPos(squareId) {
  var splt = squareId.split("-");
  var x = parseInt(splt[2]);
  var y = parseInt(splt[3]);
  return [x, y];
}

class App {
  constructor() {
    this.state = {
      selectedSquares: []
    };
    this.render();
  }
  render() {
    const {selectedSquares,} = this.state;
    fetch('/game')
        .then(function (response) {
            response.text().then(function (text) {
                document.getElementById("main")
                .innerHTML = text
            });
        })
        .catch(function (err) {
            console.log("Something went wrong!", err);
        });
  }
}

var app = new App();
window.onload = () => {
  document.getElementById("move-button").addEventListener("click", function() {
    fetch("/move", {
      method: "POST", 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(app.state.selectedSquares)
    }).then(res => {
      app.state.selectedSquares = [];
      app.render();
    });
  });
}

document.addEventListener('click', function (event) {
    if (!event.target.closest('.board-square')) return;
    selectSquare(event.target.id);
    var pos = extractPos(event.target.id);
    app.state.selectedSquares.push(pos);
    console.log(event.target);
}, false);

</script>
"""

def render():
    return f"""\
<html><head>{style}{script}</head><body>
<div id="main"></div>
<button id="move-button">Move</button>
</body></html>"""

@app.route("/")
def root():
    return render()

@app.route("/game")
def render_game():
    return pycheckers.svg.render(game, 500)

@app.route("/move", methods=["POST"])
def move():
    print(request.headers)
    print(request.json)
    piece_pos = request.json[0]
    rest = request.json[1:]
    game.move(piece_pos, rest)
    return "done"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
