from unittest import *
from produto import *
from status_code import *

# createProduto
class TestCreateProduto(TestCase):

    def test_create_produto_ok_retorno(self):
        print("Caso de teste - Produto criado com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_ok_inserido(self):
        print("Caso de teste - Verificação de existência do produto")
        produto_obtido = dict()
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        self.assertIn(produto_esperado, produto_obtido)

    def test_create_produto_nok_nome_nulo(self):
        print("Caso de teste - Nome não pode ser nulo")
        retorno_obtido = createProduto(None, "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["NOME_NONE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_marca_nula(self):
        print("Caso de teste - Marca não pode ser nula")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", None, "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["MARCA_NONE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_categoria_nula(self):
        print("Caso de teste - Categoria não pode ser nula")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", None, 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["CATEGORIA_NONE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_preco_nulo(self):
        print("Caso de teste - Preço não pode ser nulo")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", None, 3, 20)
        retorno_esperado = STATUS_CODE["PRECO_NONE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_qtd_minima_nulo(self):
        print("Caso de teste - Quantidade mínima não pode ser nulo")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, None)
        retorno_esperado = STATUS_CODE["QTD_MINIMA_NONE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_nome_tipo(self):
        print("Caso de teste - Nome deve ser string")
        retorno_obtido = createProduto(1, "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["NOME_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_marca_tipo(self):
        print("Caso de teste - Marca deve ser string")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", 1, "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["MARCA_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_categoria_tipo(self):
        print("Caso de teste - Categoria deve ser string")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", 1, 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["CATEGORIA_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_preco_tipo(self):
        print("Caso de teste - Preço deve ser int ou float")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", "3.5", 3, 20)
        retorno_esperado = STATUS_CODE["PRECO_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_preco_promocional_tipo(self):
        print("Caso de teste - Preço promocional deve ser int ou float")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, "3", 20)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_qtd_minima_tipo(self):
        print("Caso de teste - Quantidade mínima deve ser int ou float")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, "20")
        retorno_esperado = STATUS_CODE["QTD_MINIMA_TIPO_ERRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_nome_formato(self):
        print("Caso de teste - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_marca_formato(self):
        print("Caso de teste - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["MARCA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_categoria_formato(self):
        print("Caso de teste - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["CATEGORIA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_preco_formato(self):
        print("Caso de teste - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.555, 3, 20)
        retorno_esperado = STATUS_CODE["PRECO_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_preco_promocional_formato(self):
        print("Caso de teste - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3.111, 20)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_create_produto_nok_produto_existente(self):
        print("Caso de teste - Produto já existente")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoById
class TestShowProdutoById(TestCase):

    def test_show_produto_id_ok_encontrado(self):
        print("Caso de teste - Produto exibido com sucesso pelo id")
        retorno_obtido = showProdutoById(1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_show_produto_id_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo id")
        retorno_obtido = showProdutoById(1)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoByNome
class TestShowProdutoByNome(TestCase):

    def test_show_produto_nome_ok_encontrado(self):
        print("Caso de teste - Produto exibido com sucesso pelo nome")
        retorno_obtido = showProdutoByNome(1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_show_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo nome")
        retorno_obtido = showProdutoByNome(1)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateProduto

# getProdutoById
class TestGetProdutoById(TestCase):

    def test_get_produto_id_ok_retorno(self):
        print("Caso de teste - Produto obtido com sucesso pelo id")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoById(1, temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_get_produto_id_ok_obtido(self):
        print("Caso de teste - Verificação de devolução do produto pelo id")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoById(1, produto_obtido)
        self.assertIn(produto_esperado, produto_obtido)

    def test_get_produto_id_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo id")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoById(1, temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# getProdutoByNome
class TestGetProdutoByNome(TestCase):

    def test_get_produto_nome_ok_retorno(self):
        print("Caso de teste - Produto obtido com sucesso pelo nome")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoByNome(1, temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_get_produto_nome_ok_obtido(self):
        print("Caso de teste - Verificação de devolução do produto pelo nome")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoByNome(1, produto_obtido)
        self.assertIn(produto_esperado, produto_obtido)

    def test_get_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo nome")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoByNome(1, temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutos
class TestShowProdutos(TestCase):

    def test_show_produtos_ok_retorno(self):
        print("Caso de teste - Produtos exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_show_produtos_nok_nenhum_produto_cadastrado(self):
        print("Caso de teste - Nenhum produto cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_CADASTRADO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByMarca
class TestShowProdutosByMarca(TestCase):

    def test_show_produtos_marca_ok_retorno(self):
        print("Caso de teste - Produtos da marca especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByMarca("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_show_produtos_marca_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto da marca especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByMarca("Nescau")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByCategoria
class TestShowProdutosByCategoria(TestCase):

    def test_show_produtos_categoria_ok_retorno(self):
        print("Caso de teste - Produtos da categoria especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByCategoria("Bebidas")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_show_produtos_categoria_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto da categoria especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByCategoria("Laticínios")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByFaixaPreco
class TestShowProdutosByFaixaPreco(TestCase):

    def test_show_produtos_faixa_preco_ok_retorno(self):
        print("Caso de teste - Produtos na faixa de preço especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByFaixaPreco(0,10)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_show_produtos_faixa_preco_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto na faixa de preço especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByFaixaPreco(100,200)
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByNome
class TestShowProdutosByNome(TestCase):

    def test_show_produtos_nome_ok_retorno(self):
        print("Caso de teste - Produtos com nome parecido exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByNome("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_show_produtos_nome_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto com nome parecido cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByNome("Sprite")
        self.assertEqual(retorno_esperado, retorno_obtido)

# deleteProduto
class TestDeleteProduto(TestCase):

    def test_delete_produto_ok_removido(self):
        print("Caso de teste - Produto excluído com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_delete_produto_ok_removido(self):
        print("Caso de teste - Nenhum produto encontrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

# Executa os testes
if __name__ == "__main__":
    main()