__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    # Formato
    "NOME_FORMATO": 1, # Nome não pode ter mais que 50 caracteres
    "MARCA_FORMATO": 2, # Marca não pode ter mais que 50 caracteres
    "CATEGORIA_FORMATO": 3, # Categoria não pode ter mais que 50 caracteres
    "PRECO_FORMATO": 4, # Preço não pode ter mais que duas casas decimais
    "PRECO_PROMOCIONAL_FORMATO": 5, # Preço promocional não pode ter mais que duas casas decimais
    "CPF_FORMATO_INVALIDO": 6,  # CPF não está no formato especificado
    "DATA_FORMATO_INVALIDO": 7,  # Data não está no formato especificado
    "HORA_FORMATO_INVALIDO": 8,  # Hora não está no formato especificado
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
    "VENDA_CADASTRADA": 21,  # Venda cadastrada com sucesso
    "VENDA_EXISTENTE": 22,  # Venda já existente
    "VENDA_CONCLUIDA": 23,  # Venda concluída com sucesso
    "VENDA_NAO_ENCONTRADA": 24,  # Venda não encontrada
    "VENDA_JA_CONCLUIDA": 25,  # A venda já foi concluída
    "VENDA_CANCELADA": 26,  # A venda foi cancelada
    "VENDA_REMOVIDA": 27, # A venda foi removida
    "VENDA_EXIBIDA": 28,  # Venda exibida com sucesso
    "VENDA_ALTERADA": 29,  # Venda alterada com sucesso
    "PRODUTO_NAO_ENCONTRADO_EM_VENDAS": 30,  # Produto não encontrado 
    "PRODUTO_ENCONTRADO_EM_VENDAS": 31,  # Produto encontrado
    "PRODUTO_NAO_INCLUIDO_EM_VENDAS": 32,  # Produto não incluído na venda
    "CLIENTE_NAO_ENCONTRADO_EM_VENDAS": 33,  # Cliente não encontrado
    "CLIENTE_ENCONTRADO_EM_VENDAS": 34,  # Cliente encontrado
    "ESTOQUE_INSUFICIENTE": 35,  # Não há unidades suficientes do produto em estoque
    # Estoque
    "PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE": 36,  # Produto não encontrado no estoque  
    "QUANTIDADE_NEGATIVA": 37,  # Quantidade negativa
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


}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"