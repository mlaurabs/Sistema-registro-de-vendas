import unittest
from unittest.mock import patch
import os
from cliente import *
from src.status_code import *

# createCliente
class TestCreateCliente(unittest.TestCase):

    def test_01_create_cliente_ok_retorno(self):
        print("Caso de teste - Criação do cliente com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_create_cliente_ok_inserido(self):
        print("Caso de teste - Verificação de existência do cliente")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "13/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_create_cliente_nok_cpf_nulo(self):
        print("Caso de teste - CPF do cliente não pode ser nulo")
        retorno_obtido = createCliente("", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_create_cliente_nok_nome_nulo(self):
        print("Caso de teste - Nome do cliente não pode ser nulo")
        retorno_obtido = createCliente("155.998.027-36", "", "13/10/2003")
        retorno_esperado = STATUS_CODE["NOME_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_create_cliente_nok_data_nascimento_nulo(self):
        print("Caso de teste - Data de nascimento do cliente não pode ser nula")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["DATA_NASCIMENTO_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_create_cliente_nok_cpf_formato(self):
        print("Caso de teste - CPF do cliente com formato incorreto")
        retorno_obtido = createCliente("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_create_cliente_nok_nome_formato(self):
        print("Caso de teste - Nome do cliente com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_create_cliente_nok_data_nascimento_formato(self):
        print("Caso de teste - Data de nascimento do cliente inválida")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_create_cliente_nok_menor_de_idade(self):
        print("Caso de teste - Cliente menor de idade")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_10_create_produto_nok_produto_existente(self):
        print("Caso de teste - Produto já existente")
        retorno_obtido = createCliente("155.998.027-36", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CLIENTE_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showCliente
class TestShowCliente(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_cliente_id_ok_encontrado(self, mock_stdout):
        print("Caso de teste - Cliente exibido com sucesso")
        retorno_obtido = showCliente("155.998.027-36")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_cliente_id_nok_nao_encontrado(self):
        print("Caso de teste - Cliente não encontrado")
        retorno_obtido = showCliente("155.998.000-00")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateClienteByCpf
class TestUpdateClienteByCpf(unittest.TestCase):

    def test_01_update_cliente_by_cpf_ok_retorno(self):
        print("Caso de teste - Atualização do cliente pelo CPF realizada com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiroa", "")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_update_cliente_by_cpf_ok_inserido(self):
        print("Caso de teste - Verificação de existência do cliente ao atualizar pelo CPF")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiroa", "data_nascimento": "13/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_update_cliente_by_cpf_nok_cpf_nulo(self):
        print("Caso de teste - CPF do cliente não pode ser nulo")
        retorno_obtido = updateClienteByCpf("", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_cliente_by_cpf_nok_cpf_formato(self):
        print("Caso de teste - CPF do cliente com formato incorreto")
        retorno_obtido = updateClienteByCpf("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_update_cliente_by_cpf_nok_nome_formato(self):
        print("Caso de teste - Nome do cliente com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_cliente_by_cpf_nok_data_nascimento_formato(self):
        print("Caso de teste - Data de nascimento do cliente inválida")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_update_cliente_by_cpf_nok_menor_de_idade(self):
        print("Caso de teste - Cliente menor de idade")
        retorno_obtido = updateClienteByCpf("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateClienteByNome
class TestUpdateClienteByNome(unittest.TestCase):

    def test_01_update_cliente_by_nome_ok_retorno(self):
        print("Caso de teste - Atualização do cliente pelo Nome realizada com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = updateClienteByNome("155.998.027-00", "Matheus Figueiredo", "")
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_update_cliente_by_nome_ok_inserido(self):
        print("Caso de teste - Verificação de existência do cliente ao atualizar pelo Nome")
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        cliente_esperado = {"cpf": "155.998.027-00", "nome": "Matheus Figueiredo", "data_nascimento": "13/10/2003"}
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_update_cliente_by_nome_nok_nome_nulo(self):
        print("Caso de teste - Nome do cliente não pode ser nulo")
        retorno_obtido = updateClienteByNome("155.998.027-00", "", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_cliente_by_cpf_nok_nome_formato(self):
        print("Caso de teste - CPF do cliente com formato incorreto")
        retorno_obtido = updateClienteByNome("155", "Matheus Figueiredo", "13/10/2003")
        retorno_esperado = STATUS_CODE["CPF_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_update_cliente_by_nome_nok_nome_formato(self):
        print("Caso de teste - Nome do cliente com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo Matheus Figueiredo", "")
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_cliente_by_nome_nok_data_nascimento_formato(self):
        print("Caso de teste - Data de nascimento do cliente inválida")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo", "13")
        retorno_esperado = STATUS_CODE["DATA_NASCIMENTO_INVALIDA"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_update_cliente_by_nome_nok_menor_de_idade(self):
        print("Caso de teste - Cliente menor de idade")
        retorno_obtido = updateClienteByNome("155.998.027-36", "Matheus Figueiredo", "13/10/2024")
        retorno_esperado = STATUS_CODE["MENOR_DE_IDADE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# getCliente
class TestGetCliente(unittest.TestCase):

    def test_01_get_cliente_ok_retorno(self):
        print("Caso de teste - Cliente obtido com sucesso")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getCliente("155.998.027-36", temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_cliente_ok_obtido(self):
        print("Caso de teste - Verificação de devolução do cliente")
        cliente_esperado = {"cpf": "155.998.027-36", "nome": "Matheus Figueiredo", "data_nascimento": "13/10/2003"}
        cliente_obtido = dict()
        getCliente("155.998.027-36", cliente_obtido)
        self.assertEqual(cliente_esperado, cliente_obtido)

    def test_03_get_cliente_nok_nao_encontrado(self):
        print("Caso de teste - Cliente não encontrado")
        temp = dict()
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = getCliente("000.998.027-36", temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# showClientes
class TestShowClientes(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_clientes_ok_retorno(self, mock_stdout):
        print("Caso de teste - Clientes exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showClientes()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_clientes_nok_nenhum_cliente_cadastrado(self):
        print("Caso de teste - Nenhum cliente cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_CLIENTE_CADASTRADO"]
        retorno_obtido = showClientes()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showClientesByNome
class TestShowClientesByNome(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_clientes_nome_ok_retorno(self, mock_stdout):
        print("Caso de teste - Clientes com nome parecido exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showClientesByNome("Matheus")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nome_nok_nenhum_cliente_encontrado(self):
        print("Caso de teste - Nenhum cliente com nome parecido cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_CLIENTE_ENCONTRADO"]
        retorno_obtido = showClientesByNome("Amdullah")
        self.assertEqual(retorno_esperado, retorno_obtido)

# deleteCliente
class TestDeleteCliente(unittest.TestCase):

    def test_01_delete_cliente_ok_retorno(self):
        print("Caso de teste - Cliente excluído com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteCliente("155.998.027-36")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_delete_cliente_ok_removido(self):
        print("Caso de teste - Veriicação de remoção do cliente")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = showCliente("155.998.027-36")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_03_delete_cliente_nok_nenhum_cliente_encontrado(self):
        print("Caso de teste - Cliente não encontrado")
        retorno_esperado = STATUS_CODE["CLIENTE_NAO_ENCONTRADO"]
        retorno_obtido = deleteCliente("1")
        self.assertEqual(retorno_esperado, retorno_obtido)

    '''
    def test_04_delete_cliente_nok_cliente_cadastrado_em_venda(self):
        print("Caso de teste - Cliente cadastrado em venda")
        retorno_esperado = STATUS_CODE["CLIENTE_CADASTRADO_EM_VENDA"]
        retorno_obtido = deleteCliente("155.998.027.37")
        self.assertEqual(retorno_esperado, retorno_obtido)
    '''

# geraRelatorioCliente e leRelatorioCliente
class TestRelatorioCliente(unittest.TestCase):
    
    def test_01_gera_relatorio_cliente(self):
        print("Caso de teste - Relatório de clientes gerado com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = geraRelatorioCliente()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_le_relatorio_cliente(self):
        print("Caso de teste - Leitura de relatório de cliente e cadastro no sistema")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = leRelatorioCliente()
        self.assertEqual(retorno_esperado, retorno_obtido)


# Define a ordem de testes das classes
def suite():
    suite = unittest.TestSuite()

    # Adicionando as classes e os testes na ordem desejada
    suite.addTest(TestShowClientes('test_02_show_clientes_nok_nenhum_cliente_cadastrado'))
    suite.addTest(unittest.makeSuite(TestCreateCliente))
    suite.addTest(unittest.makeSuite(TestShowClientes))
    suite.addTest(unittest.makeSuite(TestGetCliente))
    suite.addTest(TestShowClientes('test_01_show_clientes_ok_retorno'))
    suite.addTest(unittest.makeSuite(TestShowClientesByNome))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByCpf))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByNome))
    suite.addTest(unittest.makeSuite(TestDeleteCliente))
    suite.addTest(unittest.makeSuite(TestRelatorioCliente))

    return suite

# Executa os testes
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())