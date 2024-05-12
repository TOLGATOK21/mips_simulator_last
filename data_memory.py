from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets

class DataMemory(QObject):
    memory_updated = pyqtSignal()
    degiskenler = {}
    degisken_adresler = {}

    def __init__(self):
        super().__init__()
        self.memory = {}  # Belleği depolamak için bir sözlük
        start_address = 0x10010000
        end_address = 0x10010400
        current_address = start_address
        while current_address <= end_address:
            if current_address == start_address:
                self.memory[current_address] = 0x00000000  # Başlangıç adresinin değeri 0x00000000
            else:
                self.memory[current_address] = 0x00000000  # Diğer adreslerin değeri 0x00000000
            current_address += 4
        
        self.current_address = 0x10010000  # Başlangıç adresi
        
        
    def update_memory(self, address, value):
    # Bellek adresindeki değeri güncelle
     if address in self.memory:
        self.memory[address] = value
        # Bellek güncellendiğinde sinyal gönder
        self.memory_updated.emit()
     else:
        print("Hata: Geçersiz bellek adresi.")


    def load_program(self, program):
        # Programı belleğe yükleyin
        for address, instruction in enumerate(program):
            self.memory[0x00400000 + address * 4] = instruction

    def write_memory(self, address, value, name_value):
        # Belleğe veri yazma
        if address in self.memory:
            self.memory[address] = value
            # Bellek güncellendiğinde sinyal gönder
            self.memory_updated.emit()
        else:
            print("Hata: Geçersiz bellek adresi.")

    def read_memory(self, address):
        # Bellekten veri okuma
        if address in self.memory:
            return self.memory[address]
        else:
            print("Hata: Geçersiz bellek adresi.")

    def get_current_address(self):
        return self.current_address

    def increment_address(self):
        self.current_address += 4

    def process_data_section(self, line):
        
        parts = line.split(':')
        
        if len(parts) == 2:
            var_name = parts[0].strip()  # Değişken adı
            data = parts[1].strip().split()  # Değer ve tür
            if len(data) == 2 and data[0] == '.word':
                value = int(data[1])  # Değeri tam sayıya dönüştürme
                self.degiskenler[var_name] = value
                # Belleğe değeri yazma
                current_address = self.get_current_address()
                self.degisken_adresler[var_name] = current_address
                self.write_memory(current_address, value, var_name)
                # Adresi 4 artırma
                self.increment_address()
                print(self.degiskenler)
