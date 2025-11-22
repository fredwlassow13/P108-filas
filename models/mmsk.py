import math

def mm_s_k(lam, mu, s, K):
    a = lam / mu
    rho = lam / (s * mu)
    aviso = "Sistema no limite da estabilidade (ρ = 1)." if abs(rho - 1) < 1e-12 else None

    # --- CASO 1: ρ = 1 (tratar separado para evitar divisão por zero)
    if abs(rho - 1) < 1e-12:

        # P0 especial para ρ = 1
        sum_terms = sum((a ** n) / math.factorial(n) for n in range(s))
        tail = (a ** s) / math.factorial(s) * (K - s + 1)
        P0 = 1 / (sum_terms + tail)

        # Probabilidades
        probs = []
        for n in range(K + 1):
            if n < s:
                pn = P0 * (a ** n) / math.factorial(n)
            else:
                pn = P0 * (a ** n) / (math.factorial(s) * (s ** (n - s)))
            probs.append(pn)

        Pk = probs[K]

        # L = soma n*P(n)
        L = sum(n * probs[n] for n in range(K + 1))

        # λ efetiva
        lam_eff = lam * (1 - Pk)

        W = L / lam_eff
        Wq = W - 1/mu
        Lq = lam_eff * Wq

        return {
            "ρ": rho,
            "P0": P0,
            "L": L,
            "Lq": Lq,
            "W": W,
            "Wq": Wq,
            "Pk (bloqueio)": Pk,
            "aviso": aviso
        }

    # --- CASO 2: ρ ≠ 1 (fórmulas normais)
    sum_terms = sum((a ** n) / math.factorial(n) for n in range(s))
    tail = (a ** s) / math.factorial(s) * (1 - rho ** (K - s + 1)) / (1 - rho)
    P0 = 1 / (sum_terms + tail)

    # Probabilidades Pn
    probs = []
    for n in range(K + 1):
        if n < s:
            pn = P0 * (a ** n) / math.factorial(n)
        else:
            pn = P0 * (a ** n) / (math.factorial(s) * (s ** (n - s)))
        probs.append(pn)

    Pk = probs[K]

    # Lq fórmula completa
    Lq = (
        P0
        * (a ** s)
        * rho
        / (math.factorial(s) * (1 - rho) ** 2)
        * (1 - rho ** (K - s + 1) - (K - s + 1) * (1 - rho) * rho ** (K - s))
    )

    # L = soma n*P(n) → mais confiável
    L = sum(n * probs[n] for n in range(K + 1))

    lam_eff = lam * (1 - Pk)
    Wq = Lq / lam_eff
    W = Wq + 1 / mu

    return {
        "ρ": rho,
        "P0": P0,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "Pk (bloqueio)": Pk,
        "aviso": aviso
    }
