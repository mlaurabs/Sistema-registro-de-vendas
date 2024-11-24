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

