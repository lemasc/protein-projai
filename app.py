from typing import TypedDict
from flask import Flask, render_template, request, jsonify
import food

app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/calculate")
def calculate_page():
    return render_template("calculate.html")


class CalculateForm(TypedDict):
    activity: str
    age: str
    allergy: str
    disease: str
    name: str
    weight: str


@app.route("/result", methods=["POST"])
def result_page():
    data: CalculateForm = request.form
    min_protein, max_protein = food.calculate_protein(
        float(data["weight"]),
        int(data["age"]),
        data["activity"],
        data["disease"]
    )
    protein = (min_protein + max_protein) / 2
    menu = food.random_food_in_range(min_protein, max_protein, data["allergy"])
    print(menu)
    return render_template("result.html", protein=f"{protein:.2f}", menu=menu, form=data)


@app.route("/data")
def data_page():
    food.get_df()
    return "Data cached at " + str(food.fetch_at)


@app.route("/purge")
def purge_page():
    food.get_df(use_cached=False)
    return "Updated at " + str(food.fetch_at)
