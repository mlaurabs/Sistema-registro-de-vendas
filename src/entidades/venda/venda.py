import re
from datetime import datetime
from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = [
    "createVenda", "concludeVenda", "cancelaVenda", "addProduto", "removeProduto", "showVenda", "showVendas",
    "showVendasCliente", "showVendasData", "updateVenda", "checkProdutoVenda", "checkClienteVenda", "deleteVenda"
]

def formatarData(data):
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        return data_formatada
    except ValueError:
        return None
    
def formatarHora(hora):
    try:
        hora_formatada = datetime.strptime(hora, "%H:%M").strftime("%H:%M")
        return hora_formatada
    except ValueError:
        return None

def validarCPF(cpf):
    """
    Valida se o CPF segue o formato 123.456.789-09 ou é uma string vazia.
    
    :param cpf: CPF a ser validado
    :type cpf: str
    :return: True se o CPF for válido ou vazio, False caso contrário
    :rtype: bool
    """
    if not cpf:  # Verifica se é uma string vazia
        return True

    # Expressão regular para validar o formato do CPF
    cpf_pattern = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return bool(re.match(cpf_pattern, cpf))

def validaCreate(funcao):

    def valida(cpf_cliente, data, hora):

        cpf_formatado = validarCPF(cpf_cliente)
        if not cpf_formatado:
            return STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"]

        data_formatada = formatarData(data)
        if not data_formatada:
            return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]
        
        hora_formatada = formatarHora(hora)
        if not hora_formatada:
            return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]
        
        return funcao(cpf_formatado, data_formatada, hora_formatada)

    return valida

def validaUpdate(funcao):

    def valida(id_venda, data, hora):

        data_formatada = formatarData(data)
        if not data_formatada:
            return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]

        hora_formatada = formatarHora(hora)
        if not hora_formatada:
            return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]

        return funcao(id_venda, data, hora)

    return valida

# Estrutura para armazenar as vendas em memória
vendas = {}

# Funções principais
def getVenda(id_venda, retorno):

    if retorno == None:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    retorno.update(vendas.get(id_venda, None))
    return STATUS_CODE["SUCESSO"]

@validaCreate
def createVenda(cpf_cliente, data, hora):

    # Confere se já não existe a venda
    for venda in vendas.values():
        if venda["cpf"] == cpf_cliente and venda["data"] == data and venda["hora"] == hora:
            return STATUS_CODE["VENDA_EXISTENTE"]

    # Delimita o id da venda
    id_venda = len(vendas) + 1

    # Cria a nova venda
    nova_venda = {
        "id": id_venda,
        "cpf": cpf_cliente,
        "data": data,
        "hora": hora,
        "status": "em processamento",
        "produtos": {}
    }

    # Registra a nova venda
    vendas[id_venda] = nova_venda

    return STATUS_CODE["SUCESSO"]

def concludeVenda(id_venda):

    from ..estoque.estoque import atualizaQtdEstoque

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag
    
    # Se a venda já estiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda já estiver sido cancelada
    if venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    # Atualiza a quantidade no estoque
    for produto_id, quantidade in venda["produtos"].items():
        flag = atualizaQtdEstoque(produto_id, -quantidade)
        # Se não houverem unidades suficientes
        if flag != STATUS_CODE["SUCESSO"]:
            return flag

    # Marca a venda como concluída
    venda["status"] = "concluída"

    return STATUS_CODE["SUCESSO"]

def cancelaVenda(id_venda):

    from ..estoque.estoque import atualizaQtdEstoque

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag
    
    # Se a venda já estiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    
    # Se a venda já estiver sido cancelada
    if venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_JA_CANCELADA"]

    # Atualiza a quantidade no estoque
    for produto_id, quantidade in venda["produtos"].items():
        flag = atualizaQtdEstoque(produto_id, -quantidade)
        # Se não houverem unidades suficientes
        if flag != STATUS_CODE["SUCESSO"]:
            return flag

    # Marca a venda como cancelada
    venda["status"] = "cancelada"

    return STATUS_CODE["SUCESSO"]

def addProduto(id_venda, id_produto, quantidade):

    from ..produto.produto import getProdutoById
    from ..estoque.estoque import getProdutoEstoque

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag

    # Pega o produto
    produto = dict()
    flag = getProdutoById(id_produto, produto)

    # Se o produto não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag
    
    # Pega o produto no estoque
    produto_estoque = dict()
    getProdutoEstoque(id_produto, produto_estoque)

    # Se não houverem unidades suficientes
    if produto_estoque["quantidade"] < quantidade:
        return STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"]

    # Altera a quantidade daquele produto na venda
    venda["produtos"][id_produto] = venda["produtos"].get(id_produto, 0) + quantidade

    return STATUS_CODE["SUCESSO"]
    
