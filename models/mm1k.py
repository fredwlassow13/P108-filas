import math
from typing import Optional

class MM1K:
    """Modelo M/M/1/K - Fila única com capacidade finita"""
    def __init__(
        self,
        lam: Optional[float] = None,
        mu: Optional[float] = None,
        K: Optional[int] = None,
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
        self.K = K
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
        if self.rho is None and self.lam is not None and self.mu is not None:
            self.rho = self.lam / self.mu
        elif self.mu is None and self.lam is not None and self.rho is not None:
            self.mu = self.lam / self.rho
        elif self.lam is None and self.mu is not None and self.rho is not None:
            self.lam = self.rho * self.mu

        if self.lam is None or self.mu is None or self.K is None:
            raise ValueError("Parâmetros insuficientes: lam, mu e K são necessários")

        if self.lam >= self.mu:
            raise ValueError("Sistema instável: λ ≥ μ (rho ≥ 1)")

        self.rho = self.lam / self.mu

        # Probabilidade do sistema vazio
        if abs(self.rho - 1) < 1e-8:
            self.P0 = 1 / (self.K + 1)
            self.L = self.K / 2
        else:
            self.P0 = (1 - self.rho) / (1 - self.rho ** (self.K + 1))
            self.L = (self.rho * (1 - (self.K + 1) * self.rho ** self.K + self.K * self.rho ** (self.K + 1))) / ((1 - self.rho) * (1 - self.rho ** (self.K + 1)))

        self.Pb = self.P0 * self.rho ** self.K
        self.lam_eff = self.lam * (1 - self.Pb)

        self.Lq = self.L - (1 - self.P0)
        self.W = self.L / self.lam_eff
        self.Wq = self.Lq / self.lam_eff

    # Probabilidades padronizadas
    def P0_sistema(self):
        return self.P0

    def P_occupied(self):
        return self.Pb

    def P_n(self, n=None):
        n = n if n is not None else self.n
        if n is None or n < 0 or n > self.K:
            return 0
        return self.P0 * self.rho ** n

    def P_n_greater_than_r(self, r=None):
        r = r if r is not None else self.r
        if r is None:
            return 0
        if r < 0:
            return 1
        elif r >= self.K:
            return 0
        prob_acumulada = sum(self.P_n(k) for k in range(r+1))
        return 1 - prob_acumulada

    def resolver(self):
        resultado = {
            "Modelo": "M/M/1/K",
            "Parâmetros": {"λ": self.lam, "μ": self.mu, "K": self.K, "ρ": self.rho, "λ_efetivo": self.lam_eff},
            "Medidas de Efetividade": {"L": self.L, "Lq": self.Lq, "W": self.W, "Wq": self.Wq},
            "Probabilidades": {"P0": self.P0_sistema(), "P_occupied": self.P_occupied()}
        }

        if self.n is not None:
            resultado["Probabilidades"][f"P({self.n})"] = self.P_n()
        if self.r is not None:
            resultado["Probabilidades"][f"P(n>{self.r})"] = self.P_n_greater_than_r()

        return resultado
