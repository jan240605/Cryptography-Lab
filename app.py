from flask import Flask, render_template, request
import random
import math

app = Flask(__name__)

# =====================================================
# FAST MODULAR EXPONENTIATION (Notebook Format)
# =====================================================
def fast_mod_exp(base, exp, mod):
    steps = []
    result = 1
    base = base % mod
    binary = bin(exp)[2:]

    steps.append(f"Binary of exponent {exp} = {binary}")
    steps.append("Using Square and Multiply Method")
    steps.append("")

    for bit in binary:
        result = (result * result) % mod
        steps.append(f"Square → result = result² mod {mod} = {result}")

        if bit == '1':
            result = (result * base) % mod
            steps.append(f"Multiply → result = result × {base} mod {mod} = {result}")

        steps.append("----")

    steps.append(f"Final Result = {result}")
    steps.append("")
    return result, steps


# =====================================================
# MILLER RABIN (Notebook Style)
# =====================================================
def miller_rabin(n, k=5):
    steps = []

    if n < 2:
        return False, ["Number < 2 → Not Prime"]

    if n in [2, 3]:
        return True, ["Small Prime"]

    if n % 2 == 0:
        return False, ["Even Number → Not Prime"]

    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    steps.append("Primality Testing")
    steps.append(f"{n}-1 = 2^{r} × {d}")
    steps.append("")

    for i in range(k):
        a = random.randint(2, n - 2)
        steps.append(f"Round {i+1}: Choose a = {a}")
        steps.append("")

        x, substeps = fast_mod_exp(a, d, n)
        steps.extend(substeps)

        if x == 1 or x == n - 1:
            steps.append("Probably Prime in this round")
            steps.append("")
            continue

        for _ in range(r - 1):
            x = (x * x) % n
            steps.append(f"Square x → {x}")

        steps.append("")

    steps.append("Probably Prime after all rounds")
    steps.append("")
    return True, steps


# =====================================================
# EXTENDED EUCLIDEAN
# =====================================================
def extended_gcd(a, b):
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    steps.append("Extended Euclidean Steps")
    steps.append("r | s | t")
    steps.append("----------------")

    while r != 0:
        q = old_r // r
        steps.append(f"q = {q}")
        steps.append(f"{r} | {s} | {t}")
        steps.append("----")

        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    steps.append(f"GCD = {old_r}")
    return old_r, old_s, steps


def mod_inverse(e, phi):
    gcd, x, steps = extended_gcd(e, phi)
    if gcd != 1:
        return None, steps

    d = x % phi
    steps.append(f"Modular Inverse d = {d}")
    return d, steps


# =====================================================
# CRT DECRYPTION
# =====================================================
def crt_decrypt(c, p, q, d):
    steps = []

    dp = d % (p - 1)
    dq = d % (q - 1)

    steps.append("Decryption Steps")
    steps.append(f"dp = d mod (p-1) = {dp}")
    steps.append(f"dq = d mod (q-1) = {dq}")
    steps.append("")

    steps.append("Compute m1:")
    m1, s1 = fast_mod_exp(c, dp, p)
    steps.extend(s1)

    steps.append("Compute m2:")
    m2, s2 = fast_mod_exp(c, dq, q)
    steps.extend(s2)

    q_inv = pow(q, -1, p)
    steps.append(f"q inverse mod p = {q_inv}")

    h = (q_inv * (m1 - m2)) % p
    steps.append(f"h = {h}")

    m = m2 + h * q
    steps.append(f"Final m = {m}")
    steps.append("")

    return m, steps


# =====================================================
# ROUTES
# =====================================================
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/rsa", methods=["GET", "POST"])
def rsa():

    if request.method == "POST":
        try:
            p = int(request.form["p"])
            q = int(request.form["q"])
            e = int(request.form["e"])
            message = request.form["message"]

            p_prime, p_steps = miller_rabin(p)
            q_prime, q_steps = miller_rabin(q)

            if not p_prime or not q_prime:
                return render_template("rsa.html",
                                       error="p or q not prime",
                                       p_steps=p_steps,
                                       q_steps=q_steps)

            n = p * q
            phi = (p - 1) * (q - 1)

            if math.gcd(e, phi) != 1:
                return render_template("rsa.html",
                                       error="e not coprime with φ(n)")

            d, eea_steps = mod_inverse(e, phi)

            cipher = []
            enc_steps = ["Encryption Steps"]

            for char in message:
                m = ord(char)
                enc_steps.append(f"ASCII('{char}') = {m}")
                c, s = fast_mod_exp(m, e, n)
                cipher.append(c)
                enc_steps.extend(s)

            decrypted = ""
            dec_steps = []

            for c in cipher:
                m, s = crt_decrypt(c, p, q, d)
                decrypted += chr(m)
                dec_steps.extend(s)

            return render_template("rsa.html",
                                   p=p, q=q,
                                   n=n, phi=phi,
                                   e=e, d=d,
                                   cipher=cipher,
                                   decrypted=decrypted,
                                   p_steps=p_steps,
                                   q_steps=q_steps,
                                   eea_steps=eea_steps,
                                   enc_steps=enc_steps,
                                   dec_steps=dec_steps)

        except Exception as ex:
            return render_template("rsa.html", error=str(ex))

    return render_template("rsa.html")


if __name__ == "__main__":
    app.run(debug=True)