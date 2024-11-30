from src import cliente, estoque, produto, venda
from src.status_code import STATUS_CODE, getStatusName

__all__ = ["menu_cliente", "menu_produto", "menu_estoque", "menu_venda"]

def confere_int(var):
    try:
        return int(var)
    except ValueError:
        return -1
    
def confere_int_venda(var):
    try:
        return int(var)
    except ValueError:
        return "-1"

def confere_float(var):
    try:
        return float(var)
    except ValueError:
        return -1

def menu_cliente():
    while(1):
        print("\n<=== === === === === ===>")
        print("-1 - Sair do módulo")
        print("1 - Cadastrar cliente")
        print("2 - Mostrar cliente")
        print("3 - Atualizar cliente")
        print("4 - Mostrar vários clientes")
        print("5 - Remover cliente")
        print("<=== === === === === ===>")

        acao = input("\n---> Indique a ação desejada: ")

        # Encerrar o programa
        if (acao == "-1"):
            break

        # Cria cliente
        if (acao == "1"):
            cpf = input("\n---> CPF: ")
            nome = input("\n---> Nome: ")
            data_nascimento = input("\n---> Data de nascimento: ")

            resultado = cliente.createCliente(cpf, nome, data_nascimento)

            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nCliente criado com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Mostrar cliente
        elif (acao == "2"):
            cpf = input("\n---> CPF: ")
            resultado = cliente.showCliente(cpf)
            if (resultado != STATUS_CODE["SUCESSO"]):
                print("\nErro: " + getStatusName(resultado) + "\n")
        
        # Atualizar cliente 
        elif (acao == "3"):
            print("\n<=== === === === === ===>")
            print("1 - CPF")
            print("2 - Nome ou data de nascimento")
            print("<=== === === === === ===>")

            acao = input("\n---> O que você deseja alterar? ")

            nome = input("\n---> Nome: ")
            cpf = input("\n---> CPF: ")
            data_nascimento = input("\n---> Data de nascimento: ")

            if (acao == "1"):
                resultado = cliente.updateClienteByNome(cpf, nome, data_nascimento)
            elif (acao == "2"):
                resultado = cliente.updateClienteByCpf(cpf, nome, data_nascimento)
            else: 
                print("\nAção inválida.\n")

            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nCliente alterado com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Mostrar vários clientes
        elif (acao == "4"):
            print("\n<=== === === === === ===>")
            print("1 - Mostrar todos")
            print("2 - Filtrar por nome")
            print("<=== === === === === ===>")

            acao = input("\n---> Como você deseja mostrar os clientes? ")

            if (acao == "1"):
                resultado = cliente.showClientes()
            elif (acao == "2"):
                nome = input("\n---> Nome: ")
                resultado = cliente.showClientesByNome(nome)
            else:
                print("\nAção inválida.\n")

            if acao in ["1", "2"] and resultado != STATUS_CODE["SUCESSO"]:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Remover cliente
        elif (acao == "5"):
            cpf = input("\n---> CPF: ")
            resultado = cliente.deleteCliente(cpf)

            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nCliente removido com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Ação inválida
        else:
            print("\nAção inválida.\n")

