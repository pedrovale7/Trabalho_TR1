import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import numpy as np
import sys
import CamadaFisica as cf
import CamadaEnlace as ce

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
        self.graph_box.set_hexpand(True)
        self.graph_box.set_vexpand(True)
        
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
        
        self.grid.attach(scrolled_window, 0, 6, 3, 6)
        
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
            # Implementar contagem de caracteres
            pass
        elif framing_method == "Enquadramento com FLAG e byte stuffing":
            framed_data = ce.byte_insertion(message)
        elif framing_method == "Enquadramento com FLAG e bit stuffing":
            # Implementar bit stuffing
            pass
        
        # Aplicar detecção de erros
        if error_detection:
            if error_method == "Bit de paridade":
                binary_sequence = ce.bit_parity(binary_sequence)
            elif error_method == "CRC-32":
                # Implementar CRC-32
                pass
            elif error_method == "Hamming":
                # Implementar Hamming
                pass
        
        # Mostrar sequência binária na saída
        buffer = self.output_text.get_buffer()
        buffer.set_text(f"Mensagem original: {message}\n")
        buffer.insert(buffer.get_end_iter(), f"Sequência binária: {binary_sequence}\n")
        
        # Executar modulações
        if digital_mod:
            signal, time = None, None
            if digital_mod == "NRZ-Polar":
                signal, time = cf.nrz_modulation(binary_sequence)
            elif digital_mod == "Manchester":
                signal, time = cf.manchester_modulation(binary_sequence)
            elif digital_mod == "Bipolar":
                signal, time = cf.bipolar_modulation(binary_sequence)
            
            if signal is not None:
                self.plot_digital_signal(signal, time, digital_mod)
        
        if analog_mod:
            analog_signal = None
            if analog_mod == "ASK":
                analog_signal = cf.ask_modulation(1, 1, binary_sequence)
            if analog_mod == "FSK":
                analog_signal = cf.fsk_modulation(1, 1, 2, binary_sequence)
            if analog_mod == "8QAM":
                analog_signal = cf.qam8_modulation(1, 2, 1, binary_sequence)

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