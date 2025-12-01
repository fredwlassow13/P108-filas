import streamlit as st
import pandas as pd
from models import MM1, MM1K, MMS, MMSK, MMSN, MM1N, MMInfinity, MMC, MG1, MPrioridades

st.set_page_config(page_title="Teoria das Filas", layout="wide")

st.markdown("""
<style>
    .param-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        border: 1px solid #334155;
    }
    .param-label { color: #94a3b8; font-size: 15px; margin-bottom: 6px; }
    .param-value { color: #e2e8f0; font-size: 32px; font-weight: bold; margin: 0; }

    .metric-card {
        background: #0f172a;
        padding: 28px 16px;
        border-radius: 16px;
        text-align: center;
        height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        border: 1px solid #1e293b;
    }
    .metric-title { color: #94a3b8; font-size: 14px; margin-bottom: 8px; }
    .metric-code  { color: #60a5fa; font-size: 20px; font-weight: bold; margin: 4px 0; }
    .metric-value { color: #22d3ee; font-size: 36px; font-weight: bold; margin: 0; }

    .rho-box {
        background: linear-gradient(90deg, #92400e, #d97706);
        color: white;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        font-size: 19px;
        font-weight: 600;
        margin: 24px 0;
        box-shadow: 0 4px 12px rgba(217,119,6,0.3);
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
    "Modelo com prioridades"
])

lam = mu = s = K = N = c = sigma2 = lam_high = lam_low = tipo = None

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

elif opcao == "Modelo com prioridades":
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: lam_high = num("λ alta prioridade (λ₁)")
    with col2: lam_low  = num("λ baixa prioridade (λ₂)")
    with col3: mu       = num("Taxa de serviço (μ)")
    with col4: sigma2   = num("Variância do serviço (σ²)", minv=0.0)
    with col5: tipo     = st.selectbox("Tipo de prioridade", ["Não-preemptiva", "Preemptiva"])

if st.button("Calcular", type="primary", use_container_width=True):
    if opcao == "Selecione":
        st.warning("Por favor, selecione um modelo.")
        st.stop()

    try:
        # Cálculo do modelo selecionado
        if   opcao == "M/M/1":           result = MM1(lam, mu).resolver()
        elif opcao == "M/M/∞":           result = MMInfinity(lam, mu).resolver()
        elif opcao == "M/M/C":           result = MMC(lam, mu, c).resolver()
        elif opcao == "M/M/s>1":         result = MMS(lam, mu, s).resolver()
        elif opcao == "M/M/1/K":         result = MM1K(lam, mu, K).resolver()
        elif opcao == "M/M/s>1/K":       result = MMSK(lam, mu, s, K).resolver()
        elif opcao == "M/M/1/N":         result = MM1N(lam, mu, N).resolver()
        elif opcao == "M/M/s>1/N":       result = MMSN(lam, mu, s, N).resolver()
        elif opcao == "M/G/1":           result = MG1(lam, mu, sigma2).resolver()
        elif opcao == "Modelo com prioridades":
            result = MPrioridades(lam_high, lam_low, mu, sigma2, preemptiva=(tipo=="Preemptiva")).resolver()

        st.markdown("---")
        st.subheader(f"Resultados — {opcao}")

        # === PARÂMETROS DE ENTRADA ===
        params = result.get("Parâmetros", {"λ": lam, "μ": mu})
        if s is not None: params["s"] = s
        if c is not None: params["c"] = c
        if K is not None: params["K"] = K
        if N is not None: params["N"] = N
        if opcao == "Modelo com prioridades":
            params = {"λ₁": lam_high, "λ₂": lam_low, "μ": mu, "σ²": sigma2}

        rho = params.pop("ρ", result.get("Medidas de Efetividade", {}).get("ρ"))

        st.markdown("**Parâmetros de entrada**")
        cols = st.columns(len(params))
        for (k, v), col in zip(params.items(), cols):
            with col:
                st.markdown(f"""
                <div class="param-card">
                    <div class="param-label">{k}</div>
                    <div class="param-value">{v:.6f}</div>
                </div>
                """, unsafe_allow_html=True)

        if rho is not None:
            st.markdown(f'<div class="rho-box">Taxa de utilização do sistema: ρ = <b>{rho:.4f}</b></div>', unsafe_allow_html=True)

        # === MEDIDAS DE DESEMPENHO (SEMPRE AS 4) ===
        medidas = result.get("Medidas de Efetividade", {})

        st.markdown("**Medidas de desempenho**")
        c1, c2, c3, c4 = st.columns(4)

        cards = [
            ("L",  "Número médio de clientes no sistema", "L", c1),
            ("Lq", "Número médio de clientes na fila",    "Lq", c2),
            ("W",  "Tempo médio no sistema",             "W", c3),
            ("Wq", "Tempo médio na fila",                "Wq", c4),
        ]

        for key, texto, codigo, col in cards:
            valor = medidas.get(key, "—")
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{texto}</div>
                    <div class="metric-code">({codigo})</div>
                    <div class="metric-value">{valor if valor == "—" else f"{valor:.6f}"}</div>
                </div>
                """, unsafe_allow_html=True)

        # === PROBABILIDADES ===
        probs = result.get("Probabilidades", {})
        if probs:
            st.markdown("**Probabilidades do estado do sistema**")
            df = pd.DataFrame([
                {"Estado": k, "Probabilidade": f"{v:.6f}".rstrip("0").rstrip(".")}
                for k, v in probs.items()
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)

        # === OUTROS RESULTADOS ===
        outros = {k: v for k, v in result.items() if k not in ["Parâmetros", "Medidas de Efetividade", "Probabilidades"]}
        if outros:
            with st.expander("Detalhes técnicos adicionais"):
                st.json(outros)

        st.caption("Teoria das Filas • Cálculo instantâneo e preciso")

    except Exception as e:
        st.error(f"Erro no cálculo: {e}")
        st.info("Verifique os valores inseridos e se ρ < 1 quando aplicável.")