import math
from typing import Optional

class MM1N:
    """Modelo M/M/1/N — população finita (correto, via processo nascimento-morte)."""

    def __init__(self, lam: float, mu: float, N: int, n: Optional[int] = None, r: Optional[int] = None):
        self.lam = lam
        self.mu = mu
        self.N = int(N)
        self.n = n
        self.r = r

        if lam <= 0 or mu <= 0 or N <= 0:
            raise ValueError("λ, μ e N devem ser positivos.")

        self._calcular()

    def _calcular(self):
        a = self.lam / self.mu

        # P0 e lista de probabilidades
        soma = sum(math.factorial(self.N) / math.factorial(self.N - k) * (a ** k)
                   for k in range(self.N + 1))

        self.P0 = 1 / soma

        self.probs = [
            math.factorial(self.N) / math.factorial(self.N - k) * (a ** k) * self.P0
            for k in range(self.N + 1)
        ]

        self.PN = self.probs[-1]      # prob. de bloqueio

        # L correto (esperança de n)
        self.L = sum(k * self.probs[k] for k in range(self.N + 1))

        # Lq correto: nº de clientes na fila = nº total - prob de estar sendo atendido
        # Número esperado em serviço = (1 - P0)
        self.Lq = self.L - (1 - self.P0)

        # λ efetivo da população finita: λ * prob. de existir cliente disponível
        self.lam_eff = self.lam * (self.N - self.L) / self.N

        # tempos
        if self.lam_eff > 0:
            self.W = self.L / self.lam_eff
            self.Wq = self.Lq / self.lam_eff
        else:
            self.W = 0
            self.Wq = 0

    # Probabilidades
    def P_n(self, n=None):
        if n is None:
            n = self.n
        if n is None or n < 0 or n > self.N:
            return 0
        return self.probs[n]

    def P_n_greater_than_r(self, r=None):
        if r is None:
            r = self.r
        if r is None:
            return 0
        if r < 0:
            return 1
        if r >= self.N:
            return 0
        return sum(self.P_n(k) for k in range(r+1, self.N+1))

    # Saída padronizada
    def resolver(self):
        resultado = {
            "Modelo": "M/M/1/N",
            "Parâmetros": {
                "λ": self.lam,
                "μ": self.mu,
                "N": self.N,
                "λ_efetivo": self.lam_eff
            },
            "Medidas de Efetividade": {
                "L": self.L,
                "Lq": self.Lq,
                "W": self.W,
                "Wq": self.Wq,
            },
            "Probabilidades": {
                "P0": self.P0,
                "PN (bloqueio)": self.PN
            }
        }

        if self.n is not None:
            resultado["Probabilidades"][f"P({self.n})"] = self.P_n(self.n)

        if self.r is not None:
            resultado["Probabilidades"][f"P(n>{self.r})"] = self.P_n_greater_than_r(self.r)

        return resultado
