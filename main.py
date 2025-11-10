from models import mm1, mm1k, mm_s, mm_s_k, mm_infinity, mm1n

def mostrar_resul(titulo, resul):
    print(f"\n=== {titulo} ===")
    for k, v in resul.items():
        if isinstance(v, float):
            print(f"{k}: {v:.6f}")
        else:
            print(f"{k}: {v}")
def main():
    print("Escolha o modelo de fila:")
    print("1 - M/M/1")
    print("2 - M/M/s")
    print("3 - M/M/∞")
    print("4 - M/M/1/K")
    print("5 - M/M/s/K")
    print("6 - M/M/1/N")

    opcao = int(input("Digite o número do modelo: "))

    lam = float(input("λ (taxa de chegada): "))
    mu = float(input("μ (taxa de serviço): "))

    if opcao == 1:
        resul = ("M/M/1", mm1(lam=lam, mu=mu))
    elif opcao == 2:
        s = int(input("Número de servidores (s): "))
        resul = ("M/M/s", mm_s(lam=lam, mu=mu, s=s))
    elif opcao == 3:
        resul = ("M/M/∞", mm_infinity(lam=lam, mu=mu))
    elif opcao == 4:
        K = int(input("Capacidade máxima do sistema (K): "))
        resul = ("M/M/1/K", mm1k(lam=lam, mu=mu, K=K))
    elif opcao == 5:
        s = int(input("Número de servidores (s): "))
        K = int(input("Capacidade máxima do sistema (K): "))
        resul = ("M/M/s/K", mm_s_k(lam=lam, mu=mu, s=s, K=K))
    elif opcao == 6:
        N = int(input("Número total de clientes (N): "))
        resul = ("M/M/1/N", mm1n(lam=lam, mu=mu, N=N))
    else:
        print("Opção inválida.")
        return

    mostrar_resul(*resul)

if __name__ == "__main__":
    main()