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

'''
#TESTE CRC:

msg_original = "1101011011"

# polinômio gerador G(x)= x^8 + x^2 + x + 1 --> [CRC-8]
crc8_polinomio = "100000111"

print(f"Mensagem original: {msg_original}")
print(f"Polinomio G(x): {crc8_polinomio}")


crc_calculado = crc_checksum(msg_original, crc8_polinomio)
print(f"CRC Calculado: {crc_calculado}")

# (msg_original + CRC) = mensagem que será transmitida
msg_a_transmitir = msg_original + crc_calculado
print(f"Mensagem a ser Transmitida: {msg_a_transmitir}")

#Recepçao:

# Caso 1: sem erros:
msg_recebida_sem_erro = msg_a_transmitir
print(f"\n--- Recepção (sem Erros) ---")
print(f"Mensagem recebida: {msg_recebida_sem_erro}")
is_correct_sem_erro = verifica_crc(msg_recebida_sem_erro, crc8_polinomio)
print(f"Dados corretos (sem erro)? {is_correct_sem_erro}")

# Caso 2: com erro (alterando o bit de indice 4):
index_erro = 4
msg_recebida_errada_list = list(msg_a_transmitir)
msg_recebida_errada_list[index_erro] = '1' if msg_recebida_errada_list[index_erro] == '0' else '0'
msg_recebida_errada = "".join(msg_recebida_errada_list)

print(f"\n--- Recepção (com erros) ---")
print(f"Mensagem Recebida (com erro no bit {index_erro + 1}): {msg_recebida_errada}")
is_correct_com_erro = verifica_crc(msg_recebida_errada, crc8_polinomio)
print(f"Dados Corretos (com erro)? {is_correct_com_erro}")

'''

"""
def decode_bit_insertion(bits:list[int]):
    flag = [0,1,1,1,1,1,1,0]
    count=0
    aux=[]

    #Remove a Flag inicial e final e retorna somente a sequencia binária
    bits_sequence = [bits[i] for i in range (8,len(bits)-8)]
    #Remover todos 0s depois de cinco 1s
    for i in bits_sequence:
        #aux=bits_sequence[i]
        if count == 5:
            if aux == 0:
                count = 0 
                i += 1 
                continue 
        
        aux.append(bits_sequence[i])
        
        if aux == 1:
            count += 1
        else: 
            count = 0
        
        i += 1

    #Transformar a sequencia binaria de volta em texto
    text_output = text_from_bits(aux)
    
    return text_output

print(decode_bit_insertion([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0]))
print(decode_bit_insertion([0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0]))
"""