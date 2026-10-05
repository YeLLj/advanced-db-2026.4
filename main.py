import struct

PAGE_SIZE = 4096

pagina = bytearray(PAGE_SIZE)

registro = struct.pack("ii", 1, 20260001)

pagina[16:24] = registro

with open("dados.db", "wb") as arquivo:
    arquivo.write(pagina)

print("Registro gravado!")