__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    # Produto
    "PRODUTO_NOME_VAZIO": 1, # Não é possível criar um Produto sem nome
    "PRODUTO_MARCA_VAZIO": 2, # Não é possível criar um Produto sem marca
    "PRODUTO_CATEGORIA_VAZIO": 3, # Não é possível criar um Produto sem categoria
    "PRODUTO_PRECO_VAZIO": 4, # Não é possível criar um Produto sem preço
    "PRODUTO_QTD_MINIMA_VAZIO": 5, # Não é possível criar um Produto sem quantidade mínima
    "PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO": 6, # Preço promocional não pode ser maior que o preço do produto
    "PRODUTO_EXISTENTE": 7, # Não podem existir produtos iguais no sistema
    "PRODUTO_NAO_ENCONTRADO": 8, # Produto não encontrado
    "PRODUTO_NENHUM_CADASTRO": 9, # Não há produtos cadastrados
    "PRODUTO_NENHUM_ENCONTRADO": 10, # Nenhum produto encontrado
    "PRODUTO_NAO_ZERADO_NO_ESTOQUE": 11, # O produto não pode ser removido se ainda houverem unidades em estoque
    "PRODUTO_CADASTRADO_EM_VENDA": 12, # O produto não pode ser removido se estiver cadastrado em alguma venda
    "PRODUTO_NOME_FORMATO_INCORRETO": 13,
    "PRODUTO_MARCA_FORMATO_INCORRETO": 14,
    "PRODUTO_CATEGORIA_FORMATO_INCORRETO": 15,
    "PRODUTO_PRECO_FORMATO_INCORRETO": 16,
    "PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO": 16,
    # Venda
    "VENDA_CPF_FORMATO_INCORRETO": 17,  # CPF não está no formato especificado
    "VENDA_DATA_FORMATO_INCORRETO": 18,  # Data não está no formato especificado
    "VENDA_HORA_FORMATO_INCORRETO": 19,  # Hora não está no formato especificado
    "VENDA_EXISTENTE": 20,  # Venda já existente
    "VENDA_NAO_ENCONTRADA": 21,  # Venda não encontrada  
    "VENDA_JA_CONCLUIDA": 22,  # A venda já foi concluída
    "VENDA_JA_CANCELADA": 23,
    "VENDA_ESTOQUE_INSUFICIENTE": 24,  # Não há unidades suficientes do produto em estoque
    "VENDA_QUANTIDADE_INSUFICIENTE": 25,
    "VENDA_PRODUTO_NAO_INCLUIDO": 26,
    "VENDA_NENHUM_CADASTRO": 27,
    "VENDA_PRODUTO_NAO_ENCONTRADO": 28,  # Produto não encontrado 
    "VENDA_CLIENTE_NAO_ENCONTRADO": 29,
    "VENDA_EM_PROCESSAMENTO": 30,
    "VENDA_PRODUTO_NAO_INCLUSO": 31,
    # Estoque
    "ESTOQUE_INSUFICIENTE": 32,
    "ESTOQUE_PRODUTO_NAO_ENCONTRADO": 33,
    "ESTOQUE_NENHUM_CADASTRO": 34,
    # Cliente
    "CLIENTE_DATA_NASCIMENTO_INVALIDA": 35,
    "CLIENTE_MENOR_DE_IDADE": 36,
    "CLIENTE_CPF_FORMATO_INCORRETO": 37,
    "CLIENTE_NOME_FORMATO_INCORRETO": 38, 
    "CLIENTE_EXISTENTE": 39, 
    "CLIENTE_NAO_ENCONTRADO": 40,
    "CLIENTE_NOME_FORMATO_INCORRETO": 41,
    "CLIENTE_NENHUM_CADASTRADO": 42,
    "CLIENTE_NENHUM_ENCONTRADO": 43,
    "CLIENTE_NAO_ENCONTRADO": 44,
    "CLIENTE_CPF_VAZIO": 45,
    "CLIENTE_NOME_VAZIO": 46,
    "CLIENTE_DATA_NASCIMENTO_VAZIO": 47,
    "CLIENTE_CADASTRADO_EM_VENDA": 48
}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"