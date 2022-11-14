import scraper
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, world!</p>", 201

@app.route("/parse", methods=["POST"])
def parse():
    url = request.form["url"]
    dyn = bool(request.form["dyn"])
    return scraper.parse_website(url, dyn)

if __name__ == "__main__":
    app.run(debug=True)