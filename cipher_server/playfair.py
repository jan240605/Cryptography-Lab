def generate_matrix(key):
    key = key.upper().replace("J", "I")
    seen = []
    matrix = []

    for ch in key:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.append(ch)

    for i in range(0, 25, 5):
        matrix.append(seen[i:i+5])

    return matrix


def find_position(matrix, ch):
    if ch == "J":
        ch = "I"
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c


def playfair_prepare(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    prepared = ""
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "X"

        if a == b:
            prepared += a + "X"
            i += 1
        else:
            prepared += a + b
            i += 2

    if len(prepared) % 2 != 0:
        prepared += "X"

    return prepared


def playfair_encrypt(text, key):
    matrix = generate_matrix(key)
    prepared = playfair_prepare(text)
    result = ""
    steps = []

    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            c1_new, c2_new = (c1+1)%5, (c2+1)%5
            result += matrix[r1][c1_new] + matrix[r2][c2_new]
            steps.append(f"{a}{b}: Same row → {matrix[r1][c1_new]}{matrix[r2][c2_new]}")
        elif c1 == c2:
            r1_new, r2_new = (r1+1)%5, (r2+1)%5
            result += matrix[r1_new][c1] + matrix[r2_new][c2]
            steps.append(f"{a}{b}: Same column → {matrix[r1_new][c1]}{matrix[r2_new][c2]}")
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
            steps.append(f"{a}{b}: Rectangle → {matrix[r1][c2]}{matrix[r2][c1]}")

    return result, steps


def playfair_decrypt(text, key):
    matrix = generate_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    result = ""
    steps = []

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            c1_new, c2_new = (c1-1)%5, (c2-1)%5
            result += matrix[r1][c1_new] + matrix[r2][c2_new]
            steps.append(f"{a}{b}: Same row → {matrix[r1][c1_new]}{matrix[r2][c2_new]}")
        elif c1 == c2:
            r1_new, r2_new = (r1-1)%5, (r2-1)%5
            result += matrix[r1_new][c1] + matrix[r2_new][c2]
            steps.append(f"{a}{b}: Same column → {matrix[r1_new][c1]}{matrix[r2_new][c2]}")
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
            steps.append(f"{a}{b}: Rectangle → {matrix[r1][c2]}{matrix[r2][c1]}")

    return result, steps
