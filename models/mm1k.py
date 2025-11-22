import math

def mm1k(lam, mu, K):

    rho = lam / mu

    if abs(rho-1) < 1e-8:
        P0 = 1 / (K+1)
        L = K / 2
    else:
        P0 = (1 - rho)/(1 - rho ** (K + 1))
        L = (rho * (1 - (K+1) * rho ** K + K * rho ** (K + 1))) / ((1 - rho) *(1 - rho ** (K + 1)))

    Pb = P0 * rho ** K
    lam_eff = lam * (1 - Pb)

    Lq = L - (1 - P0)
    W = L / lam_eff
    Wq = Lq / lam_eff

    return {
        "ρ": rho,
        "L": L,
        "Lq": max(Lq, 0),
        "W": W,
        "Wq": max(Wq, 0),
        "P0": P0,
        "Pb": Pb
    }