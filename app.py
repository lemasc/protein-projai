from flask import Flask, render_template
import food

app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/result")
def result_page():
    sites = food.random_food()
    return render_template("result.html", sites=sites)

@app.route("/data")
def data_page():
    food.get_df()
    return "Data cached at " + str(food.fetch_at)

@app.route("/purge")
def purge_page():
    food.get_df(use_cached=False)
    return "Updated at " + str(food.fetch_at)