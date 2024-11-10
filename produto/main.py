from status_code.py import STATUS_CODE

class Produto:

    cont_id = 1 # Guarda o próximo ID a ser cadastrado
    lista_produtos = [] # Lista com todos os produtos
    
    def __init__(self, nome, marca, categoria, preco, preco_promocional, qtd_minima):
        self.id = Produto.cont_id 
        self.nome = nome
        self.marca = marca
        self.categoria = categoria
        self.preco = preco
        self.preco_promocional = preco_promocional
        self.qtd_minima = qtd_minima
        Produto.cont_id += 1
        Produto.lista_produtos.append(self)

    # Verifica se os valores não None
    @staticmethod
    def verificaNone(nome, marca, categoria, preco, qtd_minima):

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "qtd_minima": qtd_minima}

        for atributo, valor in parametros.items():
            if valor == None:
                return True # O valor não pode ser nulo
        return False # Sucesso

    # Troca None por "None"
    @staticmethod
    def atualizaNone(nome, marca, categoria):
        parametros = {"nome": nome, "marca": marca, "categoria": categoria}
        for atributo, valor in parametros.items():
            if valor == None:
                parametros[atributo] = "None"
        return True # Sucesso

    # Conta se um valor tem a quantidade de casas decimais desejadas
    @staticmethod
    def contaCasasDecimais(valor, casas_desejadas):
        str_valor = str(valor)
        if '.' in str_valor:
            str_valor = str_valor.split('.')
            if len(str_valor[1]) > casas_desejadas:
                return True # Preço não pode ter mais que 2 casas decimais
        return False

    # Confere se os valores passados pelo usuário possuem o tipo de variável desejado
    @staticmethod
    def validaTipos(nome, marca, categoria, preco, preco_promocional, qtd_minima):

        if not isinstance(nome, str):
            return STATUS_CODE["NOME_TIPO_ERRADO"] # Um nome deve ser do tipo string

        if not isinstance(marca, str):
            return STATUS_CODE["MARCA_TIPO_ERRADO"] # Uma marca deve ser do tipo string

        if not isinstance(categoria, str):
            return STATUS_CODE["CATEGORIA_TIPO_ERRADO"] # Uma categoria deve ser do tipo string

        if not isinstance(preco, (int, float)):
            return STATUS_CODE["PRECO_TIPO_ERRADO"] # Um preço deve ser dos tipos int ou float

        if preco_promocional != None:
            if not isinstance(preco_promocional, (int, float)):
                return STATUS_CODE["PRECO_PROMOCIONAL_TIPO_ERRADO"] # Um preço promocional deve ser dos tipos int ou float

        if not isinstance(qtd_minima, int):
            return STATUS_CODE["QTD_MINIMA_TIPO_ERRADO"] # Uma quantidade mínima deve ser do tipo int
        
        return STATUS_CODE["SUCESSO"]

    # Valida os valores passados para a função create
    @staticmethod
    def validaCreate(nome, marca, categoria, preco, preco_promocional, qtd_minima):

        if Produto.verificaNone(nome, marca, categoria, preco, qtd_minima):
            return STATUS_CODE["PARAMETROS_OBRIGATORIOS_NONE"] # Nome, marca, categoria, preço e a quantidade mínima não podem ser NULL na criação

        flag = Produto.validaTipos(nome, marca, categoria, preco, preco_promocional, qtd_minima)
        if flag:
            return flag # Retorna qual variável foi passada no tipo errado

        if preco_promocional == None:
            preco_promocional = preco

        if len(nome) > 50:
            return STATUS_CODE["NOME_FORMATO"] # Nome não pode ter mais que 50 caracteres

        if len(marca) > 50:
            return STATUS_CODE["MARCA_FORMATO"] # Marca não pode ter mais que 50 caracteres

        if len(categoria) > 50:
            return STATUS_CODE["CATEGORIA_FORMATO"] # Categoria não pode ter mais que 50 caracteres

        if preco_promocional > preco:
            return STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"] # Preço promocional não pode ser maior que o preço do produto

        if Produto.contaCasasDecimais(preco, 2):
            return STATUS_CODE["PRECO_FORMATO"] # Preço não pode ter mais que duas casas decimais

        if Produto.contaCasasDecimais(preco_promocional, 2):
            return STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"] # Preço promocional não pode ter mais que duas casas decimais

        for produto in Produto.lista_produtos:
            if nome == produto.nome and marca == produto.marca and categoria == produto.categoria:
                return STATUS_CODE["PRODUTO_EXISTENTE"] # Não podem existir produtos iguais no sistema

        return 0
        
    # Cria um produto
    @classmethod
    def createProduto(cls, nome, marca, categoria, preco, preco_promocional, qtd_minima):

        flag = cls.validaCreate(nome, marca, categoria, preco, preco_promocional, qtd_minima)
        if flag:
            return flag # Retorna o erro encontrado na validação

        novo = cls(nome, marca, categoria, preco, preco_promocional, qtd_minima)
        return STATUS_CODE["SUCESO"] # Sucesso

    # Imprime um produto
    @classmethod
    def showProduto(cls, id):
        for produto in cls.lista_produtos:
            if id == produto.id:
                for atributo,valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                return STATUS_CODE["SUCESSO"] # Sucesso
        return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

    # Atualiza um produto
    @classmethod
    def updateProduto(cls, id, nome, marca, categoria, preco, preco_promocional):

        cls.atualizaNone(nome, marca, categoria)

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "preco_promocional": preco_promocional}

        for produto in cls.lista_produtos:
            if id == produto.id:
                for parametro_atributo, parametro_valor in parametros.items():
                    if parametro_valor is not None and parametro_valor != "None":
                        if getattr(produto, parametro_atributo) != parametro_valor:
                            setattr(produto, parametro_atributo, parametro_valor)
                            if parametro_atributo == "preco":
                                setattr(produto, "preco_promocional", parametro_valor)
                return STATUS_CODE["SUCESSO"] # Sucesso
        return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # Produto não encontrado

    # Retorna um produto
    @classmethod
    def getProduto(cls, id, retorno):
        for produto in cls.lista_produtos:
            if id == produto.id:
                for atributo, valor in produto.__dict__.items():
                    retorno.append([atributo,valor])
                return STATUS_CODE["SUCESSO"] # Sucesso
        return STATUS_CODE["PRODUTO_NAO_ENCONTRADO"] # produto não encontrado

    # Mostra todos os produtos cadastrados
    @classmethod
    def showProdutos(cls):

        if not cls.lista_produtos:
            return STATUS_CODE["NENHUM_PRODUTO_CADASTRADO"] # Não há produtos cadastrados

        for produto in cls.lista_produtos:
            for atributo, valor in produto.__dict__.items():
                print(f"{atributo}: {valor}")
            print("\n", end="")

        return STATUS_CODE["SUCESSO"] # Sucesso

    # Mostra todos os produtos de certa marca
    @classmethod
    def showProdutosByMarca(cls, marca):
        flag = False
        for produto in cls.lista_produtos:
            if marca == produto.marca:
                flag = True
                for atributo, valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                print("\n", end="")
        if flag:
            return STATUS_CODE["SUCESSO"] # Sucesso
        else:
            return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

    # Mostra todos os produtos de certa categoria
    @classmethod
    def showProdutosByCategoria(cls, categoria):
        flag = False
        for produto in cls.lista_produtos:
            if categoria == produto.categoria:
                flag = True
                for atributo, valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                print("\n", end="")
        if flag:
            return STATUS_CODE["SUCESSO"] # Sucesso
        else:
            return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

    # Mostra todos os produtos em certa faixa de preço
    @classmethod
    def showProdutosByFaixaPreco(cls, preco_min, preco_max):
        flag = False
        for produto in cls.lista_produtos:
            if produto.preco >= preco_min and produto.preco <= preco_max:
                flag = True
                for atributo, valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                print("\n", end="")
        if flag:
            return STATUS_CODE["SUCESSO"] # Sucesso
        else:
            return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

    # Mostra todos os produtos com certo nome
    @classmethod
    def showProdutosByNome(cls, nome):
        flag = False
        for produto in cls.lista_produtos:
            if nome in produto.nome:
                flag = True
                for atributo, valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                print("\n", end="")
        if flag:
            return STATUS_CODE["SUCESSO"] # Sucesso
        else:
            return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Nenhum produto encontrado

    # Deleta um produto
    @classmethod
    def deleteProduto(cls, id):
        for produto in cls.lista_produtos:
            if id == produto.id:
                cls.lista_produtos.remove(produto)
                return STATUS_CODE["SUCESSO"] # Sucesso
        return STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"] # Produto não encontrado