import unittest
from datetime import datetime
from .venda import *
from src.status_code import *


class TestCreateVenda(unittest.TestCase):

    def test01_createVenda(self):
        # Teste de criação de venda com dados válidos
        response = createVenda("12345678901", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_CADASTRADA"])

    def test02_createVenda(self):
        # Teste de criação de venda com CPF inválido
        response = createVenda("12345678", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["CLIENTE_NAO_ENCONTRADO"])

    def test03_createVenda(self):
        # Teste de venda com data no formato inválido
        response = createVenda("12345678901", "2024-11-15", "10:30")
        self.assertEqual(response, STATUS_CODE["DATA_FORMATO_INVALIDO"])

    def test04_createVenda(self):
        # Teste de venda com data no formato inválido
        response = createVenda("1*-s45678901", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["CPF_FORMATO_INVALIDO"])

    def test05_createVenda(self):
        # Teste de venda com hora no formato inválido
        response = createVenda("12345678901", "15/11/2024", "1030")
        self.assertEqual(response, STATUS_CODE["HORA_FORMATO_INVALIDO"])

    def test06_createVenda(self):
        # Teste de venda existente
        response = createVenda("12345678901", "15/11/2024", "10:30")
        self.assertEqual(response, STATUS_CODE["VENDA_EXISTENTE"])

class TestConcludeVenda(unittest.TestCase):
    def test01_concludeVenda(self):
        # Criar venda
        createVenda("12345678901", "15/11/2024", "10:30")

        # Teste de conclusão de venda com id válido
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_CONCLUIDA"])

    def test02_concludeVenda(self):
        # Teste de venda já concluída
        response = concludeVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test03_concludeVenda(self):
        # Teste de venda não encontrada
        response = concludeVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestAddProduto(unittest.TestCase):
    def test01_addProduto(self):
        # Criar venda e adicionar produto
        createVenda("12345678901", "15/11/2024", "10:30")
        
        # Teste de adição de produto com sucesso
        response = addProduto(1, 101, 5)
        self.assertEqual(response, STATUS_CODE["PRODUTO_ADICIONADO"])

    def test02_addProduto(self):
        # Teste de venda não encontrada
        response = addProduto(99, 101, 5)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test03_addProduto(self):
        # Teste de produto não encontrado no estoque
        response = addProduto(1, 999, 5)
        self.assertEqual(response, STATUS_CODE["PRODUTO_NAO_ENCONTRADO_ESTOQUE"])

    def test04_addProduto(self):    
        # Teste de estoque insuficiente
        response = addProduto(1, 101, 1000)
        self.assertEqual(response, STATUS_CODE["ESTOQUE_INSUFICIENTE"])

class TestRemoveProduto(unittest.TestCase):
    def test01_removeProduto(self):
        # Criar venda e adicionar produto
        createVenda("12345678901", "15/11/2024", "10:30")
        addProduto(1, 101, 5)

        # Teste de remoção de produto com sucesso
        response = removeProduto(1, 101, 3)
        self.assertEqual(response, STATUS_CODE["PRODUTO_REMOVIDO"])

    def test02_removeProduto(self):
        # Teste de venda não encontrada
        response = removeProduto(99, 101, 3)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

    def test03_removeProduto(self):
        # Teste de produto não incluído na venda
        response = removeProduto(1, 101, 100)
        self.assertEqual(response, STATUS_CODE["PRODUTO_NAO_INCLUIDO"])

class TestUpdateVenda(unittest.TestCase):
    def test01_updateVenda(self):
        # Teste de alteração de venda com sucesso
        createVenda("12345678901", "15/11/2024", "10:30")

        response = updateVenda(1, "05/05/2004", "13:53")
        self.assertEqual(response, STATUS_CODE["VENDA_ALTERADA"])
    
    def test02_updateVenda(self):
        # Teste de alteração de venda com data inválida
        createVenda("12345678901", "15/11/2024", "10:30")

        response = updateVenda(1, "05-05-2004", "13:53")
        self.assertEqual(response, STATUS_CODE["DATA_FORMATO_INVALIDO"])

    def test02_updateVenda(self):
        # Teste de alteração de venda com hora inválida
        createVenda("12345678901", "15/11/2024", "10:30")

        response = updateVenda(1, "05-05-2004", "13//53")
        self.assertEqual(response, STATUS_CODE["HORA_FORMATO_INVALIDO"])

class TestShowVenda(unittest.TestCase):
    def test01_showVenda(self):
        # Criar venda
        createVenda("12345678901", "15/11/2024", "10:30")

        # Teste de exibição de venda com id válido
        response = showVenda(1)
        self.assertEqual(response["id"], 1)
    
    def test02_showVenda(self):
        # Teste de venda não encontrada
        response = showVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestShowVendas(unittest.TestCase):
    def test01_showVendas(self):
        # Teste de exibição de todas as vendas
        createVenda("12345678901", "15/11/2024", "10:30")
        createVenda("12349998901", "10/10/2023", "09:30")
        response = showVendas()
        self.assertEqual(len(response), 2)

    def test02_showVendas(self):
        # Teste de nenhuma venda encontrada
        response = showVendas()
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestShowVendasClientes(unittest.TestCase):
    def test01_showVendasCliente(self):
        # Criar venda
        createVenda("12345678901", "15/11/2024", "10:30")
        createVenda("12345678901", "16/12/2024", "12:35")

        # Teste de exibição de vendas de um cliente
        response = showVendasCliente("12345678901")
        self.assertEqual(len(response), 2)

    def test02_showVendasCliente(self):
        # Teste de vendas de cliente não encontrado
        response = showVendasCliente("98765432100")
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

class TestcheckProdutoVenda(unittest.TestCase):
    def test01_checkProdutoVenda(self):
        createVenda("12345678901", "16/12/2024", "12:35")
        addProduto(1, 101, 5)

        # Teste de busca por produtos associados a vendas
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["PRODUTO_ENCONTRADO_EM_VENDAS"])
    
    def test01_checkProdutoVenda(self):
        createVenda("12345678901", "16/12/2024", "12:35")
        addProduto(1, 12, 5)

        # Teste de busca por produtos associados a vendas
        response = checkProdutoVenda(101)
        self.assertEqual(response, STATUS_CODE["PRODUTO_NAO_ENCONTRADO_EM_VENDAS"])

