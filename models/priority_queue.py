# models/priority_queue.py
import math
from typing import List, Dict, Optional

class MPrioridades:
    """
    M/G/1 com prioridades (classes ordenadas da mais alta para a mais baixa).
    Recebe lista de classes: cada classe é dict com:
      - 'lam' ou 'lambda' : taxa de chegada
      - 'mu'              : taxa de serviço
      - 'sigma2'          : variância do tempo de serviço
    preemptive = True → preemptive-resume (fórmulas clássicas)
    preemptive = False → non-preemptive (aprox. Kleinrock)

    Toda saída fica normalizada para float.
    """
    def __init__(self, classes: List[Dict[str, float]], preemptive: bool = True):
        if not isinstance(classes, list) or len(classes) == 0:
            raise ValueError("Passe uma lista não-vazia de classes")
        self.raw_classes = classes
        self.preemptive = preemptive
        self._normalize_and_validate()

    def _to_float_safe(self, x, name="value"):
        try:
            if x is None:
                return 0.0
            return float(x)
        except Exception:
            raise ValueError(f"Parâmetro {name} inválido (não numérico): {x!r}")

    def _normalize_and_validate(self):
        self.m = len(self.raw_classes)
        self.lams = []
        self.mus = []
        self.sigma2s = []
        self.ES = []
        self.ES2 = []
        self.rhos = []

        for i, c in enumerate(self.raw_classes):
            lam = self._to_float_safe(c.get("lam", c.get("lambda")), f"λ classe {i+1}")
            mu = self._to_float_safe(c.get("mu"), f"μ classe {i+1}")
            sigma2 = self._to_float_safe(c.get("sigma2", 0.0), f"σ² classe {i+1}")

            if lam < 0 or mu <= 0 or sigma2 < 0:
                raise ValueError(f"Parâmetros inválidos classe {i+1}: λ>=0, μ>0, σ²>=0")

            es = 1 / mu
            es2 = sigma2 + es ** 2
            rho = lam * es

            self.lams.append(lam)
            self.mus.append(mu)
            self.sigma2s.append(sigma2)
            self.ES.append(es)
            self.ES2.append(es2)
            self.rhos.append(rho)

        self.rho_total = sum(self.rhos)
        if self.rho_total >= 1:
            raise ValueError(f"Sistema instável: ρ_total = {self.rho_total:.6f} ≥ 1")

    # -----------------------------------------------------
    # PREEMPTIVE (EXATO)
    # -----------------------------------------------------
    def _preemptive_results(self):
        per_class = {}
        prefix = 0.0  # soma λ_i E[S_i²]

        for i in range(self.m):
            lam_i = self.lams[i]
            es_i = self.ES[i]
            es2_i = self.ES2[i]
            rho_i = self.rhos[i]

            prefix += lam_i * es2_i

            sum_rho_before = sum(self.rhos[:i])
            sum_rho_upto = sum(self.rhos[:i+1])

            denom = 2.0 * (1.0 - sum_rho_before) * (1.0 - sum_rho_upto)
            if denom <= 0:
                raise ValueError(f"Estabilidade numérica violada na classe {i+1}.")

            W_i = prefix / denom
            Wq_i = max(W_i - es_i, 0.0)
            L_i = lam_i * W_i
            Lq_i = lam_i * Wq_i

            per_class[i+1] = {
                "λ": lam_i,
                "μ": self.mus[i],
                "σ²": self.sigma2s[i],
                "ρ": rho_i,
                "E[S]": es_i,
                "E[S²]": es2_i,
                "W": W_i,
                "Wq": Wq_i,
                "L": L_i,
                "Lq": Lq_i,
            }

        totals = {
            "ρ_total": self.rho_total,
            "L": sum(c["L"] for c in per_class.values()),
            "Lq": sum(c["Lq"] for c in per_class.values()),
            "W": sum(self.lams[i] * per_class[i+1]["W"] for i in range(self.m)) / sum(self.lams),
            "Wq": sum(self.lams[i] * per_class[i+1]["Wq"] for i in range(self.m)) / sum(self.lams),
        }

        return {"per_class": per_class, "totals": totals}

    # -----------------------------------------------------
    # NON-PREEMPTIVE (APROX. KLEINROCK)
    # -----------------------------------------------------
    def _non_preemptive_approx(self):
        per_class = {}
        lambda_total = sum(self.lams)
        sum_lambda_es2 = sum(self.lams[i] * self.ES2[i] for i in range(self.m))

        for i in range(self.m):
            lam_i = self.lams[i]
            es_i = self.ES[i]
            es2_i = self.ES2[i]

            rho_upto = sum(self.rhos[:i+1])
            if rho_upto >= 1:
                raise ValueError(f"Instabilidade parcial até classe {i+1}")

            base = sum_lambda_es2 / (2 * (1 - self.rho_total))
            Wq_i = base / (1 - rho_upto)
            W_i = Wq_i + es_i
            Lq_i = lam_i * Wq_i
            L_i = lam_i * W_i

            per_class[i+1] = {
                "λ": lam_i,
                "μ": self.mus[i],
                "σ²": self.sigma2s[i],
                "ρ": self.rhos[i],
                "E[S]": es_i,
                "E[S²]": es2_i,
                "W": W_i,
                "Wq": Wq_i,
                "L": L_i,
                "Lq": Lq_i,
            }

        totals = {
            "ρ_total": self.rho_total,
            "L": sum(c["L"] for c in per_class.values()),
            "Lq": sum(c["Lq"] for c in per_class.values()),
            "W": sum(self.lams[i] * per_class[i+1]["W"] for i in range(self.m)) / lambda_total,
            "Wq": sum(self.lams[i] * per_class[i+1]["Wq"] for i in range(self.m)) / lambda_total,
        }

        return {"per_class": per_class, "totals": totals, "aviso": "Aproximação non-preemptive (Kleinrock)"}

    # -----------------------------------------------------
    # RESOLVER (PRINCIPAL)
    # -----------------------------------------------------
    def calcular(self):
        if self.preemptive:
            return self._preemptive_results()
        return self._non_preemptive_approx()

    def resolver(self):
        out = self.calcular()

        medidas = {
            "L": float(out["totals"]["L"]),
            "Lq": float(out["totals"]["Lq"]),
            "W": float(out["totals"]["W"]),
            "Wq": float(out["totals"]["Wq"]),
            "ρ": float(out["totals"]["ρ_total"]),
        }

        probabilidades = {
            "P(0)": float(max(0.0, 1 - out["totals"]["ρ_total"])),
            "ρ_total": float(out["totals"]["ρ_total"]),
        }

        return {
            "Modelo": "M/G/1 com prioridades (preemptive)" if self.preemptive else "M/G/1 com prioridades (non-preemptive, approx)",
            "Parâmetros": {
                "classes": [
                    {"λ": float(self.lams[i]), "μ": float(self.mus[i]), "σ²": float(self.sigma2s[i]), "ρ": float(self.rhos[i])}
                    for i in range(self.m)
                ],
            },
            "Medidas de Efetividade": medidas,
            "Probabilidades": probabilidades,
            "Resultados por Classe": out["per_class"],
            **({"aviso": out.get("aviso")} if out.get("aviso") else {})
        }
