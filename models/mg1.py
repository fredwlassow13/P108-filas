import math

def mg1(lam, mu, var_s):

    rho = lam / mu

    if rho >=1:
        return {"Erro": "Sistema instável: ρ >= 1"}

    e_s = 1 / mu

    e_s2 = var_s + (e_s ** 2)
    Lq = (lam ** 2 * e_s2) / (2 * (1 - rho))
    Wq = Lq / lam
    W = Wq + e_s
    L = lam * W

    return {
        "ρ": rho,
        "E[S]": e_s,
        "E[S²]": e_s2,
        "Lq": Lq,
        "Wq": Wq,
        "W": W,
        "L": L
    }