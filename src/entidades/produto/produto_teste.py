import unittest
from unittest.mock import patch
import os
from .produto import *
from src.status_code import *

# createProduto - JÁ REVISADO
class TestCreateProduto(unittest.TestCase):

    def test_01_create_produto_ok_retorno(self):
        print("Caso de teste (PRODUTO - createProduto) - Criação")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_create_produto_ok_inserido(self):
        print("Caso de teste (PRODUTO - createProduto) - Verificação de existência")
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        produto_obtido.pop("id")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_create_produto_nok_nome_vazio(self):
        print("Caso de teste (PRODUTO - createProduto) - Nome não pode estar vazio")
        retorno_obtido = createProduto("", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_NOME_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_create_produto_nok_marca_vazia(self):
        print("Caso de teste (PRODUTO - createProduto) - Marca não pode estar vazia")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_MARCA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_create_produto_nok_categoria_vazia(self):
        print("Caso de teste (PRODUTO - createProduto) - Categoria não pode estar vazia")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_CATEGORIA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_create_produto_nok_preco_vazio(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço não pode estar vazio")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", -1, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_create_produto_nok_qtd_minima_vazia(self):
        print("Caso de teste (PRODUTO - createProduto) - Quantidade mínima não estar vazia")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_QTD_MINIMA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_create_produto_nok_nome_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_create_produto_nok_marca_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_MARCA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_10_create_produto_nok_categoria_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_CATEGORIA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_11_create_produto_nok_preco_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.555, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_12_create_produto_nok_preco_promocional_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3.111, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_13_create_produto_nok_preco_promocional_maior_que_preco(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço promocional não pode ser maior que o preço")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 4, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_14_create_produto_nok_produto_existente(self):
        print("Caso de teste (PRODUTO - createProduto) - Produto já existente")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoById - JÁ REVISADO
class TestShowProdutoById(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produto_id_ok_encontrado(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutoById) - Exibicação")
        retorno_obtido = showProdutoById(1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_produto_id_nok_nao_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutoById) - Produto não encontrado")
        retorno_obtido = showProdutoById(2)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoByNome - JÁ REVISADO
class TestShowProdutoByNome(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produto_nome_ok_encontrado(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutoByNome) - Exibicação")
        retorno_obtido = showProdutoByNome("Coca-Cola Zero 350ml")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutoByNome) - Produto não encontrado")
        retorno_obtido = showProdutoByNome("Coca-Cola Zero 500ml")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateProduto - JÁ REVISADO
class TestUpdateProduto(unittest.TestCase):
    
    def test_01_update_produto_ok_retorno(self):
        print("Caso de teste (PRODUTO - updateProduto) - Atualização")
        retorno_obtido = updateProduto(1, "Coca-Cola Zero 500ml", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_02_update_produto_ok_alterado(self):
        print("Caso de teste (PRODUTO - updateProduto) - Verificação de atualização")
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 500ml", produto_obtido)
        produto_obtido.pop("id")
        produto_esperado = {"nome": "Coca-Cola Zero 500ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        self.assertEqual(produto_obtido, produto_esperado)

    def test_03_update_produto_nok_nome_formato_incorreto(self):
        print("Caso de teste (PRODUTO - updateProduto) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_produto_nok_marca_formato_incorreto(self):
        print("Caso de teste (PRODUTO - updateProduto) - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "", -1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_MARCA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_05_update_produto_nok_categoria_formato_incorreto(self):
        print("Caso de teste (PRODUTO - updateProduto) - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "", "", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", -1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_CATEGORIA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_produto_nok_preco_formato_incorreto(self):
        print("Caso de teste (PRODUTO - updateProduto) - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = updateProduto(1, "", "", "", 3.555, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_update_produto_nok_preco_promocional_formato_incorreto(self):
        print("Caso de teste (PRODUTO - updateProduto) - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = updateProduto(1, "", "", "", -1, 3.111)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_update_produto_nok_preco_promocional_maior_preco_1(self):
        print("Caso de teste (PRODUTO - updateProduto) - Preço promocional não pode ser maior que o preço (1 - Novo preço menor que o preço promocional atual)")
        retorno_obtido = updateProduto(1, "", "", "", 1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_update_produto_nok_preco_promocional_maior_preco_2(self):
        print("Caso de teste (PRODUTO - updateProduto) - Preço promocional não pode ser maior que o preço (2 - Novo preço menor que o novo preço promocional)")
        retorno_obtido = updateProduto(1, "", "", "", 3, 4)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_10_update_produto_nok_preco_promocional_maior_preco_3(self):
        print("Caso de teste (PRODUTO - updateProduto) - Preço promocional não pode ser maior que o preço (3 - Novo preço promocional maior que o preço atual)")
        retorno_obtido = updateProduto(1, "", "", "", -1, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_11_update_produto_nok_produto_nao_encontrado(self):
        print("Caso de teste (PRODUTO - updateProduto) - Produto não encontrado")
        retorno_obtido = updateProduto(2, "", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# getProdutoById - JÁ REVISADO
class TestGetProdutoById(unittest.TestCase):

    def test_01_get_produto_id_ok_retorno(self):
        print("Caso de teste (PRODUTO - getProdutoById) - Obtenção")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoById(1, temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_id_ok_obtido(self):
        print("Caso de teste (PRODUTO - getProdutoById) - Verificação de obtenção")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoById(1, produto_obtido)
        produto_obtido.pop("id")
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_get_produto_id_nok_nao_encontrado(self):
        print("Caso de teste (PRODUTO - getProdutoById) - Produto não encontrado")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoById(2, temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# getProdutoByNome - JÁ REVISADO
class TestGetProdutoByNome(unittest.TestCase):

    def test_01_get_produto_nome_ok_retorno(self):
        print("Caso de teste (PRODUTO - getProdutoByNome) - Obtenção")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoByNome("Coca-Cola Zero 350ml", temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_nome_ok_obtido(self):
        print("Caso de teste (PRODUTO - getProdutoByNome) - Verificação de retorno")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        produto_obtido.pop("id")
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_get_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste (PRODUTO - getProdutoByNome) - Produto não encontrado")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoByNome("Coca-Cola Zero 500ml", temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutos - JÁ REVISADO
class TestShowProdutos(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutos) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nok_nenhum_produto_cadastrado(self):
        print("Caso de teste (PRODUTO - showProdutos) - Nenhum produto cadastrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_CADASTRO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByMarca - JÁ REVISADO
class TestShowProdutosByMarca(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_marca_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutosByMarca) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByMarca("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_marca_nok_nenhum_produto_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutosByMarca) - Nenhum produto encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"]
        retorno_obtido = showProdutosByMarca("Nescau")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByCategoria - JÁ REVISADO
class TestShowProdutosByCategoria(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_categoria_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutosByCategoria) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByCategoria("Bebidas")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_categoria_nok_nenhum_produto_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutosByCategoria) - Nenhum produto encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"]
        retorno_obtido = showProdutosByCategoria("Laticínios")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByFaixaPreco - JÁ REVISADO
class TestShowProdutosByFaixaPreco(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_faixa_preco_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutosByFaixaPreco) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByFaixaPreco(0,10)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_faixa_preco_nok_nenhum_produto_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutosByFaixaPreco) - Nenhum produto encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"]
        retorno_obtido = showProdutosByFaixaPreco(100,200)
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByNome - JÁ REVISADO
class TestShowProdutosByNome(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_nome_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutosByNome) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByNome("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nome_nok_nenhum_produto_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutosByNome) - Nenhum produto encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_ENCONTRADO"]
        retorno_obtido = showProdutosByNome("Sprite")
        self.assertEqual(retorno_esperado, retorno_obtido)

# deleteProduto - JÁ REVISADO
class TestDeleteProduto(unittest.TestCase):

    def test_01_delete_produto_ok_retorno(self):
        print("Caso de teste (PRODUTO - deleteProduto) - Exclusão")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_delete_produto_ok_removido(self):
        print("Caso de teste (PRODUTO - deleteProduto) - Veriicação de exclusão")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = showProdutoById(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_03_delete_produto_nok_nenhum_produto_encontrado(self):
        print("Caso de teste (PRODUTO - deleteProduto) - Produto não encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = deleteProduto(2)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_04_delete_produto_nok_produto_nao_zerado_no_estoque(self):
        print("Caso de teste (PRODUTO) - Produto não zerado no estoque")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ZERADO_NO_ESTOQUE"]
        atualizaQtdEstoque(1, 5)
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_05_delete_produto_nok_produto_cadastrado_em_venda(self):
        createVenda("", "13/10/2004", "20:00")
        addProduto(1, 1, 1)
        print("Caso de teste (PRODUTO) - Produto cadastrado em venda")
        retorno_esperado = STATUS_CODE["PRODUTO_CADASTRADO_EM_VENDA"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

# geraRelatorioProduto e leRelatorioProduto
class TestRelatorioProduto(unittest.TestCase):
    
    def test_01_gera_relatorio_produto(self):
        print("Caso de teste (PRODUTO) - Geração do relatório de produtos")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = geraRelatorioProduto()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_le_relatorio_produto(self):
        print("Caso de teste (PRODUTO) - Leitura do relatório de produtos e cadastro no sistema")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = leRelatorioProduto()
        self.assertEqual(retorno_esperado, retorno_obtido)

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(TestShowProdutos('test_02_show_produtos_nok_nenhum_produto_cadastrado'))
    suite.addTest(unittest.makeSuite(TestCreateProduto))
    suite.addTest(unittest.makeSuite(TestShowProdutoById))
    suite.addTest(unittest.makeSuite(TestShowProdutoByNome))
    suite.addTest(unittest.makeSuite(TestGetProdutoById))
    suite.addTest(unittest.makeSuite(TestGetProdutoByNome))
    suite.addTest(TestShowProdutos('test_01_show_produtos_ok_retorno'))
    suite.addTest(unittest.makeSuite(TestShowProdutosByMarca))
    suite.addTest(unittest.makeSuite(TestShowProdutosByCategoria))
    suite.addTest(unittest.makeSuite(TestShowProdutosByFaixaPreco))
    suite.addTest(unittest.makeSuite(TestShowProdutosByNome))
    suite.addTest(unittest.makeSuite(TestUpdateProduto))
    suite.addTest(unittest.makeSuite(TestDeleteProduto))
    suite.addTest(unittest.makeSuite(TestRelatorioProduto))

    return suite

# Executa os testes
if __name__ == "__main__":
    from ..estoque.estoque import atualizaQtdEstoque
    from ..venda.venda import createVenda, addProduto
    runner = unittest.TextTestRunner()
    runner.run(suite())