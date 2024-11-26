from estoque import *
from src.status_code import STATUS_CODE

if __name__ == "__main__":
    print("\nTestando a função atualizaEstoque:")

    # Criar produtos no estoque
    createProdutoNoEstoque(1)
    createProdutoNoEstoque(2)

    print("\nEstoque inicial:")
    showEstoque()

    # Adicionar quantidade positiva
    print("\nAdicionando 10 unidades ao produto ID 1:")
    status = atualizaQtdEstoque(1, 10)
    if status == STATUS_CODE["SUCESSO"]:
        print("Quantidade atualizada com sucesso!")
    elif status == STATUS_CODE["ESTOQUE_INSUFICIENTE"]:
        print("Erro: Estoque insuficiente.")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]:
        print("Erro: Produto não encontrado.")

    print("\nEstoque atualizado:")
    showEstoque()

    # Remover quantidade negativa (válida)
    print("\nRemovendo 5 unidades do produto ID 1:")
    status = atualizaQtdEstoque(1, -5)
    if status == STATUS_CODE["SUCESSO"]:
        print("Quantidade atualizada com sucesso!")
    elif status == STATUS_CODE["ESTOQUE_INSUFICIENTE"]:
        print("Erro: Estoque insuficiente.")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]:
        print("Erro: Produto não encontrado.")

    print("\nEstoque atualizado:")
    showEstoque()

    # Tentar remover mais unidades do que o disponível
    print("\nTentando remover 10 unidades do produto ID 1:")
    status = atualizaQtdEstoque(1, -10)
    if status == STATUS_CODE["SUCESSO"]:
        print("Quantidade atualizada com sucesso!")
    elif status == STATUS_CODE["ESTOQUE_INSUFICIENTE"]:
        print("Erro: Estoque insuficiente.")
    elif status == STATUS_CODE["PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"]:
        print("Erro: Produto não encontrado.")

    print("\nEstoque final:")
    showEstoque()
