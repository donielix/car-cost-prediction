#!/usr/bin/env python3

from flask import Flask, render_template, request

import mlflow

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model = mlflow.sklearn.load_model(model_uri="model")
        # Get values through input bars
        distance = float(request.form.get("distance"))
        fuel_price = float(request.form.get("fuel_price"))
        output = model.predict_endpoint(
            distance=distance, fuel_price=fuel_price, mileage=0
        )
    else:
        output = ""

    return render_template("index.html", output=output)


def main():
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
