import math

def mmc(lam, mu, c):

    if c < 1:
        raise ValueError("Número de servidores deve ser >= 1")

    rho = lam / (c * mu)  # taxa de utilização por servidor
    if rho >= 1:
        raise ValueError("Sistema instável (ρ >= 1)")

    # Calcula P0 (probabilidade do sistema vazio)
    sum_terms = sum((lam / mu) ** n / math.factorial(n) for n in range(c))
    last_term = ((lam / mu) ** c) / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sum_terms + last_term)

    # Número médio na fila
    Lq = (((lam / mu) ** c) * rho / (math.factorial(c) * (1 - rho) ** 2)) * P0

    # Número médio no sistema
    L = Lq + lam / mu

    # Tempo médio na fila e no sistema
    Wq = Lq / lam
    W = Wq + 1 / mu

    return {
        "ρ": rho,
        "P0": P0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq
    }