def menu_produto():
    while(1):
        print("\n<=== === === === === ===>")
        print("-1 - Sair do módulo")
        print("1 - Criar produto")
        print("2 - Mostrar produto")
        print("3 - Atualizar produto")
        print("4 - Mostrar vários produtos")
        print("5 - Remover produto")
        print("<=== === === === === ===>")

        acao = input("\n---> Indique a ação desejada: ")

        # Encerrar o programa
        if (acao == "-1"):
            break

        # Criar produto
        elif (acao == "1"):

            nome = input("\n---> Nome: ")
            marca = input("---> Marca: ")
            categoria = input("---> Categoria: ")
            preco = input("---> Preço: ")
            preco_promocional = input("---> Preço promocional: ")

            preco = confere_float(preco)
            preco_promocional = confere_float(preco_promocional)

            resultado = produto.createProduto(nome, marca, categoria, preco, preco_promocional)

            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nProduto inserido com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Mostrar produto
        elif (acao == "2"):

            print("\n<=== === === === === ===>")
            print("1 - Buscar pelo id")
            print("2 - Buscar pelo nome")
            print("<=== === === === === ===>")
            
            acao = input("\n---> Como você deseja buscar o produto? ")

            # Buscar pelo id
            if (acao == "1"):
                id = input("\n--> ID: ")
                id = confere_int(id)
                resultado = produto.showProdutoById(id)

            # Buscar pelo nome
            elif (acao == "2"):
                nome = input("\n---> Nome: ")
                resultado = produto.showProdutoByNome(nome)

            # Ação inválida
            else:
                print("\nAção inválida.")

            # Mensagem de erro
            if acao in ["1", "2"] and resultado != STATUS_CODE["SUCESSO"]:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Atualizar produto
        elif (acao == "3"):
            
            id = input("\n---> Qual o ID do produto você deseja atualizar? ")
            id = confere_int(id)

            print("\n<== Deixe em branco os campos que não deseje atualizar ==>")
            nome = input("---> Nome: ")
            marca = input("---> Marca: ")
            categoria = input("---> Categoria: ")
            preco = input("---> Preco: ")
            preco_promocional = input("---> Preço promocional: ")

            preco = confere_float(preco)
            preco_promocional = confere_float(preco_promocional)

            resultado = produto.updateProduto(id, nome, marca, categoria, preco, preco_promocional)

            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nProduto atualizado com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Mostrar vários produtos
        elif (acao == "4"):
            print("\n<=== === === === === ===>")
            print("1 - Mostrar todos os produtos")
            print("2 - Filtrar por marca")
            print("3 - Filtrar por categoria")
            print("4 - Filtrar por faixa de preço")
            print("5 - Filtrar por nome parecido")
            print("<=== === === === === ===>")

            acao = input("\n---> Como você deseja buscar os produtos? ")

            # Mostrar todos os produtos
            if (acao == "1"):
                resultado = produto.showProdutos()

            # Filtrar por marca
            elif (acao == "2"):
                marca = input("---> Marca: ")
                resultado = produto.showProdutosByMarca(marca)

            # Filtrar por categoria
            elif (acao == "3"):
                categoria = input("---> Categoria: ")
                resultado = produto.showProdutosByCategoria(categoria)

            # Filtrar por faixa de preço
            elif (acao == "4"):
                preco_min = input("---> Preço mínimo: ")
                preco_min = confere_float(preco_min)
                preco_max = input("---> Preço máximo: ")
                preco_max = confere_float(preco_max)
                resultado = produto.showProdutosByFaixaPreco(preco_min, preco_max)

            # Filtrar por nome parecido
            elif (acao == "5"):
                nome = input("---> Nome: ")
                resultado = produto.showProdutosByNome(nome)

            # Ação inválida
            else:
                print("\nAção inválida.")

            # Mensagem de erro
            if acao in ["1", "2", "3", "4", "5"] and resultado != STATUS_CODE["SUCESSO"]:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Remover produto
        elif (acao == "5"):

            id = input("\n---> Qual produto você deseja remover? ")
            id = confere_int(id)

            resultado = produto.deleteProduto(id)
            
            if resultado == STATUS_CODE["SUCESSO"]:
                print("\nProduto removido com sucesso")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Ação inválida
        else:
            print("\nAção inválida.\n")

def menu_estoque():
    while(1):
        print("\n<=== === === === === ===>")
        print("-1 - Sair do módulo")
        print("1 - Atualizar quantidade de produto")
        print("<=== === === === === ===>")

        acao = input("\n---> Indique a ação desejada: ")

        # Encerrar o programa
        if (acao == "-1"):
            break

        # Atualiza a quantidade do produto no estoque
        if (acao == "1"):
            id_produto = input("\n---> ID do produto: ")
            quantidade = input("---> Quantidade: ")
            id_produto = confere_int(id_produto)
            quantidade = confere_int(quantidade)
            resultado = estoque.atualizaQtdEstoque(id_produto, quantidade)
            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nQuantidade alterada com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

                # Ação inválida
        
        # Ação inválida
        else:
            print("\nAção inválida.\n")

