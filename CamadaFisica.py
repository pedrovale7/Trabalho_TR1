import numpy as np 
import matplotlib.pyplot as plt 


def manchester_modulation (bit_stream):
    signal=[] 
    clock= (0,1)  #Temporizador do Manchester

    for bit in bit_stream:
        signal.extend([bit ^ clock[0], bit ^ clock [1]]) #Sinal do bit XOR Sinal do clock

    time=np.arange(len(signal)/2) #Eixo de Tempo, cada bit gera dois valores

    return signal,time

def bipolar_modulation (bit_stream):
    signal=[]
    last_bit = -1 # Definir um marcador de polaridade do ultimo bit
    
    for bit in bit_stream:
        if bit == 1:
            if last_bit == -1:
                signal.extend([1])  # +V
                last_bit = 1        # marcador trocado por 1
            else:
                signal.extend([-1]) # -V
                last_bit = -1       # marcador trocado por -1
        else:
            signal.extend([0])      # 0 continua 0

    time = np.arange(len(signal))   # Eixo do Tempo

    return signal,time
