from flask import Flask, render_template, request

import utils

app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    """GET and POST methods of the home page."""
    if request.method != "POST":
        return render_template("index.html")

    new_words = request.form["new-words"]
    words = new_words.splitlines()
    words = utils.preprocess_words(words)

    # handle potential errors
    try:
        result = utils.run(words)
        return render_template("index.html", new_words=new_words, result=result)
    except:
        return render_template("index.html")


if __name__ == "__main__":
    # fix Windows-specific exception:
    # RuntimeError: Event loop is closed.
    app.run(debug=True)
