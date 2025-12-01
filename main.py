import streamlit as st
from models import MM1, MM1K, MMS, MMSK, MMSN, MM1N, MMInfinity, MMC, MG1, MPrioridades

st.set_page_config(page_title="Teoria das filas")
st.markdown("""
<style>
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Teorias de Filas")

def num(label, default=None, minv=0.0):
    return st.number_input(label, min_value=minv, step=1e-6, format="%.6f", value=default)

if "previous_result" not in st.session_state:
    st.session_state.previous_result = None
if "previous_input" not in st.session_state:
    st.session_state.previous_input = {}

opcao = st.selectbox(
    "Selecione o modelo desejado:",
    [
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
    ]
)

# Inputs comuns
lam = mu = s = K = N = sigma2 = None

if opcao in ["M/M/1", "M/M/∞"]:
    col1, col2 = st.columns(2)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")

elif opcao == "M/M/C":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")
    with col3: c = st.number_input("Número de servidores (C)", min_value=1, step=1)

elif opcao in ["M/M/s>1", "M/M/s>1/K"]:
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")
    with col3: s = st.number_input("Número de servidores (s)", min_value=1, step=1)
    if opcao == "M/M/s>1/K":
        K = st.number_input("Capacidade máxima do sistema (K)", min_value=1, step=1)

elif opcao == "M/M/1/K":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")
    with col3: K = st.number_input("Capacidade máxima do sistema (K)", min_value=1, step=1)

elif opcao == "M/M/1/N":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")
    with col3: N = st.number_input("Tamanho da população (N)", min_value=1, step=1)

elif opcao == "M/M/s>1/N":
    col1, col2, col3, col4 = st.columns(4)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa de serviço (μ)")
    with col3: s = st.number_input("Número de servidores (s)", min_value=1, step=1)
    with col4: N = st.number_input("Tamanho da população (N)", min_value=s, step=1)

elif opcao == "M/G/1":
    col1, col2, col3 = st.columns(3)
    with col1: lam = num("Taxa de chegada (λ)")
    with col2: mu = num("Taxa média de serviço (μ)")
    with col3: sigma2 = num("Variância do tempo de serviço (σ²)", minv=0.0)

elif opcao == "Modelo com prioridades":
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: lam_high = num("Taxa de chegada prioridade alta (λ₁)")
    with col2: lam_low = num("Taxa de chegada prioridade baixa (λ₂)")
    with col3: mu = num("Taxa de serviço (μ)")
    with col4: sigma2 = num("Variância do tempo de serviço (σ²)", minv=0.0)
    with col5: tipo = st.selectbox("Tipo de prioridade", ["Não-preemptiva", "Preemptiva"])

# Botão para calcular
if st.button("Calcular"):
    if opcao == "Selecione":
        st.warning("Por favor, selecione um modelo antes de calcular.")
    else:
        try:
            # Validações básicas
            if opcao in ["M/M/1", "M/M/∞"] and (lam <= 0 or mu <= 0):
                st.error("λ e μ devem ser maiores que zero."); st.stop()
            elif opcao in ["M/M/s>1", "M/M/s>1/K"] and (lam <= 0 or mu <= 0 or s <= 0):
                st.error("λ, μ e s devem ser maiores que zero."); st.stop()
            elif opcao == "M/M/1/K" and (lam <= 0 or mu <= 0 or K <= 0):
                st.error("λ, μ e K devem ser maiores que zero."); st.stop()
            elif opcao == "M/M/C" and (lam <= 0 or mu <= 0 or c <= 0):
                st.error("λ, μ e C devem ser maiores que zero."); st.stop()
            elif opcao == "M/M/1/N" and (lam <= 0 or mu <= 0 or N <= 0):
                st.error("λ, μ e N devem ser maiores que zero."); st.stop()
            elif opcao == "M/M/s>1/N" and (lam <= 0 or mu <= 0 or s <= 0 or N <= 0):
                st.error("λ, μ, s e N devem ser maiores que zero."); st.stop()
            elif opcao == "M/G/1" and (lam <= 0 or mu <= 0 or sigma2 < 0):
                st.error("λ, μ e σ² devem ser válidos."); st.stop()
            elif opcao == "Modelo com prioridades" and (lam_high <= 0 or lam_low <= 0 or mu <= 0):
                st.error("Preencha todos os valores obrigatórios do modelo de prioridades com valores maiores que 0."); st.stop()

            # Criação dos objetos e resolução
            if opcao == "M/M/1": result = MM1(lam, mu).resolver()
            elif opcao == "M/M/s>1": result = MMS(lam, mu, s).resolver()
            elif opcao == "M/M/1/K": result = MM1K(lam, mu, K).resolver()
            elif opcao == "M/M/s>1/K": result = MMSK(lam, mu, s, K).resolver()
            elif opcao == "M/M/∞": result = MMInfinity(lam, mu).resolver()
            elif opcao == "M/M/C": result = MMC(lam, mu, c).resolver()
            elif opcao == "M/M/1/N": result = MM1N(lam, mu, N).resolver()
            elif opcao == "M/M/s>1/N": result = MMSN(lam, mu, s, N).resolver()
            elif opcao == "M/G/1": result = MG1(lam, mu, sigma2).resolver()
            elif opcao == "Modelo com prioridades":
                preemptiva = tipo == "Preemptiva"
                result = MPrioridades(lam_high, lam_low, mu, sigma2, preemptiva=preemptiva).resolver()

            # Exibição padronizada
            st.subheader("Resultados:")
            # Aqui o dicionário result já possui chaves padronizadas: ρ, P0, L, Lq, W, Wq, Pb, PN, etc.
            for key, value in result.items():
                st.write(f"**{key}:** {value:.6f}")

        except Exception as e:
            st.error(f"Ocorreu um erro inesperado no sistema: {e}")
