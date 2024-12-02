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

"""Descrição
-Gera um relatório com os produtos cadastrados no estoque, armazenando os dados em um arquivo .txt codificado em UTF-32

Objetivo
-Criar um arquivo para armazenamento ou auditoria dos produtos do estoque

Acoplamento
-Lista global estoque
-Arquivo no caminho especificado

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Relatório gerado com sucesso

Assertivas de Entrada
-O diretório do arquivo deve existir

Assertivas de Saída
-Um arquivo .txt será gerado com as informações do estoque"""
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
"""
Descrição
-A partir de um relatório .txt em UTF-32, é feito a conversão em UFT-8, e o arquivo de sáida com os produtos do estoque é lido e os adiciona à lista estoque

Objetivo
-Permitir a importação de dados previamente armazenados

Acoplamento
-Arquivo .txt com os dados do estoque

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Relatório lido e estoque importado com sucesso

Assertivas de Entrada
-O arquivo .txt deve existir e estar no formato correto (UTF-32)

Assertivas de Saída
-Os produtos serão adicionados à lista estoque
"""
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
                        "quantidade": int(partes[1].split(":")[1]),
                    }
                    estoques.append(estoque)
        
        # Atualiza o próximo ID
        cont_id = max((estoque["id_produto"] for estoque in estoques), default=0) + 1
        return STATUS_CODE["SUCESSO"]
    except Exception as e:
        print(f"Erro ao carregar estoque: {e}")
        return STATUS_CODE["ERRO"]

"""Descrição
- Executa o procedimento padrão para iniciar o uso de um módulo

Objetivo
- Carregar os dados previamente armazendados e carregá-los na estutura de dados do módulo

Assertivas de Saída
-O módulos será inciados com seus dados previamente carregados"""
def iniciarEstoques():
    print("Iniciando módulo de Estoque...")
    carregarEstoques()

"""Descrição
- Executa o procedimento padrão para encerrar o uso de um módulo

Objetivo
- Salva os dados registrados na estrutura do módulo durante a sessão

Assertivas de Saída
-Sera criado um arquivo .txt UTF-32 que contem os dados registrados"""
def encerrarEstoques():
    print("Encerrando módulo de Estoque...")
    salvarEstoques()

"""
Descrição
-Adiciona um novo produto ao estoque com quantidade inicial de 0. Os dados do produto são obtidos por meio do módulo de produtos

Objetivo
-Garantir que produtos registrados no sistema de produtos sejam incluídos no estoque

Acoplamento
-ID do produto
-Módulo de produtos para obter os dados do produto

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Produto adicionado ao estoque com sucesso
-Código de erro se o produto não for encontrado no módulo de produtos

Assertivas de Entrada
-id_produto deve ser um número inteiro

Assertivas de Saída
-Produto será adicionado à lista global estoque com quantidade inicial de 0
"""
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
    return STATUS_CODE["SUCESSO"]  # Retorna sucesso

'''
Descrição
-Atualiza a quantidade de um produto no estoque. Permite adicionar ou remover produtos

Objetivo
-Manter as quantidades no estoque atualizadas, tanto para reposição quanto para venda

Acoplamento
-ID do produto
-Quantidade a ser adicionada ou removida

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Quantidade atualizada com sucesso.
-STATUS_CODE["ESTOQUE_INSUFICIENTE"]: Tentativa de remover mais do que a quantidade disponível
-STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]: Produto não encontrado no estoque

Assertivas de Entrada
-id_produto deve ser um número inteiro
-quantidade deve ser um número inteiro (positivo ou negativo)

Assertivas de Saída
-A quantidade do produto no estoque será atualizada
-O estoque não deve ter valores negativos
'''
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
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]  # Não há itens no estoques para reduzir
                if item["quantidade"] + quantidade < 0:  # Checa se a redução deixa o estoques negativo
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]
            item["quantidade"] = item["quantidade"] + quantidade  # Atualiza a quantidade
            return STATUS_CODE["SUCESSO"]  # Operação bem-sucedida
    return STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

"""Descrição
-Exibe todos os produtos cadastrados no estoque e suas respectivas quantidades

Objetivo
-Permitir a visualização dos produtos no estoque para o usuário ou para auditoria

Acoplamento
-Lista global estoque

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Estoque exibido com sucesso
-STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]: Nenhum produto cadastrado no estoque

Assertivas de Saída
-Os detalhes de cada produto no estoque serão exibidos no terminal"""
def showEstoque():

    global estoques

    """
    Exibe todos os produtos no estoques.
    """
    if not estoques:
        return STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]

    for item in estoques:
        print(
            f"ID: {item['id_produto']}, "
            f"Quantidade: {item['quantidade']}, "
        )

    return STATUS_CODE["SUCESSO"]

'''
Descrição
-Busca um produto no estoque pelo seu ID e preenche o dicionário retorno com os dados do produto

Objetivo
-Fornecer acesso rápido às informações de um produto específico no estoque

Acoplamento
-ID do produto
-Dicionário retorno para preenchimento das informações

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Produto encontrado e dicionário preenchido
-STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]: Produto não encontrado no estoque

Assertivas de Entrada
-id_produto deve ser um número inteiro
-retorno deve ser um dicionário vazio

Assertivas de Saída
-O dicionário será preenchido com as informações do produto
-Retornará um código de erro se o produto não for encontrado
'''
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

    return STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

'''
Descrição
-Remove um produto do estoque com base no seu ID

Objetivo
-Excluir produtos do estoque que não são mais necessários

Acoplamento
-ID do produto

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Produto removido do estoque

Assertivas de Entrada
-id_produto deve ser um número inteiro

Assertivas de Saída
-O produto será removido da lista estoque
'''
def deleteProdutoEstoque(id_produto):
    
    global estoques

    for item in estoques:
        if item["id_produto"] == id_produto:
            estoques.remove(item)

    return STATUS_CODE["SUCESSO"]

'''
Descrição
-Remove todos os produtos do estoque

Objetivo
-Realizar uma limpeza completa no estoque, útil para reinicialização ou auditoria

Acoplamento:
-Lista global estoque

Assertivas de Saída
-A lista estoque estará vazia
'''
def limpaEstoque():
    global estoques
    estoques.clear()

