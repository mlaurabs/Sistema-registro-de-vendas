from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = ["createProduto", "showProdutoById", "showProdutoByNome", "updateProduto", "getProdutoById", "getProdutoByNome", "showProdutos", "showProdutosByMarca", "showProdutosByCategoria", "showProdutosByFaixaPreco", "showProdutosByNome", "deleteProduto", "geraRelatorioProduto", "leRelatorioProduto", "limpaProdutos"]

cont_id = 1 # Guarda o próximo ID a ser cadastrado
lista_produtos = [] # Lista com todos os produtos

'''
Objetivo: 
- Contar as casas decimais de um número

Descrição
- A função irá separar o número em duas partes: uma inteira e uma decimal
- Então, será feita uma checagem se o número de elementos da parte decimal é maior que a quantidade de casas decimais desejadas

Parâmetros
- Valor que deseja-se contar as casas decimais e a quantidade de casas esperadas

Retornos esperados
- True
- False

Assertivas de entrada
- valor deve ser float
- casas_desejadas deve ser int

Assertivas de saída 
- Se a quantidade de casas decimais do número for maior que a quantidade desejada, a função irá retornar True. Caso contrário, retorna False
'''
def contaCasasDecimais(valor, casas_desejadas):
    str_valor = str(valor)
    if '.' in str_valor:
        str_valor = str_valor.split('.')
        if len(str_valor[1]) > casas_desejadas:
            return True # Preço não pode ter mais que 2 casas decimais
    return False

'''
Objetivo
- Validar os valores passados para a função createProduto

Descrição
- A função será um wrapper que irá checar se os valores passados obedecem algumas regras
- Nome, marca, categoria, preço e quantidade mínima são obrigatórios
- Nome, marca e categoria não podem ter mais que 50 caracteres
- Preço e preço promocional não podem ter mais que 2 casas decimais
- O preço promocional não pode ser maior que o preço
- Não pode existir algum produto similar no sistema, isto é, com mesmo nome, marca e categoria

Parâmetros
- Nome do produto
- Marca do produto
- Categoria do produto
- Preço do produto
- Preço promocional do produto

Retornos esperados
- Nome vazio
- Marca vazia
- Categoria vazia
- Preço vazio
- Nome com formato incorreto
- Marca com formato incorreto
- Categoria com formato incorreto
- Preço com formato incorreto
- Preço promocional com formato incorreto
- Preço promocional maior que preço
- Produto existente
- Função createProduto

Assertivas de entrada
- Nome, marca e categoria devem ser strings
- Preço e preço promomocional devem ser floats

Assertivas de saída
- A função deve, se não ocorrer nenhum erro, chamar a função createProduto repassando os parâmetros recebidos
'''
def validaCreate(funcao):

    def valida(nome, marca, categoria, preco, preco_promocional):

        global lista_produtos

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco}

        for atributo, valor in parametros.items():
            if valor == "" or valor == -1:
                atributo = atributo.upper()
                erro = "PRODUTO_" + atributo + "_VAZIO"
                return STATUS_CODE[erro] # O valor não pode ser nulo

        if len(nome) > 50:
            return STATUS_CODE["PRODUTO_NOME_FORMATO_INCORRETO"] # Nome não pode ter mais que 50 caracteres

        if len(marca) > 50:
            return STATUS_CODE["PRODUTO_MARCA_FORMATO_INCORRETO"] # Marca não pode ter mais que 50 caracteres

        if len(categoria) > 50:
            return STATUS_CODE["PRODUTO_CATEGORIA_FORMATO_INCORRETO"] # Categoria não pode ter mais que 50 caracteres

        if contaCasasDecimais(preco, 2):
            return STATUS_CODE["PRODUTO_PRECO_FORMATO_INCORRETO"] # Preço não pode ter mais que duas casas decimais

        if contaCasasDecimais(preco_promocional, 2):
            return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO"] # Preço promocional não pode ter mais que duas casas decimais

        if preco_promocional != -1 and preco_promocional > preco:
            return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"] # Preço promocional não pode ser maior que o preço do produto

        for produto in lista_produtos:
            if nome == produto["nome"] and marca == produto["marca"] and categoria == produto["categoria"]:
                return STATUS_CODE["PRODUTO_EXISTENTE"] # Não podem existir produtos iguais no sistema

        return funcao(nome, marca, categoria, preco, preco_promocional)

    return valida

