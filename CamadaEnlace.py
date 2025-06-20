from bitarray import bitarray

# Função que transforma um texto em binario
def convert_to_bytes(text: str, encoding='utf-8',errors='surrogatepass'):
    bin_array=bitarray()
    bin_array.frombytes(text.encode(encoding,errors))  # transforma um texto de ASCII em bytes
    binary_sequence =[int(bit) for bit in bin_array]
    return binary_sequence

#def character_count (text: str):
    header=len(convert_to_bytes(text)) # Tamanho do Cabeçalho
    header=bin(header)[2:]
    return header + convert_to_bytes(text)
    # Perguntar para o Prof se o Header tem que ter Tamanho Fixo ou pode variar

def byte_insertion (text: str):
    binary_sequence = convert_to_bytes(text)

    # Flags e Escapes fixos, e lista auxiliar
    flag = [0,1,1,1,1,1,1,0]            #0x7E ~
    escape = [0,0,0,1,1,0,1,1]          #0x1B 
    aux = []

    #Percorrendo os bytes
    for i in range (0,len(binary_sequence),8):

        # Verifica se existe um byte igual a Flag e/ou Escape
        if (binary_sequence[i:i+8] == flag or binary_sequence[i:i+8] ==escape):
            aux.extend(escape + binary_sequence[i:i+8]) 
        else:
            aux.extend(binary_sequence[i:i+8])

    # Adiciona a Flag no inicio e no fim nos trem de bits       
    return flag + aux + flag



texto="A~"
print(byte_insertion(texto))

