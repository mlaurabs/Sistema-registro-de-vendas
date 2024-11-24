from status_codeP import STATUS_CODE
from main_produto import *
from main_estoque import *

def testar_estoque():
    print("Iniciando testes de funcionalidades do módulo de estoque...\n")

    # Passo 1: Criar produtos no módulo de produtos
    print("1. Criando produtos no módulo de produtos:")
    status = createProduto("Arroz", "Marca A", "Alimentos", 20.0, 15.0, 5)
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto 'Arroz' criado com sucesso!")
    else:
        print(f"Erro ao criar produto 'Arroz': {status}")

    status = createProduto("Feijão", "Marca B", "Alimentos", 10.0, 8.0, 10)
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto 'Feijão' criado com sucesso!")
    else:
        print(f"Erro ao criar produto 'Feijão': {status}")

    print("\nProdutos cadastrados no sistema:")
    showProdutos()

    # Passo 2: Adicionar produtos ao estoque
    print("\n2. Adicionando produtos ao estoque:")
    status = createProdutoNoEstoque(1)  # Adiciona o produto com ID 1
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto com ID 1 adicionado ao estoque com sucesso!")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto com ID 1 não encontrado.")

    status = createProdutoNoEstoque(2)  # Adiciona o produto com ID 2
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto com ID 2 adicionado ao estoque com sucesso!")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto com ID 2 não encontrado.")

    print("\nEstoque inicial:")
    showEstoque()

    # Passo 3: Atualizar a quantidade de produtos no estoque
    print("\n3. Atualizando quantidades no estoque:")
    status = addProdutoEstoque(1, 10)
    if status == STATUS_CODE["SUCESSO"]:
        print("Quantidade do produto com ID 1 atualizada com sucesso!")
    elif status == STATUS_CODE["QUANTIDADE_NEGATIVA"]:
        print("Erro: Quantidade não pode ser negativa.")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto não encontrado.")

    status = addProdutoEstoque(2, 15)
    if status == STATUS_CODE["SUCESSO"]:
        print("Quantidade do produto com ID 2 atualizada com sucesso!")
    elif status == STATUS_CODE["QUANTIDADE_NEGATIVA"]:
        print("Erro: Quantidade não pode ser negativa.")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto não encontrado.")

    print("\nEstoque atualizado:")
    showEstoque()

    # Passo 4: Buscar detalhes de um produto específico no estoque
    print("\n4. Buscando detalhes de produtos no estoque:")
    produto_detalhes = {}
    status = getProdutoEstoque(1, produto_detalhes)
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto com ID 1 encontrado:")
        for atributo, valor in produto_detalhes.items():
            print(f"{atributo}: {valor}")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto com ID 1 não encontrado.")

    produto_detalhes = {}
    status = getProdutoEstoque(3, produto_detalhes)  # Produto inexistente
    if status == STATUS_CODE["SUCESSO"]:
        print("Produto com ID 3 encontrado:")
        for atributo, valor in produto_detalhes.items():
            print(f"{atributo}: {valor}")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        print("Erro: Produto com ID 3 não encontrado.")

    print("\nTestes concluídos.")

# Executando o caso de teste completo
if __name__ == "__main__":
    testar_estoque()
