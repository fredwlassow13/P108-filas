import streamlit as st
from models import mm1, mms, mm1k, mm1n, mmsn, mg1, priority_queue, mm_infinity, mm_s_k

st.set_page_config(page_title="Teoria das filas")
st.markdown("""
<style>
/* Deixa todos os labels da mesma altura  */
div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    min-height: 45px;   /* ajuste conforme quiser (40–60 funciona bem) */
}
</style>
""", unsafe_allow_html=True)

st.title("⚙️ Teorias de Filas")

# Inicializa session_state
if "previous_result" not in st.session_state:
    st.session_state.previous_result = None
if "previous_input" not in st.session_state:
    st.session_state.previous_input = {}

opcao = st.selectbox(
    "Selecione o modelo desejado:",
    ["Selecione", "M/M/1", "M/M/∞", "M/M/s>1", "M/M/1/K", "M/M/s>1/K", "M/M/1/N", "M/M/s>1/N", "M/G/1", "Modelo com prioridades"]
)
# Inputs comuns
lam = mu = s = K = N = sigma2 = None

if opcao in ["M/M/1", "M/M/∞"]:
    num_cols = st.columns(2)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)

elif opcao in ["M/M/s>1", "M/M/s>1/K"]:
    num_cols = st.columns(4 if opcao == "M/M/s>1/K" else 3)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        s = st.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
    if opcao == "M/M/s>1/K":
        with num_cols[3]:
            K = st.number_input("Capacidade máxima do sistema (K)", min_value=1, value=1, step=1)

elif opcao in ["M/M/1/K"]:
    num_cols = st.columns(3)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        K = st.number_input("Capacidade máxima do sistema (K)", min_value=1, value=1, step=1)

elif opcao == "M/M/1/N":
    num_cols = st.columns(3)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        N = st.number_input("Tamanho da população (N)", min_value=1, value=1, step=1)

elif opcao == "M/M/s>1/N":
    num_cols = st.columns(4)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        s = st.number_input("Número de servidores (s)", min_value=1, value=1, step=1)
    with num_cols[3]:
        N = st.number_input("Tamanho da população (N)", min_value=1, value=1, step=1)

elif opcao == "M/G/1":
    num_cols = st.columns(3)
    with num_cols[0]:
        lam = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa média de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        sigma2 = st.number_input("Variância do tempo de serviço (σ²)", min_value=0.0)

elif opcao == "Modelo com prioridades":
    num_cols = st.columns(4)
    with num_cols[0]:
        lam_high = st.number_input("Taxa de chegada prioridade alta (λ₁)", min_value=0.0)
    with num_cols[1]:
        lam_low = st.number_input("Taxa de chegada prioridade baixa (λ₂)", min_value=0.0)
    with num_cols[2]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[3]:
        tipo = st.selectbox("Tipo de prioridade", ["Não-preemptiva", "Preemptiva"])



