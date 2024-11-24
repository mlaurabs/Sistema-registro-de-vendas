__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    
    # Venda
    "VENDA_CADASTRADA": 0,  # Venda cadastrada com sucesso
    "VENDA_EXISTENTE": 1,  # Venda já existente
    "VENDA_CONCLUIDA": 2,  # Venda concluída com sucesso
    "VENDA_NAO_ENCONTRADA": 3,  # Venda não encontrada
    "VENDA_JA_CONCLUIDA": 4,  # A venda já foi concluída
    "VENDA_CANCELADA": 5,  # A venda foi cancelada
    "VENDA_REMOVIDA": 6, # A venda foi removida
    "VENDA_EXIBIDA": 7,  # Venda exibida com sucesso
    "VENDA_ALTERADA": 8,  # Venda alterada com sucesso

    # Cliente
    "CLIENTE_NAO_ENCONTRADO": 9,  # Cliente não encontrado
    "CLIENTE_ENCONTRADO": 10,  # Cliente encontrado
    
    # Formato
    "CPF_FORMATO_INVALIDO": 11,  # CPF não está no formato especificado
    "DATA_FORMATO_INVALIDO": 12,  # Data não está no formato especificado
    "HORA_FORMATO_INVALIDO": 13,  # Hora não está no formato especificado

    # Produto
    "PRODUTO_ADICIONADO": 14,  # Produto adicionado à venda com sucesso
    "PRODUTO_REMOVIDO": 15,  # Produto removido com sucesso
    "PRODUTO_NAO_ENCONTRADO": 16,  # Produto não encontrado 
    "PRODUTO_ENCONTRADO": 17,  # Produto encontrado
    "PRODUTO_NAO_INCLUIDO": 18,  # Produto não incluído na venda

    # Estoque
    "ESTOQUE_INSUFICIENTE": 19,  # Não há unidades suficientes do produto em estoque
    "PRODUTO_NAO_ENCONTRADO_ESTOQUE": 20,  # Produto não encontrado no estoque  
}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"
