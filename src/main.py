from src import produto, cliente, venda
from src.status_code import STATUS_CODE, getStatusName

cliente.leRelatorioCliente()
produto.leRelatorioProduto()
venda.lerRelatorioVenda()

def confere_int(var):
    try:
        return int(var)
    except ValueError:
        return -1
    
def confere_float(var):
    try:
        return float(var)
    except ValueError:
        return -1

while(1):

    print("\n--- --- --- --- --- --- --- --- --- ---")
    print("-1 - Encerrar o programa")
    print("1 - Cliente")
    print("2 - Produto")
    print("3 - Estoque")
    print("4 - Vendas")
    print("--- --- --- --- --- --- --- --- --- ---")

    modulo = input("\nEm qual módulo você deseja mexer? ")

    # Encerrar o programa
    if (modulo == "-1"):
        break

    # Cliente
    elif (modulo == "1"):
        while(1):
            print("\n--- --- --- --- --- --- --- --- --- ---")
            print("-1 - Sair do módulo")
            print("1 - Cadastrar cliente")
            print("2 - Mostrar cliente")
            print("3 - Atualizar cliente")
            print("4 - Mostrar vários produtos")
            print("5 - Remover cliente")
            print("--- --- --- --- --- --- --- --- --- ---")

    # Produto
    elif (modulo == "2"):

        while(1):
            print("\n--- --- --- --- --- --- --- --- --- ---")
            print("-1 - Sair do módulo")
            print("1 - Criar produto")
            print("2 - Mostrar produto")
            print("3 - Atualizar produto")
            print("4 - Mostrar vários produtos")
            print("5 - Remover produto")
            print("--- --- --- --- --- --- --- --- --- ---")

            acao = input("\n---> Indique a ação desejada: ")

            # Encerrar o programa
            if (acao == "-1"):
                break

            # Criar produto
            elif (acao == "1"):

                nome = input("\n--> Nome: ")
                marca = input("--> Marca: ")
                categoria = input("--> Categoria: ")
                preco = input("--> Preço: ")
                preco_promocional = input("--> Preço promocional: ")
                qtd_minima = input("--> Quantidade mínima: ")

                preco = confere_float(preco)
                preco_promocional = confere_float(preco)
                qtd_minima = confere_int(qtd_minima)

                resultado = produto.createProduto(nome, marca, categoria, preco, preco_promocional, qtd_minima)

                if (resultado == STATUS_CODE["SUCESSO"]):
                    print("\nProduto inserido com sucesso\n")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Mostrar produto
            elif (acao == "2"):

                print("\n--- --- --- --- --- --- --- --- --- ---")
                print("1 - Buscar pelo id")
                print("2 - Buscar pelo nome")
                print("--- --- --- --- --- --- --- --- --- ---")
                
                acao = input("\n--> Como você deseja buscar o produto? ")

                # Buscar pelo id
                if (acao == "1"):
                    id = input("\nId: ")
                    id = confere_int(id)
                    resultado = produto.showProdutoById(id)

                # Buscar pelo nome
                elif (acao == "2"):
                    nome = input("\nNome: ")
                    resultado = produto.showProdutoByNome(nome)

                # Ação inválida
                else:
                    print("\nAção inválida.")

                # Mensagem de erro
                if acao in ["1", "2"] and resultado != STATUS_CODE["SUCESSO"]:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Atualizar produto
            elif (acao == "3"):
                
                id = input("Qual produto você deseja atualizar? ")
                id = confere_int(id)

                temp = dict()
                resultado = produto.getProdutoById(id, temp)

                if resultado == STATUS_CODE["SUCESSO"]:
                    print("\nValores atuais: ")
                    produto.showProdutoById(1)

                    print("-- Deixe em branco os campos que não deseje atualizar --")
                    nome = input("--> Nome: ")
                    marca = input("--> Marca: ")
                    categoria = input("--> Categoria: ")
                    preco = input("--> Preco: ")
                    preco_promocional = input("--> Preço promocional: ")

                    preco = confere_float(preco)
                    preco_promocional = confere_float(preco_promocional)

                    resultado = produto.updateProduto(id, nome, marca, categoria, preco, preco_promocional)

                    if (resultado == STATUS_CODE["SUCESSO"]):
                        print("\nProduto atualizado com sucesso\n")
                    else:
                        print("\nErro: " + getStatusName(resultado) + "\n")

                else:
                    print("Erro: produto não encontrado")

            # Mostrar vários produtos
            elif (acao == "4"):
                print("\n--- --- --- --- --- --- --- --- --- ---")
                print("1 - Mostrar todos os produtos")
                print("2 - Filtrar por marca")
                print("3 - Filtrar por categoria")
                print("4 - Filtrar por faixa de preço")
                print("5 - Filtrar por nome parecido")
                print("--- --- --- --- --- --- --- --- --- ---")

                acao = input("\n--> Como você deseja buscar os produtos? ")

                # Mostrar todos os produtos
                if (acao == "1"):
                    resultado = produto.showProdutos()

                # Filtrar por marca
                elif (acao == "2"):
                    marca = input("--> Marca: ")
                    resultado = produto.showProdutosByMarca(marca)

                # Filtrar por categoria
                elif (acao == "3"):
                    categoria = input("--> Categoria: ")
                    resultado = produto.showProdutosByCategoria(categoria)

                # Filtrar por faixa de preço
                elif (acao == "4"):
                    preco_min = input("--> Preço mínimo: ")
                    preco_min = confere_float(preco_min)
                    preco_max = input("--> Preço máximo: ")
                    preco_max = confere_float(preco_max)
                    resultado = produto.showProdutosByFaixaPreco(preco_min, preco_max)

                # Filtrar por nome parecido
                elif (acao == "5"):
                    nome = input("--> Nome: ")
                    resultado = produto.showProdutosByNome(nome)

                # Ação inválida
                else:
                    print("\nAção inválida.")

                # Mensagem de erro
                if acao in ["1", "2", "3", "4", "5"] and resultado != STATUS_CODE["SUCESSO"]:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Remover produto
            elif (acao == "5"):

                id = input("Qual produto você deseja remover? ")
                id = confere_int(id)

                resultado = produto.deleteProduto(id)
                
                if resultado == STATUS_CODE["SUCESSO"]:
                    print("\nProduto removido com sucesso")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Ação inválida
            else:
                print("\nAção inválida.\n")

    # Estoque
    elif (modulo == "3"):
        while(1):
            print("\n--- --- --- --- --- --- --- --- --- ---")
            print("-1 - Sair do módulo")
            print("1 - Alterar produto no estoque")
            print("2 - Mostrar produto no estoque")
            print("4 - Mostrar vários produtos no estoque")
            print("--- --- --- --- --- --- --- --- --- ---")

    # Vendas
    elif (modulo == "4"):
        while(1):
            print("\n--- --- --- --- --- --- --- --- --- ---")
            print("-1 - Sair do módulo")
            print("1 - Cadastrar venda")
            print("2 - Mostrar venda")
            print("3 - Atualizar venda")
            print("4 - Mostrar várias vendas")
            print("5 - Remover venda")
            print("--- --- --- --- --- --- --- --- --- ---")

            acao = input("\n---> Indique a ação desejada: ")

            # Encerrar o programa
            if (acao == "-1"):
                break

            # Criar venda
            elif (acao == "1"):

                cpf = input("\n--> CPF do cliente (opcional): ")
                data = input("--> Data da venda (dd/mm/aaaa): ")
                hora = input("--> Hora da venda (HH:mm): ")

                resultado = venda.createVenda(cpf, data, hora)

                if (resultado == STATUS_CODE["VENDA_CADASTRADA"]):
                    print("\Venda cadastrada com sucesso\n")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Mostrar venda
            elif (acao == "2"):
                id_venda = input("Qual o id da venda: ")
                id_venda = confere_int(id_venda)
                resultado = venda.showVenda(id_venda)

                if resultado == STATUS_CODE["VENDA_NAO_ENCONTRADA"]:
                    print("\nErro: " + getStatusName(resultado) + "\n")         

            # Atualizar venda
            elif (acao == "3"):
                
                id_venda = input("Qual o id da venda que deseja atualizar? ")
                id_venda = confere_int(id_venda)

                data = input("Informe a nova data: ")
                hora = input("Informe a nova hora: ")

                resultado = venda.updateVenda(id_venda, data, hora)

                if (resultado == STATUS_CODE["VENDA_ALTERADA"]):
                    print("\Venda atualizada com sucesso\n")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            #Mostrar várias vendas
            elif (acao == "4"):
                print("\n--- --- --- --- --- --- --- --- --- ---")
                print("1 - Mostrar vendas por cliente associado")
                print("2 - Mostrar vendas por data")
                print("3 - Mostrar todas as vendas")
                print("--- --- --- --- --- --- --- --- --- ---")

                acao = input("\n--> Como você deseja buscar as vendas? ")

                # Mostrar vendas por cliente associado
                if (acao == "1"):
                    cpf = input("--> CPF: ")
                    resultado = venda.showVendasCliente(cpf)

                    if (resultado == STATUS_CODE["VENDA_NAO_ENCONTRADA"]):
                        print("\nErro: " + getStatusName(resultado) + "\n")
        
                # Mostrar vendas por data
                elif (acao == "2"):
                    data = input("--> Data: ")
                    resultado = venda.showVendasData(data)

                    if (resultado == STATUS_CODE["VENDA_NAO_ENCONTRADA"]):
                        print("\nErro: " + getStatusName(resultado) + "\n")
                
                # Mostrar todas as vendas
                elif (acao == "3"):
                    resultado = venda.showVendas()

                    if (resultado == STATUS_CODE["VENDA_NAO_ENCONTRADA"]):
                        print("\nErro: " + getStatusName(resultado) + "\n")

            # Remover venda
            elif (acao == "5"):

                id_venda = input("Qual o id da venda que você deseja remover? ")
                id_venda = confere_int(id_venda)

                resultado = venda.deleteVenda(id_venda)
                
                if resultado == STATUS_CODE["VENDA_REMOVIDA"]:
                    print("\nVenda removida com sucesso")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")

            # Ação inválida
            else:
                print("\nAção inválida.\n")

        else:
            print("\nAção inválida")

cliente.geraRelatorioCliente()
produto.geraRelatorioProduto()
venda.geraRelatorioVenda()

print("Programa encerrado")