def removeProduto(id_venda, id_produto, quantidade):

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag

    # Se o produto não estiver incluído na venda
    if id_produto not in venda["produtos"] or venda["produtos"][id_produto] < quantidade:
        return STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"]

    # Altera a quantidade do produto na venda
    venda["produtos"][id_produto] -= quantidade
    
    if venda["produtos"][id_produto] == 0:
        del venda["produtos"][id_produto]

    return STATUS_CODE["SUCESSO"]

def showVenda(id_venda):

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag

    # Imprime a venda
    print("\n", end="")
    for atributo,valor in venda.items():
        print(f"{atributo}: {valor}")
    print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendas():

    # Se não houver vendas cadastradas
    if not vendas:
        return STATUS_CODE["VENDA_NENHUM_CADASTRO"]

    # Imprime as vendas
    for venda in vendas.values():
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendasCliente(cpf):

    # Pega as vendas do cliente
    vendas_cliente = [venda for venda in vendas.values() if venda["cpf"] == cpf]

    # Se não houverem vendas do cliente
    if not vendas_cliente:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    # Imprime as vendas
    for venda in vendas_cliente:
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendasData(data):

    # Pega as vendas na data
    vendas_data = [venda for venda in vendas.values() if venda["data"] == data]

    # Se não houverem vendas na data
    if not vendas_data:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    # Imprime as vendas
    for venda in vendas_data.values():
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

@validaUpdate
def updateVenda(id_venda, data, hora):

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag

    # Altera data e hora
    venda["data"] = data
    venda["hora"] = hora

    return STATUS_CODE["SUCESSO"]

def checkProdutoVenda(id_produto):

    # Procura produto nas vendas
    for venda in vendas.values():
        if id_produto in venda["produtos"]:
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"]

def checkClienteVenda(cpf_cliente):

    # Procura o cliente nas vendas
    for venda in vendas.values():
        if venda["cpf"] == cpf_cliente:
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"]

def deleteVenda(id_venda):

    # Pega a venda
    venda = dict()
    flag = getVenda(id_venda, venda)

    # Se a venda não existir
    if flag != STATUS_CODE["SUCESSO"]:
        return flag
    
    # Se a venda tiver sido concluída
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]

    # Deleta a venda
    del vendas[id_venda]

    return STATUS_CODE["SUCESSO"]

# Funções de Relatório
def geraRelatorioVenda():
    global vendas

    caminho_relativo = Path("dados/vendas/relatorio_venda_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000  # Byte Order Mark para UTF-32 LE
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, venda in enumerate(vendas.values()):
        string = ""

        for chave, valor in venda.items():
            if chave == "produtos":
                # Serializa o dicionário de produtos no formato id:quantidade;id:quantidade
                produtos_str = ";".join([f"{id}:{quantidade}" for id, quantidade in valor.items()])
                string += produtos_str + ','
            else:
                string += str(valor) + ','

        if indice != len(vendas) - 1:
            string = string[:-1] + '-'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]

def lerRelatorioVenda():
    global vendas

    venda_template = {
        "id": None, "cpf": None, "data": None, "hora": None,
        "status": None, "produtos": {}
    }

    caminho_relativo = Path("dados/vendas/relatorio_venda_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "rb")

    arquivo.read(4)  # Ignorar cabeçalho UTF-32
    conteudo = arquivo.read()
    conteudo = conteudo.decode('utf-32-le')

    conteudo = conteudo.split('-')

    for linha in conteudo:
        if linha:
            linha = linha.strip()
            linha = linha.split(',')
            i = 0

            venda = venda_template.copy()

            for atributo in venda.keys():
                if atributo == "id":
                    venda[atributo] = int(linha[i])
                elif atributo == "produtos":
                    # Produtos são armazenados como um dicionário de pares id: quantidade
                    produtos = linha[i].split(';') if linha[i] else []
                    venda[atributo] = {int(prod.split(':')[0]): int(prod.split(':')[1]) for prod in produtos}
                else:
                    venda[atributo] = linha[i]
                i += 1

            vendas[venda["id"]] = venda

    arquivo.close()
    return STATUS_CODE["SUCESSO"]