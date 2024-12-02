from src.status_code import STATUS_CODE
from pathlib import Path

__all__ = ["createProdutoNoEstoque", "atualizaQtdEstoque", "showEstoque", "getProdutoEstoque", 
           "deleteProdutoEstoque", "limpaEstoque", "geraRelatorioEstoque", "leRelatorioEstoque"]

# Lista global para armazenar os produtos no estoque
estoque = []

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

    global estoque

    from ..produto.produto import getProdutoById

    # Dicionário para armazenar os dados do produto retornado
    produto = {}

    # Busca o produto no módulo de produtos
    status = getProdutoById(id_produto, produto)
    if status != STATUS_CODE["SUCESSO"]:
        return status  # Retorna o status de erro se o produto não for encontrado

    # Adiciona o produto ao estoque
    estoque.append({
        "id_produto": produto["id"],
        "quantidade": 0  # Inicializa a quantidade no estoque
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

    global estoque

    # Verifica se o produto existe no estoque
    for item in estoque:
        if item["id_produto"] == id_produto:
            if quantidade < 0:  # Remoção de estoque
                if item["quantidade"] == 0:
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]  # Não há itens no estoque para reduzir
                if item["quantidade"] + quantidade < 0:  # Checa se a redução deixa o estoque negativo
                    return STATUS_CODE["ESTOQUE_INSUFICIENTE"]
            item["quantidade"] += quantidade  # Atualiza a quantidade
            return STATUS_CODE["SUCESSO"]  # Operação bem-sucedida

    return STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]  # Produto não encontrado

'''
Descrição
-Exibe todos os produtos cadastrados no estoque e suas respectivas quantidades

Objetivo
-Permitir a visualização dos produtos no estoque para o usuário ou para auditoria

Acoplamento
-Lista global estoque

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Estoque exibido com sucesso
-STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]: Nenhum produto cadastrado no estoque

Assertivas de Saída
-Os detalhes de cada produto no estoque serão exibidos no terminal
'''
def showEstoque():

    global estoque

    
    if not estoque:
        return STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]

    for item in estoque:
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
    Busca um produto no estoque pelo ID.
    Atualiza o dicionário 'retorno' com os detalhes do produto, se encontrado.
    """
    global estoque

    # Percorre o estoque para buscar o produto
    for item in estoque:
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
    
    global estoque

    for item in estoque:
        if item["id_produto"] == id_produto:
            estoque.remove(item)

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
    global estoque
    estoque.clear()

# Funções de Relatório
'''
Descrição
-Gera um relatório com os produtos cadastrados no estoque, armazenando os dados em um arquivo .dat codificado em UTF-32

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
-Um arquivo .dat será gerado com as informações do estoque
'''
def geraRelatorioEstoque():

    global estoque

    caminho_relativo = Path("dados/estoque/relatorio_estoque_utf32.dat")
    caminho_absoluto = caminho_relativo.resolve()

    arquivo = open(caminho_absoluto, "wb")

    bom = 0xFFFE0000
    bom_bytes = bom.to_bytes(4, byteorder="little")

    arquivo.write(bom_bytes)

    for indice, produto_estoque in enumerate(estoque):
        string = ""

        for valor in produto_estoque.values():
            string += str(valor) + ','

        if indice != len(estoque)-1:
            string = string[:-1] + '|'
        else:
            string = string[:-1]

        arquivo.write(string.encode('utf-32-le'))

    arquivo.close()

    return STATUS_CODE["SUCESSO"]


'''
Descrição
-Lê um relatório em UTF-32 com os produtos do estoque e os adiciona à lista estoque

Objetivo
-Permitir a importação de dados previamente armazenados

Acoplamento
-Arquivo .dat com os dados do estoque

Retornos Esperados
-STATUS_CODE["SUCESSO"]: Relatório lido e produtos importados com sucesso

Assertivas de Entrada
-O arquivo .dat deve existir e estar no formato correto

Assertivas de Saída
-Os produtos serão adicionados à lista estoque
'''
def leRelatorioEstoque():

    global estoque

    estoque_template = {"id_produto": None, "quantidade": None}

    caminho_relativo = Path("dados/estoque/relatorio_estoque_utf32.dat")
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

            produto_estoque = estoque_template.copy()

            for atributo in produto_estoque.keys():

                produto_estoque[atributo] = int(linha[i])
                i += 1

            estoque.append(produto_estoque)

    arquivo.close()
    return STATUS_CODE["SUCESSO"]