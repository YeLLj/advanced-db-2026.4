# M1 - Storage

## Organização das páginas

Cada página possui 4096 bytes.

Os primeiros 16 bytes são reservados para o cabeçalho.

Cada registro possui 8 bytes:
- 4 bytes para o ID
- 4 bytes para a matrícula

## Localização dos registros

O primeiro registro começa no byte 16 da página.

O segundo começa no byte 24.

O terceiro começa no byte 32.

A fórmula utilizada é:

offset = HEADER_SIZE + (slot * RECORD_SIZE)

Como:

HEADER_SIZE = 16
RECORD_SIZE = 8

o registro do slot 0 começa no byte 16.

## RID

Cada registro pode ser identificado por:

(página, slot)

Exemplo:

(0, 2)

significa página 0, slot 2.

## Persistência

Os registros são gravados no arquivo dados.db.

O arquivo pode ser fechado e aberto novamente sem perder os registros.
