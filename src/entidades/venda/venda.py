import re
from datetime import datetime
from src.status_code import STATUS_CODE
from pathlib import Path

# Encapsulamento
__all__ = [
    "getVenda", "createVenda", "concludeVenda", "cancelaVenda", "addProduto", "removeProduto", "showVenda", "showVendas",
    "showVendasCliente", "showVendasData", "updateVenda", "checkProdutoVenda", "checkClienteVenda", "deleteVenda", "limpaVendas",
    "geraRelatorioVenda", "leRelatorioVenda"
]

# Funções auxiliares

'''
Objetivo
- Conferir se a data está no formato correto

Descrição
- Aciona a função da biblioteca datetime
- Se a data estiver na formatação correta, ela será retornada. Caso contrário, será retornado None

Parâmetros
- Data a ser checada

Retornos esperados
- A data já checada
- None em caso de formatação incorreta

Assertivas de entrada
- Data deve ser uma string

Assertivas de saída
- A função irá retornar a data com a formatação correta
'''
def formatarData(data):
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        return data_formatada
    except ValueError:
        return None
    
'''
Objetivo
- Conferir se a hora está no formato correto

Descrição
- Aciona a função da biblioteca datetime
- Se a hora estiver na formatação correta, ela será retornada. Caso contrário, será retornado None

Parâmetros
- Hora a ser checada

Retornos esperados
- A hora já checada
- None em caso de formatação incorreta

Assertivas de entrada
- Hora deve ser uma string

Assertivas de saída
- A função irá retornar a hora com a formatação correta
'''
def formatarHora(hora):
    try:
        hora_formatada = datetime.strptime(hora, "%H:%M").strftime("%H:%M")
        return hora_formatada
    except ValueError:
        return None

'''
Objetivo
- Conferir se o CPF tem o formato correto

Descrição
- Confere se o CPF segue o formato AAA.AAA.AAA-AA

Parâmetros
- CPF a ser checado

Retornos esperados
- Sucesso
- CPF no formato incorreto

Assertivas de entrada
- CPF deve ser uma string

Assertivas de saída
- A função irá retornar um número indicando se o CPF está formatado correta ou erroneamente
'''
def validaCPF(cpf):

    # Verifica se o CPF tem exatamente 14 caracteres
    if len(cpf) != 14:
        return STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"]
    
    # Verifica se os pontos e o hífen estão nos lugares corretos
    if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        return STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"]
    
    # Verifica se os outros caracteres são numéricos
    numeros = cpf.replace('.', '').replace('-', '')
    if not numeros.isdigit():
        return STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"]
    
    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Validar os valores passados para a função createVenda

Descrição
- A função será um wrapper que irá checar se os valores passados obedecem algumas regras
- Data e Hora são obrigatórias
- CPF é opcional
- Serão acionadas as funções formatarData, formatarHora e validaCPF

Parâmetros
- CPF, Data e Hora

Retornos esperados
- Função createVenda
- CPF no formato incorreto
- Data no formato incorreto
- Hora no formato incorreto

Assertivas de entrada
- CPF, Data e hora devem ser strings

Assertivas de saída
- A função deve, se não ocorrer nenhum erro, chamar a função createVenda repassando os parâmetros recebidos
'''
def validaCreate(funcao):

    def valida(cpf, data, hora):

        if cpf != "":
            flag = validaCPF(cpf)
            if flag != STATUS_CODE["SUCESSO"]:
                return flag

        data = formatarData(data)
        if not data:
            return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]
        
        hora = formatarHora(hora)
        if not hora:
            return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]
        
        return funcao(cpf, data, hora)

    return valida

'''
Objetivo
- Validar os valores passados para a função uVenda

Descrição
- A função será um wrapper que irá checar se os valores passados obedecem algumas regras
- Data e Hora são obrigatórias
- CPF é opcional

Parâmetros
- ID da venda, CPF, Data e Hora

Retornos esperados
- Função updateVenda
- CPF no formato incorreto
- Data no formato incorreto
- Hora no formato incorreto

Assertivas de entrada
- CPF, Data e hora devem ser strings

Assertivas de saída
- A função deve, se não ocorrer nenhum erro, chamar a função updateVenda repassando os parâmetros recebidos
'''
def validaUpdate(funcao):

    def valida(id_venda, cpf, data, hora):

        if cpf != "":
            flag = validaCPF(cpf)
            if flag != STATUS_CODE["SUCESSO"]:
                return flag

        if data != "":
            data = formatarData(data)
            if not data:
                return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]

        if hora != "":
            hora = formatarHora(hora)
            if not hora:
                return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]

        return funcao(id_venda, cpf, data, hora)

    return valida

# Estrutura para armazenar as vendas em memória
vendas = []
# Armazena o ID disponível
cont_id = 1

# Funções principais

'''
Objetivo
- Obter os dados de uma venda usando seu ID par encontrá-la

