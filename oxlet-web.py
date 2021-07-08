from flask import Flask, render_template, request

from oxlet import preprocess_words, crawl_resource


app = Flask(__name__, static_folder="templates/images")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != "POST":
        return render_template("index.html")

    words = request.form["new-words"]
    words = words.splitlines()
    result = "".join(list(map(crawl_resource, words)))
    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
