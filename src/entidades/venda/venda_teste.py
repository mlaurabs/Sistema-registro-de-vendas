import unittest
from unittest.mock import patch
import os
from .venda import *
from src.status_code import *

class TestCreateVenda(unittest.TestCase):

    def test_01_createVenda_ok_retorno(self):
        print("Caso de teste (VENDA - createVenda) - Criação")
        response = createVenda("123.456.789-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_CADASTRADA"])

    def test_02_createVenda_nok_cpf_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - CPF inválido")
        response = createVenda("12345678", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"])

    def test_03_createVenda_nok_data_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - Data inválida")
        response = createVenda("123.456.789-01", "2024-11-15", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"])

    def test_04_createVenda_nok_hora_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - Hora inválida")
        response = createVenda("123.456.789-01", "15/11/2024", "1030")
        self.assertEqual(response, STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"])

    def test_05_createVenda_nok_venda_existente(self):
        print("Caso de teste (VENDA - createVenda) - Venda existente")
        response = createVenda("123.456.789-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_EXISTENTE"])

class TestConcludeVenda(unittest.TestCase):
    def test_01_concludeVenda_ok_retorno(self):
        # Teste de conclusão de venda com id válido
        print("Caso de teste (VENDA - concludeVenda) - Efetuação")
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_CONCLUIDA"])

    def test_02_concludeVenda_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda já concluída")
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_03_concludeVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda não encontrada")
        response = concludeVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestAddProduto(unittest.TestCase):

    def test_01_addProduto_ok_retorno(self):
        print("Caso de teste (VENDA - addProduto) - Adição de produto")
        response = addProduto(1, 101, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_ADICIONADO"])

    def test_02_addProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - addProduto) - Venda não encontrada")
        response = addProduto(99, 101, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_03_addProduto_nok_produto_nao_encontrado_no_estoque(self):
        print("Caso de teste (VENDA - addProduto) - Produto não encontrado no estoque")
        response = addProduto(1, 999, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO_NO_ESTOQUE"])

    def test_04_addProduto_estoque_insuficiente(self):    
        print("Caso de teste (VENDA - addProduto) - Estoque insuficiente")
        response = addProduto(1, 101, 1000)
        self.assertEqual(response, STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"])

class TestRemoveProduto(unittest.TestCase):
    def test_01_removeProduto_ok_retorno(self):
        print("Caso de teste (VENDA - removeProduto) - Remoção de produto")
        response = removeProduto(1, 101, 3)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_REMOVIDO"])

    def test_02_removeProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - removeProduto) - Venda não encontrada")
        response = removeProduto(99, 101, 3)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_03_removeProduto_nok_produto_nao_incluido(self):
        print("Caso de teste (VENDA - removeProduto) - Produto não incluído na venda")
        response = removeProduto(1, 101, 100)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"])

class TestUpdateVenda(unittest.TestCase):

    def test_01_updateVenda_ok_retorno(self):
        print("Caso de teste (VENDA - updateVenda) - Alteração")
        response = updateVenda(1, "05/05/2004", "13:53")
        self.assertEqual(response, STATUS_CODE["VENDA_ALTERADA"])
    
    def test_02_updateVenda_nok_data_formato_incorreto(self):
        print("Caso de teste (VENDA - updateVenda) - Data inválida")
        response = updateVenda(1, "05-05-2004", "13:53")
        self.assertEqual(response, STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"])

    def test_03_updateVenda_nok_hora_formato_incorreto(self):
        # Teste de alteração de venda com hora inválida
        print("Caso de teste (VENDA - updateVenda) - Hora inválida")
        response = updateVenda(1, "05-05-2004", "13//53")
        self.assertEqual(response, STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"])

class TestShowVenda(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVenda_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVenda) - Exibição")
        response = showVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_showVenda_nok_venda_nao_encontrada(self):
        # Teste de venda não encontrada
        print("Caso de teste (VENDA - updateVenda) - Venda não encontrada")
        response = showVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestShowVendas(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendas_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendas) - Exibição")
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendas_nok_venda_nao_encontrada(self):
        # Teste de nenhuma venda encontrada
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestShowVendasClientes(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendasCliente_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendasClientes) - Exibição")
        response = showVendasCliente("12345678901")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendasCliente_nok_nenhuma_venda_encontrada(self):
        print("Caso de teste (VENDA - updateVenda) - Nenhuma venda encontrada")
        response = showVendasCliente("98765432100")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestCheckProdutoVenda(unittest.TestCase):

    def test_01_checkProdutoVenda_ok_retorno(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto encontrado em vendas")
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_ENCONTRADO"])
    
    def test_01_checkProdutoVenda_nok_produto_nao_encontrado(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto não encontrado em nenhuma venda")
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"])

class TestCheckClienteVenda(unittest.TestCase):
    def test_01_checkClienteVenda(self):

        # Teste de busca por clientes associados a vendas
        response = checkClienteVenda("12345678901")
        self.assertEqual(response, STATUS_CODE["CLIENTE_ENCONTRADO"])

    def test_01_checkClienteVenda(self):
        createVenda("12345678102", "16/12/2024", "12:35")

        # Teste de busca por clientes associados a vendas
        response = checkClienteVenda("12345678901")
        self.assertEqual(response, STATUS_CODE["CLIENTE_NAO_ENCONTRADO"])

class TestDeleteVenda(unittest.TestCase):

    def test_01_deleteVenda_ok_retorno(self):
        print("Caso de teste (VENDA - deleteVenda) - Remoção")
        response = deleteVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_REMOVIDA"])

    def test_02_deleteVenda(self):
        print("Caso de teste (VENDA - deleteVenda) - Venda já concluída")
        response = deleteVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_03_deleteVenda(self):
        print("Caso de teste (VENDA - deleteVenda) - Venda não encontrada")
        response = deleteVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(TestShowVendas('test_02_showVendas_nok_venda_nao_encontrada'))
    suite.addTest(TestShowVendasClientes('test_02_showVendasCliente_nok_nenhuma_venda_encontrada'))
    suite.addTest(unittest.makeSuite(TestCreateVenda))
    suite.addTest(unittest.makeSuite(TestConcludeVenda))
    suite.addTest(unittest.makeSuite(TestAddProduto))
    suite.addTest(unittest.makeSuite(TestUpdateVenda))
    suite.addTest(unittest.makeSuite(TestShowVenda))
    suite.addTest(TestShowVendas('test_01_showVendas_ok_retorno'))
    suite.addTest(TestShowVendasClientes('test_01_showVendasCliente_ok_retorno'))
    suite.addTest(unittest.makeSuite(TestRemoveProduto))
    suite.addTest(unittest.makeSuite(TestDeleteVenda))

    return suite

# Executa os testes
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())