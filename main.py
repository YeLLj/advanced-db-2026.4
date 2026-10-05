import os
import struct


PAGE_SIZE = 4096
HEADER_SIZE = 16
RECORD_SIZE = 8

# Quantos registros cabem em uma página
RECORDS_PER_PAGE = (PAGE_SIZE - HEADER_SIZE) // RECORD_SIZE


def cria_banco(nome="dados.db"):
    """
    Cria o arquivo do banco caso ele ainda não exista.
    """

    if not os.path.exists(nome):
        pagina = bytearray(PAGE_SIZE)

        # Os primeiros 4 bytes guardam a quantidade
        # de registros existentes na página.
        pagina[0:4] = struct.pack("i", 0)

        with open(nome, "wb") as arquivo:
            arquivo.write(pagina)


def le_pagina(arquivo, numero):
    """
    Lê uma página específica do arquivo.
    """

    arquivo.seek(numero * PAGE_SIZE)

    dados = arquivo.read(PAGE_SIZE)

    if len(dados) != PAGE_SIZE:
        raise ValueError("Página não existe ou está incompleta.")

    return dados


def escreve_pagina(arquivo, numero, dados):
    """
    Escreve uma página específica no arquivo.
    """

    if len(dados) != PAGE_SIZE:
        raise ValueError("A página precisa ter exatamente 4096 bytes.")

    arquivo.seek(numero * PAGE_SIZE)
    arquivo.write(dados)


def quantidade_registros(pagina):
    """
    Retorna quantos registros existem na página.
    """

    return struct.unpack("i", pagina[0:4])[0]


def insere(arquivo, id, matricula):
    """
    Insere um registro no primeiro espaço disponível.
    Retorna o RID: (página, slot).
    """

    registro = struct.pack("ii", id, matricula)

    tamanho_arquivo = os.fstat(arquivo.fileno()).st_size

    quantidade_paginas = tamanho_arquivo // PAGE_SIZE

    # Procura uma página com espaço.
    for numero_pagina in range(quantidade_paginas):

        pagina = bytearray(le_pagina(arquivo, numero_pagina))

        quantidade = quantidade_registros(pagina)

        if quantidade < RECORDS_PER_PAGE:

            slot = quantidade

            offset = HEADER_SIZE + (slot * RECORD_SIZE)

            pagina[offset:offset + RECORD_SIZE] = registro

            quantidade += 1

            pagina[0:4] = struct.pack("i", quantidade)

            escreve_pagina(arquivo, numero_pagina, pagina)

            arquivo.flush()

            return numero_pagina, slot

    # Se todas as páginas estiverem cheias,
    # cria uma nova página.
    numero_pagina = quantidade_paginas

    pagina = bytearray(PAGE_SIZE)

    slot = 0

    offset = HEADER_SIZE + (slot * RECORD_SIZE)

    pagina[offset:offset + RECORD_SIZE] = registro

    pagina[0:4] = struct.pack("i", 1)

    escreve_pagina(arquivo, numero_pagina, pagina)

    arquivo.flush()

    return numero_pagina, slot


def le_registro(arquivo, pagina, slot):
    """
    Lê um registro usando seu RID (página, slot).
    """

    dados_pagina = le_pagina(arquivo, pagina)

    offset = HEADER_SIZE + (slot * RECORD_SIZE)

    dados_registro = dados_pagina[
        offset:offset + RECORD_SIZE
    ]

    return struct.unpack("ii", dados_registro)


def mostra_pagina(arquivo, numero):
    """
    Mostra os registros existentes em uma página.
    """

    pagina = le_pagina(arquivo, numero)

    quantidade = quantidade_registros(pagina)

    print(f"\nPágina {numero}")
    print(f"Registros: {quantidade}")

    for slot in range(quantidade):

        id, matricula = le_registro(
            arquivo,
            numero,
            slot
        )

        print(
            f"  Slot {slot}: "
            f"ID={id}, Matrícula={matricula}"
        )


def teste():
    """
    Testa criação, inserção e leitura do banco.
    """

    cria_banco()

    with open("dados.db", "r+b") as arquivo:

        rid1 = insere(
            arquivo,
            1,
            20260001
        )

        rid2 = insere(
            arquivo,
            2,
            20260002
        )

        rid3 = insere(
            arquivo,
            3,
            20260003
        )

        print("Registros inseridos:")

        print("Registro 1:", rid1)
        print("Registro 2:", rid2)
        print("Registro 3:", rid3)

        print()

        id, matricula = le_registro(
            arquivo,
            rid1[0],
            rid1[1]
        )

        print("Leitura do registro 1:")
        print("ID:", id)
        print("Matrícula:", matricula)

        mostra_pagina(arquivo, 0)


if __name__ == "__main__":
    teste()