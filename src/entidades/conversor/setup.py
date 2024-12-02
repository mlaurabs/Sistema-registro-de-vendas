from setuptools import setup, Extension

module = Extension(
    'converteutf832',
    sources=['converteutf832.c'],  # Inclua todos os arquivos necessários aqui
)

setup(
    name='converteutf832',
    version='1.0',
    description='Módulo de conversão entre UTF-8 e UTF-32',
    ext_modules=[module],
)
