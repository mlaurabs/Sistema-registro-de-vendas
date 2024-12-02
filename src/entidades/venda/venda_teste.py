import unittest
from unittest.mock import patch
import os
from .venda import *
from src.status_code import *

# createVenda
class TestCreateVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("123.456.789-01", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaClientes()

    def test_01_createVenda_ok_retorno(self):
        print("Caso de teste (VENDA - createVenda) - Sucesso")
        response = createVenda("123.456.789-01", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_createVenda_ok_inserido(self):
        print("Caso de teste (VENDA - createVenda) - Verificação de existência")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "123.456.789-01", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": []}
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

# createVenda (SEM CLIENTE) 
class TestCreateVendaSemCliente(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    def test_01_createVenda_ok_retorno_cliente_nulo(self):
        print("Caso de teste (VENDA - createVenda) - Sucesso sem Cliente")
        response = createVenda("", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_createVenda_ok_inserido_cliente_nulo(self):
        print("Caso de teste (VENDA - createVenda) - Verificação de existência para cliente nulo")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": []}
        self.assertEqual(response, expected)

    def test_03_createVenda_ok_retorno_cliente_nulo_repeticao(self):
        print("Caso de teste (VENDA - createVenda) - Sucesso sem Cliente (REPETIDO)")
        response = createVenda("", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_04_createVenda_ok_inserido_cliente_nulo_repeticao(self):
        print("Caso de teste (VENDA - createVenda) - Verificação de existência para cliente nulo (REPETIDO)")
        response = dict()
        getVenda(2, response)
        expected = {"id": 2, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": []}
        self.assertEqual(response, expected)

# getVenda
class TestGetVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        flag = createVenda("", "15/11/2024", "10:30")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    def test_01_get_venda_ok_retorno(self):
        print("Caso de teste (VENDA - getVenda) - Busca")
        temp = dict()
        response = getVenda(1, temp)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_get_venda_ok_inserido(self):
        print("Caso de teste (VENDA - getVenda) - Verificação de resultado")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": []}
        self.assertEqual(response, expected)

    def test_03_get_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - getVenda) - Venda não encontrada")
        temp = dict()
        response = getVenda(2, temp)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])
        
# concludeVenda
class TestConcludeVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        createVenda("", "15/11/2024", "10:50")
        cancelaVenda(2)

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    def test_01_concludeVenda_ok_retorno(self):
        print("Caso de teste (VENDA - concludeVenda) - Conclusão de venda")
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_concludeVenda_ok_alterada(self):
        print("Caso de teste (VENDA - concludeVenda) - Verificação de alteração")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "concluída", "produtos": []}
        self.assertEqual(response, expected)

    def test_03_concludeVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda não encontrada")
        response = concludeVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_concludeVenda_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda já concluída")
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_concludeVenda_nok_venda_ja_cancelada(self):
        print("Caso de teste (VENDA - concludeVenda) - Venda já cancelada")
        response = concludeVenda(2)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

# cancelaVenda
class TestCancelaVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        createVenda("", "15/11/2024", "10:50")
        concludeVenda(2)

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    def test_01_cancelaVenda_ok_retorno(self):
        print("Caso de teste (VENDA - cancelaVenda) - Cancelamento")
        response = cancelaVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_cancelaVenda_ok_alterada(self):
        print("Caso de teste (VENDA - cancelaVenda) - Verificação de alteração")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "cancelada", "produtos": []}
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

# addProduto
class TestAddProduto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Venda principal
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        atualizaQtdEstoque(1, 500)
        createVenda("", "15/11/2024", "10:30")
        # Venda concluída
        createVenda("", "15/11/2024", "10:30")
        concludeVenda(2)
        # Venda cancelada
        createVenda("", "15/11/2024", "10:30")
        cancelaVenda(3)

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaProdutos()
        limpaEstoque()

    def test_01_addProduto_ok_retorno(self):
        print("Caso de teste (VENDA - addProduto) - Produto adicionado")
        response = addProduto(1, 1, 5)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_addProduto_ok_adicionado(self):
        print("Caso de teste (VENDA - addProduto) - Verificação de adição")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": [{"id": 1, "quantidade": 5, "preco": 3}]}
        self.assertEqual(response, expected)

    def test_03_addProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - addProduto) - Venda não encontrada")
        response = addProduto(99, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_addProduto_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - addProduto) - Venda já concluída")
        response = addProduto(2, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_addProduto_nok_venda_ja_cancelada(self):
        print("Caso de teste (VENDA - addProduto) - Venda já cancelada")
        response = addProduto(3, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

    def test_06_addProduto_estoque_insuficiente(self):    
        print("Caso de teste (VENDA - addProduto) - Estoque insuficiente")
        response = addProduto(1, 1, 1000)
        self.assertEqual(response, STATUS_CODE["VENDA_ESTOQUE_INSUFICIENTE"])

# addProduto
class TestRemoveProduto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Venda principal
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        atualizaQtdEstoque(1, 500)
        createVenda("", "15/11/2024", "10:30")
        addProduto(1, 1, 5)
        # Venda concluída
        createVenda("", "15/11/2024", "10:30")
        concludeVenda(2)
        # Venda cancelada
        createVenda("", "15/11/2024", "10:30")
        cancelaVenda(3)
        # Auxiliar
        createProduto("Coca-Cola Zero 500ml", "Coca-Cola", "Bebidas", 10, 8)

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaProdutos()
        limpaEstoque()

    def test_01_removeProduto_ok_retorno(self):
        print("Caso de teste (VENDA - removeProduto) - Remoção de produto")
        response = removeProduto(1, 1, 3)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_removeProduto_ok_reduzido(self):
        print("Caso de teste (VENDA - removeProduto) - Verificação de redução")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": [{"id": 1, "quantidade": 2, "preco": 3}]}
        self.assertEqual(response, expected)

    def test_03_removeProduto_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - removeProduto) - Venda não encontrada")
        response = removeProduto(99, 1, 3)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test_04_removeProduto_nok_venda_ja_concluida(self):
        print("Caso de teste (VENDA - removeProduto) - Venda já concluída")
        response = addProduto(2, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test_05_removeProduto_nok_venda_ja_cancelada(self):
        print("Caso de teste (VENDA - removeProduto) - Venda já cancelada")
        response = addProduto(3, 1, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CANCELADA"])

    def test_06_removeProduto_nok_produto_nao_encontrado(self):
        print("Caso de teste (VENDA - removeProduto) - Produto não incluído na venda")
        response = removeProduto(1, 101, 100)
        self.assertEqual(response, STATUS_CODE["PRODUTO_NAO_ENCONTRADO"])

    def test_07_removeProduto_nok_quantidade_insuficiente(self):
        print("Caso de teste (VENDA - removeProduto) - Quantidade insuficiente")
        response = removeProduto(1, 1, 1000)
        self.assertEqual(response, STATUS_CODE["VENDA_QUANTIDADE_INSUFICIENTE"])

    def test_08_removeProduto_nok_produto_nao_incluido_na_venda(self):
        print("Caso de teste (VENDA - removeProduto) - Produto não incluído na venda")
        response = removeProduto(1, 2, 100)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_INCLUIDO"])

    def test_09_removeProduto_ok_removido(self):
        removeProduto(1, 1, 2)
        print("Caso de teste (VENDA - removeProduto) - Verificação de remoção")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "10:30", "status": "em processamento", "produtos": []}
        self.assertEqual(response, expected)

# updateVenda
class TestUpdateVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    def test_01_updateVenda_ok_retorno(self):
        print("Caso de teste (VENDA - updateVenda) - Alteração")
        response = updateVenda(1, "", "", "13:53")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_updateVenda_ok_alterada(self):
        print("Caso de teste (VENDA - updateVenda) - Verificação de alteração")
        response = dict()
        getVenda(1, response)
        expected = {"id": 1, "cpf": "", "data": "15/11/2024", "hora": "13:53", "status": "em processamento", "produtos": []}
        self.assertEqual(response, expected)
    
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

# showVenda
class TestShowVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVenda_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVenda) - Exibição")
        response = showVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_02_showVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - updateVenda) - Venda não encontrada")
        response = showVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# showVendas
