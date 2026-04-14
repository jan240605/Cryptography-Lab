import math

def fermat_factor(n):
    steps = []

    if n <= 0:
        steps.append("Invalid input.")
        return None, steps

    if n % 2 == 0:
        steps.append("n is even.")
        steps.append(f"Factors: 2 and {n//2}")
        return (2, n // 2), steps

    steps.append("n is odd. Applying Fermat's Factorization.")

    x = math.ceil(math.sqrt(n))
    steps.append(f"x = ceil(sqrt({n})) = {x}")

    while True:
        y2 = x * x - n
        steps.append(f"y² = {x}² - {n} = {y2}")
        y = int(math.sqrt(y2))

        if y * y == y2:
            factor1 = x + y
            factor2 = x - y
            steps.append(f"y² is a perfect square → y = {y}")
            steps.append(f"Factors = {x} + {y} = {factor1}, {x} - {y} = {factor2}")
            return (factor1, factor2), steps

        x += 1
        steps.append(f"Trying next x = {x}")
