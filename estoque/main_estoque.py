from status_codeE import STATUS_CODE
from main_produto import *

# Lista global para armazenar os produtos no estoque
estoque = []

def createProdutoNoEstoque(id_produto):
    """
    Adiciona um novo produto ao estoque com quantidade inicial de 0.
    """
    global estoque

    # Dicionário para armazenar os dados do produto retornado
    produto = {}

    # Busca o produto no módulo de produtos
    status = getProdutoById(id_produto, produto)
    if status != STATUS_CODE["SUCESSO"]:
        return status  # Retorna o status de erro se o produto não for encontrado

    # Adiciona o produto ao estoque
    estoque.append({
        "id_produto": produto["id"],
        "nome": produto["nome"],
        "marca": produto["marca"],
        "categoria": produto["categoria"],
        "preco": produto["preco"],
        "preco_min": produto["preco_promocional"],
        "quantidade_minima": produto["qtd_minima"],
        "quantidade": 0  # Inicializa a quantidade no estoque
    })
    return STATUS_CODE["SUCESSO"]  # Retorna sucesso

def addProdutoEstoque(id_produto, quantidade):
    """
    Atualiza a quantidade de um produto no estoque.
    - Retorna erro se o produto não estiver no estoque.
    - Retorna erro se a quantidade for negativa.
    """
    global estoque

    # Verifica se o produto existe no estoque
    for item in estoque:
        if item["id_produto"] == id_produto:
            if quantidade < 0:
                return STATUS_CODE["QUANTIDADE_NEGATIVA"]  # Erro: Quantidade negativa
            item["quantidade"] += quantidade
            return STATUS_CODE["SUCESSO"]  # Sucesso

    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

def showEstoque():
    """
    Exibe todos os produtos no estoque.
    """
    if not estoque:
        print("Estoque vazio!")
        return

    for item in estoque:
        print(
            f"ID: {item['id_produto']}, Nome: {item['nome']}, Marca: {item['marca']}, "
            f"Categoria: {item['categoria']}, Preço: {item['preco']}, "
            f"Preço Mínimo: {item['preco_min']}, Quantidade: {item['quantidade']}, "
            f"Quantidade Mínima: {item['quantidade_minima']}"
        )


def getProdutoEstoque(id_produto, retorno):
    """
    Busca um produto no estoque pelo ID.
    Atualiza o dicionário 'retorno' com os detalhes do produto, se encontrado.
    """
    global estoque

    # Percorre o estoque para buscar o produto
    for item in estoque:
        if item["id_produto"] == id_produto:
            retorno.update(item)  # Atualiza o dicionário de retorno com os detalhes do produto
            return STATUS_CODE["SUCESSO"]  # Produto encontrado

    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado





# Testando as funções


# Criando produtos para teste
# print("Criando produtos...")
# status = createProduto("Arroz", "Marca A", "Alimentos", 20.0, 15.0, 5)
# if status == STATUS_CODE["SUCESSO"]:
#     print("Produto 'Arroz' criado com sucesso!")
# else:
#     print(f"Erro ao criar produto 'Arroz': {status}")

# status = createProduto("Feijão", "Marca B", "Alimentos", 10.0, 8.0, 10)
# if status == STATUS_CODE["SUCESSO"]:
#     print("Produto 'Feijão' criado com sucesso!")
# else:
#     print(f"Erro ao criar produto 'Feijão': {status}")

# # Exibindo todos os produtos cadastrados
# print("\nProdutos cadastrados:")
# showProdutos()




# if __name__ == "__main__":
#     print("\nCriando produtos no estoque:")
#     status = createProdutoNoEstoque(1)  # Produto ID 1
#     if status == STATUS_CODE["SUCESSO"]:
#         print("Produto 1 adicionado ao estoque com sucesso!")
#     elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
#         print("Erro: Produto 1 não encontrado.")

#     status = createProdutoNoEstoque(3)  # Produto ID 3
#     if status == STATUS_CODE["SUCESSO"]:
#         print("Produto 3 adicionado ao estoque com sucesso!")
#     elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
#         print("Erro: Produto 3 não encontrado.")

#     print("\nExibindo estoque:")
#     showEstoque()

#     print("\nAdicionando 10 unidades ao produto ID 1:")
#     status = addProdutoEstoque(1, 10)
#     if status == STATUS_CODE["SUCESSO"]:
#         print("Quantidade atualizada com sucesso!")
#     elif status == STATUS_CODE["QUANTIDADE_NEGATIVA"]:
#         print("Erro: Quantidade não pode ser negativa.")
#     elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
#         print("Erro: Produto não encontrado.")

#     print("\nExibindo estoque atualizado:")
#     showEstoque()




# if __name__ == "__main__":
#     print("\nTestando a função getProdutoEstoque:")

#     # Criar produtos no estoque
#     createProdutoNoEstoque(1)
#     createProdutoNoEstoque(3)

#     # Teste 1: Produto existente
#     produto_detalhes = {}
#     status = getProdutoEstoque(1, produto_detalhes)
#     if status == STATUS_CODE["SUCESSO"]:
#         print("Produto encontrado:")
#         for atributo, valor in produto_detalhes.items():
#             print(f"{atributo}: {valor}")
#     elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
#         print("Erro: Produto não encontrado.")

#     # Teste 2: Produto inexistente
#     produto_detalhes = {}
#     status = getProdutoEstoque(2, produto_detalhes)
#     if status == STATUS_CODE["SUCESSO"]:
#         print("Produto encontrado:")
#         for atributo, valor in produto_detalhes.items():
#             print(f"{atributo}: {valor}")
#     elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
#         print("Erro: Produto não encontrado.")