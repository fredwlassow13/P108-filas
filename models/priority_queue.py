import math

def priority_queue_non_preemptive(lam_high, lam_low, mu):
    rho_high = lam_high / mu
    rho_low = lam_low / mu
    rho_total = rho_high + rho_low

    if rho_total >= 1:
        raise ValueError("Sistema instável (ρ ≥ 1)")

    # Número médio no sistema
    L_high = rho_high / (1 - rho_total)
    L_low = (rho_low * (1 + rho_high)) / (1 - rho_total)
    L = L_high + L_low

    # Número médio na fila
    Lq_high = rho_high ** 2 / (1 - rho_total)
    Lq_low = (rho_low ** 2 + 2 * rho_high * rho_low) / (1 - rho_total)
    Lq = Lq_high + Lq_low

    # Tempo médio no sistema e na fila
    W_high = L_high / lam_high if lam_high > 0 else 0
    W_low = L_low / lam_low if lam_low > 0 else 0
    W = (lam_high * W_high + lam_low * W_low) / (lam_high + lam_low)

    Wq_high = Lq_high / lam_high if lam_high > 0 else 0
    Wq_low = Lq_low / lam_low if lam_low > 0 else 0
    Wq = (lam_high * Wq_high + lam_low * Wq_low) / (lam_high + lam_low)

    return {
        "rho": rho_total,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "L_high": L_high,
        "L_low": L_low,
        "W_high": W_high,
        "W_low": W_low
    }


def priority_queue_preemptive(lam_high, lam_low, mu):
    rho_high = lam_high / mu
    rho_low = lam_low / mu
    rho_total = rho_high + rho_low

    if rho_total >= 1:
        raise ValueError("Sistema instável (ρ ≥ 1)")

    # Alta prioridade
    L_high = rho_high / (1 - rho_high)
    Lq_high = L_high - rho_high
    W_high = L_high / lam_high if lam_high > 0 else 0
    Wq_high = Lq_high / lam_high if lam_high > 0 else 0

    # Baixa prioridade
    L_low = rho_low / ((1 - rho_high) * (1 - rho_total))
    Lq_low = L_low - rho_low
    W_low = L_low / lam_low if lam_low > 0 else 0
    Wq_low = Lq_low / lam_low if lam_low > 0 else 0

    # Sistema total
    L = L_high + L_low
    Lq = Lq_high + Lq_low
    W = (lam_high * W_high + lam_low * W_low) / (lam_high + lam_low) if (lam_high + lam_low) > 0 else 0
    Wq = (lam_high * Wq_high + lam_low * Wq_low) / (lam_high + lam_low) if (lam_high + lam_low) > 0 else 0

    return {
        "rho": rho_total,
        "L": L,
        "Lq": Lq,
        "W": W,
        "Wq": Wq,
        "L_high": L_high,
        "L_low": L_low,
        "W_high": W_high,
        "W_low": W_low
    }
