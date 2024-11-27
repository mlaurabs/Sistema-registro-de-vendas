from src.status_code import STATUS_CODE
from pathlib import Path
from datetime import datetime

'''
import sys

caminho_relativo = Path("src/entidades/cliente/cliente.py")
caminho_absoluto = caminho_relativo.resolve()

sys.path.append(caminho_absoluto.parent)
'''
__all__ = ["createCliente", "showCliente", "updateClienteByCpf", "updateClienteByNome", "getCliente", "showClientes", "showClientesByNome", "deleteCliente", "geraRelatorioCliente", "leRelatorioCliente"]

lista_clientes = [] # Lista com todos os clientes

def validaDataNascimento(data_nascimento):

    try: 
        data = datetime.strptime(data_nascimento, '%d/%m/%Y') # Tenta converter a string para uma data válida
    except ValueError:
        return STATUS_CODE["CLIENTE_DATA_NASCIMENTO_INVALIDA"]  # Data inválida   
    
    # Verifica se o usuário é menor de idade
    hoje = datetime.now()
    idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))

    if idade < 18:
        return STATUS_CODE["CLIENTE_MENOR_DE_IDADE"]
    
    return STATUS_CODE["SUCESSO"]

def validaCpf(cpf):

    # Verifica se o CPF tem exatamente 14 caracteres
    if len(cpf) != 14:
        return STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
    
    # Verifica se os pontos e o hífen estão nos lugares corretos
    if cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        return STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
    
    # Verifica se os outros caracteres são numéricos
    numeros = cpf.replace('.', '').replace('-', '')
    if not numeros.isdigit():
        return STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
    
    return STATUS_CODE["SUCESSO"]

