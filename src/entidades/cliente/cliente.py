from src.status_code import STATUS_CODE
from pathlib import Path
from datetime import datetime

__all__ = ["createCliente", "showCliente", "updateClienteByCpf", "updateClienteByNome", "getCliente", "showClientes", "showClientesByNome", "deleteCliente",  "limpaClientes", "salvarclientes", "carregarclientes", "encerrarclientes", "iniciarclientes"]


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

        global clientes

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
        
        for cliente in clientes:
            if cpf == cliente["cpf"]:
                return STATUS_CODE["CLIENTE_EXISTENTE"] # Não podem existir produtos iguais no sistema

        return funcao(cpf, nome, data_nascimento)

    return valida

# Lista global para armazenar os produtos no clientes
clientes = []
cont_id = 1

# Caminhos dos arquivos
arquivo_utf32 = Path("dados/clientes/relatorio_cliente_utf32.txt")
arquivo_utf8 = Path("dados/clientes/relatorio_cliente_utf8.txt")

def salvarclientes():
    global arquivo_utf32
    global clientes  # A lista de produtos

    print("Salvando clientes...")  # Log inicial

    try:
        with open(arquivo_utf32, "wb") as arquivo:
            # Escrever o BOM (Byte Order Mark) para UTF-32-LE
            bom = 0x0000FEFF
            bom_bytes = bom.to_bytes(4, byteorder="little")
            arquivo.write(bom_bytes)

            for cliente in clientes:

                # Construir a string do produto
                atributos = [
                    f'cpf:{cliente["cpf"]}',
                    f'nome:{cliente["nome"]}',
                    f'data_nascimento:{cliente["data_nascimento"]}',
                ]

                # Concatenar a linha completa
                linha = " - ".join(atributos) + "\n"
                
                # Escrever a linha no arquivo em UTF-32-LE
                arquivo.write(linha.encode("utf-32-le"))

        print("Salvo.")  # Log final
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao salvar cliente: {e}")
        return STATUS_CODE["ERRO"]

import converteutf832  # Certifique-se de que o módulo está importado

def carregarclientes():
    global arquivo_utf32
    global arquivo_utf8
    global clientes,  cont_id # A lista de produtos

    print("Iniciando carregamento de clientes...")
    

    converteutf832.convUtf32p8(str(arquivo_utf32), str(arquivo_utf8))
    try:    
        # Lê o arquivo convertido para UTF-8
        with open(arquivo_utf8, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:  # Verifica se o conteúdo está vazio
                clientes = []
                cont_id = 1
                return STATUS_CODE["SUCESSO"]
            # Processa cada linha de produtos
            cont = 0
            linhas = conteudo.split("\n")
            clientes.clear()
            for linha in linhas:
                cont += 1
                if linha.strip():  # Ignora linhas vazias
                    # Divide os atributos pelo separador " - "
                    partes = linha.split(" - ")
                    cliente = {
                        "cpf": partes[0].split(":")[1],
                        "nome": partes[1].split(":")[1],
                        "data_nascimento": partes[2].split(":")[1],
                    }
                    clientes.append(cliente)
        
        # Atualiza o próximo ID
        cont_id = cont
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao carregar cliente: {e}")
        return STATUS_CODE["ERRO"]

def iniciarclientes():
    print("Iniciando módulo de cliente...")
    carregarclientes()

def encerrarclientes():
    print("Encerrando módulo de cliente...")
    salvarclientes()


@validaCreate
def createCliente(cpf, nome, data_nascimento):
    global clientes

    cliente ={
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
    }

    clientes.append(cliente)

    return STATUS_CODE["SUCESSO"] # Sucesso

def showCliente(cpf):

    global clientes

    for cliente in clientes:
        if cpf == cliente["cpf"]:
            print("\n", end="")
            for atributo,valor in cliente.items():
                print(f"{atributo}: {valor}")
            print("\n")
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def validaUpdate(funcao):

    def valida(cpf, nome, data_nascimento):

        global clientes

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

    global clientes

    for cliente in clientes:
        if cpf == cliente["cpf"]:

            if nome != "":
                cliente["nome"] = nome

            if data_nascimento != "":
                cliente["data_nascimento"] = data_nascimento

            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

@validaUpdate
def updateClienteByNome(cpf, nome, data_nascimento):

    global clientes

    for cliente in clientes:
        if nome == cliente["nome"]:

            if cpf != "":
                for cliente_aux in clientes:
                    if cliente_aux == cpf:
                        return STATUS_CODE["CLIENTE_EXISTENTE"]
                    
                cliente["cpf"] = cpf

            if data_nascimento != "":
                cliente["data_nascimento"] = data_nascimento

            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def getCliente(cpf, retorno):

    global clientes

    for cliente in clientes:
        if cpf == cliente["cpf"]:
            retorno.update(cliente)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def showClientes():

    global clientes

    if not clientes:
        return STATUS_CODE["CLIENTE_NENHUM_CADASTRADO"] # Não há clientes cadastrados

    for cliente in clientes:
        print("\n", end="")
        for atributo, valor in cliente.items():
            print(f"{atributo}: {valor}")
        print("\n", end="")

    return STATUS_CODE["SUCESSO"] # Sucesso

def showClientesByNome(nome):

    global clientes
    flag = False
    
    for cliente in clientes:
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

    from ..venda.venda import checkClienteVenda

    global lista_cliente

    for cliente in clientes:
        if cpf == cliente["cpf"]:
            
            flag = checkClienteVenda(cliente["cpf"])

            if flag == STATUS_CODE["SUCESSO"]:
                return STATUS_CODE["CLIENTE_CADASTRADO_EM_VENDA"]

            clientes.remove(cliente)
            return STATUS_CODE["SUCESSO"] # Sucesso
        
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

def limpaClientes():
    global clientes, cont_id
    cont_id = 1
    clientes.clear()

