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


class MMC:
    """Modelo M/M/c - Múltiplos servidores infinitos (capacidade infinita)"""
    def __init__(self, lam=None, mu=None, c=None, L=None, Lq=None, W=None, Wq=None, n=None):
        self.lam = lam
        self.mu = mu
        self.c = c  # número de servidores
        self.L = L
        self.Lq = Lq
        self.W = W
        self.Wq = Wq
        self.n = n

        self.calcular_variaveis_faltantes()

    def calcular_variaveis_faltantes(self):
        if self.lam is None or self.mu is None or self.c is None:
            raise ValueError("λ, μ e c devem ser fornecidos")

        self.rho = self.lam / (self.c * self.mu)

        # Probabilidade do sistema ocioso P0
        soma = sum((self.lam / self.mu) ** n / math.factorial(n) for n in range(self.c))
        termo_c = ((self.lam / self.mu) ** self.c) / (math.factorial(self.c) * (1 - self.rho))
        self.P0 = 1 / (soma + termo_c)

        # Lq
        self.Lq = (self.P0 * ((self.lam / self.mu) ** self.c) * self.rho) / (math.factorial(self.c) * (1 - self.rho) ** 2)

        # L
        self.L = self.Lq + self.lam / self.mu

        # Wq e W
        self.Wq = self.Lq / self.lam
        self.W = self.L / self.lam

    def probabilidade_estado_n(self, n=None):
        if n is None:
            n = self.n
        if n is None:
            return None

        if n < self.c:
            return ((self.lam / self.mu) ** n / math.factorial(n)) * self.P0
        else:
            return ((self.lam / self.mu) ** n / (math.factorial(self.c) * self.c ** (n - self.c))) * self.P0

    def resolver(self):
        resultado = {
            "Modelo": "M/M/c",
            "Parâmetros": {
                "λ": self.lam,
                "μ": self.mu,
                "c": self.c,
                "ρ": self.rho
            },
            "Medidas de Efetividade": {
                "L": self.L,
                "Lq": self.Lq,
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
