from status_code import STATUS_CODE

__all__ = ["createProduto", "showProdutoById", "showProdutoByNome", "updateProduto", "getProdutoById", "getProdutoByNome", "showProdutos", "showProdutosByMarca", "showProdutosByCategoria", "showProdutosByFaixaPreco", "showProdutosByNome", "deleteProduto"]

cont_id = 1 # Guarda o próximo ID a ser cadastrado
lista_produtos = [] # Lista com todos os produtos

# Conta se um valor tem a quantidade de casas decimais desejadas
def contaCasasDecimais(valor, casas_desejadas):
    str_valor = str(valor)
    if '.' in str_valor:
        str_valor = str_valor.split('.')
        if len(str_valor[1]) > casas_desejadas:
            return True # Preço não pode ter mais que 2 casas decimais
    return False

# Valida os valores passados para a função create
def validaCreate(funcao):

    def valida(nome, marca, categoria, preco, preco_promocional, qtd_minima):

        global lista_produtos

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "qtd_minima": qtd_minima}

        for atributo, valor in parametros.items():
            if valor == "" or valor == -1:
                atributo = atributo.upper()
                erro = atributo + "_VAZIO"
                return STATUS_CODE[erro] # O valor não pode ser nulo

        if len(nome) > 50:
            return STATUS_CODE["NOME_FORMATO"] # Nome não pode ter mais que 50 caracteres

        if len(marca) > 50:
            return STATUS_CODE["MARCA_FORMATO"] # Marca não pode ter mais que 50 caracteres

        if len(categoria) > 50:
            return STATUS_CODE["CATEGORIA_FORMATO"] # Categoria não pode ter mais que 50 caracteres

        if contaCasasDecimais(preco, 2):
            return STATUS_CODE["PRECO_FORMATO"] # Preço não pode ter mais que duas casas decimais

        if contaCasasDecimais(preco_promocional, 2):
            return STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"] # Preço promocional não pode ter mais que duas casas decimais

        if preco_promocional > preco:
            return STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"] # Preço promocional não pode ser maior que o preço do produto

        for produto in lista_produtos:
            if nome == produto["nome"] and marca == produto["marca"] and categoria == produto["categoria"]:
                return STATUS_CODE["PRODUTO_EXISTENTE"] # Não podem existir produtos iguais no sistema

        return funcao(nome, marca, categoria, preco, preco_promocional, qtd_minima)

    return valida

# Cria um produto
@validaCreate
def createProduto(nome, marca, categoria, preco, preco_promocional, qtd_minima):

    global lista_produtos, cont_id

    if preco_promocional == -1:
        preco_promocional = preco

    produto ={
        "id": cont_id,
        "nome": nome,
        "marca": marca,
        "categoria": categoria,
        "preco": preco,
        "preco_promocional": preco_promocional,
        "qtd_minima": qtd_minima,
    }

    lista_produtos.append(produto)
    cont_id += 1

    return STATUS_CODE["SUCESSO"] # Sucesso

# Imprime um produto pelo id
def showProdutoById(id):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            for atributo,valor in produto.items():
                print(f"{atributo}: {valor}")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Imprime um produto pelo nome
def showProdutoByNome(nome):

    global lista_produtos

    for produto in lista_produtos:
        if nome == produto["nome"]:
            for atributo,valor in produto.items():
                print(f"{atributo}: {valor}")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Atualiza um produto
def updateProduto(id, nome, marca, categoria, preco, preco_promocional):

    global lista_produtos

    parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "preco_promocional": preco_promocional}

    for produto in lista_produtos:
        if id == produto["id"]:
            for parametro_atributo, parametro_valor in parametros.items():
                if parametro_valor != "":
                    if produto[parametro_atributo] != parametro_valor:
                        produto[parametro_atributo] = parametro_valor
                        if parametro_atributo == "preco":
                            produto["preco_promocional"] = parametro_valor
                # Retornar que não pode ser vazio
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Retorna um produto pelo id
def getProdutoById(id, retorno):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            retorno.update(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # produto não encontrado

# Retorna um produto pelo nome
def getProdutoByNome(nome, retorno):

    global lista_produtos

    for produto in lista_produtos:
        if nome == produto["nome"]:
            retorno.update(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # produto não encontrado

# Mostra todos os produtos cadastrados
def showProdutos():

    global lista_produtos

    if not lista_produtos:
        return STATUS_CODE["NENHUM_PRODUTO_CADASTRADO"] # Não há produtos cadastrados

    for produto in lista_produtos:
        for atributo, valor in produto.items():
            print(f"{atributo}: {valor}")
        print("\n", end="")

    return STATUS_CODE["SUCESSO"] # Sucesso

# Mostra todos os produtos de certa marca
def showProdutosByMarca(marca):

    global lista_produtos
    flag = False

    for produto in lista_produtos:
        if marca == produto["marca"]:
            flag = True
            for atributo, valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

# Mostra todos os produtos de certa categoria
def showProdutosByCategoria(categoria):

    global lista_produtos
    flag = False

    for produto in lista_produtos:
        if categoria == produto["categoria"]:
            flag = True
            for atributo, valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

# Mostra todos os produtos em certa faixa de preço
def showProdutosByFaixaPreco(preco_min, preco_max):

    global lista_produtos
    flag = False

    for produto in lista_produtos:
        if produto["preco_promocional"] >= preco_min and produto["preco_promocional"] <= preco_max:
            flag = True
            for atributo, valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

# Mostra todos os produtos com certo nome
def showProdutosByNome(nome):

    global lista_produtos
    flag = False
    
    for produto in lista_produtos:
        if nome in produto["nome"]:
            flag = True
            for atributo, valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

# Deleta um produto
def deleteProduto(id):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            # Conferir se não está cadastrado em nenhuma venda
            # Conferir se não há produtos em estoque
            # Retornar erro nesses casos
            lista_produtos.remove(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Produto não encontrado