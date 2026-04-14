from flask import Flask, render_template, request
from euler import calculate_phi
from fermat import fermat_factor
from primitive import find_primitive_roots

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/euler", methods=["GET", "POST"])
def euler():
    result = None
    steps = None
    error = None
    if request.method == "POST":
        try:
            n = int(request.form["number"])
            if n <= 0:
                error = "Please enter a positive integer."
            else:
                result, steps = calculate_phi(n)
        except:
            error = "Invalid input."
    return render_template("euler.html", result=result, steps=steps, error=error)


@app.route("/fermat", methods=["GET", "POST"])
def fermat():
    result = None
    steps = None
    error = None
    if request.method == "POST":
        try:
            n = int(request.form["number"])
            if n <= 0:
                error = "Please enter a positive integer."
            else:
                result, steps = fermat_factor(n)
        except:
            error = "Invalid input."
    return render_template("fermat.html", result=result, steps=steps, error=error)


@app.route("/primitive", methods=["GET", "POST"])
def primitive():
    roots = None
    steps = None
    error = None
    if request.method == "POST":
        try:
            n = int(request.form["number"])
            if n <= 1:
                error = "Please enter a number greater than 1."
            else:
                roots, steps = find_primitive_roots(n)
        except:
            error = "Invalid input."
    return render_template("primitive.html", roots=roots, steps=steps, error=error)


if __name__ == "__main__":
    app.run(debug=True)
