import math
from typing import Optional


class MMSK:
    """Modelo M/M/s/K - Múltiplos servidores com capacidade finita"""

    def __init__(self, lambd=None, mi=None, s=None, K=None, rho=None, W=None, Wq=None, L=None, Lq=None, n=None, r=None):
        self.lambd = lambd
        self.mi = mi
        self.s = s
        self.K = K
        self.rho = rho

        self.W = W
        self.Wq = Wq
        self.L = L
        self.Lq = Lq
        self.n = n
        self.r = r

        self.calcular_variaveis_faltantes()

    def calcular_variaveis_faltantes(self):
        if self.lambd is None or self.mi is None or self.s is None or self.K is None:
            raise ValueError("λ, μ, s e K são necessários para M/M/s/K")
        if self.s < 1 or self.K < self.s:
            raise ValueError("K deve ser >= s e s >= 1")

        self.rho = self.lambd / (self.s * self.mi)

        # --- Cálculo de P0
        a = self.lambd / self.mi
        if abs(self.rho - 1) < 1e-12:  # caso ρ = 1
            sum_terms = sum((a ** n) / math.factorial(n) for n in range(self.s))
            tail = (a ** self.s) / math.factorial(self.s) * (self.K - self.s + 1)
            self.P0 = 1 / (sum_terms + tail)
        else:
            sum_terms = sum((a ** n) / math.factorial(n) for n in range(self.s))
            tail = (a ** self.s) / math.factorial(self.s) * (1 - self.rho ** (self.K - self.s + 1)) / (1 - self.rho)
            self.P0 = 1 / (sum_terms + tail)

        # Probabilidades Pn
        self.probs = []
        for n in range(self.K + 1):
            if n < self.s:
                pn = self.P0 * (a ** n) / math.factorial(n)
            else:
                pn = self.P0 * (a ** n) / (math.factorial(self.s) * (self.s ** (n - self.s)))
            self.probs.append(pn)

        self.PK = self.probs[self.K]
        self.lambda_efetivo = self.lambd * (1 - self.PK)

        # Lq
        if abs(self.rho - 1) < 1e-12:
            self.Lq = self.lambda_efetivo * (
                        sum(n * self.probs[n] for n in range(self.K + 1)) / self.lambda_efetivo - 1 / self.mi)
        else:
            self.Lq = (
                    self.P0
                    * (a ** self.s)
                    * self.rho
                    / (math.factorial(self.s) * (1 - self.rho) ** 2)
                    * (1 - self.rho ** (self.K - self.s + 1) - (self.K - self.s + 1) * (1 - self.rho) * self.rho ** (
                        self.K - self.s))
            )

        # L, Wq, W
        self.L = sum(n * self.probs[n] for n in range(self.K + 1))
        self.Wq = self.Lq / self.lambda_efetivo if self.lambda_efetivo > 0 else 0
        self.W = self.Wq + 1 / self.mi if self.mi > 0 else 0

    def probabilidade_estado_n(self, n=None):
        if n is None:
            n = self.n
        if n is None or n < 0 or n > self.K:
            return 0
        return self.probs[int(n)]

    def probabilidade_de_clientes_ser_superior(self, r=None):
        if r is None:
            r = self.r
        if r is None or r >= self.K:
            return 0
        return sum(self.probs[int(n)] for n in range(int(r) + 1, self.K + 1))

    def probabilidade_sistema_ocioso(self):
        return self.P0

    def probabilidade_sistema_cheio(self):
        return self.PK

    def resolver(self):
        resultado = {
            'Modelo': 'M/M/s/K',
            'Parâmetros': {
                'λ': self.lambd,
                'μ': self.mi,
                's': self.s,
                'K': self.K,
                'ρ': self.rho,
                'λ_efetivo': self.lambda_efetivo
            },
            'Medidas de Efetividade': {
                'L': self.L,
                'Lq': self.Lq,
                'W': self.W,
                'Wq': self.Wq
            },
            'Probabilidades': {
                'P(0)': self.P0,
                f'P({self.K})': self.PK
            }
        }

        if self.n is not None:
            resultado['Probabilidades'][f'P({self.n})'] = self.probabilidade_estado_n()

        if self.r is not None:
            resultado['Probabilidades'][f'P(n > {self.r})'] = self.probabilidade_de_clientes_ser_superior()

        return resultado
