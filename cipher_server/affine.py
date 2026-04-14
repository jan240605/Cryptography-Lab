def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


def affine_encrypt(text, a, b):
    text = text.lower().replace(" ", "")
    result = ""
    steps = []

    for ch in text:
        if ch.isalpha():
            p = ord(ch) - 97
            c = (a * p + b) % 26
            result += chr(c + 97)
            steps.append(f"({a}*{p} + {b}) mod 26 = {c} → {chr(c + 97)}")

    return result.upper(), steps


def affine_decrypt(text, a, b):
    text = text.lower().replace(" ", "")
    result = ""
    steps = []

    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Invalid a value!", ["a has no modular inverse"]

    for ch in text:
        if ch.isalpha():
            c = ord(ch) - 97
            p = (a_inv * (c - b)) % 26
            result += chr(p + 97)
            steps.append(f"{a_inv}*({c}-{b}) mod 26 = {p} → {chr(p + 97)}")

    return result.upper(), steps
