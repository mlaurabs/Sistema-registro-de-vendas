#include <stdio.h>
#include <stdlib.h>
#include <Python.h>
#include "converteutf832.h"

/* Maria Laura Barbosa Soares 2320467 3WA */
/* Vinícius Martins Rodrigues 2320308 3WA */

extern int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida);
extern int convUtf8p32(FILE *arquivo_entrada, FILE *arquivo_saida);

FILE* abrirArquivo(char* path, char* modo) {
    FILE* f = fopen(path, modo);
    return f;
}

// Retorna a quantidade de bytes que o primeiro caractere UTF-8 do Utf8Stream utiliza
int qtdBytesUtf8(unsigned char* Utf8Stream) { 
    unsigned char a = Utf8Stream[0];
    if ((a & 0x80) == 0x00) {
        return 1;
    }
    else if ((a & 0xE0) == 0xC0) {
        return 2;
    }
    else if ((a & 0xF0) == 0xE0) {
        return 3;
    }
    else {
        return 4;
    }
}

// retorna o codepoint de um caractere codificado em UTF-8
unsigned int getCodePointUTF8(unsigned char* Utf8Stream) {
    int num_bytes = qtdBytesUtf8(Utf8Stream);
    unsigned int codepoint = 0;

    if (num_bytes == 1) {
        codepoint = Utf8Stream[0];
    }
    else if (num_bytes == 2) {
        unsigned int firstByte = Utf8Stream[0] & 0x1F;
        unsigned int secondByte = Utf8Stream[1] & 0x3F;
        codepoint = (firstByte << 6) | secondByte;
    }
    else if (num_bytes == 3) {
        unsigned int firstByte = Utf8Stream[0] & 0x0F;
        unsigned int secondByte = Utf8Stream[1] & 0x3F;
        unsigned int thirdByte = Utf8Stream[2] & 0x3F;
        codepoint = (firstByte << 12) | (secondByte << 6) | thirdByte;
    }
    else {
        unsigned int firstByte = Utf8Stream[0] & 0x07;
        unsigned int secondByte = Utf8Stream[1] & 0x3F;
        unsigned int thirdByte = Utf8Stream[2] & 0x3F;
        unsigned int fourthByte = Utf8Stream[3] & 0x3F;
        codepoint = (firstByte << 18) | (secondByte << 12) | (thirdByte << 6) | fourthByte;
    }
    return codepoint;
}

// retorna o codepoint de um caractere codificado em UTF-32
unsigned int getCodePointUTF32(unsigned char* utf32Stream, int endian) {
    unsigned int codepoint = 0;

    if (endian == 1) {
        codepoint |= (utf32Stream[0] << 24);
        codepoint |= (utf32Stream[1] << 16);
        codepoint |= (utf32Stream[2] << 8);
        codepoint |= utf32Stream[3];
    }
    else {
        codepoint |= utf32Stream[0];
        codepoint |= (utf32Stream[1] << 8);
        codepoint |= (utf32Stream[2] << 16);
        codepoint |= (utf32Stream[3] << 24);
    }
    return codepoint;
}

int convUtf8p32(FILE* arquivo_entrada, FILE* arquivo_saida) {
    if (arquivo_entrada == NULL) {
        fprintf(stderr, "Houve um erro de leitura do arquivo\n");
        return -1;
    }
    if (arquivo_saida == NULL) {
        fprintf(stderr, "Houve um erro de gravação do arquivo\n");
        return -1;
    }

    unsigned char codeUTF8[4];
    unsigned int BOM = 0x0000FEFF;

    // Escreve o BOM UTF-32 no arquivo de saída (Little Endian)
    fwrite(&BOM, sizeof(BOM), 1, arquivo_saida);

    while (fread(&codeUTF8[0], sizeof(char), 1, arquivo_entrada) > 0) {
        int tamanho = qtdBytesUtf8(codeUTF8);

        for (int i = 1; i < tamanho; i++) {
            fread(&codeUTF8[i], sizeof(char), 1, arquivo_entrada);
        }

        unsigned int codepoint = getCodePointUTF8(codeUTF8);

        unsigned char utf32[4];
        utf32[0] = (codepoint & 0xFF);
        utf32[1] = (codepoint >> 8) & 0xFF;
        utf32[2] = (codepoint >> 16) & 0xFF;
        utf32[3] = (codepoint >> 24) & 0xFF;

        fwrite(utf32, sizeof(unsigned char), 4, arquivo_saida);
    }
    return 0;
}

