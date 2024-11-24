STATUS_CODE = {
    "SUCESSO": 0,  # Operação realizada com sucesso
    "PRODUTO_NAO_ENCONTRADO": 1,  # Produto não encontrado
    "QUANTIDADE_NEGATIVA": 2,  # Quantidade negativa
}

def getStatusName(codigo):
    """
    Retorna o nome do status code a partir de seu valor numérico.
    """
    for nome, valor in STATUS_CODE.items():
        if codigo == valor:
            return nome
    return "CÓDIGO DESCONHECIDO"
