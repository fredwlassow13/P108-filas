import math

def mm_s_k(lam, mu, s, K):

    rho = lam / (s * mu)
    if rho >=1:
        aviso = "Sistema possivelmente instável  (ρ >= 1)."
    else:
        aviso = None


    soma = sum((lam / mu) ** n / math.factorial(n) for n in range(s))
    soma += ((lam / mu) ** s / (math.factorial(s) * (1 - rho))) * (1 - rho ** (K - s + 1))
    P0 = 1 / soma

    probs = {}
    for n in range(K + 1):
        if n < s:
            Pn = P0 * ((lam / mu) ** n) / math.factorial(n)
        else :
            Pn = P0 * ((lam / mu) ** n) / (math.factorial(s) * (s ** (n - s)))
        probs[f"P{n}"] = Pn

    Pk = probs[f"P{K}"]

    Lq = (
        P0
        * ((lam / mu) ** s)
        * rho
        / (math.factorial(s) * (1 - rho) ** 2)
        * (1 - rho ** (K - s + 1) - (K - s + 1) * (1 - rho) * rho ** (K - s))
    )

    L = Lq + lam * (1 - Pk) / mu

    W = L / (lam * (1 - Pk))
    Wq = W - 1 / mu

    return {
        "ρ": rho,
        "P0": P0,
        **probs,
        "Pk (bloqueio)": Pk,
        "Lq": Lq,
        "L": L,
        "Wq": Wq,
        "W": W,
        "aviso": aviso,
    }