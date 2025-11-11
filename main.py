import streamlit as st
import pandas as pd
from filas import mm1, mms, mm1_k
import copy

st.set_page_config(
    page_title="Teoria das filas",
    #layout="wide"
)

st.title("⚙️ Teorias")

if "previous_result" not in st.session_state:
    st.session_state.previous_result = None
if "previous_input" not in st.session_state:
    st.session_state.previous_input = {}


def validate_decimal(value):
    return round(value, 2) if value is not None else value

opcao = st.selectbox(
    "Selecione o modelo desejado:",
    ["Selecione", "M/M/1", "M/M/s>1", "M/M/1/K", "M/M/s>1/K", "M/M/1/N", "M/M/s>1/N", "M/G/1", "Modelo com prioridades"]
)

if opcao == "M/M/1":
    st.subheader("Modelo M/M/1")
    num_cols = st.columns(2)
    with num_cols[0]:
        lmbda = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)

    if st.button("Calcular"):
        try:
            L, Lq, W, Wq, P0, rho = mm1(lmbda, mu)

            st.subheader("Respostas:")
            st.write(f"**Taxa de ocupação (ρ):** {rho:.4f}")
            st.write(f"**Probabilidade do sistema estar vazio (P₀):** {P0:.4f}")
            st.write(f"**Número médio de clientes no sistema (L):** {L:.4f}")
            st.write(f"**Número médio de clientes na fila (Lq):** {Lq:.4f}")
            st.write(f"**Tempo médio gasto no sistema por cliente (W):** {W:.4f}")
            st.write(f"**Tempo médio de espera na fila por cliente (Wq):** {Wq:.4f}")

        except ValueError as e:
            st.error(str(e))

if opcao == "M/M/s>1":
    st.subheader("Modelo M/M/s>1")
    num_cols = st.columns(3)
    with num_cols[0]:
        lmbda = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        s = st.number_input("Número de servidores (s)", min_value=1, value=1, step=1)

    if st.button("Calcular"):
        try:
            L, Lq, W, Wq, P0, rho = mms(lmbda, mu, s)

            st.subheader("Respostas:")
            st.write(f"**Taxa de ocupação (ρ):** {rho:.4f}")
            st.write(f"**Probabilidade do sistema estar vazio (P₀):** {P0:.4f}")
            st.write(f"**Número médio de clientes no sistema (L):** {L:.4f}")
            st.write(f"**Número médio de clientes na fila (Lq):** {Lq:.4f}")
            st.write(f"**Tempo médio gasto no sistema por cliente (W):** {W:.4f}")
            st.write(f"**Tempo médio de espera na fila por cliente (Wq):** {Wq:.4f}")

        except ValueError as e:
            st.error(str(e))

if opcao == "M/M/1/K":
    st.subheader("Modelo M/M/1/K")
    num_cols = st.columns(3)
    with num_cols[0]:
        lmbda = st.number_input("Taxa de chegada (λ)", min_value=0.0)
    with num_cols[1]:
        mu = st.number_input("Taxa de serviço (μ)", min_value=0.0)
    with num_cols[2]:
        K = st.number_input("Capacidade máxima do sistema (K)", min_value=1, value=1, step=1)
    
    if st.button("Calcular"):
        try:
            P0, Pn, L, Lq, W, Wq = mm1_k(lmbda, mu, K)

            st.subheader("Respostas:")
            st.write(f"**Probabilidade do sistema estar vazio (P₀):** {P0:.4f}")
            st.write(f"**Distribuição de probabilidade do número de clientes no sistema (Pn):**")
            for n in range(K + 1):
                st.write(f"P({n}) = {Pn[n]:.4f}")
            st.write(f"**Número médio de clientes no sistema (L):** {L:.4f}")
            st.write(f"**Número médio de clientes na fila (Lq):** {Lq:.4f}")
            st.write(f"**Tempo médio gasto no sistema por cliente (W):** {W:.4f}")
            st.write(f"**Tempo médio de espera na fila por cliente (Wq):** {Wq:.4f}")

        except ValueError as e:
            st.error(str(e))
