import math
from typing import List, Optional

class MPrioridades:
    """Fila de prioridade com múltiplas classes, preemptive ou non-preemptive"""
    def __init__(self, lambda_list: List[float], mu: float, s: int = 1, com_interrupcao: bool = False):
        """
        lambda_list: lista de taxas de chegada por classe, ordem da maior para menor prioridade
        mu: taxa de serviço
        s: número de servidores
        com_interrupcao: True para preemptive, False para non-preemptive
        """
        self.lambda_list = lambda_list
        self.mu = mu
        self.s = s
        self.com_interrupcao = com_interrupcao

        self.resultados = {}

    def calcular(self):
        if self.com_interrupcao:
            return self._calcular_preemptive()
        else:
            return self._calcular_non_preemptive()

    def _calcular_preemptive(self):
        resultados = {}
        rho_list = []
        L_list = []
        Lq_list = []
        W_list = []
        Wq_list = []

        rho_acum = 0
        for i, lam in enumerate(self.lambda_list):
            rho_i = lam / self.mu
            rho_acum += rho_i
            if rho_acum >= 1:
                raise ValueError(f"Sistema instável: ρ total ≥ 1 após classe {i+1}")

            # alta prioridade
            L_i = rho_i / (1 - rho_acum + rho_i)
            Lq_i = L_i - rho_i
            W_i = L_i / lam if lam > 0 else 0
            Wq_i = Lq_i / lam if lam > 0 else 0

            rho_list.append(rho_i)
            L_list.append(L_i)
            Lq_list.append(Lq_i)
            W_list.append(W_i)
            Wq_list.append(Wq_i)

            resultados[i+1] = {"λ": lam, "L": L_i, "Lq": Lq_i, "W": W_i, "Wq": Wq_i, "ρ": rho_i}

        # Sistema total
        lambda_total = sum(self.lambda_list)
        L_total = sum(L_list)
        Lq_total = sum(Lq_list)
        W_total = sum(lam * W for lam, W in zip(self.lambda_list, W_list)) / lambda_total
        Wq_total = sum(lam * Wq for lam, Wq in zip(self.lambda_list, Wq_list)) / lambda_total
        rho_total = sum(rho_list)

        resultados["sistema"] = {
            "ρ": rho_total,
            "L": L_total,
            "Lq": Lq_total,
            "W": W_total,
            "Wq": Wq_total
        }

        return resultados

    def _calcular_non_preemptive(self):
        # Para non-preemptive, usamos aproximação de duas classes
        if len(self.lambda_list) < 2:
            self.lambda_list += [0] * (2 - len(self.lambda_list))  # garante duas classes

        lam_high, lam_low = self.lambda_list[:2]
        rho_high = lam_high / self.mu
        rho_low = lam_low / self.mu
        rho_total = rho_high + rho_low

        if rho_total >= 1:
            raise ValueError("Sistema instável (ρ ≥ 1)")

        # Média no sistema
        L_high = rho_high / (1 - rho_total)
        L_low = (rho_low * (1 + rho_high)) / (1 - rho_total)
        L = L_high + L_low

        # Média na fila
        Lq_high = rho_high ** 2 / (1 - rho_total)
        Lq_low = (rho_low ** 2 + 2 * rho_high * rho_low) / (1 - rho_total)
        Lq = Lq_high + Lq_low

        # Tempos
        W_high = L_high / lam_high if lam_high > 0 else 0
        W_low = L_low / lam_low if lam_low > 0 else 0
        W = (lam_high * W_high + lam_low * W_low) / (lam_high + lam_low)
        Wq_high = Lq_high / lam_high if lam_high > 0 else 0
        Wq_low = Lq_low / lam_low if lam_low > 0 else 0
        Wq = (lam_high * Wq_high + lam_low * Wq_low) / (lam_high + lam_low)

        resultados = {
            1: {"λ": lam_high, "L": L_high, "Lq": Lq_high, "W": W_high, "Wq": Wq_high, "ρ": rho_high},
            2: {"λ": lam_low, "L": L_low, "Lq": Lq_low, "W": W_low, "Wq": Wq_low, "ρ": rho_low},
            "sistema": {"ρ": rho_total, "L": L, "Lq": Lq, "W": W, "Wq": Wq}
        }

        return resultados

    def resolver(self):
        self.resultados = self.calcular()
        return {
            "Modelo": f"Prioridade {'com' if self.com_interrupcao else 'sem'} interrupção",
            "Medidas de Efetividade": self.resultados["sistema"],
            "Resultados por Classe": {k: v for k, v in self.resultados.items() if k != "sistema"}
        }
