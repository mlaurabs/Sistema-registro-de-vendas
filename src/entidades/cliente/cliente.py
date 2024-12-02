from src.status_code import STATUS_CODE
from pathlib import Path
from datetime import datetime

__all__ = ["createCliente", "showCliente", "updateClienteByCpf", "updateClienteByNome", "getCliente", "showClientes", "showClientesByNome", "deleteCliente",  "limpaClientes", "salvarclientes", "carregarclientes", "encerrarclientes", "iniciarclientes"]

'''

Objetivo: 
Validar a data de nascimento de um cliente, verificando se a data é válida e se o cliente é maior de idade.

Descrição:
- A função tenta converter a data de nascimento fornecida em formato de string para um objeto `datetime`.
- Se a conversão falhar, retorna uma mensagem de erro indicando que a data é inválida.
- Se a data for válida, a função calcula a idade do cliente e verifica se ele é maior de idade.
- Se o cliente for menor de 18 anos, a função retorna um erro indicando que o cliente é menor de idade.

Acoplamento:
- Data de nascimento do cliente.

Retornos esperados:
- Mensagem de erro caso a data seja inválida.
- Mensagem de erro caso o cliente seja menor de idade.
- Mensagem de sucesso caso a data seja válida e o cliente seja maior de idade.

Assertivas de entrada:
- A entrada deve ser uma string no formato 'dd/mm/aaaa'.

Assertivas de saída:
- A função retornará um código de status indicando se a data é válida e se o cliente é maior de idade.



'''

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

'''

Objetivo: 
Validar o CPF de um cliente, verificando se ele segue o formato correto.

Descrição:
- A função verifica se o CPF possui exatamente 14 caracteres e se os pontos e hífen estão nas posições corretas.
- Se o formato estiver incorreto, a função retorna um código de erro indicando o problema.
- Se o CPF estiver correto, a função retorna uma mensagem de sucesso.

Acoplamento:
- CPF do cliente.

Retornos esperados:
- Mensagem de erro caso o CPF não tenha o formato correto.
- Mensagem de sucesso caso o CPF esteja no formato correto.

Assertivas de entrada:
- O CPF deve ser uma string no formato 'xxx.xxx.xxx-xx', onde 'x' é um dígito numérico.

Assertivas de saída:
- A função retornará um código de status indicando se o CPF está no formato correto.

'''

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

'''

Objetivo
- Validar os valores passados para a função createCliente.

Descrição
- A função será um wrapper que verifica se os valores fornecidos obedecem às regras estabelecidas:
  - CPF, nome e data de nascimento são obrigatórios.
  - Nome não pode ter mais de 50 caracteres e deve conter apenas letras e espaços.
  - O CPF deve estar em um formato válido.
  - A data de nascimento deve ser válida e indicar que o cliente tem pelo menos 18 anos.
  - Não pode existir um cliente com o mesmo CPF no sistema.

Acoplamento
- CPF do cliente.
- Nome e data de nascimento do cliente.
- Função `validaCpf` para validação do CPF.
- Função `validaDataNascimento` para validação da data de nascimento.
- Função createCliente.

Retornos esperados
- Mensagem de erro indicando qual elemento obrigatório está vazio.
- Mensagem de erro indicando qual elemento está no formato incorreto.
- Mensagem indicando que o cliente já existe no sistema.
- Execução da função createCliente em caso de sucesso.

Assertivas de entrada
- O CPF deve ser fornecido como uma string no formato `XXX.XXX.XXX-XX`.
- O nome deve ser uma string contendo apenas letras e espaços, com no máximo 50 caracteres.
- A data de nascimento deve ser uma string no formato `DD/MM/AAAA`.

Assertivas de saída
- Retorno de erro identificando campos obrigatórios vazios.
- Retorno de erro para CPF em formato inválido.
- Retorno de erro para nomes com caracteres ou tamanho incorretos.
- Retorno de erro para data de nascimento inválida ou menoridade.
- Retorno de erro indicando cliente já existente no sistema.
- Execução bem-sucedida da função createCliente em caso de validação correta.

'''

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


