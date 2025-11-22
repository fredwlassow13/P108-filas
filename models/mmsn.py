import math

def mmsn(lam, mu, s, N):

    rho = lam / (s * mu)

    # --- Cálculo de P0 ---
    a = lam / mu

    soma = 0

    # Parte 1: n = 0 até s-1
    for n in range(s):
        soma += (a ** n) / math.factorial(n)

    # Parte 2: n = s até N → capacidade total N
    last_term = (a ** s) / math.factorial(s)
    if abs(s * mu - lam) < 1e-8:
        # Caso limite rho = 1 → fórmula especial
        soma += last_term * (N - s + 1)
    else:
        soma += last_term * ((1 - rho ** (N - s + 1)) / (1 - rho))

    P0 = 1 / soma

    # Probabilidade N (bloqueio)
    if N < s:
        PN = P0 * (a ** N) / math.factorial(N)
    else:
        PN = P0 * (a ** N) / (math.factorial(s) * (s ** (N - s)))

    # λ efetiva
    lam_eff = lam * (1 - PN)

    # --- Cálculo de L ---
    # L = soma n * Pn
    L = 0
    for n in range(N + 1):
        if n < s:
            Pn = P0 * (a ** n) / math.factorial(n)
        else:
            Pn = P0 * (a ** n) / (math.factorial(s) * s ** (n - s))
        L += n * Pn

    # Número em serviço
    Ls = lam_eff / mu

    # Número na fila
    Lq = L - Ls

    # Tempos
    W = L / lam_eff
    Wq = Lq / lam_eff

    return {
        "ρ": rho,
        "P0": P0,
        "PN": PN,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq
    }
