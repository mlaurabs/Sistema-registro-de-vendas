import unittest
from unittest.mock import patch
import os
from .cliente import *
from src.status_code import *

# createCliente
class TestCreateCliente(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    def test_01_create_cliente_ok_retorno(self):
        print("Caso de teste (CLIENTE - createCliente) - Criação")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_create_cliente_ok_inserido(self):
        print("Caso de teste (CLIENTE - createCliente) - Verificação de existência")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "13/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_create_cliente_nok_cpf_vazio(self):
        print("Caso de teste (CLIENTE - createCliente) - CPF não pode ser vazio")
        retorno_obtido = createCliente("", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_CPF_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_create_cliente_nok_nome_vazio(self):
        print("Caso de teste (CLIENTE - createCliente) - Nome não pode ser vazio")
        retorno_obtido = createCliente("155.998.027-36", "", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_NOME_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_create_cliente_nok_data_nascimento_vazio(self):
        print("Caso de teste (CLIENTE - createCliente) - Data de nascimento não pode ser vazia")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["CLIENTE_DATA_NASCIMENTO_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_create_cliente_nok_cpf_formato_incorreto(self):
        print("Caso de teste (CLIENTE - createCliente) - CPF com formato incorreto")
        retorno_obtido = createCliente("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_create_cliente_nok_nome_formato_incorreto(self):
        print("Caso de teste (CLIENTE - createCliente) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_create_cliente_nok_data_nascimento_formato_incorreto(self):
        print("Caso de teste (CLIENTE - createCliente) - Data de nascimento inválida")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["CLIENTE_DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_update_cliente_by_cpf_nok_menor_de_idade(self):
        print("Caso de teste (CLIENTE - createCliente) - Cliente menor de idade")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["CLIENTE_MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_09_create_cliente_nok_cliente_existente(self):
        print("Caso de teste (CLIENTE - createCliente) - Cliente já existente")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showCliente
class TestShowCliente(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_cliente_id_ok_encontrado(self, mock_stdout):
        print("Caso de teste (CLIENTE - showCliente) - Exibição")
        retorno_obtido = showCliente("155.998.027-36")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_cliente_id_nok_nao_encontrado(self):
        print("Caso de teste (CLIENTE  - showCliente) - Cliente não encontrado")
        retorno_obtido = showCliente("155.998.000-00")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateClienteByCpf
class TestUpdateClienteByCpf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    def test_01_update_cliente_by_cpf_ok_retorno(self):
        print("Caso de teste (CLIENTE - updateClienteByCpf) - Atualização")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = updateClienteByCpf("155.998.027-36", "", "12/10/2003")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_update_cliente_by_cpf_ok_inserido(self):
        print("Caso de teste (CLIENTE  - updateClienteByCpf) - Verificação de existência")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "12/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_update_cliente_by_cpf_nok_cpf_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByCpf) - CPF com formato incorreto")
        retorno_obtido = updateClienteByCpf("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_cliente_by_cpf_nok_nome_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByCpf) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_update_cliente_by_cpf_nok_data_nascimento_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByCpf) - Data de nascimento inválida na atualização")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["CLIENTE_DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_cliente_by_cpf_nok_menor_de_idade(self):
        print("Caso de teste (CLIENTE - updateClienteByCpf) - Cliente menor de idade")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["CLIENTE_MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateClienteByNome
class TestUpdateClienteByNome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    def test_01_update_cliente_by_nome_ok_retorno(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - Atualização")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = updateClienteByNome("", "Matheus Figueiredo", "10/10/2003")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_update_cliente_by_nome_ok_inserido(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - Verificação de existência")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "10/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_update_cliente_by_cpf_nok_nome_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - CPF com formato incorreto")
        retorno_obtido = updateClienteByNome("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_CPF_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_cliente_by_nome_nok_nome_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["CLIENTE_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_update_cliente_by_nome_nok_data_nascimento_formato_incorreto(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - Data de nascimento inválida")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["CLIENTE_DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_cliente_by_nome_nok_menor_de_idade(self):
        print("Caso de teste (CLIENTE - updateClienteByNome) - Cliente menor de idade")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["CLIENTE_MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# getCliente
class TestGetCliente(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    def test_01_get_cliente_ok_retorno(self):
        print("Caso de teste (CLIENTE - getCliente) - Obtenção")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getCliente("155.998.027-36", temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_cliente_ok_obtido(self):
        print("Caso de teste (CLIENTE - getCliente) - Verificação de devolução")
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "13/10/2003"}
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_get_cliente_nok_nao_encontrado(self):
        print("Caso de teste (CLIENTE - getCliente) - Cliente não encontrado")
        temp = dict()
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = getCliente("000.998.027-36", temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# showClientes
class TestShowClientes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_clientes_ok_retorno(self, mock_stdout):
        print("Caso de teste (CLIENTE - showClientes) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showClientes()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_clientes_nok_nenhum_cliente_cadastrado(self):
        limpaClientes()
        print("Caso de teste (CLIENTE - showClientes) - Nenhum cliente cadastrado")
        retorno_esperado = STATUS_CODE["CLIENTE_NENHUM_CADASTRADO"]
        retorno_obtido = showClientes()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showClientesByNome
class TestShowClientesByNome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_clientes_nome_ok_retorno(self, mock_stdout):
        print("Caso de teste (CLIENTE - showClientesByNome) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showClientesByNome("Matheus")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nome_nok_nenhum_cliente_encontrado(self):
        print("Caso de teste (CLIENTE - showClientesByNome) - Nenhum cliente com nome parecido cadastrado")
        retorno_esperado = STATUS_CODE["CLIENTE_NENHUM_ENCONTRADO"]
        retorno_obtido = showClientesByNome("Amdullah")
        self.assertEqual(retorno_esperado, retorno_obtido)

# deleteCliente
class TestDeleteCliente(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Removido
        createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")
        # Castrado em venda
        createCliente("155.998.027-55", "Jonas Emanuel", "13/09/1987")
        createVenda("155.998.027-55", "20/05/2023", "12:53")

    @classmethod
    def tearDownClass(cls):
        limpaClientes()
        limpaVendas()

    def test_01_delete_cliente_ok_retorno(self):
        print("Caso de teste (CLIENTE - deleteCliente) - Exclusão")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteCliente("155.998.027-36")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_delete_cliente_nok_cliente_cadastrado_em_venda(self):
        print("Caso de teste (CLIENTE - deleteCliente) - Cliente cadastrado em venda")
        retorno_esperado = STATUS_CODE["CLIENTE_CADASTRADO_EM_VENDA"]
        retorno_obtido = deleteCliente("155.998.027-55")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_03_delete_cliente_ok_removido(self):
        print("Caso de teste (CLIENTE - deleteCliente) - Veriicação de remoção")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = showCliente("155.998.027-36")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_04_delete_cliente_nok_nenhum_cliente_encontrado(self):
        print("Caso de teste (CLIENTE - deleteCliente) - Cliente não encontrado")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = deleteCliente("1")
        self.assertEqual(retorno_esperado, retorno_obtido)

class TestRelatorioCliente(unittest.TestCase):
    
    def test_01_carregar_cliente(self):
        print("Caso de teste (CLIENTE - carregarClientes) - Geração do relatório")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = carregarclientes()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_salvar_cliente(self):
        print("Caso de teste (CLIENTE - leRelatorioCliente) - Leitura do relatório e cadastro no sistema")
        retorno_esperado = STATUS_CODE["ERRO"]
        retorno_obtido = salvarclientes()
        self.assertIsNot(retorno_esperado, retorno_obtido)

# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(unittest.makeSuite(TestCreateCliente))
    suite.addTest(unittest.makeSuite(TestShowCliente))
    suite.addTest(unittest.makeSuite(TestGetCliente))
    suite.addTest(unittest.makeSuite(TestShowClientes))
    suite.addTest(unittest.makeSuite(TestShowClientesByNome))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByCpf))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByNome))
    suite.addTest(unittest.makeSuite(TestDeleteCliente))
    suite.addTest(unittest.makeSuite(TestRelatorioCliente))

    return suite

# Executa os testes
if __name__ == "__main__":
    from ..venda.venda import createVenda, limpaVendas
    runner = unittest.TextTestRunner()
    runner.run(suite())