int convUtf32p8(FILE *arquivo_entrada, FILE *arquivo_saida) {
    if (arquivo_entrada == NULL) {
        fprintf(stderr, "Houve um erro de leitura do arquivo\n");
        return -1;
    }
    if (arquivo_saida == NULL) {
        fprintf(stderr, "Houve um erro de gravação do arquivo\n");
        return -1;
    }
    unsigned char buffer[4];
    int endian = 0;

    unsigned char bom[4];
    fread(bom, sizeof(unsigned char), 4, arquivo_entrada);

    if (bom[0] == 0x00 && bom[1] == 0x00 && bom[2] == 0xFE && bom[3] == 0xFF) {
        endian = 1; // Big Endian
    }
    else if (bom[0] == 0xFF && bom[1] == 0xFE && bom[2] == 0x00 && bom[3] == 0x00) {
        endian = 0; // Little Endian
    }
    else {
        fprintf(stderr, "BOM inválido ou ausente.");
        return -1;
    }

    while (fread(buffer, sizeof(unsigned char), 4, arquivo_entrada) == 4) {
        unsigned int unicode = getCodePointUTF32(buffer, endian);
        unsigned char utf8[5];

        int bytes = 0;
        if (unicode <= 0x7F) {
            utf8[0] = (unsigned char)unicode;
            bytes = 1;
        } 
        else if (unicode <= 0x7FF) {
            utf8[0] = 0xC0 | ((unicode >> 6) & 0x1F);
            utf8[1] = 0x80 | (unicode & 0x3F);
            bytes = 2;
        } 
        else if (unicode <= 0xFFFF) {
            utf8[0] = 0xE0 | ((unicode >> 12) & 0x0F);
            utf8[1] = 0x80 | ((unicode >> 6) & 0x3F);
            utf8[2] = 0x80 | (unicode & 0x3F);
            bytes = 3;
        } 
        else if (unicode <= 0x10FFFF) {
            utf8[0] = 0xF0 | ((unicode >> 18) & 0x07);
            utf8[1] = 0x80 | ((unicode >> 12) & 0x3F);
            utf8[2] = 0x80 | ((unicode >> 6) & 0x3F);
            utf8[3] = 0x80 | (unicode & 0x3F);
            bytes = 4;
        }
        fwrite(utf8, sizeof(unsigned char), bytes, arquivo_saida);
    }

    return 0;
}

// Método para definir como a função será exposta no Python
static PyObject* py_convUtf8p32(PyObject *self, PyObject *args) {
    const char* input_file;
    const char* output_file;

    if (!PyArg_ParseTuple(args, "ss", &input_file, &output_file)) {
        return NULL;
    }

    FILE* input = fopen(input_file, "rb");
    FILE* output = fopen(output_file, "wb");

    if (convUtf8p32(input, output) != 0) {
        fclose(input);
        fclose(output);
        return NULL;
    }

    fclose(input);
    fclose(output);

    Py_RETURN_NONE;
}

static PyObject* py_convUtf32p8(PyObject *self, PyObject *args) {
    const char* input_file;
    const char* output_file;

    if (!PyArg_ParseTuple(args, "ss", &input_file, &output_file)) {
        return NULL;
    }

    FILE* input = fopen(input_file, "rb");
    FILE* output = fopen(output_file, "wb");

    if (convUtf32p8(input, output) != 0) {
        fclose(input);
        fclose(output);
        return NULL;
    }

    fclose(input);
    fclose(output);

    Py_RETURN_NONE;
}

// Definindo os métodos do módulo
static PyMethodDef ConverteMethods[] = {
    {"convUtf8p32", py_convUtf8p32, METH_VARARGS, "Converte UTF-8 para UTF-32."},
    {"convUtf32p8", py_convUtf32p8, METH_VARARGS, "Converte UTF-32 para UTF-8."},
    {NULL, NULL, 0, NULL}  // Termina a lista de métodos
};

// Definindo a estrutura do módulo
static struct PyModuleDef converteutf832module = {
    PyModuleDef_HEAD_INIT,
    "converteutf832",  // Nome do módulo
    "Módulo de conversão entre UTF-8 e UTF-32",  // Descrição
    -1,  // Globalmente acessível
    ConverteMethods  // Lista de métodos
};

// Função de inicialização do módulo
PyMODINIT_FUNC PyInit_converteutf832(void) {
    return PyModule_Create(&converteutf832module);
}
