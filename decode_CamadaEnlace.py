import CamadaEnlace as ce
from bitarray import bitarray

def is_valid_utf8(byte_list):
    try:
        bytes(byte_list).decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False

def text_from_bits(bits: list[int], enconding = "utf-8", errors = "surrogatepass" ):
    
    array=bitarray(bits)                        # Cria um Bitarray
    bytes=array.tobytes()                       # Converte para uma sequencia de Bytes
    
    if is_valid_utf8(bytes):
        text_output = bytes.decode(enconding,errors)# Transforma novamente em texto ASCII
    else:
        text_output = "Sequência de bits impossível de decodificar"    
    return text_output

def decode_charactere_count(bits: list[int]):
    print(bits)
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

def decode_bit_insertion(bits:list[int]): 
    # O transmissor insere um '0' após 5 1s
    # entao procuraremos 5 '1's seguidos e retiraremos o '0' que os segue

    aux = []
    count_ones = 0 #contador de '1's

    #remove as flags inicial e final
    bits_sequence = [bits[i] for i in range (8,len(bits)-8)] 

    i = 0
    while i < len(bits_sequence):
        current_bit = bits_sequence[i]

        if current_bit == 1:
            count_ones += 1
            aux.append(current_bit) # Adiciona o 1 ao resultado
        else: # bit atual == 0
            if count_ones == 5:
                # se encontramos 5 1's e esse proximo bit é 0, ele é o bit de stuffing, que NÃO é adicionado ao 'aux'
                # reset na contagem
                count_ones = 0 
                i += 1 
                continue
            else:
                # nesse caso é um '0' normal, entao ele é add ao 'aux'
                aux.append(current_bit)
                count_ones = 0

        i += 1

    # converte a sequencia binaria denovo em texto
    text_output = text_from_bits(aux)

    return text_output


def verifica_bit_parity(binary_sequence: list[int]):
    error_verif = None
    parity_bit = binary_sequence[-1]
    parity= sum(binary_sequence)%2                              # soma = 0 paridade par
                                                                # soma = 1 paridade impar
    if parity != parity_bit:
        error_verif = "Erro detectado - Bit de Paridade"
    return error_verif, binary_sequence                                 # Remove o ultimo bit (paridade)

def verifica_crc(binary_sequence: list[int]):

    # a verificaçao acontece da mesma forma que o checksum(XOR)
    # se o resto for tudo 0 significa que está sem erro
    resto = ce.crc_checksum(binary_sequence)
    # if not (all(bit == '0' for bit in resto)): # Original: comparação com string '0'
    if not (all(bit == 0 for bit in resto)): # Corrigido: comparação com inteiro 0
        error_verif = "Erro detectado - CRC"
        return error_verif, binary_sequence
    else: 
        return "OK", binary_sequence

def corr_haming(framing_method, binary_sequence: list[int]):                         # Função que faz a correção do erro
                                                          # da sequencia de hamming
    decode=[]
    hamming_sequence = []
    
    if framing_method == "Contagem de caracteres":
        binary_sequence = binary_sequence[:28]
    elif framing_method == "Enquadramento com FLAG e byte stuffing":
        binary_sequence = binary_sequence[:42]
    elif framing_method == "Enquadramento com FLAG e bit stuffing":
        binary_sequence = binary_sequence[:42]

    for i in range(0,len(binary_sequence), 7):
        aux = list(binary_sequence[i:i+7])
        t1 = str((aux[0] ^ aux[2] ^ aux[4] ^ aux[6])%2)   # | LSB   Calcula a posição onde aconteceu o erro
        t2 = str((aux[1] ^ aux[2] ^ aux[5] ^ aux[6])%2)   # |       por meio da aplicação de XOR
        t3 = str((aux[3]^ aux[4]^ aux[5] ^ aux[6])%2)     # v MSB

        error = int(t3+t2+t1,2)                           # concatena os erros, se achar algum erro, error !=0
        if error != 0:                                          
            aux[error-1] = 1-aux[error-1]
            decode = [aux[2],aux[4],aux[5],aux[6]]        # resgata somente os dados tirando as paridades    
            hamming_sequence.extend(decode)          
        else: 
            decode =[aux[2],aux[4],aux[5],aux[6]]
            hamming_sequence.extend(decode)

    if len(hamming_sequence)< len(binary_sequence):       # tira os paddings adicionais
        return hamming_sequence[:len(hamming_sequence)]
    return hamming_sequence [:len(binary_sequence)]