Descrição
- A função procura uma venda, pelo seu ID, numa lista que armazena todos as vendas cadastrados
- Se encontrada, a venda é retornado por um parâmetro recebido

Parâmetros
- O código identificador da venda
- A variável onde será retornado a venda

Retornos esperados
- Sucesso
- Produto não encontrado

Assertivas de entrada
- O ID deve ser int
- O retorno deve ser um dicionário

Assertivas de saída
- A variável retorno será preenchida com os valores do venda, caso seja encontrada
'''
def getVenda(id, retorno):

    global vendas

    for venda in vendas:
        if venda["id"] == id:
            retorno.update(venda)
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

'''
Descrição
- Antes de executar a função, os dados passam por um wrapper que os valida
- Deverá ser conferido se o cliente existe e, se ele existir, se nenhuma venda duplicada existe (mesmo cliente, data e horário)
- Uma venda será criada com os parâmetros passados
- A venda será adicionada na lista de vendas cadastradas

Parâmetros
- CPF do cliente
- Data da venda
- Hora da venda

Retornos esperados
- Sucesso
- Cliente não encontrado
- Venda já existente

Assertivas de entrada
- CPF, data e hora devem ser strings
- Todos os parâmetros devem chegar já validados

Assertivas de saída 
- A venda será cadastrada na lista de vendas

Restrição
- Como as vendas não podem ser gravados diretamente numa base de dados, elas devem ser gravados numa lista encapsulada
'''
@validaCreate
def createVenda(cpf, data, hora):

    from ..cliente.cliente import getCliente
    global vendas, cont_id

    # Se houver a tentativa de usar um cadastro, verificar se existe
    if cpf != "":
        temp = dict()
        flag = getCliente(cpf, temp)
        if flag != STATUS_CODE["SUCESSO"]:
            return flag # CLIENTE_NAO_ENCONTRADO

    # Confere se já não existe a venda para um cliente
    if cpf != "":
        for venda in vendas:
            if venda["cpf"] == cpf and venda["data"] == data and venda["hora"] == hora:
                return STATUS_CODE["VENDA_EXISTENTE"]

    # Cria a nova venda
    nova_venda = {
        "id": cont_id,
        "cpf": cpf,
        "data": data,
        "hora": hora,
        "status": "em processamento",
        "produtos": []
    }

    vendas.append(nova_venda)
    cont_id += 1

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Alterar o status de uma venda para concluída

Descrição
- A venda é procura na lista de vendas
- Se ela tiver sido encontrada e não tiver sido concluída, nem cancelada, ela é concluída

Parâmetros
- O ID da venda a ser concluída

Retornos
- Sucesso
- Venda não encontrada
- Venda já concluída
- Venda já cancelada

Assertivas de entrada
- ID da venda deve ser int

Assertivas de saída
- O status da venda passa de "em processamento" para "concluída"
'''
def concludeVenda(id_venda):

    global vendas

    flag = 1

    # Pega a venda
    for venda in vendas:
        if venda["id"] == id_venda:
            flag = 0
            break

    # Se a venda não existir
    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    
    # Se a venda já estiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda já estiver sido cancelada
    if venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    venda["status"] = "concluída"

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Alterar o status de uma venda para cancelada

Descrição
- A venda é procura na lista de vendas
- Se ela tiver sido encontrada e não tiver sido concluída, nem cancelada, ela é cancelada

Parâmetros
- O ID da venda a ser cancelada

Retornos
- Sucesso
- Venda não encontrada
- Venda já concluída
- Venda já cancelada

Assertivas de entrada
- ID da venda deve ser int

