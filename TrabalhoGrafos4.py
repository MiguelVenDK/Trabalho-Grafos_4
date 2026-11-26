import math


def criar_grafo():
    return {}


def inserir_vertice(grafo, vertice):
    if vertice not in grafo:
        grafo[vertice] = []
        print(f"Vértice '{vertice}' inserido com sucesso.")
    else:
        print(f"O vértice '{vertice}' já existe no grafo.")


def inserir_aresta(grafo, origem, destino, peso=1, nao_direcionado=False):
    if origem not in grafo:
        inserir_vertice(grafo, origem)
    if destino not in grafo:
        inserir_vertice(grafo, destino)

    if not any(v == destino for v, _ in grafo[origem]):
        grafo[origem].append((destino, peso))
        if nao_direcionado and not any(v == origem for v, _ in grafo[destino]):
            grafo[destino].append((origem, peso))
        print(f"Aresta entre {origem} e {destino} (peso {peso}) inserida com sucesso.")
    else:
        print("Essa aresta já existe.")


def vizinhos(grafo, vertice):
    if vertice in grafo:
        return grafo[vertice]
    return []


def listar_vizinhos(grafo, vertice):
    lista = vizinhos(grafo, vertice)
    if vertice in grafo:
        print(f"Vizinhos de {vertice}: {lista}")
    else:
        print("Vértice não encontrado.")


def exibir_grafo(grafo):
    if not grafo:
        print("O grafo está vazio.")
    else:
        print("\n--- Estrutura do Grafo (Lista de Adjacência) ---")
        for vertice in grafo:
            print(f"{vertice} -> {grafo[vertice]}")
        print("-" * 45)


def remover_aresta(grafo, origem, destino, nao_direcionado=False):
    if origem in grafo:
        novos_vizinhos = [(v, p) for v, p in grafo[origem] if v != destino]
        if len(novos_vizinhos) < len(grafo[origem]):
            grafo[origem] = novos_vizinhos
            if nao_direcionado and destino in grafo:
                grafo[destino] = [(v, p) for v, p in grafo[destino] if v != origem]
            print("Aresta removida com sucesso.")
        else:
            print("Aresta não encontrada.")
    else:
        print("Aresta não encontrada.")


def remover_vertice(grafo, vertice, nao_direcionado=True):
    if vertice not in grafo:
        print("Vértice não encontrado.")
        return

    del grafo[vertice]

    for outro in grafo:
        grafo[outro] = [(v, p) for v, p in grafo[outro] if v != vertice]

    print(f"Vértice '{vertice}' e suas conexões foram removidos.")


def existe_aresta(grafo, origem, destino):
    if origem in grafo and any(v == destino for v, _ in grafo[origem]):
        return True
    return False


def grau_vertices(grafo):
    graus = {}
    for vertice in grafo:
        saida = len(grafo[vertice])
        entrada = 0
        for outro in grafo:
            entrada += sum(1 for v, _ in grafo[outro] if v == vertice)
        total = entrada + saida
        graus[vertice] = {"entrada": entrada, "saida": saida, "total": total}
    return graus


def percurso_valido(grafo, caminho):
    if len(caminho) < 2:
        return True

    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i + 1]
        if not existe_aresta(grafo, origem, destino):
            return False
    return True


def dijkstra(grafo, inicio, destino):
    if inicio not in grafo or destino not in grafo:
        return [], math.inf

    
    processados = []

    
    distancias = {v: math.inf for v in grafo}

    
    anterior = {v: None for v in grafo}

    
    distancias[inicio] = 0

    
    while len(processados) < len(grafo):
        
        atual = None
        menor_dist = math.inf
        for v in grafo:
            if v not in processados and distancias[v] < menor_dist:
                menor_dist = distancias[v]
                atual = v

        
        if atual is None or menor_dist == math.inf:
            break

        
        if atual == destino:
            break

        
        processados.append(atual)

        
        for vizinho, peso in vizinhos(grafo, atual):
            if vizinho in processados:
                continue

            
            nova_distancia = distancias[atual] + peso

            
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anterior[vizinho] = atual

    
    if distancias[destino] == math.inf:
        return [], math.inf

    caminho = []
    passo = destino
    while passo is not None:
        caminho.append(passo)
        passo = anterior[passo]
    caminho.reverse()

    return caminho, distancias[destino]


def main():
    grafo = criar_grafo()

    while True:
        print("\n--- MENU DO GRAFO ---")
        print("1. Inserir Vértice")
        print("2. Inserir Aresta")
        print("3. Exibir Grafo")
        print("4. Listar Vizinhos")
        print("5. Verificar Aresta")
        print("6. Calcular Graus")
        print("7. Verificar Percurso")
        print("8. Remover Aresta")
        print("9. Remover Vértice")
        print("10. Menor Caminho (Dijkstra)")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            v = input("Digite o nome do vértice: ")
            inserir_vertice(grafo, v)
        elif opcao == "2":
            origem = input("Vértice de origem: ")
            destino = input("Vértice de destino: ")
            peso_str = input("Peso da aresta (padrão 1): ").strip()
            peso = float(peso_str) if peso_str else 1
            if peso.is_integer():
                peso = int(peso)
            nd = input("O grafo é não direcionado? (s/n): ").lower() == 's'
            inserir_aresta(grafo, origem, destino, peso=peso, nao_direcionado=nd)
        elif opcao == "3":
            exibir_grafo(grafo)
        elif opcao == "4":
            v = input("Digite o vértice: ")
            listar_vizinhos(grafo, v)
        elif opcao == "5":
            origem = input("Origem: ")
            destino = input("Destino: ")
            if existe_aresta(grafo, origem, destino):
                print(f"Sim, existe aresta de {origem} para {destino}.")
            else:
                print(f"Não existe aresta direta de {origem} para {destino}.")
        elif opcao == "6":
            graus = grau_vertices(grafo)
            print("\n--- Graus dos Vértices ---")
            for v, g in graus.items():
                print(f"Vértice {v} -> Entrada: {g['entrada']}, Saída: {g['saida']}, Total: {g['total']}")
            print("-" * 28)
        elif opcao == "7":
            caminho_str = input("Digite o caminho separado por espaços (ex: A B C): ")
            caminho = caminho_str.split()
            if percurso_valido(grafo, caminho):
                print("O percurso é VÁLIDO!")
            else:
                print("O percurso é INVÁLIDO!")
        elif opcao == "8":
            origem = input("Origem da aresta: ")
            destino = input("Destino da aresta: ")
            nd = input("O grafo é não direcionado? (s/n): ").lower() == 's'
            remover_aresta(grafo, origem, destino, nao_direcionado=nd)
        elif opcao == "9":
            v = input("Digite o vértice a ser removido: ")
            remover_vertice(grafo, v)
        elif opcao == "10":
            inicio = input("Vértice de início: ")
            destino = input("Vértice de destino: ")
            caminho, dist = dijkstra(grafo, inicio, destino)
            if caminho:
                print(f"Menor caminho: {' -> '.join(caminho)} | Distância total: {dist}")
            else:
                print("Não existe caminho entre os vértices informados.")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()