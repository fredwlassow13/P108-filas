# models/mmsn.py
import math
from typing import Optional, Dict, List

class MMSN:
    """
    M/M/s/N - múltiplos servidores com população finita (fonte finita).
    Estados: n = 0..N (n clientes no sistema).
    Taxa de chegada em estado n: lambda_n = (N - n) * lam
    Taxa de serviço em estado n: mu_n = min(n, s) * mu
    """

    def __init__(
        self,
        lam: float,
        mu: float,
        s: int,
        N: int,
        n: Optional[int] = None,
        r: Optional[int] = None
    ):
        self.lam = float(lam)
        self.mu = float(mu)
        self.s = int(s)
        self.N = int(N)
        self.n = n
        self.r = r

        if self.lam <= 0 or self.mu <= 0:
            raise ValueError("λ e μ devem ser maiores que zero.")
        if self.s < 1:
            raise ValueError("s (número de servidores) deve ser >= 1.")
        if self.N < 0:
            raise ValueError("N deve ser >= 0.")
        if self.N < self.s:
            # ainda é válido ter N < s, interpretamos corretamente (há no máximo N servidores em uso)
            pass

        # resultados
        self.probs: List[float] = []
        self.P0: float = 0.0
        self.PN: float = 0.0
        self.L: float = 0.0
        self.Lq: float = 0.0
        self.lambda_eff: float = 0.0
        self.W: float = 0.0
        self.Wq: float = 0.0
        self.rho: Optional[float] = None

        self._compute_all()

    def _lambda_at(self, n: int) -> float:
        """taxa de chegada em estado n (n clientes presentes)"""
        # chegadas vêm da população restante (N - n) com taxa base lam
        return (self.N - n) * self.lam

    def _mu_at(self, n: int) -> float:
        """taxa total de serviço quando há n clientes"""
        return min(n, self.s) * self.mu

    def _compute_all(self):
        # construir probs iterativamente: p0 = 1 (não normalizado), p_n = p_{n-1} * lambda_{n-1}/mu_n
        raw = [1.0]  # raw[0] = 1
        for n in range(1, self.N + 1):
            lam_prev = self._lambda_at(n - 1)
            mu_n = self._mu_at(n)
            # se mu_n == 0 então não há saída (n=0), mas para n>=1 mu_n>0 pois min(n,s) >=1
            if mu_n == 0:
                raw.append(0.0)
            else:
                raw.append(raw[-1] * (lam_prev / mu_n))

        # normaliza com soma
        ssum = sum(raw)
        if ssum == 0:
            raise ValueError("Soma das probabilidades brutas é zero — verifique parâmetros.")
        self.probs = [r / ssum for r in raw]
        self.P0 = self.probs[0]
        self.PN = self.probs[self.N]

        # L = soma n * p_n
        self.L = sum(n * p for n, p in enumerate(self.probs))

        # Lq = soma (n - s)_+ * p_n
        self.Lq = sum(max(n - self.s, 0) * p for n, p in enumerate(self.probs))

        # taxa de chegada efetiva: lambda_eff = sum_{n=0}^{N-1} lambda_n * p_n
        # mas lambda_n = (N - n) * lam  ==> lambda_eff = lam * sum (N - n) p_n = lam * (N - L)
        self.lambda_eff = self.lam * (self.N - self.L)

        # tempos médios
        if self.lambda_eff > 0:
            self.W = self.L / self.lambda_eff
            self.Wq = self.Lq / self.lambda_eff
        else:
            self.W = 0.0
            self.Wq = 0.0

        # uma medida de 'rho' utilizável: carga por servidor média (usada apenas informativamente)
        # definida como rho = lam * (N - E[n]) / (s * mu) ? aqui colocamos rho instantâneo aproximado:
        try:
            self.rho = (self.lam * (self.N - self.L)) / (self.s * self.mu)
        except Exception:
            self.rho = None

    # métodos de consulta
    def probabilidade_estado_n(self, n: Optional[int] = None) -> float:
        if n is None:
            n = self.n
        if n is None or n < 0 or n > self.N:
            return 0.0
        return float(self.probs[int(n)])

    def taxa_chegada_efetiva(self) -> float:
        return float(self.lambda_eff)

    def probabilidade_sistema_ocioso(self) -> float:
        return float(self.P0)

    def probabilidade_sistema_cheio(self) -> float:
        return float(self.PN)

    def probabilidade_acima_de_r(self, r: Optional[int] = None) -> float:
        if r is None:
            r = self.r
        if r is None:
            return 0.0
        if r < 0:
            return 1.0
        if r >= self.N:
            return 0.0
        return float(sum(self.probs[k] for k in range(r + 1, self.N + 1)))

    def resolver(self) -> Dict:
        resultado = {
            "Modelo": "M/M/s/N",
            "Parâmetros": {
                "λ": self.lam,
                "μ": self.mu,
                "s": self.s,
                "N": self.N,
                "ρ (approx)": self.rho,
                "λ_efetivo": self.lambda_eff
            },
            "Medidas de Efetividade": {
                "L": self.L,
                "Lq": self.Lq,
                "W": self.W,
                "Wq": self.Wq
            },
            "Probabilidades": {
                "P(0)": self.P0,
                f"P({self.N}) (bloqueio)": self.PN
            }
        }

        # adicionar distribuição completa em "Detalhes" (não bugará a exibição principal)
        distrib = {f"P({k})": self.probs[k] for k in range(self.N + 1)}
        resultado["Distribuicao"] = distrib

        # se usuário pediu P(n) particular ou r, adiciona
        if self.n is not None:
            resultado["Probabilidades"][f"P({self.n})"] = self.probabilidade_estado_n(self.n)
        if self.r is not None:
            resultado["Probabilidades"][f"P(n>{self.r})"] = self.probabilidade_acima_de_r(self.r)

        return resultado
