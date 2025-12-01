# main.py — VERSÃO FINAL, COMPLETA E PERFEITA
import streamlit as st
import pandas as pd
from models import (
    MM1, MM1K, MMS, MMSK, MMSN, MM1N,
    MMInfinity, MMC, MG1,
    MPrioridades
)

# ----------------- UTILIDADES -----------------
def safe_float(value):
    try:
        return float(value)
    except Exception:
        return None

def safe_float_fmt(value, fmt="{:.6f}"):
    f = safe_float(value)
    if f is None:
        return str(value)
    try:
        return fmt.format(f)
    except Exception:
        return str(value)

# ========================= CONFIGURAÇÃO =========================
st.set_page_config(page_title="Teoria das Filas", layout="wide")

# ========================= ESTILO PROFISSIONAL =========================
st.markdown("""
<style>
    .param-card {
        background: #1e293b; padding: 20px; border-radius: 14px; text-align: center;
        height: 110px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3); border: 1px solid #334155;
    }
    .param-label { color: #94a3b8; font-size: 15px; margin-bottom: 6px; }
    .param-value { color: #e2e8f0; font-size: 32px; font-weight: bold; margin: 0; }

    .metric-card {
        background: #0f172a; padding: 28px 16px; border-radius: 16px; text-align: center;
        height: 170px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4); border: 1px solid #1e293b;
    }
    .metric-title { color: #94a3b8; font-size: 14px; margin-bottom: 8px; }
    .metric-code  { color: #60a5fa; font-size: 20px; font-weight: bold; margin: 4px 0; }
    .metric-value { color: #22d3ee; font-size: 36px; font-weight: bold; margin: 0; }

    .rho-box {
        background: linear-gradient(90deg, #92400e, #d97706); color: white;
        padding: 16px; border-radius: 12px; text-align: center; font-size: 19px;
        font-weight: 600; margin: 24px 0; box-shadow: 0 4px 12px rgba(217,119,6,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.title("Teoria das Filas")

def num(label, minv=0.0):
    return st.number_input(label, min_value=minv, step=1e-6, format="%.6f")

# ========================= SELEÇÃO DO MODELO =========================
opcao = st.selectbox("Selecione o modelo desejado:", [
    "Selecione",
    "M/M/1",
    "M/M/∞",
    "M/M/C",
    "M/M/s>1",
    "M/M/1/K",
    "M/M/s>1/K",
    "M/M/1/N",
    "M/M/s>1/N",
    "M/G/1",
    "Modelo com prioridades (M/G/1)"
], index=0)

# ========================= VARIÁVEIS =========================
lam = mu = s = K = N = c = sigma2 = None
classes_data = []
prioridade_tipo = None

# ========================= ENTRADA DE DADOS =========================
if opcao in ["M/M/1", "M/M/∞"]:
    col1, col2 = st.columns(2)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")

elif opcao == "M/M/C":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")
    with col3: c   = st.number_input("Número de servidores (c)", min_value=1, step=1)

elif opcao in ["M/M/s>1", "M/M/s>1/K"]:
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")
    with col3: s   = st.number_input("Número de servidores (s)", min_value=2, step=1)
    if opcao == "M/M/s>1/K":
        K = st.number_input("Capacidade do sistema (K)", min_value=s+1, step=1)

elif opcao == "M/M/1/K":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")
    with col3: K   = st.number_input("Capacidade do sistema (K)", min_value=1, step=1)

elif opcao == "M/M/1/N":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")
    with col3: N   = st.number_input("Tamanho da população (N)", min_value=1, step=1)

elif opcao == "M/M/s>1/N":
    col1, col2, col3, col4 = st.columns(4)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu  = num("Taxa de serviço (μ)")
    with col3: s   = st.number_input("Número de servidores (s)", min_value=2, step=1)
    with col4: N   = st.number_input("Tamanho da população (N)", min_value=s, step=1)

elif opcao == "M/G/1":
    col1, col2, col3 = st.columns(3)
    with col1: lam    = num("Taxa de chegada (λ)")
    with col2: mu     = num("Taxa média de serviço (μ)")
    with col3: sigma2 = num("Variância do tempo de serviço (σ²)", minv=0.0)

elif opcao == "Modelo com prioridades (M/G/1)":
    prioridade_tipo = st.selectbox("Tipo de prioridade:", ["Não-preemptiva", "Preemptiva"])
    num_classes = st.number_input("Número de classes de prioridade:", min_value=2, max_value=10, value=2, step=1)

    st.markdown("### Parâmetros por classe (da maior para a menor prioridade)")
    cols = st.columns(3)
    classes_data = []
    for i in range(num_classes):
        with cols[i % 3]:
            st.markdown(f"**Classe {i+1}**")
            lam_i   = num(f"λ da classe {i+1}")
            mu_i    = num(f"μ da classe {i+1}")
            sigma2_i = num(f"σ² da classe {i+1}", minv=0.0)
            classes_data.append({"lam": lam_i, "mu": mu_i, "sigma2": sigma2_i})

# ========================= BOTÃO CALCULAR =========================
if st.button("Calcular", type="primary", use_container_width=True):
    if opcao == "Selecione":
        st.warning("Por favor, selecione um modelo.")
        st.stop()

    try:
        # ==================== CÁLCULO DO MODELO ====================
        if   opcao == "M/M/1":           result = MM1(lam, mu).resolver()
        elif opcao == "M/M/∞":           result = MMInfinity(lam, mu).resolver()
        elif opcao == "M/M/C":           result = MMC(lam, mu, c).resolver()
        elif opcao == "M/M/s>1":         result = MMS(lam, mu, s).resolver()
        elif opcao == "M/M/1/K":         result = MM1K(lam, mu, K).resolver()
        elif opcao == "M/M/s>1/K":       result = MMSK(lam, mu, s, K).resolver()
        elif opcao == "M/M/1/N":         result = MM1N(lam, mu, N).resolver()
        elif opcao == "M/M/s>1/N":       result = MMSN(lam, mu, s, N).resolver()
        elif opcao == "M/G/1":           result = MG1(lam, mu, sigma2).resolver()
        elif opcao == "Modelo com prioridades (M/G/1)":
            preemptive = (prioridade_tipo == "Preemptiva")
            result = MPrioridades(classes_data, preemptive=preemptive).resolver()

        st.markdown("---")
        st.subheader(f"Resultados — {opcao}")

        # ==================== PARÂMETROS DE ENTRADA ====================
        params = result.get("Parâmetros", {})

        # Se o modelo não retornou, reconstruímos manualmente
        if not params:
            params = {"λ": lam, "μ": mu}
            if s is not None: params["s"] = s
            if c is not None: params["c"] = c
            if K is not None: params["K"] = K
            if N is not None: params["N"] = N
            if sigma2 is not None: params["σ²"] = sigma2

        # Prioridades dinâmicas
        if opcao == "Modelo com prioridades (M/G/1)":
            params = {}
            for i, cls in enumerate(classes_data, 1):
                params[f"λ{i}"] = cls["lam"]
                params[f"μ{i}"] = cls["mu"]
                if cls["sigma2"] > 0:
                    params[f"σ²{i}"] = cls["sigma2"]

        # Remove ρ dos parâmetros (vai aparecer destacado)
        rho_val = params.pop("ρ", None)
        if rho_val is None:
            rho_val = result.get("Medidas de Efetividade", {}).get("ρ")

        # Exibe os parâmetros em cards
        st.markdown("**Parâmetros de entrada**")
        cols = st.columns(len(params))
        for (label, valor), col in zip(params.items(), cols):
            with col:
                st.markdown(f"""
                <div class="param-card">
                    <div class="param-label">{label}</div>
                    <div class="param-value">{safe_float_fmt(valor, "{:.6f}")}</div>
                </div>
                """, unsafe_allow_html=True)

        # ρ destacado
        if rho_val is not None:
            st.markdown(f"""
            <div class="rho-box">
                Utilização do sistema: ρ = <b>{safe_float_fmt(rho_val, "{:.4f}")}</b>
            </div>
            """, unsafe_allow_html=True)

        # ==================== MEDIDAS PRINCIPAIS ====================
        medidas = result.get("Medidas de Efetividade", {})
        st.markdown("### Medidas de desempenho (globais)")
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            ("L",  "Número médio no sistema", "L", c1),
            ("Lq", "Número médio na fila",    "Lq", c2),
            ("W",  "Tempo no sistema",        "W", c3),
            ("Wq", "Tempo na fila",           "Wq", c4),
        ]
        for key, texto, codigo, col in cards:
            valor = medidas.get(key, "—")
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{texto}</div>
                    <div class="metric-code">({codigo})</div>
                    <div class="metric-value">{safe_float_fmt(valor, "{:.6f}")}</div>
                </div>
                """, unsafe_allow_html=True)

        # ==================== RESULTADOS POR CLASSE ====================
        if result.get("Resultados por Classe"):
            st.markdown("### Resultados por classe de prioridade")
            df = pd.DataFrame.from_dict(result["Resultados por Classe"], orient="index")
            df = df.applymap(safe_float_fmt)
            st.dataframe(df.style.format("{:.6f}"), use_container_width=True)

        # ==================== PROBABILIDADES ====================
        if result.get("Probabilidades"):
            st.markdown("### Probabilidades do estado do sistema")
            probs = [{"Estado": k, "Probabilidade": safe_float_fmt(v, "{:.6f}")}
                     for k, v in result["Probabilidades"].items()]
            st.dataframe(pd.DataFrame(probs), use_container_width=True, hide_index=True)

        # ==================== DETALHES TÉCNICOS ====================
        outros = {k: v for k, v in result.items()
                  if k not in ["Parâmetros", "Medidas de Efetividade", "Resultados por Classe", "Probabilidades"]}
        if outros:
            with st.expander("Detalhes técnicos avançados"):
                st.json(outros)

        st.caption("Teoria das Filas • Cálculo instantâneo e preciso")

    except Exception as e:
        st.error(f"Erro no cálculo: {e}")
        st.info("Verifique os valores inseridos (ex: ρ < 1, parâmetros positivos, etc).")