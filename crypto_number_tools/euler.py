def calculate_phi(n):
    result = n
    temp = n
    p = 2
    steps = []

    while p * p <= temp:
        if temp % p == 0:
            steps.append(f"{p} is a prime factor of {temp}")
            steps.append(f"Applying: result = result - result/{p}")
            result -= result // p
            while temp % p == 0:
                temp //= p
                steps.append(f"Dividing by {p}, new temp = {temp}")
        p += 1

    if temp > 1:
        steps.append(f"{temp} is a remaining prime factor")
        steps.append(f"Applying: result = result - result/{temp}")
        result -= result // temp

    return result, steps
