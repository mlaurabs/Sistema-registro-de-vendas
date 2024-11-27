import re
from datetime import datetime
from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = [
    "createVenda", "concludeVenda", "addProduto", "removeProduto", "showVenda", "showVendas",
    "showVendasCliente", "showVendasData", "updateVenda", "checkProdutoVenda", "checkClienteVenda", "deleteVenda"
]

def formatarDataHora(data, hora):
    try:
        data_formatada = datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y")
        hora_formatada = datetime.strptime(hora, "%H:%M").strftime("%H:%M")
        return data_formatada, hora_formatada
    except ValueError:
        return None, None

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


# Estrutura para armazenar as vendas em memória
vendas = {}

# Funções principais
def getVendaPorId(id_venda):
    return vendas.get(id_venda, None)

def createVenda(cpf_cliente, data, hora):
    data_formatada, hora_formatada = formatarDataHora(data, hora)
    cpf_validate = validarCPF(cpf_cliente)

    if not cpf_validate:
        return STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"]

    if not data_formatada:
        return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]
    if not hora_formatada:
        return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]

    for venda in vendas.values():
        if venda["cpf"] == cpf_cliente and venda["data"] == data and venda["hora"] == hora:
            return STATUS_CODE["VENDA_EXISTENTE"]

    id_venda = len(vendas) + 1
    nova_venda = {
        "id": id_venda,
        "cpf": cpf_cliente,
        "data": data_formatada,
        "hora": hora_formatada,
        "status": "em processamento",
        "produtos": {}
    }

    vendas[id_venda] = nova_venda

    return STATUS_CODE["VENDA_CADASTRADA"]

def concludeVenda(id_venda):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]
    if venda["status"] == "cancelada":
        return STATUS_CODE["VENDA_CANCELADA"]

    for produto_id, quantidade in venda["produtos"].items():
        atualizarQtdEstoque(produto_id, -quantidade)

    venda["status"] = "concluída"
    return STATUS_CODE["VENDA_CONCLUIDA"]

def addProduto(id_venda, id_produto, quantidade):

    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    
    temp = dict()
    flag = getProdutoById(id_produto, temp)
    if flag == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        return flag
    
    prodEst = getProdutoEstoque(id_produto)
    if prodEst == STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]:
        return STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]
    
    if prodEst["quantidade"] < quantidade:
        return STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"]

    venda["produtos"][id_produto] = venda["produtos"].get(id_produto, 0) + quantidade
    return STATUS_CODE["VENDA_PRODUTO_ADICIONADO"]
    
def removeProduto(id_venda, id_produto, quantidade):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    if id_produto not in venda["produtos"] or venda["produtos"][id_produto] < quantidade:
        return STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"]

    venda["produtos"][id_produto] -= quantidade
    if venda["produtos"][id_produto] == 0:
        del venda["produtos"][id_produto]

    return STATUS_CODE["VENDA_PRODUTO_REMOVIDO"]

def showVenda(id_venda):

    venda = getVendaPorId(id_venda)

    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    
    print("\n", end="")
    for atributo,valor in venda.items():
        print(f"{atributo}: {valor}")
    print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendas():

    global vendas

    if not vendas:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    for venda in vendas.values():
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendasCliente(cpf):
    vendas_cliente = [venda for venda in vendas.values() if venda["cpf"] == cpf]

    if not vendas_cliente:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    for venda in vendas_cliente.values():
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

def showVendasData(data):
    vendas_data = [venda for venda in vendas.values() if venda["data"] == data]
    if not vendas_data:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    for venda in vendas_data.values():
        print("\n", end="")
        for atributo,valor in venda.items():
            print(f"{atributo}: {valor}")
        print("\n")

    return STATUS_CODE["SUCESSO"]

def updateVenda(id_venda, data, hora):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    data_formatada, hora_formatada = formatarDataHora(data, hora)
    if not data_formatada:
        return STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"]
    if not hora_formatada:
        return STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"]

    venda["data"] = data_formatada
    venda["hora"] = hora_formatada

    return STATUS_CODE["VENDA_ALTERADA"]

def checkProdutoVenda(id_produto):
    for venda in vendas.values():
        if id_produto in venda["produtos"]:
            return STATUS_CODE["VENDA_PRODUTO_ENCONTRADO"]
    return STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"]

def checkClienteVenda(cpf_cliente):
    for venda in vendas.values():
        if venda["cpf"] == cpf_cliente:
            return STATUS_CODE["VENDA_CLIENTE_ENCONTRADO"]
    return STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"]

def deleteVenda(id_venda):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]

    del vendas[id_venda]
    return STATUS_CODE["VENDA_REMOVIDA"]

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

if __name__ == "__main__":
    from ..produto.produto import getProdutoById
    from ..estoque.estoque import atualizarQtdEstoque, getProdutoEstoque, getQuantidadeEstoque