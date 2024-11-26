import os
from datetime import datetime
from src.status_code import STATUS_CODE, getStatusName

from pathlib import Path
import sys

caminho_relativo = Path("src/entidades/venda/venda.py")
caminho_absoluto = caminho_relativo.resolve()

sys.path.append(caminho_absoluto.parent)

from entidades.produto.produto import getProdutoById
# from entidades.produto.cliente import ...
from entidades.produto.estoque import atualizarQtdEstoque, getProdutoEstoque, getQuantidadeEstoque

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

def registrarVendasNoArquivo(vendas):
    """
    Reescreve o arquivo com todas as vendas em formato persistido.
    """
    with open("vendas.txt", "w", encoding="utf-8") as file:
        for venda in vendas.values():
            produtos = venda["produtos"]
            produtos_str = str(produtos).replace("'", "\"")
            linha = f"{venda['id']}|{venda['cpf']}|{venda['data']}|{venda['hora']}|{venda['status']}|{produtos_str}\n"
            file.write(linha)

def carregarVendasDoArquivo():
    """
    Carrega as vendas previamente registradas no arquivo vendas.txt.
    Retorna um dicionário com as vendas carregadas.
    """
    vendas = {}
    if os.path.exists("vendas.txt"):
        with open("vendas.txt", "r", encoding="utf-8") as file:
            for linha in file:
                id_venda, cpf, data, hora, status, produtos = linha.strip().split("|")
                vendas[int(id_venda)] = {
                    "id": int(id_venda),
                    "cpf": cpf,
                    "data": data,
                    "hora": hora,
                    "status": status,
                    "produtos": eval(produtos) if produtos else {}
                }
    return vendas

# Estrutura para armazenar as vendas em memória
vendas = carregarVendasDoArquivo()

# Funções principais
def getVendaPorId(id_venda):
    return vendas.get(id_venda, None)

def createVenda(cpf_cliente, data, hora):
    data_formatada, hora_formatada = formatarDataHora(data, hora)

    if not data_formatada:
        return STATUS_CODE["DATA_FORMATO_INVALIDO"]
    if not hora_formatada:
        return STATUS_CODE["HORA_FORMATO_INVALIDO"]

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
    registrarVendasNoArquivo(vendas)

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
        estoque.atualizarQtdEstoque(produto_id, -quantidade)

    venda["status"] = "concluída"
    registrarVendasNoArquivo(vendas)
    return STATUS_CODE["VENDA_CONCLUIDA"]

def addProduto(id_venda, id_produto, quantidade):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    if produto.getProdutoById(id_produto) == STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]:
        return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
    if estoque.getProdutoEstoque(id_produto) == STATUS_CODE["PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]:
        return STATUS_CODE["PRODUTO_NAO_ENCONTRADO_ESTOQUE"]
    if estoque.getQuantidadeEstoque(id_produto) < quantidade:
        return STATUS_CODE["ESTOQUE_INSUFICIENTE"]

    venda["produtos"][id_produto] = venda["produtos"].get(id_produto, 0) + quantidade
    registrarVendasNoArquivo(vendas)
    return STATUS_CODE["PRODUTO_ADICIONADO"]

def removeProduto(id_venda, id_produto, quantidade):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    if id_produto not in venda["produtos"] or venda["produtos"][id_produto] < quantidade:
        return STATUS_CODE["PRODUTO_NAO_INCLUIDO"]

    venda["produtos"][id_produto] -= quantidade
    if venda["produtos"][id_produto] == 0:
        del venda["produtos"][id_produto]

    registrarVendasNoArquivo(vendas)
    return STATUS_CODE["PRODUTO_REMOVIDO"]

def showVenda(id_venda):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return venda

def showVendas():
    if not vendas:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return vendas

def showVendasCliente(cpf):
    vendas_cliente = [venda for venda in vendas.values() if venda["cpf"] == cpf]
    if not vendas_cliente:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return vendas_cliente

def showVendasData(data):
    vendas_data = [venda for venda in vendas.values() if venda["data"] == data]
    if not vendas_data:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    return vendas_data

def updateVenda(id_venda, data, hora):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

    data_formatada, hora_formatada = formatarDataHora(data, hora)
    if not data_formatada:
        return STATUS_CODE["DATA_FORMATO_INVALIDO"]
    if not hora_formatada:
        return STATUS_CODE["HORA_FORMATO_INVALIDO"]

    venda["data"] = data_formatada
    venda["hora"] = hora_formatada
    registrarVendasNoArquivo(vendas)

    return STATUS_CODE["VENDA_ALTERADA"]

def checkProdutoVenda(id_produto):
    for venda in vendas.values():
        if id_produto in venda["produtos"]:
            return STATUS_CODE["PRODUTO_ENCONTRADO_EM_VENDAS"]
    return STATUS_CODE["PRODUTO_NAO_ENCONTRADO_EM_VENDAS"]

def checkClienteVenda(cpf_cliente):
    for venda in vendas.values():
        if venda["cpf"] == cpf_cliente:
            return STATUS_CODE["CLIENTE_ENCONTRADO"]
    return STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]

def deleteVenda(id_venda):
    venda = getVendaPorId(id_venda)
    if not venda:
        return STATUS_CODE["VENDA_NAO_ENCONTRADA"]
    if venda["status"] == "concluída":
        return STATUS_CODE["VENDA_JA_CONCLUIDA"]

    del vendas[id_venda]
    registrarVendasNoArquivo(vendas)
    return STATUS_CODE["VENDA_REMOVIDA"]