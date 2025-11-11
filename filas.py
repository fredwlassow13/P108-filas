import math

def mm1(lmbda, mu):
    if lmbda >= mu:
        raise ValueError("Sistema instável: λ ≥ μ")

    rho = lmbda / mu
    P0 = 1 - rho
    L = lmbda / (mu - lmbda)
    Lq = (lmbda ** 2) / (mu * (mu - lmbda))
    W = 1 / (mu - lmbda)
    Wq = lmbda / (mu * (mu - lmbda))

    return [L, Lq, W, Wq, P0, rho]

def mms(lmbda, mu, s):
    if s < 2:
        raise ValueError("Use s >= 2 para o modelo M/M/s>1")

    rho = lmbda / (s * mu)
    if rho >= 1:
        raise ValueError("Sistema instável: λ ≥ s·μ")

    # P0 (probabilidade de sistema vazio)
    soma = sum((lmbda / mu) ** n / math.factorial(n) for n in range(s))
    termo = ((lmbda / mu) ** s / (math.factorial(s) * (1 - rho)))
    P0 = 1 / (soma + termo)

    # Lq (nº médio na fila)
    Lq = (P0 * ((lmbda / mu) ** s) * rho) / (math.factorial(s) * ((1 - rho) ** 2))

    # L, Wq, W
    L = Lq + (lmbda / mu)
    Wq = Lq / lmbda
    W = Wq + (1 / mu)

    return [L, Lq, W, Wq, P0, rho]

def mm1_k(lam, mu, K):
    
    rho = lam / mu
    P0 = 1 - (rho / (1 - rho**(K+1)))
    Pn = [(1 - rho) / (1 - rho**(K+1)) * (rho**n) for n in range(K+1)]
    L = (rho / (1 - rho)) - ((K+1) * (rho**(K+1))) / (1 - rho**(K+1))
    Lq = L - (1 - P0)
    W = L / lam
    Wq = Lq / lam
    
    return P0, Pn, L, Lq, W, Wq