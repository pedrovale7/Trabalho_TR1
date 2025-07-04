import random

def decode_nrz_polar(bit_stream):
    
    for n in range(0, len(bit_stream)):
        if random.randint(0, 100) <= 10:
            if bit_stream[n] == 1:
                bit_stream[n] = 0
            else:
                bit_stream[n] = 1

    demodulate_bit_stream=[]
    for bit in bit_stream:
        if bit==1:
            demodulate_bit_stream.append(1)     # Se 1 --> 1
        else:
            demodulate_bit_stream.append(0)     # Se -1 -->0

    return demodulate_bit_stream

def decode_manchester(bit_stream):
    # Adicionando erro:
    # se erro < 0.1 : flipa o bit
    for i in range (0, len(bit_stream),2):
        if random.randint(0,100) <=10:
            if bit_stream[i:i+1]==[0,1]:
                bit_stream[i:i+1]==[1,0]
            else:
                bit_stream[i:i+1]==[0,1]

    demodulate_bit_stream=[]
    for bit in range(0,len(bit_stream),2):
        if bit_stream[bit]==0 and bit_stream[bit+1]==1 : demodulate_bit_stream.append(0)    #Se 01 --> 0
        else: demodulate_bit_stream.append(1)                                               #Se 10 --> 1

    return demodulate_bit_stream

def decode_bipolar (bit_stream):
    
    for n in range(0, len(bit_stream)):
        if random.randint(0, 100) <= 10:
            if bit_stream[n] == 1:
                bit_stream[n] = random.randint(0, -1)
            else:
                bit_stream[n] = random.randint(0, 1)
    
    demodulate_bit_stream=[]
    for bit in bit_stream:
        if bit==1 or bit==-1: demodulate_bit_stream.append(1)       #Se 1 ou -1 --> 1
        else: demodulate_bit_stream.append(0)                       #Se 0 --> 0

    return demodulate_bit_stream

def main(digital_demodulation : str ,analogic_demodulation: str, binary_input: str):

    binary_sequence =[int(bit) for bit in binary_input]     # Transformar a sequencia de bits em inteiros

    # Escolhendo a modulação por Portadora
    #if (analogic_demodulation == "ASK"):
     #   analogic_signal=ask_demodulation(1, 1, binary_sequence)
    #elif(analogic_demodulation == "FSK"):
     #   analogic_signal=fsk_demodulation(1, 2, 1,binary_sequence)
    #elif(analogic_demodulation == "8QAM"):
     #   analogic_signal=qam8_demodulation(0.5, 1.0, 1, binary_sequence)


    #if(analogic_demodulation != None):
     #   plt.figure(figsize=(10,4))
      #  plt.plot(analogic_signal)
       # plt.title(f"Sinal demodulado por {analogic_demodulation}")
        #plt.xlabel("Amostras")
        #plt.ylabel("Amplitude")
        #plt.show()
        #plt.close()

    # Escolha do Metodos de Modulação Digital
    if (digital_demodulation == "NRZ-Polar"):
        signal = decode_nrz_polar(binary_sequence)
    elif (digital_demodulation == "Manchester"):
        signal = decode_manchester(binary_sequence)
    elif(digital_demodulation == "Bipolar"):
        signal= decode_bipolar(binary_sequence)