# Botão único para calcular
if st.button("Calcular"):
    if opcao == "Selecione":
        st.warning("Por favor, selecione um modelo antes de calcular.")
    else:
        try:
            if opcao in ["M/M/1", "M/M/∞"]:
                if lam <= 0 or mu <= 0:
                    st.error("Preencha todos os valores obrigatórios (λ e μ) com valores maiores que 0.")
                    st.stop()
            elif opcao in ["M/M/s>1", "M/M/s>1/K"]:
                if lam <= 0 or mu <= 0 or s <= 0:
                    st.error("Preencha todos os valores obrigatórios (λ, μ, s) com valores maiores que 0.")
                    st.stop()
            elif opcao in ["M/M/1/K"]:
                if lam <= 0 or mu <= 0 or K <= 0:
                    st.error("Preencha todos os valores obrigatórios (λ, μ, K) com valores maiores que 0.")
                    st.stop()
            elif opcao == "M/M/1/N":
                if lam <= 0 or mu <= 0 or N <= 0:
                    st.error("Preencha todos os valores obrigatórios (λ, μ, N) com valores maiores que 0.")
                    st.stop()
            elif opcao == "M/M/s>1/N":
                if lam <= 0 or mu <= 0 or s <= 0 or N <= 0:
                    st.error("λ, μ, s e N devem ser maiores que zero.")
                    st.stop()
            elif opcao == "M/G/1":
                if lam <= 0 or mu <= 0 or sigma2 < 0:
                    st.error("Preencha todos os valores obrigatórios (λ, μ, σ²) com valores válidos.")
                    st.stop()
            elif opcao == "Modelo com prioridades":
                if lam_high <= 0 or lam_low <= 0 or mu <= 0:
                    st.error("Preencha todos os valores obrigatórios para o modelo de prioridades com valores maiores que 0.")
                    st.stop()

            if opcao == "M/M/1":
                L, Lq, W, Wq, P0, rho = mm1(lam, mu)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {rho:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {P0:.4f}")
                st.write(f"**Número médio no sistema (L):** {L:.4f}")
                st.write(f"**Número médio na fila (Lq):** {Lq:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {W:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {Wq:.4f}")

            elif opcao == "M/M/s>1":
                result = mms(lam, mu, s)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {result['rho']:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {result['P0']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")

            elif opcao == "M/M/1/K":
                result = mm1k(lam, mu, K)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {result['ρ']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {result['P0']:.4f}")
                st.write(f"**Probabilidade de bloqueio (Pb):** {result['Pb']:.4f}")

            elif opcao == "M/M/s>1/K":
                result = mm_s_k(lam, mu, s, K)
                st.subheader("Respostas:")
                if result["aviso"]:
                    st.warning(result["aviso"])
                st.write(f"**Taxa de ocupação (ρ):** {result['ρ']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {result['P0']:.4f}")
                st.write(f"**Probabilidade de bloqueio (Pb):** {result['Pk (bloqueio)']:.4f}")

            elif opcao == "M/M/∞":
                result = mm_infinity(lam, mu)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {result['ρ']:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {result['P0']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")


            elif opcao == "M/M/1/N":
                result = mm1n(lam, mu, N)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {result['ρ']:.4f}")
                st.write(f"**Probabilidade do sistema vazio (P₀):** {result['P0']:.4f}")
                st.write(f"**Probabilidade de bloqueio (PN):** {result['PN (bloqueio)']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")

            elif opcao == "M/M/s>1/N":
                result = mmsn(lam, mu, s, N)
                st.subheader("Respostas:")
                st.write(f"**ρ:** {result['ρ']:.4f}")
                st.write(f"**P₀:** {result['P0']:.4f}")
                st.write(f"**PN:** {result['PN']:.4f}")
                st.write(f"**L:** {result['L']:.4f}")
                st.write(f"**Lq:** {result['Lq']:.4f}")
                st.write(f"**W:** {result['W']:.4f}")
                st.write(f"**Wq:** {result['Wq']:.4f}")

            elif opcao == "M/G/1":
                result = mg1(lam, mu, sigma2)
                st.subheader("Respostas:")
                st.write(f"**Taxa de ocupação (ρ):** {result['ρ']:.4f}")
                st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")

            elif opcao == "Modelo com prioridades":
                try:
                    if tipo == "Não-preemptiva":
                        result = priority_queue.priority_queue_non_preemptive(lam_high, lam_low, mu)
                    else:
                        result = priority_queue.priority_queue_preemptive(lam_high, lam_low, mu)

                    st.subheader("Resultados:")
                    st.write(f"**Taxa de ocupação total (ρ):** {result['rho']:.4f}")
                    st.write(f"**Número médio no sistema (L):** {result['L']:.4f}")
                    st.write(f"**Número médio na fila (Lq):** {result['Lq']:.4f}")
                    st.write(f"**Tempo médio no sistema (W):** {result['W']:.4f}")
                    st.write(f"**Tempo médio na fila (Wq):** {result['Wq']:.4f}")
                    st.write(f"**L_high / L_low:** {result['L_high']:.4f} / {result['L_low']:.4f}")
                    st.write(f"**W_high / W_low:** {result['W_high']:.4f} / {result['W_low']:.4f}")
                except ValueError as e:
                    st.error(str(f"Erro no calculo do modelo com prioridades: {e}"))
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado no sistema: {e}")



