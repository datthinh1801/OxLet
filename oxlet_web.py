from flask import Flask, render_template, request
import helper


app = Flask(__name__, static_folder="templates/images")


@app.route("/", methods=["GET", "POST"])
def index():
    """GET and POST methods of the home page."""
    if request.method != "POST":
        return render_template("index.html")

    new_words = request.form["new-words"]
    words = new_words.splitlines()
    words = helper.preprocess_words(words)

    # handle potential errors
    try:
        result = helper.run(words)
        return render_template("index.html", new_words=new_words, result=result)
    except:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
