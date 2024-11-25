import unittest
from unittest.mock import patch
import os
from produto import *
from src.status_code import *

# createProduto
class TestCreateProduto(unittest.TestCase):

    def test_01_create_produto_ok_retorno(self):
        print("Caso de teste - Produto criado com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_create_produto_ok_inserido(self):
        print("Caso de teste - Verificação de existência do produto")
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        produto_obtido.pop("id")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_create_produto_nok_nome_nulo(self):
        print("Caso de teste - Nome não pode ser nulo")
        retorno_obtido = createProduto("", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["NOME_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_create_produto_nok_marca_nula(self):
        print("Caso de teste - Marca não pode ser nula")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["MARCA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_05_create_produto_nok_categoria_nula(self):
        print("Caso de teste - Categoria não pode ser nula")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["CATEGORIA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_create_produto_nok_preco_nulo(self):
        print("Caso de teste - Preço não pode ser nulo")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", -1, 3, 20)
        retorno_esperado = STATUS_CODE["PRECO_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_create_produto_nok_qtd_minima_nulo(self):
        print("Caso de teste - Quantidade mínima não pode ser nulo")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, -1)
        retorno_esperado = STATUS_CODE["QTD_MINIMA_VAZIO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_create_produto_nok_nome_formato(self):
        print("Caso de teste - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_create_produto_nok_marca_formato(self):
        print("Caso de teste - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["MARCA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_10_create_produto_nok_categoria_formato(self):
        print("Caso de teste - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["CATEGORIA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_11_create_produto_nok_preco_formato(self):
        print("Caso de teste - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.555, 3, 20)
        retorno_esperado = STATUS_CODE["PRECO_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_12_create_produto_nok_preco_promocional_formato(self):
        print("Caso de teste - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3.111, 20)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_13_create_produto_nok_preco_promocional_maior_preco(self):
        print("Caso de teste - Preço promocional maior que o preço ")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 4, 20)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_14_create_produto_nok_produto_existente(self):
        print("Caso de teste - Produto já existente")
        retorno_obtido = createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
        retorno_esperado = STATUS_CODE["PRODUTO_EXISTENTE"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoById
class TestShowProdutoById(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produto_id_ok_encontrado(self, mock_stdout):
        print("Caso de teste - Produto exibido com sucesso pelo id")
        retorno_obtido = showProdutoById(1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_produto_id_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo id")
        retorno_obtido = showProdutoById(2)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutoByNome
class TestShowProdutoByNome(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produto_nome_ok_encontrado(self, mock_stdout):
        print("Caso de teste - Produto exibido com sucesso pelo nome")
        retorno_obtido = showProdutoByNome("Coca-Cola Zero 350ml")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_02_show_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo nome")
        retorno_obtido = showProdutoByNome("Coca-Cola Zero 500ml")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# updateProduto
class TestUpdateProduto(unittest.TestCase):
    
    def test_01_update_produto_ok_retorno(self):
        print("Caso de teste - Produto atualizado com sucesso")
        retorno_obtido = updateProduto(1, "Coca-Cola Zero 500ml", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["SUCESSO"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_02_update_produto_ok_alterado(self):
        print("Caso de teste - Verificação de atualização do produto")
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 500ml", produto_obtido)
        produto_obtido.pop("id")
        produto_esperado = {"nome": "Coca-Cola Zero 500ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        self.assertEqual(produto_obtido, produto_esperado)

    def test_03_update_produto_nok_nome_formato(self):
        print("Caso de teste - Nome com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["NOME_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_04_update_produto_nok_marca_formato(self):
        print("Caso de teste - Marca com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "", -1, -1)
        retorno_esperado = STATUS_CODE["MARCA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)
    
    def test_05_update_produto_nok_categoria_formato(self):
        print("Caso de teste - Categoria com formato incorreto (excede 50 caracteres)")
        retorno_obtido = updateProduto(1, "", "", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", -1, -1)
        retorno_esperado = STATUS_CODE["CATEGORIA_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_06_update_produto_nok_preco_formato(self):
        print("Caso de teste - Preço com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = updateProduto(1, "", "", "", 3.555, -1)
        retorno_esperado = STATUS_CODE["PRECO_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_07_update_produto_nok_preco_promocional_formato(self):
        print("Caso de teste - Preço promocional com formato incorreto (mais de 2 casas decimais)")
        retorno_obtido = updateProduto(1, "", "", "", -1, 3.111)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_FORMATO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_08_update_produto_nok_preco_promocional_maior_preco_1(self):
        print("Caso de teste - Preço promocional maior que o preço (1 - Novo preço menor que o preço promocional atual)")
        retorno_obtido = updateProduto(1, "", "", "", 1, -1)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_09_update_produto_nok_preco_promocional_maior_preco_2(self):
        print("Caso de teste - Preço promocional maior que o preço (2 - Novo preço menor que o novo preço promocional)")
        retorno_obtido = updateProduto(1, "", "", "", 3, 4)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_10_update_produto_nok_preco_promocional_maior_preco_3(self):
        print("Caso de teste - Preço promocional maior que o preço (3 - Novo preço promocional maior que o preço atual)")
        retorno_obtido = updateProduto(1, "", "", "", -1, 20)
        retorno_esperado = STATUS_CODE["PRECO_PROMOCIONAL_MAIOR_PRECO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

    def test_11_update_produto_nok_produto_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado")
        retorno_obtido = updateProduto(2, "", "", "", -1, -1)
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        self.assertEqual(retorno_obtido, retorno_esperado)

# getProdutoById
class TestGetProdutoById(unittest.TestCase):

    def test_01_get_produto_id_ok_retorno(self):
        print("Caso de teste - Produto obtido com sucesso pelo id")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoById(1, temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_id_ok_obtido(self):
        print("Caso de teste - Verificação de devolução do produto pelo id")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoById(1, produto_obtido)
        produto_obtido.pop("id")
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_get_produto_id_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo id")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoById(2, temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# getProdutoByNome
class TestGetProdutoByNome(unittest.TestCase):

    def test_01_get_produto_nome_ok_retorno(self):
        print("Caso de teste - Produto obtido com sucesso pelo nome")
        temp = dict()
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = getProdutoByNome("Coca-Cola Zero 350ml", temp)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_get_produto_nome_ok_obtido(self):
        print("Caso de teste - Verificação de devolução do produto pelo nome")
        produto_esperado = {"nome": "Coca-Cola Zero 350ml", "marca": "Coca-Cola", "categoria": "Bebidas", "preco": 3.5, "preco_promocional": 3, "qtd_minima": 20}
        produto_obtido = dict()
        getProdutoByNome("Coca-Cola Zero 350ml", produto_obtido)
        produto_obtido.pop("id")
        self.assertEqual(produto_esperado, produto_obtido)

    def test_03_get_produto_nome_nok_nao_encontrado(self):
        print("Caso de teste - Produto não encontrado pelo nome")
        temp = dict()
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = getProdutoByNome("Coca-Cola Zero 500ml", temp)
        self.assertEqual(retorno_obtido, retorno_esperado)

# showProdutos
class TestShowProdutos(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_ok_retorno(self, mock_stdout):
        print("Caso de teste - Produtos exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nok_nenhum_produto_cadastrado(self):
        print("Caso de teste - Nenhum produto cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_CADASTRADO"]
        retorno_obtido = showProdutos()
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByMarca
class TestShowProdutosByMarca(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_marca_ok_retorno(self, mock_stdout):
        print("Caso de teste - Produtos da marca especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByMarca("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_marca_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto da marca especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByMarca("Nescau")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByCategoria
class TestShowProdutosByCategoria(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_categoria_ok_retorno(self, mock_stdout):
        print("Caso de teste - Produtos da categoria especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByCategoria("Bebidas")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_categoria_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto da categoria especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByCategoria("Laticínios")
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByFaixaPreco
class TestShowProdutosByFaixaPreco(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_faixa_preco_ok_retorno(self, mock_stdout):
        print("Caso de teste - Produtos na faixa de preço especificada exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByFaixaPreco(0,10)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_faixa_preco_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto na faixa de preço especificada cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByFaixaPreco(100,200)
        self.assertEqual(retorno_esperado, retorno_obtido)

# showProdutosByNome
class TestShowProdutosByNome(unittest.TestCase):

    @patch('sys.stdout', new_callable=lambda: open(os.devnull, 'w'))
    def test_01_show_produtos_nome_ok_retorno(self, mock_stdout):
        print("Caso de teste - Produtos com nome parecido exibidos com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = showProdutosByNome("Coca-Cola")
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_show_produtos_nome_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Nenhum produto com nome parecido cadastrado")
        retorno_esperado = STATUS_CODE["NENHUM_PRODUTO_ENCONTRADO"]
        retorno_obtido = showProdutosByNome("Sprite")
        self.assertEqual(retorno_esperado, retorno_obtido)

# deleteProduto
class TestDeleteProduto(unittest.TestCase):

    def test_01_delete_produto_ok_retorno(self):
        print("Caso de teste - Produto excluído com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_delete_produto_ok_removido(self):
        print("Caso de teste - Veriicação de remoção do produto")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = showProdutoById(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_03_delete_produto_nok_nenhum_produto_encontrado(self):
        print("Caso de teste - Produto não encontrado")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ENCONTRADO"]
        retorno_obtido = deleteProduto(2)
        self.assertEqual(retorno_esperado, retorno_obtido)

    '''
    def test_04_delete_produto_nok_produto_nao_zerado_no_estoque(self):
        print("Caso de teste - Produto não zerado no estoque")
        retorno_esperado = STATUS_CODE["PRODUTO_NAO_ZERADO_NO_ESTOQUE"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_05_delete_produto_nok_produto_cadastrado_em_venda(self):
        print("Caso de teste - Produto cadastrado em venda")
        retorno_esperado = STATUS_CODE["PRODUTO_CADASTRADO_EM_VENDA"]
        retorno_obtido = deleteProduto(1)
        self.assertEqual(retorno_esperado, retorno_obtido)
    '''

# geraRelatorioProduto e leRelatorioProduto
class TestRelatorioProduto(unittest.TestCase):
    
    def test_01_gera_relatorio_produto(self):
        print("Caso de teste - Relatório de produtos gerado com sucesso")
        retorno_esperado = STATUS_CODE["SUCESSO"]
        retorno_obtido = geraRelatorioProduto()
        self.assertEqual(retorno_esperado, retorno_obtido)

    def test_02_le_relatorio_produto(self):
        print("Caso de teste - Leitura de relatório de produto e cadastro no sistema")
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
    runner = unittest.TextTestRunner()
    runner.run(suite())