import unittest
from unittest.mock import patch
import os
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

# createProduto
class TestCreateProduto(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

    def test_01_create_produto_ok_retorno(self):
        print("Caso de teste (PRODUTO - createProduto) - Criação")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_create_produto_ok_inserido(self):
        print("Caso de teste (PRODUTO - createProduto) - Verificação de existência")
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        produto_obtido.pop("id")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3}
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_create_produto_nok_nome_vazio(self):
        print("Caso de teste (PRODUTO - createProduto) - Nome não pode estar vazio")
        retorno_obtido = createProduto("", "Coca-Cola", "Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_NOME_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_create_produto_nok_marca_vazia(self):
        print("Caso de teste (PRODUTO - createProduto) - Marca não pode estar vazia")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "", "Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_MARCA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_create_produto_nok_categoria_vazia(self):
        print("Caso de teste (PRODUTO - createProduto) - Categoria não pode estar vazia")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_CATEGORIA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_create_produto_nok_preco_vazio(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço não pode estar vazio")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", -1, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_create_produto_nok_nome_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_NOME_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_create_produto_nok_marca_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_MARCA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_create_produto_nok_categoria_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_CATEGORIA_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_10_create_produto_nok_preco_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.555, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_11_create_produto_nok_preco_promocional_formato_incorreto(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3.111)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_FORMATO_INCORRETO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_12_create_produto_nok_preco_promocional_maior_que_preco(self):
        print("Caso de teste (PRODUTO - createProduto) - Preço promocional não pode ser maior que o preço")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 4)
        retorno_esperado = STATUS_CODE["PRODUTO_PRECO_PROMOCIONAL_MAIOR_QUE_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_13_create_produto_nok_produto_existente(self):
        print("Caso de teste (PRODUTO - createProduto) - Produto já existente")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        retorno_esperado = STATUS_CODE["PRODUTO_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoById
class TestShowProdutoById(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produto_id_ok_encontrado(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutoById) - Exibição")
        retorno_obtido = showProdutoById(1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_produto_id_nok_nao_encontrado(self):
        print("Caso de teste (PRODUTO - showProdutoById) - Produto não encontrado")
        retorno_obtido = showProdutoById(2)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoByNome
class TestShowProdutoByNome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

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

# updateProduto
class TestUpdateProduto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()
    
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
        produto_esperado = {"nome": "Coca-Cola Zero 500ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3}
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

# getProdutoById
class TestGetProdutoById(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

    def test_01_get_produto_id_ok_retorno(self):
        print("Caso de teste (PRODUTO - getProdutoById) - Obtenção")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoById(1, temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_id_ok_obtido(self):
        print("Caso de teste (PRODUTO - getProdutoById) - Verificação de obtenção")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3}
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

# getProdutoByNome
class TestGetProdutoByNome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

    def test_01_get_produto_nome_ok_retorno(self):
        print("Caso de teste (PRODUTO - getProdutoByNome) - Obtenção")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoByNome("Coca-Cola Zero 350ml", temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_nome_ok_obtido(self):
        print("Caso de teste (PRODUTO - getProdutoByNome) - Verificação de retorno")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3}
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

# showProdutos
class TestShowProdutos(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_ok_retorno(self, mock_stdout):
        print("Caso de teste (PRODUTO - showProdutos) - Exibição")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nok_nenhum_produto_cadastrado(self):
        limpaProdutos()
        print("Caso de teste (PRODUTO - showProdutos) - Nenhum produto cadastrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NENHUM_CADASTRO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByMarca
class TestShowProdutosByMarca(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

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

# showProdutosByCategoria
class TestShowProdutosByCategoria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

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

# showProdutosByFaixaPreco
class TestShowProdutosByFaixaPreco(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

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

# showProdutosByNome
class TestShowProdutosByNome(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()

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

# deleteProduto
class TestDeleteProduto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Removido
        createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3)
        # Não zerado no estoque
        createProduto("Fanta Laranja 1L", "Fanta", "Bebidas", 10, 8)
        atualizaQtdEstoque(2, 5)
        # Cadastrado em venda
        createProduto("Guaraná 1L", "Guaraná", "Bebidas", 9, 7.5)
        atualizaQtdEstoque(3, 5)
        createVenda("", "13/10/2004", "20:00")
        addProduto(1, 3, 5)

    @classmethod
    def tearDownClass(cls):
        limpaProdutos()
        limpaVendas()
        limpaEstoque()

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
        retorno_obtido = deleteProduto(99)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_04_delete_produto_nok_produto_nao_zerado_no_estoque(self):
        print("Caso de teste (PRODUTO) - Produto não zerado no estoque")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ZERADO_NO_ESTOQUE"]
        retorno_obtido = deleteProduto(2)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_05_delete_produto_nok_produto_cadastrado_em_venda(self):
        print("Caso de teste (PRODUTO) - Produto cadastrado em venda")
        retorno_esperado = STATUS_CODE["PRODUTO_CADASTRADO_EM_VENDA"]
        retorno_obtido = deleteProduto(3)
        self.assertEqual(retorno_esperado, retorno_obtido)

class TestRelatorioProduto(unittest.TestCase):
    
    def test_01_carregar_produtos(self):
        print("Caso de teste (PRODUTO - carregarProdutos) - Carrega os produtos salvos")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = carregarProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_salvar_produtos(self):
        print("Caso de teste (PRODUTO - salvarProdutos) - Salva os produtos")
        retorno_esperado = STATUS_CODE["ERRO"]
        retorno_obtido = salvarProdutos()
        self.assertIsNot(retorno_esperado, retorno_obtido)

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

    # Venda
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
    

    # Produto
    suite.addTest(unittest.makeSuite(TestCreateProduto))
    suite.addTest(unittest.makeSuite(TestShowProdutoById))
    suite.addTest(unittest.makeSuite(TestShowProdutoByNome))
    suite.addTest(unittest.makeSuite(TestGetProdutoById))
    suite.addTest(unittest.makeSuite(TestGetProdutoByNome))
    suite.addTest(unittest.makeSuite(TestShowProdutos))
    suite.addTest(unittest.makeSuite(TestShowProdutosByMarca))
    suite.addTest(unittest.makeSuite(TestShowProdutosByCategoria))
    suite.addTest(unittest.makeSuite(TestShowProdutosByFaixaPreco))
    suite.addTest(unittest.makeSuite(TestShowProdutosByNome))
    suite.addTest(unittest.makeSuite(TestUpdateProduto))
    suite.addTest(unittest.makeSuite(TestDeleteProduto))
    

    # Estoque
    suite.addTest(unittest.makeSuite(TestCreateProdutoNoEstoque))
    suite.addTest(unittest.makeSuite(TestAtualizaQtdEstoque))
    suite.addTest(unittest.makeSuite(TestGetProdutoEstoque))
    suite.addTest(unittest.makeSuite(TestShowEstoque))
    suite.addTest(unittest.makeSuite(TestDeleteProdutoEstoque))
    

    # Cliente
    suite.addTest(unittest.makeSuite(TestCreateCliente))
    suite.addTest(unittest.makeSuite(TestShowCliente))
    suite.addTest(unittest.makeSuite(TestGetCliente))
    suite.addTest(unittest.makeSuite(TestShowClientes))
    suite.addTest(unittest.makeSuite(TestShowClientesByNome))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByCpf))
    suite.addTest(unittest.makeSuite(TestUpdateClienteByNome))
    suite.addTest(unittest.makeSuite(TestDeleteCliente))
    

    suite.addTest(unittest.makeSuite(TestRelatorioEstoque))
    suite.addTest(unittest.makeSuite(TestRelatorioCliente))
    suite.addTest(unittest.makeSuite(TestRelatorioVenda))
    suite.addTest(unittest.makeSuite(TestRelatorioProduto))


    return suite

# Executa os testes
if __name__ == "__main__":
    from .entidades.cliente.cliente import *
    from .entidades.estoque.estoque import *
    from .entidades.produto.produto import *
    from .entidades.venda.venda import *
    runner = unittest.TextTestRunner()
    runner.run(suite())
 