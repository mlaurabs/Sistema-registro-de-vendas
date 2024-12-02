from datetime import datetime
from src.status_code import STATUS_CODE
from pathlib import Path
import converteutf832

# Encapsulamento
__all__ = [
    "getVenda", "createVenda", "concludeVenda", "cancelaVenda", "addProduto", "removeProduto", "showVenda", "showVendas",
    "showVendasCliente", "showVendasData", "updateVenda", "checkProdutoVenda", "checkClienteVenda", "deleteVenda", "limpaVendas", "salvarVendas", 
    "carregarVendas", "iniciarVendas", "encerrarVendas" 
]



# Funções auxiliares
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

# Funções de persitência de dados
# Lista de vendas e contador de IDs
vendas = []
cont_id = 1

# Caminhos dos arquivos
arquivo_utf32 = Path("dados/vendas/relatorio_venda_utf32.txt")
arquivo_utf8 = Path("dados/vendas/relatorio_venda_utf8.txt")

def salvarVendas():
    global arquivo_utf32
    global vendas
    print("Salvando vendas...")  # Log inicial

    try:
        with open(arquivo_utf32, "wb") as arquivo:
            # Escrever o BOM (Byte Order Mark) para UTF-32-LE
            bom = 0x0000FEFF
            bom_bytes = bom.to_bytes(4, byteorder="little")
            arquivo.write(bom_bytes)

            for venda in vendas:

                # Construir a string da venda
                atributos = [
                    f'id:{venda["id"]}',
                    f'data:{venda["data"]}',
                    f'hora:{venda["hora"]}',
                    f'status:{venda["status"]}'
                ]

                # Construir os produtos no formato {id de produto, quantidade, preco}
                produtos = " - ".join([
                    f'{{id:{produto["id"]}, quantidade:{produto["quantidade"]}, preco:{produto["preco"]}}}'
                    for produto in venda.get("produtos", [])
                ])

                # Concatenar a linha completa
                linha = " - ".join(atributos) + (f" - {produtos}" if produtos else "") + "\n"
                
                # Escrever a linha no arquivo em UTF-32-LE
                arquivo.write(linha.encode("utf-32-le"))

        print("Salvo")  # Log final
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao salvar vendas: {e}")
        return STATUS_CODE["ERRO"]

import converteutf832  # Certifique-se de que o módulo está importado

def carregarVendas():
    global arquivo_utf32
    global arquivo_utf8
    global vendas, cont_id

    print("Iniciando carregamento de vendas...")

    # Converte o arquivo UTF-32 para UTF-8 usando o módulo converteutf832
    converteutf832.convUtf32p8(str(arquivo_utf32), str(arquivo_utf8))
    
    try:
        with open(arquivo_utf8, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:  # Verifica se o conteúdo está vazio
                vendas = []
                cont_id = 1
                return STATUS_CODE["SUCESSO"]

            # Processa cada linha de vendas
            cont = 0
            linhas = conteudo.split("\n")
            vendas.clear()
            for linha in linhas:
                cont +=1
                if linha.strip():  # Ignora linhas vazias
                    # Divide os atributos pelo separador " - "
                    partes = linha.split(" - ")
                    venda = {
                        "id": int(partes[0].split(":")[1]),
                        "data": partes[1].split(":")[1],
                        "hora": partes[2].split(":")[1],
                        "status": partes[3].split(":")[1],
                        "produtos": []
                    }

                    # Processa os produtos, caso existam
                    for parte in partes[4:]:
                        if parte.startswith("{") and parte.endswith("}"):
                            # Remove as chaves e divide os atributos do produto
                            produto = parte[1:-1].split(", ")
                            produto_dict = {
                                atributo.split(":")[0]: (
                                    int(atributo.split(":")[1])
                                    if atributo.split(":")[0] != "preco"
                                    else float(atributo.split(":")[1])
                                )
                                for atributo in produto
                            }
                            venda["produtos"].append(produto_dict)

                    vendas.append(venda)

            # Atualiza o próximo ID
            cont_id = max((venda["id"] for venda in vendas), default=0) + 1

        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao carregar vendas: {e}")
        return STATUS_CODE["ERRO"]


def iniciarVendas():
    """
    Inicializa o módulo de vendas carregando os dados do arquivo.
    """
    print("Iniciando módulo de vendas...")
    carregarVendas()
    

def encerrarVendas():
    """
    Finaliza o módulo de vendas salvando os dados no arquivo UTF-32.
    """
    print("Encerrando módulo de vendas...")
    salvarVendas()
    

# Funções principais

def getVenda(id, retorno):

    global vendas

    for venda in vendas:
        if venda["id"] == id:
            retorno.update(venda)
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_NAO_ENCONTRADA"]

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
    if int(produto_estoque["quantidade"]) < quantidade:
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

def checkProdutoVenda(id_produto):

    global vendas

    # Procura produto nas vendas
    for venda in vendas:
        for produto in venda["produtos"]:
            if produto["id"] == id_produto:
                return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"]

def checkClienteVenda(cpf_cliente):

    global vendas

    # Procura o cliente nas vendas
    for venda in vendas:
        if venda["cpf"] == cpf_cliente:
            return STATUS_CODE["SUCESSO"]
        
    return STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"]

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

def limpaVendas():
    global vendas, cont_id
    cont_id = 1
    vendas.clear()
