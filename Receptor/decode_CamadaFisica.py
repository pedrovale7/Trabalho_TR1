import random

def decode_nrz_polar(bit_stream):

    demodulate_bit_stream=[]
    for bit in bit_stream:
        if bit==1:
            demodulate_bit_stream.append(1)     # Se 1 --> 1
        else:
            demodulate_bit_stream.append(0)     # Se -1 -->0

    return demodulate_bit_stream

def decode_manchester(bit_stream):

    demodulate_bit_stream=[]
    for bit in range(0,len(bit_stream),2):
        if bit_stream[bit]==0 and bit_stream[bit+1]==1 : demodulate_bit_stream.append(0)    #Se 01 --> 0
        else: demodulate_bit_stream.append(1)                                               #Se 10 --> 1

    return demodulate_bit_stream

def decode_bipolar (bit_stream):
    
    demodulate_bit_stream=[]
    for bit in bit_stream:
        if bit==1 or bit==-1: demodulate_bit_stream.append(1)       #Se 1 ou -1 --> 1
        else: demodulate_bit_stream.append(0)                       #Se 0 --> 0

    return demodulate_bit_stream

def main(digital_demodulation : str, binary_input: list [int]):

    # Escolha do Metodos de demodulação Digital
    if (digital_demodulation == "NRZ-Polar"):
        signal = decode_nrz_polar(binary_input)
    elif (digital_demodulation == "Manchester"):
        signal = decode_manchester(binary_input)
    elif(digital_demodulation == "Bipolar"):
        signal= decode_bipolar(binary_input)