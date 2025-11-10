import math

def mm1k(lam, mu, K):

    rho = lam / mu

    if abs(rho-1) < 1e-8:
        P0 = 1 / (K+1)
        L = K / 2
    else:
        P0 = (1 - rho)/(1 - rho ** (K + 1))
        L = (rho * (1 - (K+1) * rho ** K + K * rho ** (K + 1))) / ((1 - rho) *(1 - rho ** (K + 1)))

    Pk = P0 * rho ** K
    Pb = Pk

    W = L / (lam * (1 - Pk))
    Wq = W - (1 / mu)

    probs = {f"P{n}": P0 * rho ** n for n in range(K + 1)}

    return {
        "ρ": rho,
        "P0": P0,
        **probs,
        "L": L,
        "W": W,
        "Wq": Wq,
        "Pb (bloqueio)": Pb
    }