class TestcheckClienteVenda(unittest.TestCase):
    def test01_checkClienteVenda(self):
        createVenda("12345678901", "16/12/2024", "12:35")

        # Teste de busca por clientes associados a vendas
        response = checkClienteVenda("12345678901")
        self.assertEqual(response, STATUS_CODE["CLIENTE_ENCONTRADO"])

    def test01_checkClienteVenda(self):
        createVenda("12345678102", "16/12/2024", "12:35")

        # Teste de busca por clientes associados a vendas
        response = checkClienteVenda("12345678901")
        self.assertEqual(response, STATUS_CODE["CLIENTE_NAO_ENCONTRADO"])

class TestDeleteVenda(unittest.TestCase):
    def test01_deleteVenda(self):
        # Criar 
        createVenda("12345678901", "15/11/2024", "10:30")

        # Teste de remoção de venda com sucesso
        response = deleteVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_REMOVIDA"])

    def test02_deleteVenda(self):
        # Criar e concluir venda
        createVenda("12345678901", "15/11/2024", "10:30")
        concludeVenda(1)

        # Teste de remoção de venda já concluída
        response = deleteVenda(1)
        self.assertEqual(response, STATUS_CODE["VENDA_JA_CONCLUIDA"])

    def test03_deleteVenda(self):
        # Teste de venda não encontrada
        response = deleteVenda(99)
        self.assertEqual(response, STATUS_CODE["VENDA_NAO_ENCONTRADA"])

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(unittest.makeSuite(TestCreateVenda))
    suite.addTest(unittest.makeSuite(TestConcludeVenda))
    suite.addTest(unittest.makeSuite(TestAddProduto))
    suite.addTest(unittest.makeSuite(TestRemoveProduto))
    suite.addTest(unittest.makeSuite(TestUpdateVenda))
    suite.addTest(unittest.makeSuite(TestShowVenda))
    suite.addTest(unittest.makeSuite(TestShowVendas))
    suite.addTest(unittest.makeSuite(TestShowVendasClientes))
    suite.addTest(unittest.makeSuite(TestcheckProdutoVenda))
    suite.addTest(unittest.makeSuite(TestcheckClienteVenda))
    suite.addTest(unittest.makeSuite(TestDeleteVenda))

    return suite

# Executa os testes
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())