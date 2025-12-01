import math
from typing import Optional

class MG1:
    def __init__(
        self,
        lam: Optional[float] = None,
        mu: Optional[float] = None,
        sigma: Optional[float] = None,  # desvio padrão do tempo de serviço
        rho: Optional[float] = None,
        n: Optional[int] = None,
        r: Optional[int] = None,
        t_sistema: Optional[float] = None,
        t_fila: Optional[float] = None,
        L: Optional[float] = None,
        Lq: Optional[float] = None,
        W: Optional[float] = None,
        Wq: Optional[float] = None
    ):
        self.lam = lam
        self.mu = mu
        self.sigma = sigma
        self.rho = rho
        self.n = n
        self.r = r
        self.t_sistema = t_sistema
        self.t_fila = t_fila
        self.L = L
        self.Lq = Lq
        self.W = W
        self.Wq = Wq

        self._calcular_variaveis_faltantes()

    def _calcular_variaveis_faltantes(self):
        if self.lam is None and self.mu is not None and self.rho is not None:
            self.lam = self.rho * self.mu
        elif self.mu is None and self.lam is not None and self.rho is not None:
            self.mu = self.lam / self.rho

        if self.lam is None or self.mu is None:
            raise ValueError("Parâmetros insuficientes para calcular MG1")

        if self.lam >= self.mu:
            raise ValueError("Sistema instável: λ ≥ μ")

        self.rho = self.lam / self.mu

        # Fórmulas MG1 usando fator de variabilidade C_s² = (σμ)^2
        Cs2 = (self.sigma * self.mu) ** 2 if self.sigma is not None else 1  # se não informado, assume M/M/1
        self.Lq = (self.rho ** 2 * (1 + Cs2)) / (2 * (1 - self.rho))
        self.Wq = self.Lq / self.lam
        self.W = self.Wq + 1 / self.mu
        self.L = self.lam * self.W

    # Probabilidades
    def P0(self):
        return 1 - self.rho

    def P_occupied(self):
        return self.rho

    def P_n(self, n=None):
        n = n if n is not None else self.n
        if n is None:
            return None
        return (1 - self.rho) * (self.rho ** n)

    def P_n_greater_than_r(self, r=None):
        r = r if r is not None else self.r
        if r is None:
            return None
        return self.rho ** (r + 1)

    def P_W_greater_than_t(self, t=None):
        t = t if t is not None else self.t_sistema
        if t is None:
            return None
        return math.exp(- (1 - self.rho) * self.mu * t)

    def P_Wq_greater_than_t(self, t=None):
        t = t if t is not None else self.t_fila
        if t is None:
            return None
        return self.rho * math.exp(- (1 - self.rho) * self.mu * t)

    # Resultado padronizado
    def resolver(self):
        resultado = {
            "Modelo": "M/G/1",
            "Parâmetros": {"λ": self.lam, "μ": self.mu, "ρ": self.rho, "σ": self.sigma},
            "Medidas de Efetividade": {"L": self.L, "Lq": self.Lq, "W": self.W, "Wq": self.Wq},
            "Probabilidades": {
                "P0": self.P0(),
                "P_occupied": self.P_occupied()
            }
        }

        if self.n is not None:
            resultado["Probabilidades"]["P(n)"] = self.P_n()
        if self.r is not None:
            resultado["Probabilidades"]["P(n>r)"] = self.P_n_greater_than_r()
            resultado["Probabilidades"]["P(n<r)"] = 1 - self.P_n_greater_than_r()
        if self.t_sistema is not None:
            resultado["Probabilidades"]["P(W>t)"] = self.P_W_greater_than_t()
        if self.t_fila is not None:
            resultado["Probabilidades"]["P(Wq>t)"] = self.P_Wq_greater_than_t()

        return resultado
