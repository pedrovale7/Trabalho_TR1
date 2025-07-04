from bitarray import bitarray

# Função que transforma um texto em binario
def convert_to_bytes(text: str, encoding='utf-8',errors='surrogatepass'):
    bin_array=bitarray()
    bin_array.frombytes(text.encode(encoding,errors))  # transforma um texto de ASCII em bytes
    binary_sequence =[int(bit) for bit in bin_array]
    return binary_sequence

def character_count (binary_sequence):

    header_size = 8              # Tamanho fixo do Cabeçalho de 8 bits

    header=len(binary_sequence)  # Calcula o comprimento de bits
    header=bin(header)[2:].zfill(header_size)
    
    header = [int(bit) for bit in header]

    return header + binary_sequence

def byte_insertion (binary_sequence):

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

def bit_insertion (binary_sequence):

    flag = [0,1,1,1,1,1,1,0]        #0x7E
    count = 0
    aux = []

    for i in binary_sequence:
        aux.append(i)
        if binary_sequence[i]==1:
            count += 1
            if (count == 5):
                aux.append(0)
                count = 0
        else: count = 0

    return flag + aux  + flag