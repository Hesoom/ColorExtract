from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    color_data = {
        "#481830": 0.301746,
        "#783030": 0.212460,
        "#306078": 0.166667,
        "#486090": 0.084683,
        "#183060": 0.082381,
        "#d86048": 0.053175,
        "#a84830": 0.037222,
        "#300018": 0.026349,
        "#781818": 0.017857,
        "#f0d860": 0.007857
    }

    return render_template("index.html",colors=color_data)

if __name__ == "__main__":
    app.run(debug=True)