'''
Descrição
- Antes de executar a função, os dados passam por um wrapper que os valida
- Será feita uma checagem se o preço promocional está vazio. Se estiver, ele passa a ser igual ao preço
- Um produto será criado coms os parâmetros passados
- O produto será criado no estoque
- O produto será adicionado na lista de produtos cadastrados

Parâmetros
- Nome do produto
- Marca do produto
- Categoria do produto
- Preço do produto
- Preço promocional do produto

Retornos esperados
- Sucesso

Assertivas de entrada
- Nome, marca e categoria devem ser strings
- Preço e preço promocional devem ser floats (preço promocional pode ser nulo)
- Todos os parâmetros devem checar já validados

Assertivas de saída 
- O produto será cadastrados na lista de produtos e cadastrado no estoque

Restrição
- Como os produtos não podem ser gravados diretamente numa base de dados, eles devem ser gravados numa lista encapsulada
'''
@validaCreate
def createProduto(nome, marca, categoria, preco, preco_promocional):

    from ..estoque.estoque import createProdutoNoEstoque

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
    }

    lista_produtos.append(produto)
    cont_id += 1

    createProdutoNoEstoque(produto["id"])

    return STATUS_CODE["SUCESSO"] # Sucesso

'''
Descrição
- A função procura um produto, pelo seu ID, numa lista que armazena todos os produtos cadastrados
- São impressos os atributos e os valores do produto, se encontrado

Parâmetros
- O código identificador do produto

Retornos esperados
- Produto não encontrado na lista
- Sucesso na exibição

Assertivas de entrada
- O ID deve ser um int

Assertivas de saída
- O produto será exibido na interface, caso seja encontrado
'''
def showProdutoById(id):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque

    for produto in lista_produtos:
        if id == produto["id"]:
            print("\n", end="")
            for atributo,valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(id, produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])         
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

'''
Descrição
- A função procura um produto, pelo seu nome, numa lista que armazena todos os produtos cadastrados
- São impressos os atributos e os valores do produto, se encontrado

Parâmetros
- O código identificador do produto

Retornos esperados
- Produto não encontrado na lista
- Sucesso na exibição

Assertivas de entrada
- O nome deve ser uma string

Assertivas de saída
- O produto será exibido na interface, caso seja encontrado
'''
def showProdutoByNome(nome):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque

    for produto in lista_produtos:
        if nome == produto["nome"]:
            print("\n", end="")
            for atributo,valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(produto["id"], produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])    
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

'''
Objetivo
- Validar os valores passados para a função updateProduto

Descrição
- A função será um wrapper que irá checar se os valores passados obedecem algumas regras
- Nome, marca, categoria, preço e quantidade mínima são obrigatórios
- Nome, marca e categoria não podem ter mais que 50 caracteres
- Preço e preço promocional não podem ter mais que 2 casas decimais
- O preço promocional não pode ser maior que o preço
- Não pode existir algum produto similar no sistema, isto é, com mesmo nome, marca e categoria

Parâmetros
- Nome do produto
- Marca do produto
- Categoria do produto
- Preço do produto
- Preço promocional do produto

Retornos esperados
- Nome com formato incorreto
- Marca com formato incorreto
- Categoria com formato incorreto
- Preço com formato incorreto
- Preço promocional com formato incorreto
- Função updateProduto

Assertivas de entrada
- Nome, marca e categoria devem ser strings
- Preço e preço promomocional devem ser floats

Assertivas de saída
- A função deve, se não ocorrer nenhum erro, chamar a função updateProduto repassando os parâmetros recebidos
'''
def validaUpdate(funcao):

    def valida(id, nome, marca, categoria, preco, preco_promocional):

        global lista_produtos
            
        if nome != "" and len(nome) > 50:
            return STATUS_CODE["PRODUTO_NOME_FORMATO_INCORRETO"] # Nome não pode ter mais que 50 caracteres

        if marca != "" and len(marca) > 50:
            return STATUS_CODE["PRODUTO_MARCA_FORMATO_INCORRETO"] # Marca não pode ter mais que 50 caracteres

        if categoria != "" and len(categoria) > 50:
            return STATUS_CODE["PRODUTO_CATEGORIA_FORMATO_INCORRETO"] # Categoria não pode ter mais que 50 caracteres

        if preco != -1 and contaCasasDecimais(preco, 2):
            return STATUS_CODE["PRODUTO_PRECO_FORMATO_INCORRETO"] # Preço não pode ter mais que duas casas decimais

        if preco_promocional != -1 and contaCasasDecimais(preco_promocional, 2):
            return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO"] # Preço promocional não pode ter mais que duas casas decimais
        
        return funcao(id, nome, marca, categoria, preco, preco_promocional)
    
    return valida

