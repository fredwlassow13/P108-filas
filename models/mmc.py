import math

def mm_infinity(lam, mu):

    rho = lam / mu
    L = rho
    W = 1/ mu
    Wq = 0
    P0 = math.exp(-rho)

    probs = {f"P{n}": math.exp(-rho) * (rho ** n) / math.factorial(n) for n in range(6)}

    return {
        "ρ": rho,
        "P0": P0,
        **probs,
        "L": L,
        "W": W,
        "Wq": Wq
    }