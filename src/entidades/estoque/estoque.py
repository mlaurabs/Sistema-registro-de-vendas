from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = ["createProdutoNoEstoque", "atualizaQtdEstoque", "showEstoque", "getProdutoEstoque", 
           "deleteProdutoEstoque", "limpaEstoque", "salvarEstoques", "carregarEstoques","iniciarEstoques", "encerrarEstoques" ]

# Lista global para armazenar os produtos no estoques
estoques = []
cont_id = 1

# Caminhos dos arquivos
arquivo_utf32 = Path("dados/estoque/relatorio_estoque_utf32.txt")
arquivo_utf8 = Path("dados/estoque/relatorio_estoque_utf8.txt")

def salvarEstoques():
    global arquivo_utf32
    global estoques  # A lista de produtos

    print("Salvando estoque...")  # Log inicial

    try:
        with open(arquivo_utf32, "wb") as arquivo:
            # Escrever o BOM (Byte Order Mark) para UTF-32-LE
            bom = 0x0000FEFF
            bom_bytes = bom.to_bytes(4, byteorder="little")
            arquivo.write(bom_bytes)

            for estoque in estoques:
                print(f"Estoque atual: {estoque}")  # Log por produto

                # Construir a string do produto
                atributos = [
                    f'id_produto:{estoque["id_produto"]}',
                    f'quantidade:{estoque["quantidade"]}',
                ]

                # Concatenar a linha completa
                linha = " - ".join(atributos) + "\n"
                
                # Escrever a linha no arquivo em UTF-32-LE
                arquivo.write(linha.encode("utf-32-le"))

        print("Salvo.")  # Log final
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao salvar estoque: {e}")
        return STATUS_CODE["ERRO"]

import converteutf832  # Certifique-se de que o módulo está importado

def carregarEstoques():
    global arquivo_utf32
    global arquivo_utf8
    global estoques,  cont_id # A lista de produtos

    print("Iniciando carregamento de estoque...")
    
    converteutf832.convUtf32p8(str(arquivo_utf32), str(arquivo_utf8))
    try:    
        # Lê o arquivo convertido para UTF-8
        with open(arquivo_utf8, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
            if not conteudo:  # Verifica se o conteúdo está vazio
                print("Arquivo UTF-32 está vazio.")
                estoques = []
                cont_id = 1
                return STATUS_CODE["SUCESSO"]
            # Processa cada linha de produtos
            linhas = conteudo.split("\n")
            estoques.clear()
            for linha in linhas:
                if linha.strip():  # Ignora linhas vazias
                    # Divide os atributos pelo separador " - "
                    partes = linha.split(" - ")
                    estoque = {
                        "id_produto": int(partes[0].split(":")[1]),
                        "quantidade": partes[1].split(":")[1],
                    }
                    estoques.append(estoque)
        
        # Atualiza o próximo ID
        cont_id = max((estoque["id_produto"] for estoque in estoques), default=0) + 1
        print("Estoque carregado com sucesso:", estoques)
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao carregar estoque: {e}")
        return STATUS_CODE["ERRO"]

def iniciarEstoques():
    print("Iniciando módulo de Estoque...")
    carregarEstoques()
    print()

def encerrarEstoques():
    print("Encerrando módulo de Estoque...")
    salvarEstoques()
    print()

def createProdutoNoEstoque(id_produto):
    """
    Adiciona um novo produto ao estoques com quantidade inicial de 0.
    """
    global estoques

    from ..produto.produto import getProdutoById

    # Dicionário para armazenar os dados do produto retornado
    produto = {}

    # Busca o produto no módulo de produtos
    status = getProdutoById(id_produto, produto)
    if status != STATUS_CODE["SUCESSO"]:
        return status  # Retorna o status de erro se o produto não for encontrado

    # Adiciona o produto ao estoques
    estoques.append({
        "id_produto": produto["id"],
        "quantidade": 0  # Inicializa a quantidade no estoques
    })
    print(estoques)
    return STATUS_CODE["SUCESSO"]  # Retorna sucesso

def atualizaQtdEstoque(id_produto, quantidade):
    """
    Atualiza o estoques de um produto.
    - Adiciona se a quantidade for positiva.
    - Remove se a quantidade for negativa, desde que não deixe o estoques negativo.
    - Retorna erro se o produto não estiver no estoques ou se não houver itens suficientes.
    """
    global estoques
    # Verifica se o produto existe no estoques
    for item in estoques:
        if item["id_produto"] == id_produto:
            if quantidade < 0:  # Remoção de estoques
                if int( item["quantidade"]) == 0:
                    return STATUS_CODE["estoques_INSUFICIENTE"]  # Não há itens no estoques para reduzir
                if int( item["quantidade"]) + quantidade < 0:  # Checa se a redução deixa o estoques negativo
                    return STATUS_CODE["estoques_INSUFICIENTE"]
            item["quantidade"] = str(int(item["quantidade"]) + quantidade)  # Atualiza a quantidade
            print(item["quantidade"])
            return STATUS_CODE["SUCESSO"]  # Operação bem-sucedida
    return STATUS_CODE["estoques_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

def showEstoque():

    global estoques

    """
    Exibe todos os produtos no estoques.
    """
    if not estoques:
        return STATUS_CODE["estoques_NENHUM_CADASTRO"]

    for item in estoques:
        print(
            f"ID: {item['id_produto']}, "
            f"Quantidade: {item['quantidade']}, "
        )

    return STATUS_CODE["SUCESSO"]

def getProdutoEstoque(id_produto, retorno):
    """
    Busca um produto no estoques pelo ID.
    Atualiza o dicionário 'retorno' com os detalhes do produto, se encontrado.
    """
    global estoques

    # Percorre o estoques para buscar o produto
    for item in estoques:
        if item["id_produto"] == id_produto:
            retorno.update(item)  # Atualiza o dicionário de retorno com os detalhes do produto
            return STATUS_CODE["SUCESSO"]  # Produto encontrado

    return STATUS_CODE["estoques_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

def deleteProdutoEstoque(id_produto):
    
    global estoques

    for item in estoques:
        if item["id_produto"] == id_produto:
            estoques.remove(item)

    return STATUS_CODE["SUCESSO"]

def limpaEstoque():
    global estoques
    estoques.clear()

