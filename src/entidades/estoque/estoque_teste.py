import unittest
from unittest.mock import patch
import os
from .estoque import *
from src.status_code import *

# Testes para createProdutoNoEstoque
class TestCreateProdutoNoEstoque(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaEstoque()
        limpaProdutos()

    def test_01_createProdutoNoEstoque_ok_retorno(self):
        print("Caso de teste (ESTOQUE - createProdutoNoEstoque) - Produto criado no estoque com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createProdutoNoEstoque(1)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_createProdutoNoEstoque_ok_inserido(self):
        print("Caso de teste (ESTOQUE - createProdutoNoEstoque) - Produto criado no estoque com sucesso")
        produto_obtido = dict()
        getProdutoEstoque(1, produto_obtido)
        produto_esperado = {"id_produto": 1, "quantidade": 0}
        self.assertEqual(produto_obtido, produto_esperado)

    def test_03_createProdutoNoEstoque_nok_produto_nao_encontrado(self):
        print("Caso de teste (ESTOQUE - createProdutoNoEstoque) - Produto não encontrado ao tentar criar no estoque")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = createProdutoNoEstoque(999)
        self.assertEqual(retorno_obtido, retorno_esperado)

# Testes para atualizaQtdEstoque
class TestAtualizaQtdEstoque(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        createProdutoNoEstoque(1)

    @classmethod
    def tearDownClass(cls):
        limpaEstoque()
        limpaProdutos()

    def test_01_atualizaQtdEstoque_ok_adicao(self):
        print("Caso de teste (ESTOQUE - atualizaQtdEstoque) - Adicionar quantidade ao estoque com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = atualizaQtdEstoque(1, 10)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_atualizaQtdEstoque_ok_remocao(self):
        print("Caso de teste (ESTOQUE - atualizaQtdEstoque) - Remover quantidade do estoque com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = atualizaQtdEstoque(1, -5)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_03_atualizaQtdEstoque_nok_insuficiente(self):
        print("Caso de teste (ESTOQUE - atualizaQtdEstoque) - Estoque insuficiente ao tentar remover")
        retorno_esperado = STATUS_CODE["ESTOQUE_INSUFICIENTE"]
        retorno_obtido = atualizaQtdEstoque(1, -20)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_atualizaQtdEstoque_nok_produto_nao_encontrado(self):
        print("Caso de teste (ESTOQUE - atualizaQtdEstoque) - Produto não encontrado ao atualizar quantidade")
        retorno_esperado = STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = atualizaQtdEstoque(999, 10)
        self.assertEqual(retorno_obtido, retorno_esperado)

# Testes para getProdutoEstoque
class TestGetProdutoEstoque(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        createProdutoNoEstoque(1)

    @classmethod
    def tearDownClass(cls):
        limpaEstoque()
        limpaProdutos()

    def test_01_getProdutoEstoque_ok(self):
        print("Caso de teste (ESTOQUE - getProdutoEstoque) - Obter produto no estoque com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        produto_detalhes = {}
        retorno_obtido = getProdutoEstoque(1, produto_detalhes)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_getProdutoEstoque_nok_produto_nao_encotrado(self):
        print("Caso de teste (ESTOQUE - getProdutoEstoque) - Produto não encontrado no estoque")
        retorno_esperado = STATUS_CODE["ESTOQUE_PRODUTO_NAO_ENCONTRADO"]
        produto_detalhes = {}
        retorno_obtido = getProdutoEstoque(999, produto_detalhes)
        self.assertEqual(retorno_obtido, retorno_esperado)

# Testes para showEstoque
class TestShowEstoque(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        createProdutoNoEstoque(1)

    @classmethod
    def tearDownClass(cls):
        limpaEstoque()
        limpaProdutos()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showEstoque_ok(self, mock_stdout):
        print("Caso de teste (ESTOQUE - showEstoque) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showEstoque()
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_showEstoque_nok_nenhum_cadastro(self):
        limpaEstoque()
        print("Caso de teste (ESTOQUE - showEstoque) - Nenhum produto cadastrado no estoque")
        retorno_esperado = STATUS_CODE["ESTOQUE_NENHUM_CADASTRO"]
        retorno_obtido = showEstoque()
        self.assertEqual(retorno_obtido, retorno_esperado)

# Testes para deleteProdutoEstoque
class TestDeleteProdutoEstoque(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        createProdutoNoEstoque(1)

    @classmethod
    def tearDownClass(cls):
        limpaEstoque()
        limpaProdutos()

    def test_01_deleteProdutoEstoque_ok(self):
        print("Caso de teste (ESTOQUE - deleteProdutoEstoque) - Remoção")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteProdutoEstoque(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

# Testes para geraRelatorioEstoque e lerRelatorioEstoque
class TestRelatorioEstoque(unittest.TestCase):
    
    def test_01_carregar_estoque(self):
        print("Caso de teste (ESTOQUE - carregarEstoque) - Geração do relatório de estoque")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = carregarEstoques()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_salvar_estoque(self):
        print("Caso de teste (ESTOQUE - salvarEstoque) - Leitura do relatório de estoque e cadastro no sistema")
        retorno_esperado = STATUS_CODE["ERRO"]
        retorno_obtido = salvarEstoques()
        self.assertIsNot(retorno_esperado, retorno_obtido)

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    suite.addTest(unittest.makeSuite(TestCreateProdutoNoEstoque))
    suite.addTest(unittest.makeSuite(TestAtualizaQtdEstoque))
    suite.addTest(unittest.makeSuite(TestGetProdutoEstoque))
    suite.addTest(unittest.makeSuite(TestShowEstoque))
    suite.addTest(unittest.makeSuite(TestDeleteProdutoEstoque))
    suite.addTest(unittest.makeSuite(TestRelatorioEstoque))

    return suite

# Executa os testes
if __name__ == "__main__":
    from ..produto.produto import createProduto, limpaProdutos
    runner = unittest.TextTestRunner()
    runner.run(suite())