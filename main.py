import flask

import pycheckers
import pycheckers.svg

from flask import Flask

app = Flask(__name__)

game = pycheckers.CheckersGame.with_board(
    {
        (1, 0): pycheckers.CheckerPiece(
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
class App {
  constructor() {
    this.state = {
      x: null,
      y: null
    };
    this.render();
  }
  render() {
    const {x, y} = this.state;
    fetch('/game')
        .then(function (response) {
            response.text().then(function (text) {
                document
                .body
                .innerHTML = text
            });
        })
        .catch(function (err) {
            console.log("Something went wrong!", err);
        });
  }
}

window.onload = () => new App();

document.addEventListener('click', function (event) {
    if (!event.target.closest('.board-square')) return;
    console.log(event.target);
}, false);
</script>
"""

def render():
    output = f"<html><head>{style}{script}</head><body>\n"
    return output + "</body></html>"

@app.route("/")
def root():
    return render()

@app.route("/game")
def render_game():
    return pycheckers.svg.render(game, 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