'''
Descrição
- Antes de executar a função, os dados passam por um wrapper que os valida
- Será feita uma busca na lista com base no ID do produto
- Se o produto for encontrado, seus atributos serão mudados desde que os parâmetros não estejam vazios
- Se o preço promocional for ficar maior que o preço, a função será abortada

Parâmetros
- Nome do produto
- Marca do produto
- Categoria do produto
- Preço do produto
- Preço promocional do produto

Retornos esperados
- Sucesso
- Produto não encontrado
- Preço promocional maior que o preço

Assertivas de entrada
- ID
- Nome, marca e categoria devem ser strings (se forem vazios, "")
- Preço e preço promocional devem ser floats (se forem vazios, -1)
- Todos os parâmetros devem checar já validados

Assertivas de saída 
- O produto será alterado na lista de produtos

Hipótese
- Quem chama a função deve preencher os valores inteiros/float com -1 caso sejam deixados em branco para evitar erros do Python
'''
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
                    return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
                elif preco_promocional != -1 and preco < preco_promocional:
                    return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
                else:
                    produto["preco"] = preco

            if preco_promocional != -1:
                if preco_promocional > produto["preco"]:
                    return STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
                else:
                    produto["preco_promocional"] = preco_promocional      

            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

'''
Objetivo
- Obter os dados de um produto usando seu ID par encontrá-lo

Descrição
- A função procura um produto, pelo seu ID, numa lista que armazena todos os produtos cadastrados
- Se encontrado, o produto é retornado por um parâmetro recebido

Parâmetros
- O código identificador do produto
- A variável onde será retornado o produto

Retornos esperados
- Sucesso
- Produto não encontrado

Assertivas de entrada
- O ID deve ser int
- O retorno deve ser um dicionário

Assertivas de saída
- A variável retorno será preenchida com os valores do produto, caso seja encontrado
'''
def getProdutoById(id, retorno):

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            retorno.update(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # produto não encontrado

'''
Objetivo
- Obter os dados de um produto usando seu Nome par encontrá-lo

Descrição
- A função procura um produto, pelo seu Nome, numa lista que armazena todos os produtos cadastrados
- Se encontrado, o produto é retornado por um parâmetro recebido

Parâmetros
- O nome do produto
- A variável onde será retornado o produto

Retornos esperados
- Sucesso
- Produto não encontrado

Assertivas de entrada
- O Nome deve ser string
- O retorno deve ser um dicionário

Assertivas de saída
- A variável retorno será preenchida com os valores do produto, caso seja encontrado
'''
def getProdutoByNome(nome, retorno):

    global lista_produtos

    for produto in lista_produtos:
        if nome == produto["nome"]:
            retorno.update(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # produto não encontrado

'''
Objetivo
- Imprimir todos os produtos cadastrados

Descrição
- A função irá percorrer a lista de produtos cadastrados, imprimindo os valores de cada um

Retornos esperados
- Sucesso
- Nenhum produto encontrado

Assertivas de saída
- Os produtos serão exibidos na interface, caso sejam encontrados
'''
def showProdutos():

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque

    if not lista_produtos:
        return STATUS_CODE["PRODUTO_NENHUM_CADASTRO"] # Não há produtos cadastrados

    for produto in lista_produtos:
        print("\n", end="")
        for atributo, valor in produto.items():
            if atributo != "preco_promocional":
                print(f"{atributo}: {valor}")
            else:
                print(f"{atributo}: {valor}", end="")
        produto_estoque = dict()
        getProdutoEstoque(produto["id"], produto_estoque)
        print("\nno estoque: ", end="")
        print(produto_estoque["quantidade"])    
        print("\n", end="")

    return STATUS_CODE["SUCESSO"] # Sucesso

'''
Objetivo
- Imprimir todos os produtos cadastrados com certa marca

Descrição
- A função irá percorrer a lista de produtos cadastrados, imprimindo os valores de cada um

Parâmetros
- Marca a ser buscada

Retornos esperados
- Sucesso
- Nenhum produto encontrado

Assertivas de entrada
- Marca deve ser string

Assertivas de saída
- Os produtos serão exibidos na interface, caso sejam encontrados
'''
def showProdutosByMarca(marca):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque
    flag = False

    for produto in lista_produtos:
        if marca == produto["marca"]:
            flag = True
            print("\n", end="")
            for atributo, valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(produto["id"], produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])    
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"] # Nenhum produto encontrado

'''
Objetivo
- Imprimir todos os produtos cadastrados com certa categoria

Descrição
- A função irá percorrer a lista de produtos cadastrados, imprimindo os valores de cada um

Parâmetros
- Categoria a ser buscada

Retornos esperados
- Sucesso
- Nenhum produto encontrado

Assertivas de entrada
- Categoria deve ser string

Assertivas de saída
- Os produtos serão exibidos na interface, caso sejam encontrados
'''
def showProdutosByCategoria(categoria):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque
    flag = False

    for produto in lista_produtos:
        if categoria == produto["categoria"]:
            flag = True
            print("\n", end="")
            for atributo, valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(produto["id"], produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])    
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"] # Nenhum produto encontrado

