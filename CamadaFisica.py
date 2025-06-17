import numpy as np 
import matplotlib.pyplot as plt 


def manchester_modulation (bit_stream):
    signal=[] 
    clock= (0,1)  #Temporizador do Manchester

    for bit in bit_stream:
        signal.extend([bit ^ clock[0], bit ^ clock [1]]) #Sinal do bit XOR Sinal do clock

    time=np.arange(len(signal)) #Eixo de Tempo, cada bit gera dois valores

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



def main(digital_modulation : str ,analogic_modulation: str, binary_input: str):

    binary_sequence =[int(bit) for bit in binary_input]     # Transformar a sequencia de bits em inteiros

    # Escolha do Metodos de Modulação Digital
    if (digital_modulation == "NRZ-Polar"):
        signal,time = nrz_modulation(binary_sequence)
    elif (digital_modulation == "Manchester"):
        signal,time = manchester_modulation(binary_sequence)
    elif(digital_modulation == "Bipolar"):
        signal,time = bipolar_modulation(binary_sequence)

    plt.figure(figsize=(8,4))
    plt.plot(time, signal, drawstyle="steps-pre")
    plt.title(f"Modulação Digital {digital_modulation}")
    plt.xlabel("Tempo")
    plt.ylabel("Amplitude")
    plt.xticks(np.arange(0,len(time),1))
    for i in time:
        plt.axvline(i,color="black", linestyle="--",linewidth=0.5)
    plt.show()
    plt.close()
'''
    # Escolhendo a modulação por Portadora
    if (analogic_modulation == "ASK"):
        analogic_signal=ask_modulation()
    elif(analogic_modulation == "FSK"):
        analogic_signal=fsk_modulation()
    elif(analogic_modulation == "8QAM"):
        analogic_signal=qam8_modulation()

    plt.figure(figsize=(8,4))
    plt.plot(analogic_signal)
    plt.title(f"Sinal modulado por {analogic_modulation}")
    plt.xlabel("Amostras")
    plt.ylabel("Amplitude")
    for i in time:
        plt.axvline(i,color="black", linestyle="--",linewidth=0.5)
    plt.show()
    plt.close()
              
''' 







bin="0101010001010101010101"
main("Bipolar",None,bin)