import math

def mm1(lam, mu):
    if lam >= mu:
        raise ValueError("Sistema instável: λ ≥ μ")

    rho = lam / mu
    P0 = 1 - rho
    L = lam / (mu - lam)
    Lq = (lam ** 2) / (mu * (mu - lam))
    W = 1 / (mu - lam)
    Wq = lam / (mu * (mu - lam))

    return [L, Lq, W, Wq, P0, rho]