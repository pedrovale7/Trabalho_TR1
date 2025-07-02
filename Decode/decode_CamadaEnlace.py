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