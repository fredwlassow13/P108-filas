import math
from typing import Optional

class MM1N:
    """Modelo M/M/1/N - População finita"""
    def __init__(
        self,
        lam: Optional[float] = None,
        mu: Optional[float] = None,
        N: Optional[int] = None,
        rho: Optional[float] = None,
        n: Optional[int] = None,
        r: Optional[int] = None,
        L: Optional[float] = None,
        Lq: Optional[float] = None,
        W: Optional[float] = None,
        Wq: Optional[float] = None,
        t_sistema: Optional[float] = None,
        t_fila: Optional[float] = None
    ):
        self.lam = lam
        self.mu = mu
        self.N = N
        self.rho = rho
        self.n = n
        self.r = r
        self.L = L
        self.Lq = Lq
        self.W = W
        self.Wq = Wq
        self.t_sistema = t_sistema
        self.t_fila = t_fila

        self._calcular_variaveis_faltantes()

    def _calcular_variaveis_faltantes(self):
        if self.rho is None and self.lam is not None and self.mu is not None and self.N is not None:
            self.rho = (self.N * self.lam) / self.mu
        elif self.mu is None and self.lam is not None and self.rho is not None and self.N is not None:
            self.mu = (self.N * self.lam) / self.rho
        elif self.lam is None and self.mu is not None and self.rho is not None and self.N is not None:
            self.lam = (self.rho * self.mu) / self.N

        if self.lam is None or self.mu is None or self.N is None:
            raise ValueError("Parâmetros insuficientes: lam, mu e N são necessários")

        # Probabilidade do sistema vazio
        soma = sum((math.factorial(self.N) / math.factorial(self.N - k)) * ((self.lam/self.mu) ** k) for k in range(self.N + 1))
        self.P0 = 1 / soma

        # Probabilidade de cada estado n
        self.probs = [(math.factorial(self.N) / math.factorial(self.N - k)) * ((self.lam/self.mu) ** k) * self.P0 for k in range(self.N + 1)]
        self.PN = self.probs[-1]  # Probabilidade de bloqueio (estado N)

        # L e W
        self.L = sum(k * p for k, p in enumerate(self.probs))
        self.lam_eff = self.lam * (self.N - self.L) / self.N
        self.W = self.L / self.lam_eff if self.lam_eff > 0 else 0
        self.Wq = self.W - 1 / self.mu
        self.Lq = self.lam_eff * self.Wq

    # Probabilidades padronizadas
    def P0_sistema(self):
        return self.P0

    def P_n(self, n=None):
        n = n if n is not None else self.n
        if n is None or n < 0 or n > self.N:
            return 0
        return self.probs[n]

    def P_n_greater_than_r(self, r=None):
        r = r if r is not None else self.r
        if r is None:
            return 0
        if r < 0:
            return 1
        elif r >= self.N:
            return 0
        return sum(self.P_n(k) for k in range(r+1, self.N + 1))

    def resolver(self):
        resultado = {
            "Modelo": "M/M/1/N",
            "Parâmetros": {"λ": self.lam, "μ": self.mu, "N": self.N, "ρ": self.rho, "λ_efetivo": self.lam_eff},
            "Medidas de Efetividade": {"L": self.L, "Lq": self.Lq, "W": self.W, "Wq": self.Wq},
            "Probabilidades": {"P0": self.P0_sistema(), "PN (bloqueio)": self.P_n(self.N)}
        }

        if self.n is not None:
            resultado["Probabilidades"][f"P({self.n})"] = self.P_n()
        if self.r is not None:
            resultado["Probabilidades"][f"P(n>{self.r})"] = self.P_n_greater_than_r()

        return resultado
