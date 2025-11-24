import math

def mm_infinity(lam, mu):

    rho = lam / mu
    L = rho
    W = 1/ mu
    Wq = 0
    P0 = math.exp(-rho)


    return {
        "ρ": rho,
        "P0": P0,
        "L": L,
        "W": W,
        "Wq": Wq
    }