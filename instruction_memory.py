from PyQt5.QtCore import QObject, pyqtSignal
from data_memory import DataMemory

class InstructionMemory(QObject):
    instruction_memory_updated = pyqtSignal()
    data_memory= DataMemory()
    register_table_updated = pyqtSignal(dict)
   

    def __init__(self):
        super().__init__()
        self.memory = {}
        self.next_address = 0x00400000  # Başlangıç adresi
        self.pc = 0x00400000 
        

    def load_program(self, program):
     """
     Programı belleğe yükleyin.
     """
     for instruction in program:
        opcode = instruction[0]
        operands = instruction[1:]

        if self.next_address in self.memory:
            print("Hata: Bu adreste zaten bir komut var.")
            continue

        self.memory[self.next_address] = {'opcode': opcode, 'operands': operands}
        
    # Adresi bir sonraki komut için artır
        self.next_address += len(program) * 4

    def read_instruction(self, address):
        """
        Belirtilen adresteki komutu oku.
        """
        if address in self.memory:
            return self.memory[address]
        else:
            print("Hata: Geçersiz adres")
            return None

    def process_text_section(self, text):
    
     rows = text.split('\n')
     program = []

     for row in rows:
        row = row.strip()  # Satırın başındaki ve sonundaki boşlukları temizle
        if not row:  # Eğer satır boşsa atla
            continue
        
        # Satırı boşluğa kadar ve komut parçalarına ayır
        parts = row.split(' ', 1)
        opcode, rest = parts[0], parts[1] if len(parts) > 1 else ''
    
        # Operandları ayır
        operands = rest.split(',') if rest else []

        # Programa ekle
        program.append((opcode, *operands))
        
    # Komutları belleğe yükle
        self.load_program(program)
        print(f"Address: {self.next_address}, Program: {program}")
    
    # Güncelleme sinyalini yayınla
        self.instruction_memory_updated.emit()
        
    def next_step(self):
     if self.pc in self.memory:
        instruction = self.memory[self.pc]
        opcode = instruction['opcode']
        operands = instruction['operands']
        
        if opcode == 'lw':
            self.lw(operands)
        elif opcode == 'sw':
            self.sw(operands)
        elif opcode == 'add':
            self.add(operands)
        elif opcode == 'sub':
            self.sub(operands)
        elif opcode == 'j':
            address = operands[0]
            self.jump(address)
        elif opcode == 'jal':
            address = operands[0]
            self.jal(address)
        else:
            print(f"Current Address: {self.pc}, Opcode: {opcode}, Operands: {operands}")
     else:
        print("Hata: Geçersiz adres")

    # Program sayacını bir sonraki adrese geçir
     self.pc += 4
     self.update_register_table(self.registers)


    def lw(self, operands):
    # İlk operand register adı, ikinci operand ise data belleğindeki değişkenin adı olacak
     register_name  = operands[0]
     var_name = operands[1].strip()


    # Data belleği sözlüğünden değişkenin değerini al
     if var_name in DataMemory.degiskenler:
        value = self.data_memory.degiskenler[var_name]
     else:
        print(f"Hata: {var_name} adında bir değişken bulunamadı.")
        return

    # Register sözlüğünü güncelle
     if register_name in self.registers:
        self.registers[register_name] = value
        print(f"{register_name} register'ı {value} değişkeninin değeriyle güncellendi.")
        print(self.registers)
        self.update_register_table(self.registers)
        self.register_table_updated.emit(self.registers)
     else:
        print(f"Hata: {register_name} geçersiz bir register adı.")

     






    def sw(self, operands):
    # İşlem için gerekli operandları al
     register_name = operands[0]  # Kaynak register
     var_name = operands[1].strip()  # Hedef değişken adı 

    # Veriyi register'dan al
     if register_name in self.registers:
        value = self.registers[register_name]
        print("ALINAN REGİSTERDAKİ DEĞER:", value)
     else:
        print(f"Hata: {register_name} adında bir register bulunamadı.")
        return

    # Değişken adına ait bellek adresini al
     if var_name in self.data_memory.degisken_adresler:
        address = self.data_memory.degisken_adresler[var_name]
        print("BELLEK ADDRESİ", hex(address))
     else:
        print(f"Hata: {var_name} adında bir değişken bulunamadı.")
        return
    # Verinin güncellenmesi
     


    # Belleğe veriyi yaz
     self.data_memory.update_memory(address, value)
     print(f"{register_name} register'ındaki değer {var_name} değişkeninin adresindeki belleğe yazıldı.")


    def add(self, operands):
    # Gerekli operandları alın
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

    # İlk iki registerdan değerleri al
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        # Değerleri topla
        result = value_1 + value_2
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının toplamı olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")
        
    def sub(self,operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()
     

    # İlk iki registerdan değerleri al
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        print("SUB FONK DEĞERLERİ ", value_1, value_2)
        # Değerleri topla
        result = (int(value_1) - int(value_2))
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının farkı olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")
        pass
    def logical_and(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

    # İlk iki registerdan değerleri al
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        # Mantıksal AND işlemi yap
        result = value_1 & value_2
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının mantıksal AND'i olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def logical_or(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

    # İlk iki registerdan değerleri al
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        # Mantıksal OR işlemi yap
        result = value_1 | value_2
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının mantıksal OR'u olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def set_less_than(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

    # İlk iki registerdan değerleri al
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        # Küçüklük karşılaştırması yap
        result = 1 if value_1 < value_2 else 0
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının küçüklük karşılaştırması sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def set_less_than_immediate(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     immediate = int(operands[2].strip())

    # İlk registerın değerini al
     if register_name_1 in self.registers:
        value_1 = self.registers[register_name_1]
        
        # Küçüklük karşılaştırması yap
        result = 1 if value_1 < immediate else 0
        # Sonucu ilk registera yaz
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {immediate} değerlerinin küçüklük karşılaştırması sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")    
    def jump(self, address):
    # pc'yi yeni adrese ayarla
     self.pc = address

    def jal(self, address):
    # pc'yi yeni adrese ayarla
     self.registers["$ra"] = self.pc + 4  # Return Address'i kaydet
     self.pc = address

     
     
     
    registers = {
            "$zero": 0x00000000,   # Zero Register
            "$at": 0x00000000,     # Assembler Temporary
            "$v0": 0x00000000,     # Return Value 0
            "$v1": 0x00000000,     # Return Value 1
            "$a0": 0x00000000,     # Argument 0
            "$a1": 0x00000000,     # Argument 1
            "$a2": 0x00000000,     # Argument 2
            "$a3": 0x00000000,     # Argument 3
            "$t0": 0x00000000,     # Temporary 0
            "$t1": 0x00000000,     # Temporary 1
            "$t2": 0x00000000,     # Temporary 2
            "$t3": 0x00000000,     # Temporary 3
            "$t4": 0x00000000,     # Temporary 4
            "$t5": 0x00000000,     # Temporary 5
            "$t6": 0x00000000,     # Temporary 6
            "$t7": 0x00000000,     # Temporary 7
            "$s0": 0x00000000,     # Saved Temporary 0
            "$s1": 0x00000000,     # Saved Temporary 1
            "$s2": 0x00000000,     # Saved Temporary 2
            "$s3": 0x00000000,     # Saved Temporary 3
            "$s4": 0x00000000,     # Saved Temporary 4
            "$s5": 0x00000000,     # Saved Temporary 5
            "$s6": 0x00000000,     # Saved Temporary 6
            "$s7": 0x00000000,     # Saved Temporary 7
            "$t8": 0x00000000,     # Temporary 8
            "$t9": 0x00000000,     # Temporary 9
            "$k0": 0x00000000,     # Kernel Temporary 0
            "$k1": 0x00000000,     # Kernel Temporary 1
            "$gp": 0x00000000,     # Global Pointer
            "$sp": 0x00000000,     # Stack Pointer
            "$fp": 0x00000000,     # Frame Pointer
            "$ra": 0x00000000,     # Return Address
            "pc": 0x00000000,
            "hi": 0x00000000,
            "lo": 0x00000000,
        }
    

    def update_register_table(self, updated_registers):
        # Register tablosunu güncelle
        self.registers = updated_registers

        # Güncelleme sinyalini yayınla
        self.register_table_updated.emit(self.registers)
     
     
    

        