def validaCreate(funcao):

    def valida(cpf, nome, data_nascimento):

        global lista_clientes

        parametros = {"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento}

        for atributo, valor in parametros.items():
            if valor == "":
                atributo = atributo.upper()
                erro = "CLIENTE_" + atributo + "_VAZIO"
                return STATUS_CODE[erro] # O valor não pode ser nulo

        flag = validaCpf(cpf)
        if flag != STATUS_CODE["SUCESSO"]:
            return flag
        
        if len(nome) > 50:
            return STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"] # Nome não pode ter mais que 50 caracteres e só aceita caracteres

        temp = nome

        if not temp.replace(" ", "").isalpha():
            return STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"]

        flag = validaDataNascimento(data_nascimento)
        if flag != STATUS_CODE["SUCESSO"]:
            return flag
        
        for cliente in lista_clientes:
            if cpf == cliente["cpf"]:
                return STATUS_CODE["CLIENTE_EXISTENTE"] # Não podem existir produtos iguais no sistema

        return funcao(cpf, nome, data_nascimento)

    return valida

@validaCreate
def createCliente(cpf, nome, data_nascimento):

    global lista_clientes

    produto ={
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
    }

    lista_clientes.append(produto)

    return STATUS_CODE["SUCESSO"] # Sucesso

def showCliente(cpf):

    global lista_clientes

    for cliente in lista_clientes:
        if cpf == cliente["cpf"]:
            print("\n", end="")
            for atributo,valor in cliente.items():
                print(f"{atributo}: {valor}")
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def validaUpdate(funcao):

    def valida(cpf, nome, data_nascimento):

        global lista_clientes

        if cpf != "":
            flag = validaCpf(cpf)
            if flag != STATUS_CODE["SUCESSO"]:
                return flag


        if nome != "":
            if len(nome) > 50:
                return STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"] # Nome não pode ter mais que 50 caracteres e só aceita caracteres

            temp = nome

            if not temp.replace(" ", "").isalpha():
                return STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"]

        if data_nascimento != "":
            flag = validaDataNascimento(data_nascimento)
            if flag != STATUS_CODE["SUCESSO"]:
                return flag

        return funcao(cpf, nome, data_nascimento)

    return valida

@validaUpdate
def updateClienteByCpf(cpf, nome, data_nascimento):

    global lista_clientes

    for cliente in lista_clientes:
        if cpf == cliente["cpf"]:

            if nome != "":
                cliente["nome"] = nome

            if data_nascimento != "":
                cliente["data_nascimento"] = data_nascimento

            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

@validaUpdate
def updateClienteByNome(cpf, nome, data_nascimento):

    global lista_clientes

    for cliente in lista_clientes:
        if nome == cliente["nome"]:

            if cpf != "":
                for cliente_aux in lista_clientes:
                    if cliente_aux == cpf:
                        return STATUS_CODE["CLIENTE_EXISTENTE"]
                    
                cliente["cpf"] = cpf

            if data_nascimento != "":
                cliente["data_nascimento"] = data_nascimento

            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def getCliente(cpf, retorno):

    global lista_clientes

    for cliente in lista_clientes:
        if cpf == cliente["cpf"]:
            retorno.update(cliente)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def showClientes():

    global lista_clientes

    if not lista_clientes:
        return STATUS_CODE["CLIENTE_NENHUM_CADASTRADO"] # Não há clientes cadastrados

    for cliente in lista_clientes:
        print("\n", end="")
        for atributo, valor in cliente.items():
            print(f"{atributo}: {valor}")
        print("\n", end="")

    return STATUS_CODE["SUCESSO"] # Sucesso

def showClientesByNome(nome):

    global lista_clientes
    flag = False
    
    for cliente in lista_clientes:
        if nome.upper() in cliente["nome"].upper():
            flag = True
            print("\n", end="")
            for atributo, valor in cliente.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")
    if flag:
        return STATUS_CODE["SUCESSO"] # Sucesso
    else:
        return STATUS_CODE["CLIENTE_NENHUM_ENCONTRADO"] # Nenhum cliente encontrado

def deleteCliente(cpf):

    global lista_cliente

    for cliente in lista_clientes:
        if cpf == cliente["cpf"]:
            
            '''
            flag = checkProdutoVenda(cliente["cpf"])

            if flag == STATUS_CODE["CLIENTE_ENCONTRADO"]:
                return STATUS_CODE["CLIENTE_CADASTRADO_EM_VENDA"]
            '''

            lista_clientes.remove(cliente)
            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

'''
Descrição
- Os produtos cadastrados no sistema serão lidos e impressos num arquivo .dat
- O arquivo .dat deve estar em UTF-32
- Serão impresso apenas os valores dos produtos
- Valores referentes à diferentes atributos deverão ser separados por ,
- Diferentes produtos verão ser separados por -

Retornos esperados
- Mensagem de sucesso caso o relatório seja gerado com sucesso

Assertivas de entrada
- O arquivo .dat para armazenar os dados deve existir no local especificado

Assertivas de saída 
- Os dados dos produtos serão impressos no arquivo .dat em UTF-32
'''
def geraRelatorioCliente():

    global lista_clientes

    caminho_relativo = Path("dados/clientes/relatorio_cliente_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, cliente in enumerate(lista_clientes):
        string = ""

        for valor in cliente.values():
            string += str(valor) + ','

        if indice != len(lista_clientes)-1:
            string = string[:-1] + '-'
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
- Mensagem de sucesso caso o relatório seja lido e os produtos sejam cadastrados com sucesso

Assertivas de entrada
- O arquivo .dat da onde serão lidos os dados deve existir no local especificado

Assertivas de saída 
- Os dados dos produtos serão lidos arquivo .dat em UTF-32 e serão cadastrados no sistema
'''
def leRelatorioCliente():

    global lista_clientes

    cliente_template = {"cpf": None, "nome": None, "data_nascimento": None}

    caminho_relativo = Path("dados/clientes/relatorio_cliente_utf32.dat")
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

            cliente = cliente_template.copy()

            for atributo in cliente.keys():

                cliente[atributo] = linha[i]

            lista_clientes.append(cliente)

    arquivo.close()
    return STATUS_CODE["SUCESSO"]