class TestShowVendas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        createVenda("", "15/11/2024", "10:50")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendas_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendas) - Exibição")
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendas_nok_venda_nao_encontrada(self):
        limpaVendas()
        print("Caso de teste (VENDA - showVendas) - Nenhuma venda cadastrada")
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["VENDA_NENHUM_CADASTRO"])

# showVendasCliente
class TestShowVendasClientes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("123.456.789-01", "Matheus Figueiredo", "13/10/2003")
        createVenda("123.456.789-01", "15/11/2024", "10:30")
        createVenda("123.456.789-01", "15/11/2024", "10:50")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaClientes()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendasCliente_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendasClientes) - Exibição")
        response = showVendasCliente("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_showVendasCliente_nok_cliente_nao_encontrado(self):  
        print("Caso de teste (VENDA - showVendasClientes) - Cliente não encontrado")
        response = showVendasCliente("123")
        self.assertEqual(response, STATUS_CODE["CLIENTE_NAO_ENCONTRADO"])

    def test_03_showVendasCliente_nok_nenhuma_venda_encontrada(self):  
        limpaVendas()
        print("Caso de teste (VENDA - showVendasClientes) - Nenhuma venda encontrada")
        response = showVendasCliente("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# showVendasData
class TestShowVendasData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        createVenda("", "15/11/2024", "10:50")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_showVendasData_ok_retorno(self, mock_stdout):
        print("Caso de teste (VENDA - showVendasData) - Exibição")
        response = showVendasData("15/11/2024")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_03_showVendasData_nok_nenhuma_venda_encontrada(self):  
        limpaVendas()
        print("Caso de teste (VENDA - showVendasData) - Nenhuma venda encontrada")
        response = showVendasData("15/11/2024")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# checkProdutoVenda
class TestCheckProdutoVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        atualizaQtdEstoque(1, 500)
        addProduto(1, 1, 5)

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaProdutos()
        limpaEstoque()

    def test_01_checkProdutoVenda_ok_retorno(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto encontrado em vendas")
        response = checkProdutoVenda(1)
        self.assertEqual(response, STATUS_CODE["SUCESSO"])
    
    def test_01_checkProdutoVenda_nok_produto_nao_encontrado(self):
        print("Caso de teste (VENDA - checkProdutoVenda) - Produto não encontrado em nenhuma venda")
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["VENDA_PRODUTO_NAO_ENCONTRADO"])

# checkClienteVenda
class TestCheckClienteVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("123.456.789-01", "Matheus Figueiredo", "13/10/2003")
        createVenda("123.456.789-01", "15/11/2024", "10:30")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()
        limpaClientes()

    def test_01_checkClienteVenda_ok_retorno(self):
        print("Caso de teste (VENDA - checkClienteVenda) - Cliente encontrado em vendas")
        response = checkClienteVenda("123.456.789-01")
        self.assertEqual(response, STATUS_CODE["SUCESSO"])

    def test_02_checkClienteVenda_nok_cliente_nao_encontrado(self):
        print("Caso de teste (VENDA - checkClienteVenda) - Cliente não encontrado em vendas")
        response = checkClienteVenda("12")
        self.assertEqual(response, STATUS_CODE["VENDA_CLIENTE_NAO_ENCONTRADO"])

# deleteVenda
class TestDeleteVenda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createVenda("", "15/11/2024", "10:30")
        cancelaVenda(1)
        createVenda("", "15/11/2024", "10:30")
        concludeVenda(2)
        createVenda("", "15/11/2024", "10:30")

    @classmethod
    def tearDownClass(cls):
        limpaVendas()

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
        response = deleteVenda(3)
        self.assertEqual(response, STATUS_CODE["VENDA_EM_PROCESSAMENTO"])

    def test_04_deleteVenda_nok_venda_nao_encontrada(self):
        print("Caso de teste (VENDA - deleteVenda) - Venda não encontrada")
        response = deleteVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestRelatorioVenda(unittest.TestCase):
    
    def test_01_carregar_vendas(self):
        print("Caso de teste (VENDA - carregarVendas) - Carrega as vendas salvas")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = carregarVendas()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_carregar_vendas(self):
        print("Caso de teste (VENDA - salvarVendas) - Salvar vendas")
        retorno_esperado = STATUS_CODE["ERRO"]
        retorno_obtido = salvarVendas()
        self.assertIsNot(retorno_esperado, retorno_obtido)

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(unittest.makeSuite(TestCreateVenda))
    suite.addTest(unittest.makeSuite(TestCreateVendaSemCliente))
    suite.addTest(unittest.makeSuite(TestGetVenda))
    suite.addTest(unittest.makeSuite(TestConcludeVenda))
    suite.addTest(unittest.makeSuite(TestCancelaVenda))
    suite.addTest(unittest.makeSuite(TestAddProduto))
    suite.addTest(unittest.makeSuite(TestRemoveProduto))
    suite.addTest(unittest.makeSuite(TestUpdateVenda))
    suite.addTest(unittest.makeSuite(TestShowVenda))
    suite.addTest(unittest.makeSuite(TestShowVendas))
    suite.addTest(unittest.makeSuite(TestShowVendasClientes))
    suite.addTest(unittest.makeSuite(TestShowVendasData))
    suite.addTest(unittest.makeSuite(TestCheckProdutoVenda))
    suite.addTest(unittest.makeSuite(TestCheckClienteVenda))
    suite.addTest(unittest.makeSuite(TestDeleteVenda))
    suite.addTest(unittest.makeSuite(TestRelatorioVenda))

    return suite

# Executa os testes
if __name__ == "__main__":
    from ..cliente.cliente import createCliente, limpaClientes
    from ..produto.produto import createProduto, limpaProdutos
    from ..estoque.estoque import atualizaQtdEstoque, limpaEstoque
    runner = unittest.TextTestRunner()
    runner.run(suite())
