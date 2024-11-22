from produto import *
from status_code import *

'''
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)
    print(getStatusName(resultado))
'''

# NOME_TIPO_ERRADO
print("\nEsperado: NOME_TIPO_ERRADO")
if resultado := createProduto(1, "Coca-Cola", "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# MARCA_TIPO_ERRADO
print("\nEsperado: MARCA_TIPO_ERRADO")
if resultado := createProduto("Coca-Cola Zero 350ml", 1, "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# CATEGORIA_TIPO_ERRADO
print("\nEsperado: CATEGORIA_TIPO_ERRADO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", 1, 3.5, 3, 20):
    print(getStatusName(resultado))

# PRECO_TIPO_ERRADO
print("\nEsperado: PRECO_TIPO_ERRADO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", "3.5", 3, 20):
    print(getStatusName(resultado))

# PRECO_PROMOCIONAL_TIPO_ERRADO
print("\nEsperado: PRECO_PROMOCIONAL_TIPO_ERRADO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, "3", 20):
    print(getStatusName(resultado))

# QTD_MINIMA_TIPO_ERRADO
print("\nEsperado: QTD_MINIMA_TIPO_ERRADO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, "20"):
    print(getStatusName(resultado))

# NOME_NONE
print("\nEsperado: NOME_NONE")
if resultado := createProduto(None, "Coca-Cola", "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# MARCA_NONE
print("\nEsperado: MARCA_NONE")
if resultado := createProduto("Coca-Cola Zero 350ml", None, "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# CATEGORIA_NONE
print("\nEsperado: CATEGORIA_NONE")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", None, 3.5, 3, 20):
    print(getStatusName(resultado))

# PRECO_NONE
print("\nEsperado: PRECO_NONE")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", None, 3, 20):
    print(getStatusName(resultado))

# QTD_MINIMA_NONE
print("\nEsperado: QTD_MINIMA_NONE")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, None):
    print(getStatusName(resultado))

# NOME_FORMATO
print("\nEsperado: NOME_FORMATO")
if resultado := createProduto("Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# MARCA_FORMATO
print("\nEsperado: MARCA_FORMATO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola Coca-Cola", "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# CATEGORIA_FORMATO
print("\nEsperado: CATEGORIA_FORMATO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# PRECO_PROMOCIONAL_MAIOR_PRECO
print("\nEsperado: PRECO_PROMOCIONAL_MAIOR_PRECO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 4, 20):
    print(getStatusName(resultado))

# PRECO_FORMATO
print("\nEsperado: PRECO_FORMATO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.555, 3, 20):
    print(getStatusName(resultado))

# PRECO_PROMOCIONAL_FORMATO
print("\nEsperado: PRECO_PROMOCIONAL_FORMATO")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3.111, 20):
    print(getStatusName(resultado))

# NENHUM_PRODUTO_CADASTRADO
print("\nEsperado: NENHUM_PRODUTO_CADASTRADO")
if resultado := showProdutos():
    print(getStatusName(resultado))

# SUCESSO
print("\nEsperado: SUCESSO")
if not (resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20)):
    print(getStatusName(resultado))

# PRODUTO_EXISTENTE
print("\nEsperado: PRODUTO_EXISTENTE")
if resultado := createProduto("Coca-Cola Zero 350ml", "Coca-Cola", "Bebidas", 3.5, 3, 20):
    print(getStatusName(resultado))

# PRODUTO_NAO_ENCONTRADO
print("\nEsperado: PRODUTO_NAO_ENCONTRADO")
if resultado := showProduto(2):
    print(getStatusName(resultado))

# NENHUM_PRODUTO_ENCONTRADO
print("\nEsperado: NENHUM_PRODUTO_ENCONTRADO")
if resultado := showProdutosByCategoria("Laticínios"):
    print(getStatusName(resultado))