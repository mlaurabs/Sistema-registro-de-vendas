from src.status_code import STATUS_CODE
from pathlib import Path
import sys

caminho_relativo = Path("src/entidades/produto/produto.py")
caminho_absoluto = caminho_relativo.resolve()

sys.path.append(caminho_absoluto.parent)

# Agora você pode importar o módulo estoque
from entidades.estoque.estoque import createProdutoNoEstoque, getProdutoEstoque
from entidades.venda.venda import checkProdutoVenda

__all__ = ["createProduto", "showProdutoById", "showProdutoByNome", "updateProduto", "getProdutoById", "getProdutoByNome", "showProdutos", "showProdutosByMarca", "showProdutosByCategoria", "showProdutosByFaixaPreco", "showProdutosByNome", "deleteProduto", "geraRelatorioProduto", "leRelatorioProduto"]

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

    # createProdutoNoEstoque(produto["id"])

    return STATUS_CODE["SUCESSO"] # Sucesso

# Imprime um produto pelo id
def showProdutoById(id):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            print("\n", end="")
            for atributo,valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Imprime um produto pelo nome
def showProdutoByNome(nome):

    global lista_produtos

    for produto in lista_produtos:
        if nome == produto["nome"]:
            print("\n", end="")
            for atributo,valor in produto.items():
                print(f"{atributo}: {valor}")
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Valida os valores passados para a função update
def validaUpdate(funcao):

    def valida(id, nome, marca, categoria, preco, preco_promocional):

        global lista_produtos
            
        if nome != "" and len(nome) > 50:
            return STATUS_CODE["NOME_FORMATO"] # Nome não pode ter mais que 50 caracteres

        if marca != "" and len(marca) > 50:
            return STATUS_CODE["MARCA_FORMATO"] # Marca não pode ter mais que 50 caracteres

        if categoria != "" and len(categoria) > 50:
            return STATUS_CODE["CATEGORIA_FORMATO"] # Categoria não pode ter mais que 50 caracteres

        if preco != -1 and contaCasasDecimais(preco, 2):
            return STATUS_CODE["PRECO_FORMATO"] # Preço não pode ter mais que duas casas decimais

        if preco_promocional != -1 and contaCasasDecimais(preco_promocional, 2):
            return STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"] # Preço promocional não pode ter mais que duas casas decimais
        
        return funcao(id, nome, marca, categoria, preco, preco_promocional)
    
    return valida

# Atualiza um produto
@validaUpdate
def updateProduto(id, nome, marca, categoria, preco, preco_promocional):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:

            if nome != "":
                produto["nome"] = nome

            if marca != "":
                produto["marca"] = marca

            if categoria != "":
                produto["categoria"] = marca

            if preco != -1:
                if preco < produto["preco_promocional"] and preco_promocional == -1:
                    return STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
                elif preco_promocional != -1 and preco < preco_promocional:
                    return STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
                else:
                    produto["preco"] = preco

            if preco_promocional != -1:
                if preco_promocional > produto["preco"]:
                    return STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
                else:
                    produto["preco_promocional"] = preco_promocional      

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
        print("\n", end="")
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
            print("\n", end="")
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
            print("\n", end="")
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
            print("\n", end="")
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
        if nome.upper() in produto["nome"].upper():
            flag = True
            print("\n", end="")
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
            
            '''
            estoque = dict()
            flag = getProdutoEstoque(produto["id"], estoque)

            if flag != STATUS_CODE["SUCESSO"]:
                return flag
            
            if estoque["quantidade"] != 0:
                return STATUS_CODE["PRODUTO_NAO_ZERADO_NO_ESTOQUE"]
            
            flag = checkProdutoVenda(produto["id"])

            if flag == STATUS_CODE["PRODUTO_ENCONTRADO"]:
                return STATUS_CODE["PRODUTO_CADASTRADO_EM_VENDA"]
            '''

            lista_produtos.remove(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

# Gera um relatório com todos os produtos
def geraRelatorioProduto():

    global lista_produtos

    caminho_relativo = Path("dados/produtos/relatorio_produto_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, produto in enumerate(lista_produtos):
        string = ""

        for valor in produto.values():
            string += str(valor) + ','

        if indice != len(lista_produtos)-1:
            string = string[:-1] + '-'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]

# Lê um relatório com todos os produtos e os cadastra no sistema
def leRelatorioProduto():

    global lista_produtos, cont_id

    produto_template = {"id": None, "nome": None, "marca": None, "categoria": None, "preco": None, "preco_promocional": None, "qtd_minima": None}

    caminho_relativo = Path("dados/produtos/relatorio_produto_utf32.dat")
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

            produto = produto_template.copy()

            for atributo in produto.keys():

                if atributo == "id":
                    produto[atributo] = int(linha[i])

                elif atributo in ["preco", "preco_promocional", "qtd_minima"]:
                    produto[atributo] = float(linha[i])

                else:
                    produto[atributo] = linha[i]

                i += 1

            lista_produtos.append(produto)
            cont_id = int(produto["id"]) + 1

    arquivo.close()
    return STATUS_CODE["SUCESSO"]