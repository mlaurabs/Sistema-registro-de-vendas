from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = ["createProdutoNoEstoque", "atualizaQtdEstoque", "showEstoque", "getProdutoEstoque", 
           "deleteProdutoEstoque", "limpaEstoque", "geraRelatorioEstoque", "leRelatorioEstoque"]

# Lista global para armazenar os produtos no estoque
estoque = []

def createProdutoNoEstoque(id_produto):
    """
    Adiciona um novo produto ao estoque com quantidade inicial de 0.
    """
    global estoque

    from ..produto.produto import getProdutoById

    # Dicionário para armazenar os dados do produto retornado
    produto = {}

    # Busca o produto no módulo de produtos
    status = getProdutoById(id_produto, produto)
    if status != STATUS_CODE["SUCESSO"]:
        return status  # Retorna o status de erro se o produto não for encontrado

    # Adiciona o produto ao estoque
    estoque.append({
        "id_produto": produto["id"],
        "quantidade": 0  # Inicializa a quantidade no estoque
    })
    return STATUS_CODE["SUCESSO"]  # Retorna sucesso

def atualizaQtdEstoque(id_produto, quantidade):
    """
    Atualiza o estoque de um produto.
    - Adiciona se a quantidade for positiva.
    - Remove se a quantidade for negativa, desde que não deixe o estoque negativo.
    - Retorna erro se o produto não estiver no estoque ou se não houver itens suficientes.
    """
    global estoque

    # Verifica se o produto existe no estoque
    for item in estoque:
        if item["id_produto"] == id_produto:
            if quantidade < 0:  # Remoção de estoque
                if item["quantidade"] == 0:
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]  # Não há itens no estoque para reduzir
                if item["quantidade"] + quantidade < 0:  # Checa se a redução deixa o estoque negativo
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]
            item["quantidade"] += quantidade  # Atualiza a quantidade
            return STATUS_CODE["SUCESSO"]  # Operação bem-sucedida

    return STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

def showEstoque():

    global estoque

    """
    Exibe todos os produtos no estoque.
    """
    if not estoque:
        return STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]

    for item in estoque:
        print(
            f"ID: {item['id_produto']}, "
            f"Quantidade: {item['quantidade']}, "
        )

    return STATUS_CODE["SUCESSO"]

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

    return STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

def deleteProdutoEstoque(id_produto):
    
    global estoque

    for item in estoque:
        if item["id_produto"] == id_produto:
            estoque.remove(item)

    return STATUS_CODE["SUCESSO"]

def limpaEstoque():
    global estoque
    estoque.clear()

# Funções de Relatório

def geraRelatorioEstoque():

    global estoque

    caminho_relativo = Path("dados/estoque/relatorio_estoque_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, produto_estoque in enumerate(estoque):
        string = ""

        for valor in produto_estoque.values():
            string += str(valor) + ','

        if indice != len(estoque)-1:
            string = string[:-1] + '-'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]

def leRelatorioEstoque():

    global estoque

    estoque_template = {"id_produto": None, "quantidade": None}

    caminho_relativo = Path("dados/estoque/relatorio_estoque_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "rb")

    arquivo.read(4)
    conteudo = arquivo.read()
    conteudo = conteudo.decode('utf-32-le')

    conteudo = conteudo.split('-')

    for linha in conteudo:
        if linha:
            
            linha = linha.strip()
            linha = linha.split(',')
            i = 0

            produto_estoque = estoque_template.copy()

            for atributo in estoque.keys():

                produto_estoque[atributo] = linha[i]

            estoque.append(produto_estoque)

    arquivo.close()
    return STATUS_CODE["SUCESSO"]