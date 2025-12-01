import math
from typing import Optional

class MM1:
    def __init__(
        self,
        lam: Optional[float] = None,
        mu: Optional[float] = None,
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
        if self.lam is not None and self.mu is not None:
            if self.lam >= self.mu:
                raise ValueError("Sistema instável: λ ≥ μ")
            self.rho = self.lam / self.mu
            self.L = self.lam / (self.mu - self.lam)
            self.Lq = (self.lam ** 2) / (self.mu * (self.mu - self.lam))
            self.W = 1 / (self.mu - self.lam)
            self.Wq = self.lam / (self.mu * (self.mu - self.lam))
        elif self.lam is not None and self.rho is not None:
            self.mu = self.lam / self.rho
            self.L = self.lam / (self.mu - self.lam)
            self.Lq = (self.lam ** 2) / (self.mu * (self.mu - self.lam))
            self.W = 1 / (self.mu - self.lam)
            self.Wq = self.lam / (self.mu * (self.mu - self.lam))
        elif self.mu is not None and self.rho is not None:
            self.lam = self.rho * self.mu
            self.L = self.lam / (self.mu - self.lam)
            self.Lq = (self.lam ** 2) / (self.mu * (self.mu - self.lam))
            self.W = 1 / (self.mu - self.lam)
            self.Wq = self.lam / (self.mu * (self.mu - self.lam))
        else:
            raise ValueError("Parâmetros insuficientes para calcular MM1")

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
        return math.exp(-self.mu * (1 - self.rho) * t)

    def P_Wq_greater_than_t(self, t=None):
        t = t if t is not None else self.t_fila
        if t is None:
            return None
        return self.rho * math.exp(-self.mu * (1 - self.rho) * t)

    # Resultado padronizado
    def resolver(self):
        resultado = {
            "Modelo": "M/M/1",
            "Parâmetros": {"λ": self.lam, "μ": self.mu, "ρ": self.rho},
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