Assertivas de saída
- O status da venda passa de "em processamento" para "cancelada"
'''
def cancelaVenda(id_venda):

    from ..estoque.estoque import atualizaQtdEstoque

    flag = 1

    # Pega a venda
    for venda in vendas:
        if venda["id"] == id_venda:
            flag = 0
            break

    # Se a venda não existir
    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    
    # Se a venda já estiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda já estiver sido cancelada
    if venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    # Devolve os produtos ao estoque
    for produto_id, quantidade in venda["produtos"]:
        atualizaQtdEstoque(produto_id, quantidade)

    venda["status"] = "cancelada"

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Adicionar um produto, sua quantidade desejada e seu preço à uma venda 

Descrição
- A função deve procurar a venda na lista de vendas, além de checar se ela não foi cancelada ou concluída.
- Deve também checar se há quantidades disponíveis em estoque.
- Se tudo estiver nos conformes, a quantidade do produto no estoque deve ser alterada e o produto deve ser cadastrado na venda

Parâmetros
- O ID da venda
- O ID do produto
- A quantidade a ser adicionada do produto na venda

Retornos
- Sucesso
- Venda não encontrada
- Venda já concluída
- Não há unidades disponíveis no estoque

Assertivas de entrada
- ID da venda, ID do produto e quantidade devem ser int

Assertivas de saída
- O ID do produto, a quantidade desejada e seu preço devem ser adicionados à venda e a quantidade no estoque deve ser alterada.
'''
def addProduto(id_venda, id_produto, quantidade):

    global vendas

    from ..produto.produto import getProdutoById
    from ..estoque.estoque import getProdutoEstoque, atualizaQtdEstoque

    flag = 1

    # Pega a venda
    for venda in vendas:
        if venda["id"] == id_venda:
            flag = 0
            break

    # Se a venda não existir
    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    # Se a venda tiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda tiver sido cancelada
    elif venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    # Pega o produto
    produto = dict()
    flag = getProdutoById(id_produto, produto)

    # Se o produto não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag # PRODUTO_NAO_ENCONTRADO
    
    # Pega o produto no estoque
    produto_estoque = dict()
    getProdutoEstoque(id_produto, produto_estoque)

    # Se não houverem unidades suficientes
    if produto_estoque["quantidade"] < quantidade:
        return STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"]
    
    flag = 1

    # Se o produto já estiver na venda
    for produto2 in venda["produtos"]:
        if produto2["id"] == id_produto:
            produto2["quantidade"] += quantidade
            flag = 0
            break

    # Se o produto não estiver na venda
    if flag:
        venda["produtos"].append({"id": id_produto, "quantidade": quantidade, "preco": produto["preco_promocional"]})

    # Remove as unidades comercializadas do estoque
    atualizaQtdEstoque(id_produto, -quantidade)

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Remover a quantidade de unidades desejadas do produto indicado

Descrição
- A função deve procurar a venda na lista de vendas, além de checar se ela não foi cancelada ou concluída.
- Se tudo estiver nos conformes, a quantidade do produto no estoque deve ser alterada e o as unidades do produto devem ser retiradas da venda
- Se a quantidade de unidades de um produto passar a ser 0, ele deve ser removido da venda

Parâmetros
- O ID da venda
- O ID do produto
- A quantidade a ser removida do produto na venda

Retornos
- Sucesso
- Venda não encontrada
- Venda já concluída

Assertivas de entrada
- ID da venda, ID do produto e quantidade devem ser int

Assertivas de saída
- A quantidade do produto na venda deve ser alterada, assim como a quantidade em estoque. Se a quantidade do produto passar a ser 0, ele deve ser removido da venda.
'''  
def removeProduto(id_venda, id_produto, quantidade):

    global vendas

    from ..produto.produto import getProdutoById
    from ..estoque.estoque import atualizaQtdEstoque

    flag = 1

    # Pega a venda
    for venda in vendas:
        if venda["id"] == id_venda:
            flag = 0
            break

    # Se a venda não existir
    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    
    # Se a venda tiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda tiver sido cancelada
    elif venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    # Pega o produto
    produto = dict()
    flag = getProdutoById(id_produto, produto)

    # Se o produto não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag # PRODUTO_NAO_ENCONTRADO
    
    flag = 1
    
    # Acha o produto e tira a quantidade pedida
    for produto in venda["produtos"]:
        if produto["id"] == id_produto:
            if quantidade > produto["quantidade"]:
                return STATUS_CODE["VENDA_QUANTIDADE_INSUFICIENTE"]
            produto["quantidade"] -= quantidade
            # Remove o produto na venda
            if produto["quantidade"] == 0:
                venda["produtos"].remove(produto)
            flag = 0
            break

    # Se o produto não estiver na venda
    if flag:
        return STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"]

    # Devolve as unidades não comercializadas ao estoque
    atualizaQtdEstoque(id_produto, -quantidade)

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- A venda vai ser buscado com base no seu ID e seus atributos e valores irão ser exibidos na tela, assim como sua quantidade em estoque

Parâmetros
- ID da venda

Retornos
- Sucesso
- Venda não encontrada

Assertivas de entrada
- O ID da venda deve ser um INT

Assertivas de saída
- Os dados do produto serão exibidos no terminal
'''
def showVenda(id_venda):

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag # VENDA_NAO_ENCONTRADA

    # Imprime a venda
    print("\n", end="")
    for atributo,valor in venda.items():
        print(f"{atributo}: {valor}")
    print("\n")

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- Todas as vendas (atributos e valores) irão ser exibidos na tela, assim como sua quantidade em estoque

