import math

class MMInfinity:
    """Modelo M/M/∞ - Servidores infinitos"""
    def __init__(self, lam=None, mu=None, L=None, W=None, Wq=None, n=None):
        self.lam = lam
        self.mu = mu
        self.L = L
        self.W = W
        self.Wq = Wq
        self.n = n

        self.calcular_variaveis_faltantes()

    def calcular_variaveis_faltantes(self):
        if self.lam is None or self.mu is None:
            raise ValueError("λ e μ devem ser fornecidos")

        self.rho = self.lam / self.mu
        self.L = self.rho
        self.W = 1 / self.mu
        self.Wq = 0  # Sem fila em servidores infinitos
        self.P0 = math.exp(-self.rho)

    def probabilidade_estado_n(self, n=None):
        if n is None:
            n = self.n
        if n is None:
            return None
        return (self.rho ** n / math.factorial(n)) * self.P0

    def resolver(self):
        resultado = {
            "Modelo": "M/M/∞",
            "Parâmetros": {
                "λ": self.lam,
                "μ": self.mu,
                "ρ": self.rho
            },
            "Medidas de Efetividade": {
                "L": self.L,
                "W": self.W,
                "Wq": self.Wq
            },
            "Probabilidades": {
                "P0": self.P0
            }
        }

        if self.n is not None:
            resultado["Probabilidades"][f"P({self.n})"] = self.probabilidade_estado_n()

        return resultado
