import math
from typing import Optional


class MMSN:
    """Modelo M/M/s/N - Múltiplos servidores com população finita"""

    def __init__(self, lambd=None, mi=None, s=None, N=None, rho=None, W=None, Wq=None, L=None, Lq=None, n=None):
        self.lambd = lambd
        self.mi = mi
        self.s = s
        self.N = N
        self.rho = rho

        self.W = W
        self.Wq = Wq
        self.L = L
        self.Lq = Lq
        self.n = n

        self.calcular_variaveis_faltantes()

    def calcular_variaveis_faltantes(self):
        if self.lambd is None or self.mi is None or self.s is None or self.N is None:
            raise ValueError("λ, μ, s e N são necessários para M/M/s/N")
        if self.s < 1 or self.N < self.s:
            raise ValueError("N deve ser >= s e s >= 1")

        self.rho = (self.N * self.lambd) / (self.s * self.mi)

        a = self.lambd / self.mi

        # --- P0 ---
        soma = 0
        for n in range(0, self.s):
            soma += math.factorial(self.N) / (math.factorial(self.N - n) * math.factorial(n)) * (a ** n)
        for n in range(self.s, self.N + 1):
            soma += math.factorial(self.N) / (
                        math.factorial(self.N - n) * math.factorial(self.s) * (self.s ** (n - self.s))) * (a ** n)
        self.P0 = 1 / soma

        # --- Probabilidades ---
        self.probs = []
        for n in range(self.N + 1):
            if n < self.s:
                pn = math.factorial(self.N) / (math.factorial(self.N - n) * math.factorial(n)) * (a ** n) * self.P0
            else:
                pn = math.factorial(self.N) / (
                            math.factorial(self.N - n) * math.factorial(self.s) * (self.s ** (n - self.s))) * (
                                 a ** n) * self.P0
            self.probs.append(pn)

        # --- Cálculos de L, Lq ---
        self.L = sum(n * self.probs[n] for n in range(self.N + 1))
        self.Lq = sum(max(n - self.s, 0) * self.probs[n] for n in range(self.N + 1))

        # --- λ efetiva e tempos ---
        self.lambda_efetivo = self.lambd * (self.N - self.L)
        self.Wq = self.Lq / self.lambda_efetivo if self.lambda_efetivo > 0 else 0
        self.W = self.L / self.lambda_efetivo if self.lambda_efetivo > 0 else 0

    def probabilidade_estado_n(self, n=None):
        if n is None:
            n = self.n
        if n is None or n < 0 or n > self.N:
            return 0
        return self.probs[int(n)]

    def taxa_chegada_efetiva(self):
        return self.lambda_efetivo

    def probabilidade_sistema_ocioso(self):
        return self.P0

    def resolver(self):
        resultado = {
            'Modelo': 'M/M/s/N',
            'Parâmetros': {
                'λ': self.lambd,
                'μ': self.mi,
                's': self.s,
                'N': self.N,
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
                'P(0)': self.P0
            }
        }

        if self.n is not None:
            resultado['Probabilidades'][f'P({self.n})'] = self.probabilidade_estado_n()

        return resultado