Retornos
- Sucesso
- Nenhuma venda encontrada

Assertivas de saída
- Os dados dos produtos serãos exibidos no terminal
'''
def showVendas():

    global vendas

    # Se não houver vendas cadastradas
    if not vendas:
        return STATUS_CODE["VENDA_NENHUM_CADASTRO"]

    # Imprime as vendas
    for venda in vendas:
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- Todas as vendas (atributos e valores) de um cliente irão ser exibidos na tela, assim como sua quantidade em estoque

Parâmetros
- CPF do cliente

Retornos
- Sucesso
- Nenhuma venda encontrada
- Cliente não encontrado

Assertivas de entrada
- O CPF do cliente deve ser uma string

Assertivas de saída
- Os dados dos produtos serãos exibidos no terminal
'''
def showVendasCliente(cpf):

    from ..cliente.cliente import getCliente

    # Se houver a tentativa de usar um cadastro, verificar se existe
    if cpf != "":
        temp = dict()
        flag = getCliente(cpf, temp)
        if flag != STATUS_CODE["SUCESSO"]:
            return flag # CLIENTE_NAO_ENCONTRADO

    global vendas

    flag = 1

    # Pega as vendas do cliente
    for venda in vendas:
        if venda["cpf"] == cpf:
            flag = 0
            print("\n", end="")
            for atributo,valor in venda.items():
                print(f"{atributo}: {valor}")
            print("\n")

    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- Todas as vendas (atributos e valores) em uma data irão ser exibidas na tela, assim como sua quantidade em estoque

Parâmetros
- Data a ser buscada

Retornos
- Sucesso
- Nenhuma venda encontrada

Assertivas de entrada
- A data deve ser uma string

Assertivas de saída
- Os dados dos produtos serãos exibidos no terminal
'''
def showVendasData(data):

    global vendas

    flag = 1

    # Pega as vendas do cliente
    for venda in vendas:
        if venda["data"] == data:
            flag = 0
            print("\n", end="")
            for atributo,valor in venda.items():
                print(f"{atributo}: {valor}")
            print("\n")

    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return STATUS_CODE["SUCESSO"]

'''
Descrição
- Antes de executar a função, os dados passam por um wrapper que os valida
- Uma venda será buscada na lista de vendas
- Se algum campo não estiver vazio, significa que o usuário deseja alterá-lo

Parâmetros
- ID da venda
- CPF do cliente
- Data da venda
- Hora da venda

Retornos esperados
- Sucesso
- Venda não encontrada

Assertivas de entrada
- ID deve ser int 
- CPF, data e hora devem ser strings (podem ser nulos)
- Todos os parâmetros devem chegar já validados

Assertivas de saída 
- Os atributos da venda específica serão atualizados na lista de vendas
'''
@validaUpdate
def updateVenda(id_venda, cpf, data, hora):

    flag = 1

    # Pega a venda
    for venda in vendas:
        if venda["id"] == id_venda:
            flag = 0
            break

    # Se a venda não existir
    if flag:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    # Altera cpf, data e hora
    if cpf != "":
        venda["cpf"] = cpf
    
    if data != "":
        venda["data"] = data

    if hora != "":
        venda["hora"] = hora

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Checar se um produto específico está cadastrado em alguma venda

Descrição
- Um produto é buscado pelo seu ID em todas as vendas cadastradas
- Um retorno específico é retornado caso o produto seja, ou não, encontrado

Parâmetros
- O ID do produto a ser buscado

Retornos
- Sucesso
- Produto não encontrado em vendas

Assertivas de entrada
- O ID do produto deve ser um int

Assertivas de saída 
- Um valor será retornado caso o produto seja ou não encontrado em vendas
'''
def checkProdutoVenda(id_produto):

    global vendas

    # Procura produto nas vendas
    for venda in vendas:
        for produto in venda["produtos"]:
            if produto["id"] == id_produto:
                return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"]

'''
Objetivo
- Checar se um cliente específico está cadastrado em alguma venda

Descrição
- Um cliente é buscado pelo seu CPF em todas as vendas cadastradas
- Um retorno específico é retornado caso o cliente seja, ou não, encontrado

Parâmetros
- O CPF do cliente a ser buscado

Retornos
- Sucesso
- Cliente não encontrado em vendas

Assertivas de entrada
- O CPF do cliente deve ser uma string

Assertivas de saída 
- Um valor será retornado caso o cliente seja ou não encontrado em vendas
'''
def checkClienteVenda(cpf_cliente):

    global vendas

    # Procura o cliente nas vendas
    for venda in vendas:
        if venda["cpf"] == cpf_cliente:
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"]

