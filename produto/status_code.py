STATUS_CODE = {
    "SUCESSO": 0, # Sucesso
    "NOME_TIPO_ERRADO": 1, # Um nome deve ser do tipo string
    "MARCA_TIPO_ERRADO": 2, # Uma marca deve ser do tipo string
    "CATEGORIA_TIPO_ERRADO": 3, # Uma categoria deve ser do tipo string
    "PRECO_TIPO_ERRADO": 4, # Um preço deve ser dos tipos int ou float
    "PRECO_PROMOCIONAL_TIPO_ERRADO": 5, # Um preço promocional deve ser dos tipos int ou float
    "QTD_MINIMA_TIPO_ERRADO": 6, # Uma quantidade mínima deve ser do tipo int
    "PARAMETROS_OBRIGATORIOS_NONE": 7, # Nome, marca, categoria, preço e a quantidade mínima não podem ser NULL na criação
    "NOME_FORMATO": 8, # Nome não pode ter mais que 50 caracteres
    "MARCA_FORMATO": 9, # Marca não pode ter mais que 50 caracteres
    "CATEGORIA_FORMATO": 10, # Categoria não pode ter mais que 50 caracteres
    "PRECO_PROMOCIONAL_MAIOR_PRECO": 11, # Preço promocional não pode ser maior que o preço do produto
    "PRECO_FORMATO": 12, # Preço não pode ter mais que duas casas decimais
    "PRECO_PROMOCIONAL_FORMATO": 13, # Preço promocional não pode ter mais que duas casas decimais
    "PRODUTO_EXISTENTE": 14, # Não podem existir produtos iguais no sistema
    "PRODUTO_NAO_ENCONTRADO": 15, # Produto não encontrado
    "NENHUM_PRODUTO_CADASTRADO": 16, # Não há produtos cadastrados
    "NENHUM_PRODUTO_ENCONTRADO": 17, # Nenhum produto encontrado
}

def getStatusName(retorno):
    for nome, valor in STATUS_CODE.items():
        if retorno == valor:
            return nome
    return "Código de status desconhecido"