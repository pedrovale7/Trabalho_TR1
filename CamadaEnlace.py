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

def bit_parity(binary_sequence : list [int]):
    
    ones = sum(binary_sequence)     # Conta a quantidade de 1s 
    parity_bit = 0                  # Define o bit de paridade

    if ones % 2 != 0:               # Se a quantidade de 1s for par, o bit de paridade é igual a 0
        parity_bit = 1              # caso contrário, é igual a 1

    binary_sequence.append(parity_bit) # Adiciona o bit de paridade ao fim do trem de bits

    return binary_sequence

def crc_checksum(trem_a_ser_dividido: list[int]): # função que faz o XOR
    polinomio_bits = [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1] # Polinômio CRC-32
    polinomio_grau = len(polinomio_bits) - 1

    trem_atual_aux = list(trem_a_ser_dividido) 

    for i in range(len(trem_atual_aux) - polinomio_grau):
        if trem_atual_aux[i] == 1:
            for j in range(len(polinomio_bits)):
                trem_atual_aux[i + j] ^= polinomio_bits[j]

    crc_resto = trem_atual_aux[-polinomio_grau:]
    return crc_resto

def prepara_CRC_para_transmissao(dados_originais: list[int]): 
    #prepara corretamente o quadro para enviar ao receptor
    polinomio_grau = 32 # Grau do polinômio CRC-32

    # anexa zeros aos DAODS ORIGINAIS
    dados_com_zeros_para_calculo = list(dados_originais) + [0] * polinomio_grau

    # chama crc_checksum para calcular o CRC (utilizando dados COM ZEROS ANEXADOS)
    crc_calculado = crc_checksum(dados_com_zeros_para_calculo) 

    # quadro final será (DADOS ORIGINAIS) + (CRC CALCULADO)
    quadro_para_enviar = list(dados_originais) + crc_calculado
    
    return quadro_para_enviar

"""def crc_checksum(data: list [int]):
    
    # converte os dados e o polinomio para listas:
    data_bits = data
    polinomio_bits = [1, 0, 0, 0, 0, 0, 1, 1, 1]

    # grau do polinomio:
    polinomio_grau = len(polinomio_bits) - 1

    # adiciona um numero de zeros a data igual ao grau do polinomio:
    data_aumentada = data_bits + [0] * polinomio_grau

    # XOR da data com o polinomio
    # variavel temporaria para nao alterar os dados originais
    data_atual = data_aumentada

    for i in range(len(data_bits)):
        # se o primeiro bit for 1, realiza a operação XOR
        if data_atual[i] == 1:
            for j in range(len(polinomio_bits)):
                # XOR do bit atual dos dados com o bit correspondente do polinomio
                data_atual[i + j] ^= polinomio_bits[j]

    # o CRC é o resto dessa divisao
    # ou seja, são os últimos 'polinomio_grau' bits
    crc_resto = data_atual[-polinomio_grau:]
    data_bits.append(crc_resto)
    return data_atual
"""

def hamming(binary_sequence: list [int]):
    #Hamming 7/4
    
    hamming_byte=[]
    aux=[]

    # Esse laço de repetição vai dividir a sequencia binaria em nibbles, 
    # para que adicione 3 bits de paridades 2^^n resultando em 7 bits totais
    for i in range (0, len(binary_sequence),4):
        nibble = binary_sequence[i:i+4]

        if len(nibble) < 4 :
            nibble.extend([0] * (4-len(nibble)))        # Verificação se a binary_sequence é multiplo de 4

        # (p1,p2,m3,p4,m5,m6,m7)
        # (      n0,  ,n1,n2,n3)

        p1=  (nibble[0] ^ nibble[1] ^ nibble[3])
        p2=  (nibble[0] ^ nibble[2] ^ nibble[3])        # Calcula o bit de paridade
        p4=  (nibble[1] ^ nibble[2] ^ nibble[3])

        byte= [p1,p2,nibble[0],p4,nibble[1],nibble[2],nibble[3]]    # byte resultante
        
        hamming_byte.extend(byte)

    return hamming_byte