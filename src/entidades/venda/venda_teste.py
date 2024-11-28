import unittest
from unittest.mock import patch
import os
from .venda import *
from src.status_code import *

# createVenda - JÁ REVISADO
class TestCreateVenda(unittest.TestCase):

    def test_01_createVenda_ok_retorno(self):
        createCliente("123.456.789-01", "Matheus Figueiredo", "13/10/2003")
        print("Caso de teste (VENDA - createVenda) - Sucesso")
        response = createVenda("123.456.789-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_createVenda_ok_inserido(self):
        print("Caso de teste (VENDA - createVenda) - Verificação de existência")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_createVenda_ok_cliente_nao_encontrado(self):
        print("Caso de teste (VENDA - createVenda) - Cliente não encontrado")
        response = createVenda("100.000.719-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["CLIENTE_NAO_ENCONTRADO"])

    def test_04_createVenda_nok_cpf_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - CPF no formato incorreto")
        response = createVenda("12345678", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"])

    def test_05_createVenda_nok_data_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - Data no formato incorreto")
        response = createVenda("123.456.789-01", "2024-11-15", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"])

    def test_05_createVenda_nok_hora_formato_incorreto(self):
        print("Caso de teste (VENDA - createVenda) - Hora no formato incorreto")
        response = createVenda("123.456.789-01", "15/11/2024", "10-30")
        self.assertEqual(response, STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"])

    def test_06_createVenda_nok_venda_existente(self):
        print("Caso de teste (VENDA - createVenda) - Venda existente")
        response = createVenda("123.456.789-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_EXISTENTE"])

# createVenda (SEM CLIENTE) - JÁ REVISADO
class TestCreateVendaSemCliente(unittest.TestCase):

    def test_01_createVenda_ok_retorno_cliente_nulo(self):
        print("Caso de teste (VENDA - createVenda) - Sucesso sem Cliente")
        response = createVenda("", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_createVenda_ok_inserido_cliente_nulo(self):
        print("Caso de teste (VENDA - createVenda) - Verificação de existência para cliente nulo")
        response = dict()
        getVenda(5, response)
        expected = {"id": 5, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produto": {}}
        self.assertEqual(response, expected)

# createVenda - JÁ REVISADO
class TestGetVenda(unittest.TestCase):

    def test_01_get_venda_ok_retorno(self):
        print("Caso de teste (VENDA - getVenda) - Busca")
        response = getVenda(1, response)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_get_venda_ok_inserido(self):
        print("Caso de teste (VENDA - getVenda) - Verificação de resultado")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_get_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - getVenda) - Venda não encontrada")
        response = getVenda(1, response)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# concludeVenda - JÁ REVISADO
class TestConcludeVenda(unittest.TestCase):

    def test_01_concludeVenda_ok_retorno(self):
        print("Caso de teste (VENDA - concludeVenda) - Conclusão de venda")
        createVenda("123.456.789-01", "15/11/2024", "20:00")
        response = concludeVenda(2)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_concludeVenda_ok_alterada(self):
        print("Caso de teste (VENDA - concludeVenda) - Verificação de alteração")
        response = dict()
        getVenda(2, response)
        expected = {"id": 2, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "20:00", "status": "concluída", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_concludeVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda não encontrada")
        response = concludeVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_concludeVenda_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda já concluída")
        response = concludeVenda(2)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_concludeVenda_nok_venda_ja_cancelada(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda já cancelada")
        createVenda("123.456.789-01", "15/11/2024", "12:00")
        cancelaVenda(3)
        response = concludeVenda(3)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

# cancelaVenda - JÁ REVISADO
class TestCancelaVenda(unittest.TestCase):

    def test_01_cancelaVenda_ok_retorno(self):
        print("Caso de teste (VENDA - cancelaVenda) - Cancelamento")
        response = cancelaVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_cancelaVenda_ok_alterada(self):
        print("Caso de teste (VENDA - cancelaVenda) - Verificação de alteração")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "10:30", "status": "cancelada", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_cancelaVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - cancelaVenda) - Venda não encontrada")
        response = cancelaVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_cancelaVenda_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - cancelaVenda) - Venda já concluída")
        response = cancelaVenda(2)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_cancela_Venda_nok_venda_ja_cancelada(self):
        print("Caso de teste (VENDA - cancelaVenda) - Venda já cancelada")
        response = cancelaVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

        print("Caso de teste (VENDA - cancelaVenda) - Venda não encontrada")
        response = cancelaVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# addProduto - REVISAR TESTE 2
class TestAddProduto(unittest.TestCase):

    def test_01_addProduto_ok_retorno(self):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 0)
        atualizaQtdEstoque(1, 500)
        createVenda("123.456.789-01", "15/11/2024", "05:00")
        print("Caso de teste (VENDA - addProduto) - Produto adicionado")
        response = addProduto(4, 1, 5)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_addProduto_ok_adicionado(self):
        print("Caso de teste (VENDA - addProduto) - Verificação de adição")
        response = dict()
        getVenda(4, response)
        expected = {"id": 4, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "05:00", "status": "em processamento", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_addProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - addProduto) - Venda não encontrada")
        response = addProduto(99, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_addProduto_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - addProduto) - Venda já concluída")
        response = addProduto(2, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_addProduto_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - addProduto) - Venda já cancelada")
        response = addProduto(1, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

    def test_06_addProduto_estoque_insuficiente(self):    
        print("Caso de teste (VENDA - addProduto) - Estoque insuficiente")
        response = addProduto(4, 1, 1000)
        self.assertEqual(response, STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"])

# addProduto - REVISAR TESTE 2
class TestRemoveProduto(unittest.TestCase):

    def test_01_removeProduto_ok_retorno(self):
        print("Caso de teste (VENDA - removeProduto) - Remoção de produto")
        response = removeProduto(4, 1, 1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_removeProduto_ok_removido(self):
        print("Caso de teste (VENDA - addProduto) - Verificação de remoção")
        response = dict()
        getVenda(4, response)
        expected = {"id": 4, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "05:00", "status": "em processamento", "produto": {}}
        self.assertEqual(response, expected)

    def test_03_removeProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - removeProduto) - Venda não encontrada")
        response = removeProduto(99, 1, 3)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_removeProduto_nok_produto_nao_incluido(self):
        print("Caso de teste (VENDA - removeProduto) - Produto não incluído na venda")
        response = removeProduto(4, 101, 100)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"])

    def test_05_removeProduto_nok_quantidade_insuficiente(self):
        print("Caso de teste (VENDA - removeProduto) - Produto não incluído na venda")
        response = removeProduto(4, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_QUANTIDADE_INSUFICIENTE"])

# updateVENDA - REVISAR
class TestUpdateVenda(unittest.TestCase):

    def test_01_updateVenda_ok_retorno(self):
        print("Caso de teste (VENDA - updateVenda) - Alteração")
        response = updateVenda(1, "", "", "13:53")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_updateVenda_ok_alterada(self):
        print("Caso de teste (VENDA - updateVenda) - Verificação de alteração")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "13:53", "status": "cancelada", "produto": {}}

        self.assertEqual(response, )
    
    def test_03_updateVenda_nok_cpf_formato_incorreto(self):
        print("Caso de teste (VENDA - updateVenda) - Data inválida")
        response = updateVenda(1, "314", "", "")
        self.assertEqual(response, STATUS_CODE["VENDA_CPF_FORMATO_INCORRETO"])

    def test_04_updateVenda_nok_data_formato_incorreto(self):
        print("Caso de teste (VENDA - updateVenda) - Data inválida")
        response = updateVenda(1, "", "05-05-2004", "")
        self.assertEqual(response, STATUS_CODE["VENDA_DATA_FORMATO_INCORRETO"])

    def test_05_updateVenda_nok_hora_formato_incorreto(self):
        print("Caso de teste (VENDA - updateVenda) - Hora inválida")
        response = updateVenda(1, "", "", "13//53")
        self.assertEqual(response, STATUS_CODE["VENDA_HORA_FORMATO_INCORRETO"])

    def test_06_updateVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - updateVenda) - Venda não encontrada")
        response = updateVenda(99, "", "", "13:53")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# showVenda - JÁ REVISADO
class TestShowVenda(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVenda_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVenda) - Exibição")
        response = showVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_showVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - updateVenda) - Venda não encontrada")
        response = showVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# showVendas - JÁ REVISADO
class TestShowVendas(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendas_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendas) - Exibição")
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendas_nok_venda_nao_encontrada(self):
        # Teste de nenhuma venda encontrada
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["VENDA_NENHUM_CADASTRO"])

# showVendasCliente - JÁ REVISADO
class TestShowVendasClientes(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendasCliente_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendasClientes) - Exibição")
        response = showVendasCliente("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendasCliente_nok_nenhuma_venda_encontrada(self):
        print("Caso de teste (VENDA - updateVenda) - Nenhuma venda encontrada")
        response = showVendasCliente("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# checkProdutoVenda - JÁ REVISADO
class TestCheckProdutoVenda(unittest.TestCase):

    def test_01_checkProdutoVenda_ok_retorno(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto encontrado em vendas")
        response = checkProdutoVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_01_checkProdutoVenda_nok_produto_nao_encontrado(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto não encontrado em nenhuma venda")
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"])

# checkClienteVenda - JÁ REVISADO
class TestCheckClienteVenda(unittest.TestCase):

    def test_01_checkClienteVenda_ok_retorno(self):
        print("Caso de teste (VENDA - checkClienteVenda) - Cliente encontrado em vendas")
        response = checkClienteVenda("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_checkClienteVenda_nok_cliente_nao_encontrado(self):
        print("Caso de teste (VENDA - checkClienteVenda) - Cliente encontrado em vendas")
        response = checkClienteVenda("12")
        self.assertEqual(response, STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"])

# deleteVenda - JÁ REVISADO
class TestDeleteVenda(unittest.TestCase):

    def test_01_deleteVenda_ok_retorno(self):
        print("Caso de teste (VENDA - deleteVenda) - Remoção")
        response = deleteVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_deleteVenda_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - deleteVenda) - Venda já concluída")
        response = deleteVenda(2)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_03_deleteVenda_nok_venda_em_processamento(self):
        createVenda("123.456.789-01", "15/11/2024", "00:01")
        response = deleteVenda(4)
        self.assertEqual(response, STATUS_CODE["VENDA_EM_PROCESSAMENTO"])

    def test_04_deleteVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - deleteVenda) - Venda não encontrada")
        response = deleteVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# geraRelatorioVenda e lerRelatorioVenda

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(TestShowVendas('test_02_showVendas_nok_venda_nao_encontrada'))
    suite.addTest(TestShowVendasClientes('test_02_showVendasCliente_nok_nenhuma_venda_encontrada'))
    suite.addTest(unittest.makeSuite(TestCreateVenda))
    suite.addTest(unittest.makeSuite(TestGetVenda))
    suite.addTest(unittest.makeSuite(TestConcludeVenda))
    suite.addTest(unittest.makeSuite(TestAddProduto))
    suite.addTest(unittest.makeSuite(TestUpdateVenda))
    suite.addTest(unittest.makeSuite(TestShowVenda))
    suite.addTest(TestShowVendas('test_01_showVendas_ok_retorno'))
    suite.addTest(TestShowVendasClientes('test_01_showVendasCliente_ok_retorno'))
    suite.addTest(unittest.makeSuite(TestRemoveProduto))
    suite.addTest(unittest.makeSuite(TestDeleteVenda))
    suite.addTest(unittest.makeSuite(TestCreateVendaSemCliente))

    return suite

# Executa os testes
if __name__ == "__main__":
    from ..cliente.cliente import createCliente
    from ..produto.produto import createProduto
    from ..estoque.estoque import atualizaQtdEstoque
    runner = unittest.TextTestRunner()
    runner.run(suite())