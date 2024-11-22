__all__ = ["STATUS_CODE", "getStatusName"]

STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    "NOME_TIPO_ERRADO": 1, # Um nome deve ser do tipo string
    "MARCA_TIPO_ERRADO": 2, # Uma marca deve ser do tipo string
    "CATEGORIA_TIPO_ERRADO": 3, # Uma categoria deve ser do tipo string
    "PRECO_TIPO_ERRADO": 4, # Um preço deve ser dos tipos int ou float
    "PRECO_PROMOCIONAL_TIPO_ERRADO": 5, # Um preço promocional deve ser dos tipos int ou float
    "QTD_MINIMA_TIPO_ERRADO": 6, # Uma quantidade mínima deve ser do tipo int
    "NOME_NONE": 7, # Não é possível criar um Produto sem nome
    "MARCA_NONE": 8, # Não é possível criar um Produto sem marca
    "CATEGORIA_NONE": 9, # Não é possível criar um Produto sem categoria
    "PRECO_NONE": 10, # Não é possível criar um Produto sem preço
    "QTD_MINIMA_NONE": 11, # Não é possível criar um Produto sem quantidade mínima
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