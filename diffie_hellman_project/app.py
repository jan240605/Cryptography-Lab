import math
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "diffie_hellman_secret_key"

# --- MATHEMATICAL UTILITIES ---

def is_prime(n):
    """Checks if n is a prime number."""
    if n < 2: return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_prime_factors(n):
    """Returns unique prime factors of n."""
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors

def is_primitive_root(alpha, q):
    """Verifies if alpha is a primitive root modulo q."""
    if not is_prime(q): return False
    phi = q - 1
    factors = get_prime_factors(phi)
    for p in factors:
        # Check if alpha^((q-1)/p) mod q == 1
        if pow(alpha, phi // p, q) == 1:
            return False
    return True

def mod_exp_steps(base, exp, mod):
    """Calculates modular exponentiation and records each algorithm step."""
    result = 1
    steps = []
    steps.append(f"Problem: {base}^{exp} mod {mod}")
    
    curr_base = base
    curr_exp = exp
    
    while curr_exp > 0:
        steps.append(f"Result={result}, Base={curr_base}, Exp={curr_exp}")
        if curr_exp % 2 == 1:
            prev_res = result
            result = (result * curr_base) % mod
            steps.append(f" -> Exp is odd: ({prev_res} * {curr_base}) mod {mod} = {result}")
        
        curr_base = (curr_base * curr_base) % mod
        steps.append(f" -> Square Base: ({curr_base})")
        
        curr_exp = curr_exp // 2
        steps.append(f" -> Half Exp: {curr_exp}")
        steps.append("-" * 15)

    steps.append(f"Final Result = {result}")
    return result, steps

# --- FLASK ROUTES ---

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dh", methods=["POST"])
def dh():
    try:
        q = int(request.form["q"])
        alpha = int(request.form["alpha"])
        xA = int(request.form["xA"])
        xB = int(request.form["xB"])

        # 1. Validation Checks
        if not is_prime(q):
            flash(f"Error: {q} is not a prime number.")
            return redirect(url_for('home'))
        
        if not is_primitive_root(alpha, q):
            flash(f"Error: {alpha} is not a primitive root of {q}.")
            return redirect(url_for('home'))

        # 2. Key Exchange Calculations
        YA, stepsYA = mod_exp_steps(alpha, xA, q)
        YB, stepsYB = mod_exp_steps(alpha, xB, q)
        KA, stepsKA = mod_exp_steps(YB, xA, q)
        KB, stepsKB = mod_exp_steps(YA, xB, q)

        return render_template(
            "dh.html", q=q, alpha=alpha, xA=xA, xB=xB,
            YA=YA, YB=YB, KA=KA, KB=KB,
            stepsYA=stepsYA, stepsYB=stepsYB,
            stepsKA=stepsKA, stepsKB=stepsKB
        )
    except ValueError:
        flash("Please enter valid whole numbers.")
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)


