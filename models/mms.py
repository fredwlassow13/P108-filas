import math

def mm_s(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return "Sistema instável: ρ >= 1 "

    sum_terms = sum((lam / mu) ** n / math.factorial(n) for n in range(s))
    p0 = 1 / (sum_terms + ((lam / mu) ** s / math.factorial(s)) * 1 / (1 - rho))

    pq = ((lam/mu)**s / math.factorial(s)) * (rho / (1-rho)) * p0
    Lq = pq / (1-rho)
    L = Lq + lam/mu
    Wq = Lq / lam
    W = Wq + 1/mu

    return {
        "ρ": rho,
        "P0": p0,
        "P_queue": pq,
        "Lq": Lq,
        "Wq": Wq,
        "W": W
    }