"""Descrição
-Gera um relatório com os clientes cadastrados no sistema, armazenando os dados em um arquivo .txt codificado em UTF-32

Objetivo
-Criar um arquivo para armazenamento ou auditoria dos clientes registrados

Acoplamento
-Lista global clientes
-Arquivo no caminho especificado

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Relatório gerado com sucesso

Assertivas de Entrada
-O diretório do arquivo deve existir

Assertivas de Saída
-Um arquivo .txt será gerado com as informações dos clinetes cadastrados"""
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

"""
Descrição
-A partir de um relatório .txt em UTF-32, é feito a conversão em UFT-8, e o arquivo de sáida com os clientes registrados é lido e os adiciona à lista clientes

Objetivo
-Permitir a importação de dados previamente armazenados

Acoplamento
-Arquivo .txt com os dados dos clientes registrados

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Relatório lido e clientes importados com sucesso

Assertivas de Entrada
-O arquivo .txt deve existir e estar no formato correto (UTF-32)

Assertivas de Saída
-Os clintes serão adicionados à lista clientes
"""
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

"""Descrição
- Executa o procedimento padrão para iniciar o uso de um módulo

Objetivo
- Carregar os dados previamente armazendados e carregá-los na estutura de dados do módulo

Assertivas de Saída
-O módulos será inciados com seus dados previamente carregados"""
def iniciarclientes():
    print("Iniciando módulo de cliente...")
    carregarclientes()

"""Descrição
- Executa o procedimento padrão para encerrar o uso de um módulo

Objetivo
- Salva os dados registrados na estrutura do módulo durante a sessão

Assertivas de Saída
-Sera criado um arquivo .txt UTF-32 que contem os dados registrados"""
def encerrarclientes():
    print("Encerrando módulo de cliente...")
    salvarclientes()



'''

Descrição
- Antes de executar a função, os dados passam por um wrapper que os valida
- Um cliente será criado com os parâmetros passados
- O cliente será adicionado na lista de clientes cadastrados

Acoplamento
- CPF do cliente
- Nome do cliente
- Data de nascimento do cliente

Retornos esperados
- Mensagem de sucesso caso o cliente seja cadastrado no sistema

Assertivas de entrada
- CPF deve ser uma string no formato válido (somente números, com 11 dígitos)
- Nome deve ser uma string
- Data de nascimento deve ser uma string no formato 'DD/MM/AAAA'

Assertivas de saída
- O cliente será adicionado à lista que armazena todos os clientes cadastrados


'''
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

'''

Descrição
- A função procura um cliente pelo seu CPF em uma lista que armazena todos os clientes cadastrados.
- São exibidos os atributos e os valores do cliente, caso ele seja encontrado.

Acoplamento
- O CPF do cliente.

Retornos esperados
- Indicação de que o cliente foi encontrado e exibido.
- Erro indicando que o cliente não foi encontrado.

Assertivas de entrada
- O CPF deve ser uma string no formato `XXX.XXX.XXX-XX`.

Assertivas de saída
- Os dados do cliente serão exibidos na interface, caso ele seja encontrado.


'''
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


'''

Objetivo
- Validar os valores passados para a função updateCliente.

Descrição
- A função será um wrapper que irá verificar se os valores passados obedecem a regras específicas.
- Todos os atributos podem ser nulos.
- O CPF deve estar no formato correto.
- O nome não pode ter mais que 50 caracteres e deve conter apenas caracteres alfabéticos.
- A data de nascimento deve estar no formato correto e indicar uma idade maior ou igual a 18 anos.

Acoplamento
- CPF do cliente.
- Nome do cliente.
- Data de nascimento do cliente.

Retornos esperados
- Uma mensagem indicando qual elemento está no formato errado.
- Função updateCliente.

Assertivas de entrada
- CPF deve ser uma string no formato `XXX.XXX.XXX-XX` ou vazio.
- Nome deve ser uma string contendo apenas letras ou vazio.
- Data de nascimento deve ser uma string no formato `DD/MM/AAAA` ou vazio.

Assertivas de saída
- Se algum dos elementos estiver no formato errado, a função retornará um erro que identifica qual.
- Em caso de sucesso, a função irá executar updateCliente.


'''
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

