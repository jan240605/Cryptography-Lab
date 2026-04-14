from flask import Flask, render_template, request
from vigenere import vigenere_encrypt, vigenere_decrypt
from affine import affine_encrypt, affine_decrypt
from playfair import playfair_encrypt, playfair_decrypt, generate_matrix

app = Flask(__name__)

@app.route("/vigenere", methods=["GET", "POST"])
def vigenere():
    output, steps = "", []
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"]
        action = request.form["action"]
        if action == "encrypt":
            output, steps = vigenere_encrypt(text, key)
        else:
            output, steps = vigenere_decrypt(text, key)
    return render_template("vigenere.html", output=output, steps=steps)


@app.route("/affine", methods=["GET", "POST"])
def affine():
    output, steps = "", []
    if request.method == "POST":
        text = request.form["text"]
        a = int(request.form["a"])
        b = int(request.form["b"])
        action = request.form["action"]
        if action == "encrypt":
            output, steps = affine_encrypt(text, a, b)
        else:
            output, steps = affine_decrypt(text, a, b)
    return render_template("affine.html", output=output, steps=steps)


@app.route("/playfair", methods=["GET", "POST"])
def playfair():
    output, steps, matrix = "", [], None
    if request.method == "POST":
        text = request.form["text"]
        key = request.form["key"]
        action = request.form["action"]
        matrix = generate_matrix(key)
        if action == "encrypt":
            output, steps = playfair_encrypt(text, key)
        else:
            output, steps = playfair_decrypt(text, key)
    return render_template("playfair.html", output=output, steps=steps, matrix=matrix)


@app.route("/")
def home():
    return """
    <h2>CRT Cipher Tools</h2>
    <ul>
        <li><a href='/vigenere'>Vigenère Cipher</a></li>
        <li><a href='/affine'>Affine Cipher</a></li>
        <li><a href='/playfair'>Playfair Cipher</a></li>
    </ul>
    """
    
if __name__ == "__main__":
    app.run(debug=True)