'''
Objetivo
- Imprimir todos os produtos cadastrados pertencentes a certa faixa de preço

Descrição
- A função irá percorrer a lista de produtos cadastrados, imprimindo os valores de cada um

Parâmetros
- Preço mínimo
- Preço máximo

Retornos esperados
- Sucesso
- Nenhum produto encontrado

Assertivas de entrada
- Preço mínimo e preço máximo devem ser floats

Assertivas de saída
- Os produtos serão exibidos na interface, caso sejam encontrados
'''
def showProdutosByFaixaPreco(preco_min, preco_max):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque
    flag = False

    for produto in lista_produtos:
        if produto["preco_promocional"] >= preco_min and produto["preco_promocional"] <= preco_max:
            flag = True
            print("\n", end="")
            for atributo, valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(produto["id"], produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])    
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"] # Nenhum produto encontrado

'''
Objetivo
- Imprimir todos os produtos cadastrados com nome parecido com o indicado

Descrição
- A função irá percorrer a lista de produtos cadastrados, imprimindo os valores de cada um

Parâmetros
- Nome a ser buscado

Retornos esperados
- Sucesso
- Nenhum produto encontrado

Assertivas de entrada
- Nome deve ser string

Assertivas de saída
- Os produtos serão exibidos na interface, caso sejam encontrados
'''
def showProdutosByNome(nome):

    global lista_produtos
    from ..estoque.estoque import getProdutoEstoque
    flag = False
    
    for produto in lista_produtos:
        if nome.upper() in produto["nome"].upper():
            flag = True
            print("\n", end="")
            for atributo, valor in produto.items():
                if atributo != "preco_promocional":
                    print(f"{atributo}: {valor}")
                else:
                    print(f"{atributo}: {valor}", end="")
            produto_estoque = dict()
            getProdutoEstoque(produto["id"], produto_estoque)
            print("\nno estoque: ", end="")
            print(produto_estoque["quantidade"])    
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"] # Nenhum produto encontrado

