__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    "NOME_VAZIO": 7, # Não é possível criar um Produto sem nome
    "MARCA_VAZIO": 8, # Não é possível criar um Produto sem marca
    "CATEGORIA_VAZIO": 9, # Não é possível criar um Produto sem categoria
    "PRECO_VAZIO": 10, # Não é possível criar um Produto sem preço
    "QTD_MINIMA_VAZIO": 11, # Não é possível criar um Produto sem quantidade mínima
    "NOME_FORMATO": 12, # Nome não pode ter mais que 50 caracteres
    "MARCA_FORMATO": 13, # Marca não pode ter mais que 50 caracteres
    "CATEGORIA_FORMATO": 14, # Categoria não pode ter mais que 50 caracteres
    "PRECO_PROMOCIONAL_MAIOR_PRECO": 15, # Preço promocional não pode ser maior que o preço do produto
    "PRECO_FORMATO": 16, # Preço não pode ter mais que duas casas decimais
    "PRECO_PROMOCIONAL_FORMATO": 17, # Preço promocional não pode ter mais que duas casas decimais
    "PRODUTO_EXISTENTE": 18, # Não podem existir produtos iguais no sistema
    "PRODUTO_NAO_ENCONTRADO": 19, # Produto não encontrado
    "NENHUM_PRODUTO_CADASTRADO": 20, # Não há produtos cadastrados
    "NENHUM_PRODUTO_ENCONTRADO": 21, # Nenhum produto encontrado
}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"