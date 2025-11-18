import math
def mms(lam, mu, s):
    if s < 2:
        raise ValueError("Use s >= 2 para o modelo M/M/s>1")

    rho = lam / (s * mu)
    if rho >= 1:
        raise ValueError("Sistema instável: λ ≥ s·μ")

    # P0 (probabilidade de sistema vazio)
    soma = sum((lam / mu) ** n / math.factorial(n) for n in range(s))
    termo = ((lam / mu) ** s / (math.factorial(s) * (1 - rho)))
    P0 = 1 / (soma + termo)

    # Lq (nº médio na fila)
    Lq = (P0 * ((lam / mu) ** s) * rho) / (math.factorial(s) * ((1 - rho) ** 2))

    # L, Wq, W
    L = Lq + (lam / mu)
    Wq = Lq / lam
    W = Wq + (1 / mu)

    return [L, Lq, W, Wq, P0, rho]