'''
Descrição
- Um produto, identificado pelo seu ID, será removido do sistema
- O produto não poderá ser removido se estiver cadastrado em alguma venda
- O produto não poderá ser removido se ainda houverem unidades disponíveis no estoque

Parâmetros
- Código identificador do produto

Retornos esperados
- Sucesso
- Produto não encontrado
- Produto cadastrado em venda
- Unidades disponíveis em estoque

Assertivas de entrada
- ID deve ser int

Assertivas de saída 
- Caso esteja dentro das condições estabelicidas, o produto será removido da lista de produtos
'''
def deleteProduto(id):

    from ..estoque.estoque import getProdutoEstoque, deleteProdutoEstoque
    from ..venda.venda import checkProdutoVenda

    global lista_produtos

    for produto in lista_produtos:
        if id == produto["id"]:
            
            estoque = dict()
            getProdutoEstoque(produto["id"], estoque)
            
            if estoque["quantidade"] != 0:
                return STATUS_CODE["PRODUTO_NAO_ZERADO_NO_ESTOQUE"]
            
            flag = checkProdutoVenda(produto["id"])

            if flag == STATUS_CODE["SUCESSO"]:
                return STATUS_CODE["PRODUTO_CADASTRADO_EM_VENDA"]

            deleteProdutoEstoque(produto["id"])

            lista_produtos.remove(produto)
            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

'''
Objetivo
- Limpar a lista de produtos e resetar o ID

Descrição
- A função irá esvazias a lista onde estão armazenados todos os produtos
- O contador que armazena o ID do próximo produto a ser cadastrado voltará a ser 1

Assertivas de saída
- A lista de produtos será esvaziada
- O contador será reiniciado
'''
def limpaProdutos():
    global lista_produtos, cont_id
    cont_id = 1
    lista_produtos.clear()

'''
Descrição
- Os produtos cadastrados no sistema serão lidos e impressos num arquivo .dat
- O arquivo .dat deve estar em UTF-32
- Serão impresso apenas os valores dos produtos
- Valores referentes à diferentes atributos deverão ser separados por ,
- Diferentes produtos verão ser separados por |

Retornos esperados
- Sucesso

Assertivas de entrada
- O arquivo .dat para armazenar os dados deve existir no local especificado

Assertivas de saída 
- Os dados dos produtos serão impressos no arquivo .dat em UTF-32

Hipótese
- Como os arquvivos devem passar por uma "compressão", eles deverão ser gravados em UTF-32
'''
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
            string = string[:-1] + '|'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- Os produtos presentes em um arquivo .dat serão lidos e cadastrados no sistema
- O arquivo .dat está em UTF-32
- Estão impresso apenas os valores dos produtos
- Valores referentes à diferentes atributos estão ser separados por ,
- Diferentes produtos estão ser separados por -

Retornos esperados
- Sucesso

Assertivas de entrada
- O arquivo .dat da onde serão lidos os dados deve existir no local especificado

Assertivas de saída 
- Os dados dos produtos serão lidos arquivo .dat em UTF-32 e serão cadastrados no sistema
'''
def leRelatorioProduto():

    global lista_produtos, cont_id

    produto_template = {"id": None, "nome": None, "marca": None, "categoria": None, "preco": None, "preco_promocional": None}

    caminho_relativo = Path("dados/produtos/relatorio_produto_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "rb")

    arquivo.read(4)
    conteudo = arquivo.read()
    conteudo = conteudo.decode('utf-32-le')

    conteudo = conteudo.split('|')

    for linha in conteudo:
        if linha:
            
            linha = linha.strip()
            linha = linha.split(',')
            i = 0

            produto = produto_template.copy()

            for atributo in produto.keys():

                if atributo == "id":
                    produto[atributo] = int(linha[i])

                elif atributo in ["preco", "preco_promocional"]:
                    produto[atributo] = float(linha[i])

                else:
                    produto[atributo] = linha[i]

                i += 1

            lista_produtos.append(produto)
            cont_id = int(produto["id"]) + 1

    arquivo.close()
    return STATUS_CODE["SUCESSO"]