__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    "ERRO": 2,
    # Produto
    "PRODUTO_NOME_VAZIO": 9, # Não é possível criar um Produto sem nome
    "PRODUTO_MARCA_VAZIO": 10, # Não é possível criar um Produto sem marca
    "PRODUTO_CATEGORIA_VAZIO": 11, # Não é possível criar um Produto sem categoria
    "PRODUTO_PRECO_VAZIO": 12, # Não é possível criar um Produto sem preço
    "PRODUTO_QTD_MINIMA_VAZIO": 13, # Não é possível criar um Produto sem quantidade mínima
    "PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO": 14, # Preço promocional não pode ser maior que o preço do produto
    "PRODUTO_EXISTENTE": 15, # Não podem existir produtos iguais no sistema
    "PRODUTO_NAO_ENCONTRADO": 16, # Produto não encontrado
    "PRODUTO_NENHUM_CADASTRO": 17, # Não há produtos cadastrados
    "PRODUTO_NENHUM_ENCONTRADO": 18, # Nenhum produto encontrado
    "PRODUTO_NAO_ZERADO_NO_ESTOQUE": 19, # O produto não pode ser removido se ainda houverem unidades em estoque
    "PRODUTO_CADASTRADO_EM_VENDA": 20, # O produto não pode ser removido se estiver cadastrado em alguma venda
    "PRODUTO_NOME_FORMATO_INCORRETO": 100,
    "PRODUTO_MARCA_FORMATO_INCORRETO": 101,
    "PRODUTO_CATEGORIA_FORMATO_INCORRETO": 102,
    "PRODUTO_PRECO_FORMATO_INCORRETO": 103,
    "PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO": 104,
    # Venda
    "VENDA_CPF_FORMATO_INCORRETO": 6,  # CPF não está no formato especificado
    "VENDA_DATA_FORMATO_INCORRETO": 7,  # Data não está no formato especificado
    "VENDA_HORA_FORMATO_INCORRETO": 8,  # Hora não está no formato especificado
    "VENDA_EXISTENTE": 22,  # Venda já existente
    "VENDA_NAO_ENCONTRADA": 24,  # Venda não encontrada  
    "VENDA_JA_CONCLUIDA": 25,  # A venda já foi concluída
    "VENDA_JA_CANCELADA": 81,
    "VENDA_ESTOQUE_INSUFICIENTE": 35,  # Não há unidades suficientes do produto em estoque
    "VENDA_QUANTIDADE_INSUFICIENTE": 124,
    "VENDA_PRODUTO_NAO_INCLUIDO": 87,
    "VENDA_NENHUM_CADASTRO": 502,
    "VENDA_PRODUTO_NAO_ENCONTRADO": 30,  # Produto não encontrado 
    "VENDA_CLIENTE_NAO_ENCONTRADO": 501,
    "VENDA_EM_PROCESSAMENTO": 307,
    "VENDA_PRODUTO_NAO_INCLUSO": 308,
    # Estoque
    "ESTOQUE_INSUFICIENTE": 777,
    "ESTOQUE_PRODUTO_NAO_ENCONTRADO": 778,
    "ESTOQUE_NENHUM_CADASTRO": 779,
    # Cliente
    "CLIENTE_DATA_NASCIMENTO_INVALIDA": 38,
    "CLIENTE_MENOR_DE_IDADE": 39,
    "CLIENTE_CPF_FORMATO_INCORRETO": 40,
    "CLIENTE_NOME_FORMATO_INCORRETO": 41, 
    "CLIENTE_EXISTENTE": 42, 
    "CLIENTE_NAO_ENCONTRADO": 43,
    "CLIENTE_NOME_FORMATO_INCORRETO": 44,
    "CLIENTE_NENHUM_CADASTRADO": 45,
    "CLIENTE_NENHUM_ENCONTRADO": 46,
    "CLIENTE_NAO_ENCONTRADO": 47,
    "CLIENTE_CPF_VAZIO": 48,
    "CLIENTE_NOME_VAZIO": 49,
    "CLIENTE_DATA_NASCIMENTO_VAZIO": 50,
    "CLIENTE_CADASTRADO_EM_VENDA": 51
}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"