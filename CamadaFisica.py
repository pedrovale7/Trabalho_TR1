import numpy as np 
import matplotlib.pyplot as plt 


def manchester_modulation (bit_stream):
    #Manchester Unipolar
    
    signal=[] 
    clock= (0,1)  #Temporizador do Manchester

    for bit in bit_stream:
        signal.extend([bit ^ clock[0], bit ^ clock [1]]) #Sinal do bit XOR Sinal do clock

    return signal

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

    return signal

#Jose Artur - 180020439
def nrz_modulation(bit_stream):
    
    signal = []
    for bit in bit_stream:
        if bit == 1:
            signal.extend([1])   # +V para 1
        else:
            signal.extend([-1])  # -V para 0

    return signal 

def ask_modulation(amplitude, frequency, bit_stream):

    signal_size = len(bit_stream)
    signal = np.zeros(signal_size * 100)  

    for i in range(signal_size):
        if bit_stream[i] == 1 : 
            for j in range(100):
                signal[(i * 100) + j] = amplitude * np.sin(2 * np.pi * frequency * j / 100)
        else:
            for j in range(100):
                signal[(i * 100) + j] = 0

    return signal

#Henrique Izar - 222026985
def fsk_modulation(amplitude, frequency_1, frequency_2, bit_stream):
    signal_size = len(bit_stream)
    signal = np.zeros(signal_size*100)

    for i in range(signal_size):
        if bit_stream[i] ==1:
            for j in range(100):
                signal[((i)*100) + j] = amplitude * np.sin(2 * np.pi * frequency_1 * j / 100)
        else:
            for j in range(100):
                signal[((i)*100) + j] = amplitude * np.sin(2 * np.pi * frequency_2 * j / 100)
    return signal


def qam8_modulation(amplitude_low, amplitude_high, frequency_portadora, bit_stream):
    #dicionario para as respectivas amplitudes e fases:
    symbol_map = {
       
        "000": (amplitude_low, 0),
        "001": (amplitude_low, 90),
        "010": (amplitude_low, 180),
        "011": (amplitude_low, 270),
        "100": (amplitude_high, 45),
        "101": (amplitude_high, 135),
        "110": (amplitude_high, 225),
        "111": (amplitude_high, 315)
    }


    # garantindo que o stream de bits seja um múltiplo de 3,
    #  e se nao for, completar com '0':
    bits_faltantes = 3 - (len(bit_stream) % 3) if len(bit_stream) % 3 != 0 else 0
    if bits_faltantes > 0:
        print(f"Bit stream nao é multiplo de 3. Completando com {bits_faltantes} zeros.")
        bit_stream.extend([0] * bits_faltantes)

    num_symbols = len(bit_stream) // 3
    
    qam_signal = np.zeros(num_symbols * 100)


    
    for i in range(num_symbols):
        # converte 3 bits para uma string:
        str_bits = "".join(str(bit) for bit in bit_stream[i*3 : (i+1)*3])
        
        # converte grau para radiano:
        amplitude, grau = symbol_map[str_bits]
        radianos = np.deg2rad(grau)

        # calcula I e Q para usar na formula S(t)=I(t)⋅cos(2πft)−Q(t)⋅sin(2πft)
        I = amplitude * np.cos(radianos)
        Q = amplitude * np.sin(radianos)

        # grafico de onda:
        for j in range(100):
            # normaliza tempo de 0 a 1:
            tempo_normalizado = j / 100
            
            # formula: S(t) = I * cos(2pift) - Q * sin(2pift)
            qam_signal[(i * 100) + j] = \
                (I * np.cos(2 * np.pi * frequency_portadora * tempo_normalizado)) - \
                (Q * np.sin(2 * np.pi * frequency_portadora * tempo_normalizado))
            
    return qam_signal



def main(digital_modulation : str ,analogic_modulation: str, binary_input: list[int]):

   
    # Escolha do Metodos de Modulação Digital
    if (digital_modulation == "NRZ-Polar"):
        signal = nrz_modulation(binary_input)
    elif (digital_modulation == "Manchester"):
        signal = manchester_modulation(binary_input)
    elif(digital_modulation == "Bipolar"):
        signal = bipolar_modulation(binary_input)

    time = np.linspace(0, len(binary_input), len(signal), endpoint=False)

    if(digital_modulation!= None):
        plt.figure(figsize=(12,4))
        plt.plot(time, signal, drawstyle="steps-pre")
        plt.title(f"Modulação Digital {digital_modulation}")
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.show()
        plt.close()


    # Escolhendo a modulação por Portadora
    if (analogic_modulation == "ASK"):
        analogic_signal=ask_modulation(1, 1, binary_input)
    elif(analogic_modulation == "FSK"):
        analogic_signal=fsk_modulation(1, 2, 1,binary_input)
    elif(analogic_modulation == "8QAM"):
        analogic_signal=qam8_modulation(0.5, 1.0, 1, binary_input)


    if(analogic_modulation != None):
        plt.figure(figsize=(10,4))
        plt.plot(analogic_signal)
        plt.title(f"Sinal modulado por {analogic_modulation}")
        plt.xlabel("Amostras")
        plt.ylabel("Amplitude")
        plt.show()
        plt.close()