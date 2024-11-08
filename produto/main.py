class Produto:
    cont_id = 1
    lista_produtos = []
    
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
    @classmethod
    def verifica_none(cls, nome, marca, categoria, preco, qtd_minima):

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "qtd_minima": qtd_minima}

        for atributo, valor in parametros.items():
            if valor == None:
                return 1 # O valor não pode ser nulo
        return 0 # Sucesso

    # Troca None por -1
    @classmethod
    def atualiza_none(cls, nome, marca, categoria):
        parametros = {"nome": nome, "marca": marca, "categoria": categoria}
        for atributo, valor in parametros.items():
            if valor == None:
                valor = "-1"
        return 0 # Sucesso
    
    @classmethod
    def createProduto(cls, nome, marca, categoria, preco, preco_promocional, qtd_minima):

        if cls.verifica_none(nome, marca, categoria, preco, qtd_minima) == 1:
            return 1 # Nome, marca, categoria, preço e a quantidade mínima não podem ser NULL

        if preco_promocional == None:
            preco_promocional = preco

        novo = cls(nome, marca, categoria, preco, preco_promocional, qtd_minima)
        return 0 # Sucesso

    @classmethod
    def showProduto(cls, id):
        for produto in cls.lista_produtos:
            if id == produto.id:
                for atributo,valor in produto.__dict__.items():
                    print(f"{atributo}: {valor}")
                return 0 # Sucesso
        return 1 # Produto não encontrado

    @classmethod
    def updateProduto(cls, id, nome, marca, categoria, preco, preco_promocional):

        cls.atualiza_none(nome, marca, categoria)

        parametros = {"nome": nome, "marca": marca, "categoria": categoria, "preco": preco, "preco_promocional": preco_promocional}

        for produto in cls.lista_produtos:
            if id == produto.id:
                for parametro_atributo, parametro_valor in parametros.items():
                    if parametro_valor is not None and parametro_atributo != "-1":
                        if getattr(produto, parametro_atributo) != parametro_valor:
                            setattr(produto, parametro_atributo, parametro_valor)
                            if parametro_atributo == "preco":
                                setattr(produto, "preco_promocional", parametro_valor)
                return 0 # Sucesso
        return 1 # Produto não encontrado

    @classmethod
    def getProduto(cls, id, retono):
        for produto in cls.lista_produtos:
            if id == produto.id:
                for atributo, valor in produto.__dict__.items():
                    retorno.append([atributo,valor])
                return 0 # Sucesso
        return 1 # produto não encontrado

Produto.createProduto("Coca Cola Zero 350ml", "Coca-Cola", "Bebidas", 4.5, None, 0)
'''
Produto.showProduto(1)
print("\n")
Produto.updateProduto(1, None, None, None, 6.5, None)
Produto.showProduto(1)
'''
retorno = list()
Produto.getProduto(1, retorno)
for atributo, valor in retorno:
    print(f"{atributo}: {valor}")