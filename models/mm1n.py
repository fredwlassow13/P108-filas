import math

def mm1n(lam, mu, N):

    rho = lam / mu

    if abs(rho - 1) < 1e-8:
        p0 = 1 / (N + 1)
    else:
        p0 = (1 - rho) / (1 - rho ** (N + 1))

    probs = [p0 * (rho ** n) for n in range(N + 1)]
    pN = probs[-1]

    if abs(rho - 1) < 1e-8:
        L = N / 2
    else:
        L = (rho * (1 - (N + 1) * rho ** N + N * rho ** (N + 1))) / ((1 - rho) * (1 - rho ** (N + 1)))


    W = L / (lam * (1 - pN))
    Wq = W - 1 / mu

    return {
        "ρ": rho,
        "P0": p0,
        "PN (bloqueio)": pN,
        "L": L,
        "W": W,
        "Wq": Wq
    }