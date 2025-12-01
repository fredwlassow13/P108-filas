import math
from typing import Optional


class MMS:
    """Modelo M/M/s - Fila múltipla, população infinita"""

    def __init__(self, lambd=None, mi=None, s=None, rho=None, W=None, Wq=None, L=None, Lq=None, n=None, t_sistema=None,
                 t_fila=None, r=None):
        self.lambd = lambd
        self.mi = mi
        self.s = s
        self.rho = rho

        self.W = W
        self.Wq = Wq
        self.L = L
        self.Lq = Lq
        self.n = n
        self.t_sistema = t_sistema
        self.t_fila = t_fila
        self.r = r

        self.calcular_variaveis_faltantes()

    def calcular_variaveis_faltantes(self):
        if self.lambd is None or self.mi is None or self.s is None:
            raise ValueError("λ, μ e s são necessários para calcular o modelo M/M/s")
        if self.s < 2:
            raise ValueError("Use s >= 2 para o modelo M/M/s>1")

        self.rho = self.lambd / (self.s * self.mi)
        if self.rho >= 1:
            raise ValueError("Sistema instável: λ ≥ s·μ")

        # P0
        soma = sum((self.lambd / self.mi) ** n / math.factorial(n) for n in range(self.s))
        termo = ((self.lambd / self.mi) ** self.s) / (math.factorial(self.s) * (1 - self.rho))
        self.P0 = 1 / (soma + termo)

        # Lq
        self.Lq = (self.P0 * (self.lambd / self.mi) ** self.s * self.rho) / (
                    math.factorial(self.s) * (1 - self.rho) ** 2)

        # L, Wq, W
        self.L = self.Lq + (self.lambd / self.mi)
        self.Wq = self.Lq / self.lambd
        self.W = self.Wq + (1 / self.mi)

    def probabilidade_estado_n(self, n=None):
        if n is None:
            n = self.n
        if n is None:
            return 0
        P0 = self.P0
        if n < self.s:
            return ((self.lambd / self.mi) ** n / math.factorial(n)) * P0
        else:
            denominador = math.factorial(self.s) * (self.s ** (n - self.s))
            return ((self.lambd / self.mi) ** n / denominador) * P0

    def probabilidade_de_clientes_ser_superior(self, r=None):
        if r is None:
            r = self.r
        if r is None:
            return 0

        P0 = self.P0
        if r < self.s - 1:
            prob_acum = sum(self.probabilidade_estado_n(k) for k in range(r + 1))
            return 1 - prob_acum
        else:
            numerador = (self.s * self.rho) ** self.s
            denominador = math.factorial(self.s) * (1 - self.rho)
            return (numerador / denominador) * (self.rho ** (r + 1 - self.s)) * P0

    def probabilidade_sistema_ocioso(self):
        return self.P0

    def probabilidade_sistema_ocupado(self):
        return 1 - self.P0

    def resolver(self):
        resultado = {
            'Modelo': f'M/M/s>1',
            'Parâmetros': {
                'λ': self.lambd,
                'μ': self.mi,
                's': self.s,
                'ρ': self.rho
            },
            'Medidas de Efetividade': {
                'L': self.L,
                'Lq': self.Lq,
                'W': self.W,
                'Wq': self.Wq
            },
            'Probabilidades': {
                'P(0)': self.probabilidade_sistema_ocioso(),
                'P(ocupado)': self.probabilidade_sistema_ocupado()
            }
        }

        if self.n is not None:
            resultado['Probabilidades'][f'P({self.n})'] = self.probabilidade_estado_n()

        if self.r is not None:
            resultado['Probabilidades'][f'P(n > {self.r})'] = self.probabilidade_de_clientes_ser_superior()
            resultado['Probabilidades'][f'P(n < {self.r})'] = 1 - self.probabilidade_de_clientes_ser_superior()

        return resultado
