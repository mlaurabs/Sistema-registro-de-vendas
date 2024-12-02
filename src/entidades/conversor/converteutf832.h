#include <stdio.h>
#include <stdlib.h>

/* Maria Laura Barbosa Soares 2320467 3WA */
/* Vinícius Martins Rodrigues 2320308 3WA */

// Função para abrir arquivos
FILE* abrirArquivo(char* path, char* modo);

// Função para determinar a quantidade de bytes de uma sequência UTF-8
int qtdBytesUtf8(unsigned char* Utf8Stream);

// Função para converter uma sequência UTF-8 em um ponto de código Unicode (UTF8)
unsigned int getCodePointUTF8(unsigned char* Utf8Stream);

// Função para converter de UTF-8 para UTF-32 e salvar no arquivo de saída
int convUtf8p32(FILE* arquivo_entrada, FILE* arquivo_saida);

// Função para converter uma sequência UTF-32 em um ponto de código Unicode (UTF32)
unsigned int getCodePointUTF32(unsigned char* utf32Stream, int endian);

// Função para converter de UTF-32 para UTF-8 e salvar no arquivo de saída
int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida);
