from src import cliente, estoque, produto, venda, menu

# cliente.leRelatorioCliente()
# estoque.leRelatorioEstoque()
# produto.leRelatorioProduto()
# venda.leRelatorioVenda()

cliente.iniciarclientes()
produto.iniciarProdutos()
estoque.iniciarEstoques()
venda.iniciarVendas()

while(1):

    print("\n<=== === === === === ===>")
    print("-1 - Encerrar o programa")
    print("1 - Cliente")
    print("2 - Produto")
    print("3 - Estoque")
    print("4 - Venda")
    print("<=== === === === === ===>")

    modulo = input("\n---> Em qual módulo você deseja mexer? ")

    # Encerrar o programa
    modulo 
    if (modulo == "-1"):
        break

    # Cliente
    elif (modulo == "1"):
        menu.menu_cliente()

    # Produto
    elif (modulo == "2"):
        menu.menu_produto()

    # Estoque
    elif (modulo == "3"):
        menu.menu_estoque()

    # Vendas
    elif (modulo == "4"):
        menu.menu_venda()

    # Ação inválida
    else:
        print("\nAção inválida")

cliente.encerrarclientes()
produto.encerrarProdutos()
estoque.encerrarEstoques()
venda.encerrarVendas()

print("Programa encerrado")