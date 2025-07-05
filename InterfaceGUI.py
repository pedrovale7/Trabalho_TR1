import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import numpy as np
import CamadaFisica as cf
import CamadaEnlace as ce
import transmissor as tm
import Receptor as rc
import threading
import decode_CamadaEnlace as decode_ce

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulador de Comunicações")
        self.set_default_size(800, 600)
        
        # Configuração do layout principal
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.add(self.grid)
        
        # Seção de entrada de dados
        self.create_input_section()
        
        # Seção de seleção de modulação digital
        self.create_digital_modulation_section()
        
        # Seção de seleção de modulação analógica
        self.create_analog_modulation_section()
        
        # Seção de enquadramento e detecção de erros
        self.create_framing_section()
        
        # Área de visualização dos resultados
        self.create_output_section()
        
        # Botão de execução
        self.run_button = Gtk.Button(label="Executar Simulação")
        self.run_button.connect("clicked", self.on_run_clicked)
        self.grid.attach(self.run_button, 0, 5, 3, 1)
        
        # Área para gráficos
        self.graph_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.grid.attach(self.graph_box, 3, 0, 100, 80)
        
    def create_input_section(self):
        # Label e entrada para mensagem
        input_label = Gtk.Label(label="Mensagem de Entrada:")
        self.grid.attach(input_label, 0, 0, 1, 1)
        
        self.input_entry = Gtk.Entry()
        self.input_entry.set_hexpand(True)
        self.grid.attach(self.input_entry, 1, 0, 2, 1)
        
    def create_digital_modulation_section(self):
        # Label para modulação digital
        digital_label = Gtk.Label(label="Modulação Digital:")
        self.grid.attach(digital_label, 0, 1, 1, 1)
        
        # Combo box para seleção de modulação digital
        self.digital_combo = Gtk.ComboBoxText()
        self.digital_combo.append_text("NRZ-Polar")
        self.digital_combo.append_text("Manchester")
        self.digital_combo.append_text("Bipolar")
        self.digital_combo.set_active(0)
        self.grid.attach(self.digital_combo, 1, 1, 2, 1)
        
    def create_analog_modulation_section(self):
        # Label para modulação analógica
        analog_label = Gtk.Label(label="Modulação por Portadora:")
        self.grid.attach(analog_label, 0, 2, 1, 1)
        
        # Combo box para seleção de modulação analógica
        self.analog_combo = Gtk.ComboBoxText()
        self.analog_combo.append_text("ASK")
        self.analog_combo.append_text("FSK")
        self.analog_combo.append_text("8QAM")
        self.analog_combo.set_active(0)
        self.grid.attach(self.analog_combo, 1, 2, 2, 1)
        
    def create_framing_section(self):
        # Label para métodos de enquadramento
        framing_label = Gtk.Label(label="Método de Enquadramento:")
        self.grid.attach(framing_label, 0, 3, 1, 1)
        
        # Combo box para seleção de enquadramento
        self.framing_combo = Gtk.ComboBoxText()
        self.framing_combo.append_text("Contagem de caracteres")
        self.framing_combo.append_text("Enquadramento com FLAG e byte stuffing")
        self.framing_combo.append_text("Enquadramento com FLAG e bit stuffing")
        self.framing_combo.set_active(0)
        self.grid.attach(self.framing_combo, 1, 3, 2, 1)
        
        # Checkbox para detecção de erros
        self.error_check = Gtk.CheckButton(label="Adicionar detecção de erros")
        self.grid.attach(self.error_check, 0, 4, 1, 1)
        
        # Combo box para seleção de método de detecção
        self.error_combo = Gtk.ComboBoxText()
        self.error_combo.append_text("Bit de paridade")
        self.error_combo.append_text("CRC-32")
        self.error_combo.append_text("Hamming")
        self.error_combo.set_active(0)
        self.error_combo.set_sensitive(False)
        self.grid.attach(self.error_combo, 1, 4, 2, 1)
        
        # Conectar sinal do checkbox
        self.error_check.connect("toggled", self.on_error_check_toggled)
        
    def create_output_section(self):
        # Scrolled window para a saída
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        
        self.output_text = Gtk.TextView()
        self.output_text.set_editable(False)
        self.output_text.set_wrap_mode(Gtk.WrapMode.WORD)
        scrolled_window.add(self.output_text)
        
        self.grid.attach(scrolled_window, 0, 6, 3, 50)
        
    def on_error_check_toggled(self, button):
        self.error_combo.set_sensitive(button.get_active())
        
    def on_run_clicked(self, button):
        # Obter dados de entrada
        message = self.input_entry.get_text()
        digital_mod = self.digital_combo.get_active_text()
        analog_mod = self.analog_combo.get_active_text()
        framing_method = self.framing_combo.get_active_text()
        error_detection = self.error_check.get_active()
        error_method = self.error_combo.get_active_text() if error_detection else None
        
        # Limpar área de gráficos
        for child in self.graph_box.get_children():
            self.graph_box.remove(child)
        
        # Processar a mensagem
        self.process_message(message, digital_mod, analog_mod, framing_method, error_detection, error_method)
        
    def process_message(self, message, digital_mod, analog_mod, framing_method, error_detection, error_method):
        # Converter mensagem para bits
        binary_sequence = ce.convert_to_bytes(message)
        
        # Aplicar enquadramento
        if framing_method == "Contagem de caracteres":
            framed_data = ce.character_count(binary_sequence)
            pass
        elif framing_method == "Enquadramento com FLAG e byte stuffing":
            framed_data = ce.byte_insertion(binary_sequence)
        elif framing_method == "Enquadramento com FLAG e bit stuffing":
            framed_data = ce.bit_insertion(binary_sequence)
            pass
        
        # Aplica o formato para detecção e correção de erro
        if error_detection:
            if error_method == "Bit de paridade":
                framed_data = ce.bit_parity(framed_data)
            elif error_method == "CRC-32":
                framed_data = ce.crc_checksum(framed_data)
                pass
            elif error_method == "Hamming":
                framed_data = ce.hamming(framed_data)
                pass

        # Crie uma instância do receptor compartilhado
        receiver = rc.Receiver()

        # Inicie o receptor em uma thread separada
        receiver_thread = threading.Thread(target=receiver.TCPServer, daemon=True)
        receiver_thread.start()

        # Aguarde um breve momento para o servidor iniciar
        import time
        time.sleep(0.5)

        # Envie os dados
        if not tm.startServer(framed_data):
            buffer = self.output_text.get_buffer()
            buffer.insert(buffer.get_end_iter(), "\nErro: Falha ao transmitir dados!\n")
            return

        # Espere os dados serem recebidos (timeout de 5 segundos)
        if receiver.data_ready.wait(timeout=5):
            received_data = receiver.sent_data
            
            # Agora você pode usar received_bits no resto do processamento
            buffer = self.output_text.get_buffer()
            buffer.insert(buffer.get_end_iter(), f"\nDados recebidos: {received_data}\n")
            
        else:
            buffer = self.output_text.get_buffer()
            buffer.insert(buffer.get_end_iter(), "\nTimeout: Nenhum dado recebido!\n")

        #Detecção do erro e decodificação
        if error_detection:
            if error_method == "Bit de paridade":
                decoded_data = decode_ce.verifica_bit_parity(receiver.sent_data)
            elif error_method == "CRC-32":
                decoded_data = decode_ce.verifica_crc(receiver.sent_data)
                pass
            elif error_method == "Hamming":
                decoded_data = decode_ce.corr_haming(receiver.sent_data)
                pass


        # Mostrar sequência binária na saída
        buffer = self.output_text.get_buffer()
        buffer.set_text(f"Mensagem original: {message}\n\n")
        buffer.insert(buffer.get_end_iter(), f"Sequência binária original:\n {binary_sequence}\n\n")
        buffer.insert(buffer.get_end_iter(), f"Sequência binária enquadrada enviada:\n {framed_data}\n\n")
        buffer.insert(buffer.get_end_iter(), f"Sequência binária recebida:\n {received_data}\n")
        buffer.insert(buffer.get_end_iter(), f"Posição do erro:\n {receiver.changed_bit_position}\n")
        buffer.insert(buffer.get_end_iter(), f"Sequencia autenticada:\n {decoded_data}\n")

        # Executar modulações
        if digital_mod:
            if digital_mod == "NRZ-Polar":
                signal = cf.main(digital_mod, analog_mod = None, decoded_data)
            elif digital_mod == "Manchester":
                signal = cf.manchester_modulation(bit_sequence)
            elif digital_mod == "Bipolar":
                signal = cf.bipolar_modulation(bit_sequence)
            
            if signal is not None:
                self.plot_digital_signal(signal, time, digital_mod)
        
        if analog_mod:
            analog_signal = None
            if analog_mod == "ASK":
                analog_signal = cf.ask_modulation(1, 1, bit_sequence)
            if analog_mod == "FSK":
                analog_signal = cf.fsk_modulation(1, 1, 2, bit_sequence)
            if analog_mod == "8QAM":
                analog_signal = cf.qam8_modulation(1, 2, 1, bit_sequence)

            if analog_signal is not None:
                self.plot_analog_signal(analog_signal, analog_mod)
    
    def plot_digital_signal(self, signal, time, title):
        fig = plt.Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, signal, drawstyle="steps-pre")
        ax.set_title(f"Modulação Digital {title}")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Amplitude")
        ax.set_xticks(np.arange(0, len(time), 1))
        for i in time:
            ax.axvline(i, color="black", linestyle="--", linewidth=0.5)
        
        canvas = FigureCanvas(fig)
        self.graph_box.pack_start(canvas, True, True, 0)
        canvas.show()
    
    def plot_analog_signal(self, signal, title):
        fig = plt.Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(signal)
        ax.set_title(f"Sinal modulado por {title}")
        ax.set_xlabel("Amostras")
        ax.set_ylabel("Amplitude")
        
        canvas = FigureCanvas(fig)
        self.graph_box.pack_start(canvas, True, True, 0)
        canvas.show()

# Inicializar e mostrar a janela
win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()