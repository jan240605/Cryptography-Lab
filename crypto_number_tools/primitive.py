def power(base, exp, mod):
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res


def get_prime_factors(n):
    factors = []
    steps = []

    if n % 2 == 0:
        factors.append(2)
        steps.append("2 is a prime factor")
        while n % 2 == 0:
            n //= 2

    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            steps.append(f"{i} is a prime factor")
            while n % i == 0:
                n //= i
        i += 2

    if n > 2:
        factors.append(n)
        steps.append(f"{n} is a prime factor")

    return factors, steps


def find_primitive_roots(n):
    steps = []
    phi = n - 1
    steps.append(f"φ({n}) = {phi}")

    factors, factor_steps = get_prime_factors(phi)
    steps.extend(factor_steps)
    steps.append(f"Prime factors of φ({n}): {factors}")

    roots = []

    for r in range(2, n):
        is_primitive = True
        steps.append(f"\nChecking r = {r}")
        for f in factors:
            value = power(r, phi // f, n)
            steps.append(f"{r}^({phi}//{f}) mod {n} = {value}")
            if value == 1:
                steps.append("→ Not a primitive root")
                is_primitive = False
                break
        if is_primitive:
            steps.append(f"→ {r} is a primitive root")
            roots.append(r)

    return roots, steps
