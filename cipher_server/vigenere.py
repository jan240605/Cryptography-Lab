def vigenere_encrypt(text, key):
    text = text.lower().replace(" ", "")
    key = key.lower()
    result = ""
    steps = []
    k = 0

    for i, ch in enumerate(text):
        if ch.isalpha():
            p = ord(ch) - 97
            kch = ord(key[k % len(key)]) - 97
            c = (p + kch) % 26
            result += chr(c + 97)
            steps.append(f"{ch} + {key[k % len(key)]} → {chr(c + 97)}")
            k += 1

    return result.upper(), steps


def vigenere_decrypt(text, key):
    text = text.lower().replace(" ", "")
    key = key.lower()
    result = ""
    steps = []
    k = 0

    for i, ch in enumerate(text):
        if ch.isalpha():
            c = ord(ch) - 97
            kch = ord(key[k % len(key)]) - 97
            p = (c - kch) % 26
            result += chr(p + 97)
            steps.append(f"{ch} - {key[k % len(key)]} → {chr(p + 97)}")
            k += 1

    return result.upper(), steps