def menu_venda():
    while(1):
        print("\n<=== === === === === ===>")
        print("-1 - Sair do módulo")
        print("1 - Criar venda")
        print("2 - Adicionar produto à venda")
        print("3 - Remover produto da venda")
        print("4 - Mostra venda")
        print("5 - Mostrar vendas")
        print("6 - Alterar status da venda")
        print("7 - Deletar venda")
        print("<=== === === === === ===>")

        acao = input("\n---> Indique a ação desejada: ")

        # Sair do módulo
        if (acao == "-1"):
            break

        # Criar venda
        elif (acao == "1"):
            cpf = input("---> CPF: ")
            data = input("---> Data: ")
            hora = input("---> Hora: ")
            resultado = venda.createVenda(cpf,data,hora)
            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nVenda criada com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")
        
        # Adicionar produto à venda
        elif (acao == "2"):
            id_venda = input("\n---> ID da venda: ")
            id_produto = input("\n---> ID do produto: ")
            quantidade = input("\n---> Quantidade: ")
            id_venda = confere_int(id_venda)
            id_produto = confere_int(id_produto)
            quantidade = confere_int_venda(quantidade)
            if quantidade != "-1" or quantidade > 0:
                resultado = venda.addProduto(id_venda, id_produto, quantidade)
                if (resultado == STATUS_CODE["SUCESSO"]):
                    print("\nProduto adicionado na venda com sucesso\n")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")
            else:
                print("Quantidade inválida")

        # Remove produto da venda
        elif (acao == "3"):
            id_venda = input("\n---> ID da venda: ")
            id_produto = input("\n---> ID do produto: ")
            quantidade = input("\n---> Quantidade: ")
            id_venda = confere_int(id_venda)
            id_produto = confere_int(id_produto)
            quantidade = confere_int_venda(quantidade)
            if quantidade != "-1" or quantidade < 0:
                resultado = venda.removeProduto(id_venda, id_produto, quantidade)
                if (resultado == STATUS_CODE["SUCESSO"]):
                    print("\nProduto removido na venda com sucesso\n")
                else:
                    print("\nErro: " + getStatusName(resultado) + "\n")
            else:
                print("Quantidade inválida")

        # Mostra venda
        elif (acao == "4"):
            id_venda = input("\n---> ID da venda: ")
            id_venda = confere_int(id_venda)
            resultado = venda.showVenda(id_venda)
            if (resultado != STATUS_CODE["SUCESSO"]):
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Mostra várias vendas
        elif (acao == "5"):
            print("\n<=== === === === === ===>")
            print("1 - Mostrar todas as vendas")
            print("2 - Mostrar vendas de um cliente")
            print("3 - Mostrar vendas numa data")
            print("<=== === === === === ===>")

            acao = input("\n---> Como você deseja mostrar as vendas? ")

            # Mostrar todas as vendas
            if acao == "1":
                resultado = venda.showVendas()
            
            elif acao == "2":
                cpf = input("\n---> CPF: ")
                resultado = venda.showVendasCliente(cpf)

            elif acao == "3":
                data = input("\n---> Data: ")
                resultado = venda.showVendasData(data)

            else:
                print("\nAção inválida")

            # Mensagem de erro
            if acao in ["1", "2", "3"] and resultado != STATUS_CODE["SUCESSO"]:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Alterar status da venda
        elif (acao == "6"):
            print("\n<=== === === === === ===>")
            print("1 - Concluir venda")
            print("2 - Cancelar venda")
            print("<=== === === === === ===>")

            acao = input("\n---> Indique a ação desejada: ")

            id_venda = input("---> ID da venda: ")
            id_venda = confere_int(id_venda)

            if acao == "1":
                resultado = venda.concludeVenda(id_venda)
            elif acao == "2":
                resultado = venda.cancelaVenda(id_venda)
            else:
                print("\nAção inválida")

            # Mensagem de erro
            if acao in ["1", "2"] and resultado != STATUS_CODE["SUCESSO"]:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Deletar venda
        elif (acao == "7"):
            id_venda = input("\n---> ID da venda: ")
            id_venda = confere_int(id_venda) 
            resultado = venda.deleteVenda(id_venda)
            if (resultado == STATUS_CODE["SUCESSO"]):
                print("\nVenda criada com sucesso\n")
            else:
                print("\nErro: " + getStatusName(resultado) + "\n")

        # Ação inválida
        else:
            print("\nAção inválida")