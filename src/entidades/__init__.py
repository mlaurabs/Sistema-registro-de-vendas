#Consolida as funções relacionadas às entidades básicas do sistema: produto, cliente, venda e estoque.

# pensei de fazer init.py pra cada um.. mas teria q estar pacotes separados diretmente em src ao invés de entidade

from .produto import # completar com os métodos de acesso disponíveis
from .cliente import # completar com os métodos de acesso disponíveis
from .venda import # completar com os métodos de acesso disponíveis
from .estoque import atualizar_estoque, verificar_estoque

# Exportar apenas as funções públicas do módulo `entidades`
__all__ = [
    #metódos de acesso
    '''
    Ex:
    "adicionar_produto", "listar_produtos",
    "adicionar_cliente", "listar_clientes",
    "registrar_venda", "listar_vendas",
    "atualizar_estoque", "verificar_estoque"
    '''
    
]