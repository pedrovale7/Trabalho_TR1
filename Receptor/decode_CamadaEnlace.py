from bitarray import bitarray

def text_from_bits(bits: list[int], enconding = "utf-8", errors = "surrogatepass" ):
    
    array=bitarray(bits)                        # Cria um Bitarray
    bytes=array.tobytes()                       # Converte para uma sequencia de Bytes
    text_output = bytes.decode(enconding,errors)# Transforma novamente em texto ASCII

    return text_output

def decode_charactere_count(bits: list[int]):
    bits_sequence = [bits[i] for i in range(8,len(bits))] # Remover o header para ter somente a sequencia de bits
    text_output = text_from_bits(bits_sequence)           # Transformar a sequencia de bits de volta em texto
    
    return text_output

def decode_byte_insertion(bits: list[int]):
    flag = [0,1,1,1,1,1,1,0]       #0x7E ~         
    escape = [0,0,0,1,1,0,1,1]     #0x1B 
    aux=[]   

    #Remove a Flag inicial e final e retorna somente a sequencia binária
    bits_sequence = [bits[i] for i in range (8,len(bits)-8)] 

    #Verificar se existe algum escape na sequencia binaria e remove-lo
    for i in range(0, len(bits_sequence),8):
        if (bits_sequence[i:i+8]!=escape):
            aux.extend(bits_sequence[i:i+8])

    #Transformar a sequencia binaria de volta em texto
    text_output = text_from_bits(aux)
    
    return text_output

# Faltando o bit_insertion

#CRC:
def crc_checksum(data, polinomio):
    
    # converte os dados e o polinomio para listas:
    data_bits = [int(bit) for bit in data]
    polinomio_bits = [int(bit) for bit in polinomio]

    # grau do polinomio:
    polinomio_grau = len(polinomio_bits) - 1

    # adiciona um numero de zeros a data igual ao grau do polinomio:
    data_aumentada = data_bits + [0] * polinomio_grau

    # XOR da data com o polinomio
    # variavel temporaria para nao alterar os dados originais
    data_atual = list(data_aumentada)

    for i in range(len(data_bits)):
        # se o primeiro bit for 1, realiza a operação XOR
        if data_atual[i] == 1:
            for j in range(len(polinomio_bits)):
                # XOR do bit atual dos dados com o bit correspondente do polinomio
                data_atual[i + j] ^= polinomio_bits[j]

    # o CRC é o resto dessa divisao
    # ou seja, são os últimos 'polinomio_grau' bits
    crc_resto = data_atual[-polinomio_grau:]
    return "".join(str(bit) for bit in crc_resto)

def verifica_crc(data_recebida, polinomio):
    
    # a verificaçao acontece da mesma forma que o checksum(XOR)
    # se o resto for tudo 0 significa que está sem erro
    resto = crc_checksum(data_recebida, polinomio)
    return all(bit == '0' for bit in resto)

def bit_parity(binary_sequence : list [int]):
    
    ones = sum(binary_sequence)
    parity_bit = 0

    if ones % 2 != 0:
        parity_bit = 1

    binary_sequence.append(parity_bit)

    return binary_sequence

def hamming(binary_sequence: list [int]):
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