'''

Descrição:
- Antes de executar a função, os dados passam por um wrapper que os valida.
- Apenas os campos fornecidos serão atualizados; campos omitidos permanecem inalterados.

Acoplamento:
- CPF do cliente.
- Nome do cliente.
- Data de nascimento do cliente.

Retornos esperados:
- Mensagem de sucesso caso o cliente seja atualizado no sistema.
- Mensagem de erro caso o cliente não seja encontrado.

Assertivas de entrada:
- O CPF deve ser uma string válida e existente na lista de clientes.
- Nome deve ser uma string ou "" para indicar ausência de alteração.
- Data de nascimento deve ser uma string ou "" para indicar ausência de alteração.

Assertivas de saída: 
- Os campos informados (nome e/ou data de nascimento) serão atualizados na lista de clientes.
- Nenhuma alteração será realizada caso o CPF não seja encontrado.

'''
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

'''

Descrição:
- Antes de executar a função, os dados passam por um wrapper que os valida.
- Apenas os campos fornecidos serão atualizados; campos omitidos permanecem inalterados.
- O CPF será atualizado somente se não for duplicado na lista.

Acoplamento:
- Nome do cliente.
- CPF do cliente.
- Data de nascimento do cliente.

Retornos esperados:
- Mensagem de sucesso caso o cliente seja atualizado no sistema.
- Mensagem de erro caso o CPF já esteja registrado para outro cliente.
- Mensagem de erro caso o cliente não seja encontrado.

Assertivas de entrada:
- O nome deve ser uma string válida e existente na lista de clientes.
- CPF deve ser uma string única ou "" para indicar ausência de alteração.
- Data de nascimento deve ser uma string ou "" para indicar ausência de alteração.

Assertivas de saída: 
- Os campos informados (CPF e/ou data de nascimento) serão atualizados na lista de clientes.
- Nenhuma alteração será realizada caso o nome não seja encontrado ou o CPF seja duplicado.


'''
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


'''

Objetivo: 
Buscar um cliente na lista de clientes cadastrados utilizando o CPF como identificador.

Descrição:
- A função procura um cliente, pelo CPF, numa lista que armazena todos os clientes cadastrados.
- Se encontrado, os dados do cliente são retornados por meio de um parâmetro recebido.

Acoplamento:
- O CPF do cliente.
- A variável onde será retornado o cliente.

Retornos esperados:
- Indicação de que o cliente foi encontrado e os dados retornados.
- Erro indicando que o cliente não foi encontrado.

Assertivas de entrada:
- O CPF deve ser uma string.
- O retorno deve ser um dicionário.

Assertivas de saída:
- A variável retorno será preenchida com os valores do cliente, caso seja encontrado.


'''
def getCliente(cpf, retorno):

    global clientes

    for cliente in clientes:
        if cpf == cliente["cpf"]:
            retorno.update(cliente)
            return STATUS_CODE["SUCESSO"] # Sucesso
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"] # Cliente não encontrado

'''

Objetivo: 
Exibir todos os clientes cadastrados no sistema.

Descrição:
- A função irá procurar e imprimir todos os clientes cadastrados.

Retornos esperados:
- Indicação de que os clientes foram encontrados e exibidos.
- Erro indicando que nenhum cliente foi encontrado.

Assertivas de saída:
- Os clientes serão exibidos na interface, caso sejam encontrados.

'''
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

'''

Objetivo: 
Exibir todos os clientes cadastrados cujo nome contenha uma sequência específica de caracteres.

Descrição:
- A função irá procurar e imprimir todos os clientes cadastrados que possuem em seu nome a sequência de caracteres especificada.

Acoplamento:
- O nome do cliente que deseja-se buscar.

Retornos esperados:
- Indicação de que os clientes foram encontrados e exibidos.
- Erro indicando que nenhum cliente foi encontrado.

Assertivas de entrada:
- O nome deve ser uma string.

Assertivas de saída:
- Os clientes serão exibidos na interface, caso sejam encontrados.

'''
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

'''

Objetivo: 
Remover um cliente do sistema com base no CPF informado.

Descrição:
- Um cliente, identificado pelo seu CPF, será removido do sistema.
- O cliente não poderá ser removido se estiver cadastrado em alguma venda.

Acoplamento:
- CPF do cliente.

Retornos esperados:
- Mensagem de sucesso caso o cliente seja removido do sistema.
- Mensagem de erro caso o cliente não seja encontrado.
- Mensagem de erro caso o cliente esteja cadastrado em uma venda.

Assertivas de entrada:
- CPF deve ser uma string.

Assertivas de saída: 
- Caso esteja dentro das condições estabelecidas, o cliente será removido da lista de clientes.


'''
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