'''
Descrição
- Uma venda será buscada com base no seu ID numa lista que armazena todas as vendas
- Se ela tiver sido encontrada, não tiver sido concluída e não estiver em processamento, ela deverá ser removida dessa lista

Parâmetros
- O ID da venda a ser removida

Retornos
- Sucesso
- Venda não encontrada
- Venda já concluída
- Venda em processamento

Assertivas de entrada
- O ID da venda deve ser int

Assertivas de saída
- A venda deverá ser deletada da lista
'''
def deleteVenda(id_venda):

    global vendas

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag # VENDA_NAO_ENCONTRADA
    
    # Se a venda tiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]

    # Verifica se a venda ainda está em processamento
    if venda["status"] == "em processamento":
        return STATUS_CODE["VENDA_EM_PROCESSAMENTO"]

    # Deleta a venda
    vendas.remove(venda)

    return STATUS_CODE["SUCESSO"]

'''
Objetivo
- Limpar a lista de vendas e resetar o ID

Descrição
- A função irá esvaziar a lista onde estão armazenadas todas as vendas
- O contador que armazena o ID da próxima venda a ser cadastrada voltará a ser 1

Assertivas de saída
- A lista de vendas será esvaziada
- O contador será reiniciado
'''
def limpaVendas():
    global vendas, cont_id
    cont_id = 1
    vendas.clear()

# Funções de Relatório

'''
Descrição
- As vendas cadastradas no sistema serão lidas e impressas num arquivo .dat
- O arquivo .dat deve estar em UTF-32
- Serão impresso sapenas os valores das vendas
- Valores referentes à diferentes atributos deverão ser separados por ,
- Diferentes vendas verão ser separadas por |

Retornos esperados
- Sucesso

Assertivas de entrada
- O arquivo .dat para armazenar os dados deve existir no local especificado

Assertivas de saída 
- Os dados das vendas serão impressos no arquivo .dat em UTF-32

Hipótese
- Como os arquvivos devem passar por uma "compressão", eles deverão ser gravados em UTF-32
'''
def geraRelatorioVenda():

    global vendas

    caminho_relativo = Path("dados/vendas/relatorio_venda_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, venda in enumerate(vendas):
        string = ""

        for atributo, valor in venda.items():
            if atributo != "produtos":
                if valor != "":
                    string += str(valor) + ','
                else:
                    string += " " + ','
            else:
                for produto in venda["produtos"]:
                    for valor in produto.values():
                        string += str(valor) + ','

        if indice != len(vendas)-1:
            string = string[:-1] + '|'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]


'''
Descrição
- As vendas presentes em um arquivo .dat serão lidas e cadastradas no sistema
- O arquivo .dat está em UTF-32
- Estão impressos apenas os valores das vendas
- Valores referentes à diferentes atributos estão ser separados por ,
- Diferentes vendas estão ser separados por -

Retornos esperados
- Sucesso

Assertivas de entrada
- O arquivo .dat da onde serão lidos os dados deve existir no local especificado

Assertivas de saída 
- Os dados dos produtos serão lidos arquivo .dat em UTF-32 e serão cadastrados no sistema
'''
def leRelatorioVenda():

    global vendas, cont_id

    venda_template = {"id": None, "cpf": None, "data": None, "hora": None, "status": None, "produtos": []}

    caminho_relativo = Path("dados/vendas/relatorio_venda_utf32.dat")
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

            tam = len(linha)

            venda = venda_template.copy()

            for atributo in venda.keys():

                if i == tam:
                   break

                if atributo != "produtos":
                    if atributo == "id":
                        venda[atributo] = int(linha[i])
                    else:
                        if linha[i] != " ":
                            venda[atributo] = linha[i]
                        else:
                            venda[atributo] = ""
                    i += 1
                    
                else:
                    while (i != tam):
                        produto = {"id": None, "quantidade": None, "preco": None} 
                        for atributo2 in produto.keys():
                            if atributo2 == "preco":
                                produto[atributo2] = float(linha[i])
                            else:
                                produto[atributo2] = int(linha[i])
                            i += 1
                        venda["produtos"].append(produto)

            vendas.append(venda)
            cont_id = int(venda["id"]) + 1

    arquivo.close()
    return STATUS_CODE["SUCESSO"]