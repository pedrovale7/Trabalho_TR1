from bitarray import bitarray

# Função que transforma um texto em binario
def convert_to_bytes(text: str, encoding='utf-8',errors='surrogatepass'):
    bin_array=bitarray()
    bin_array.frombytes(text.encode(encoding,errors))  # transforma um texto de ASCII em bytes
    binary_sequence =[int(bit) for bit in bin_array]
    return binary_sequence

def character_count (text: str):

    binary_sequence = convert_to_bytes(text)

    header=len(binary_sequence)  # Tamanho do Cabeçalho
    header=bin(header)[2:] 
    
    header = [bit for bit in header]

    return header + binary_sequence


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

def bit_insertion (text: str):
    binary_sequence= convert_to_bytes(text)

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


def bit_parity(text):
    
    binary_sequence= convert_to_bytes(text)
    ones = sum(binary_sequence)
    parity_bit = 0

    if ones % 2 != 0:
        parity_bit = 1

    binary_sequence.append(parity_bit)

    return binary_sequence

def hamming(text: str):
    binary_sequence = convert_to_bytes(text)
    #Hamming 7/4

    hamming_sequence = []
    for i in range (0, len(binary_sequence),4):
        nibble = binary_sequence[i:i+4]

        if len(nibble) < 4 :
            nibble.extend([0] * (4-len(nibble)))

        # (p1,p2,m3,p4,m5,m6,m7)
        # (      n0,  ,n1,n2,n3)

        p=  [(nibble[0]^nibble[1]^nibble[3]),
            (nibble[0]^nibble[2]^nibble[3]),
            (nibble[1]^nibble[2]^nibble[3])]

        bits= [p[0],p[1],nibble[0],p[2],nibble[1],nibble[2],nibble[3]]
        hamming_sequence.extend(bits)

    return hamming_sequence
