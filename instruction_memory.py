from PyQt5.QtCore import QObject, pyqtSignal
from data_memory import DataMemory
import sys

class InstructionMemory(QObject):
    instruction_memory_updated = pyqtSignal()
    data_memory= DataMemory()
    register_table_updated = pyqtSignal(dict)
    output_of_code = " "
    output_of_code_changed = pyqtSignal(str)


   

    def __init__(self):
        super().__init__()
        self.memory = {}
        self.next_address = 0x00400000 
        self.pc = 0x00400000 
        self.loop_addresses = {}
       
        

    def load_program(self, program):
    
     for instruction in program:
        opcode = instruction[0].strip()
        operands = instruction[1:]

        if self.next_address in self.memory:
            print("Hata: Bu adreste zaten bir komut var.")
            continue

       
        if opcode.endswith(':'):
            
            label = opcode[:-1]
           
            self.loop_addresses[label] = self.next_address
           
            opcode = instruction[0]
            operands = instruction[1:]

        
        self.memory[self.next_address] = {'opcode': opcode, 'operands': operands}
        
       
        self.next_address += 4
        print(self.loop_addresses)


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
        row = row.strip() 
        if not row:  
            continue
        
        
        parts = row.split(' ', 1)
        opcode, rest = parts[0], parts[1] if len(parts) > 1 else ''
    
       
        operands = rest.split(',') if rest else []

        
        program.append((opcode, *operands))
        
    
        self.load_program(program)
        print(f"Address: {self.next_address}, Program: {program}")
    
    
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
        elif opcode == 'and':
            self.logical_and(operands)
        elif opcode == 'or':
            self.logical_or(operands)
        elif opcode == 'slt':
            self.set_less_than(operands)
        elif opcode == 'slti':
            self.set_less_than_immediate(operands)
        elif opcode == 'mul':
            self.mul(operands)
        elif opcode == 'mult':
            self.mul(operands)
        elif opcode == 'div':
            self.div(operands)
        elif opcode == 'j':
            self.jump(operands)
        elif opcode == 'jal':
            self.jump(operands)
        elif opcode == 'beq':
            self.beq(operands)
        elif opcode == 'bne':
            self.blt(operands)
        elif opcode == 'blt':
            self.blt(operands)
        elif opcode == 'bgt':
            self.bgt(operands)
        elif opcode == 'ble':
            self.ble(operands)
        elif opcode == 'bge':
            self.bge(operands)
        elif opcode == 'li':
            self.li(operands)
        elif opcode == 'addi':
            self.addi(operands)
        elif opcode == 'subi':
            self.subi(operands)
        elif opcode == 'syscall':
            self.syscall()
        elif opcode == 'move':
            self.move(operands)
            
        elif opcode == 'xor':
            self.xor(operands)
            
        elif opcode == 'nor':
            self.nor(operands)
            
        elif opcode == 'jr':
            self.jr(operands)
        elif opcode == 'andi':
            self.andi(operands)
        elif opcode == 'ori':
            self.ori(operands)
        
        elif opcode == 'sub':
            self.sub(operands)
        elif opcode == 'and':
            self.logical_and(operands)
        
        
        
        
        

        
        elif opcode == 'loop':
            pass
            
        else:
            print(f"Current Address: {self.pc}, Opcode: {opcode}, Operands: {operands}")
     else:
        print("Hata: Geçersiz adres")

   
     self.registers["pc"] = self.pc
     self.pc += 4
     

     
     self.update_register_table(self.registers)
     
    def run(self):
     while self.pc in self.memory:
        self.next_step()



    def syscall(self):
        """
        System call işlevini çağırır.
        """
        
        syscall_number = self.registers["$v0"]
        
        if syscall_number == 1:  
            self.output_of_code = str(self.output_of_code) + str(self.registers["$a0"])
            self.output_of_code_changed.emit(self.output_of_code)
            return print(str(self.output_of_code))
         
            
            
            
        
        elif syscall_number == 10: 
            print_value2 = "Program ended..."
            print(str(print_value2))
            sys.exit()
        
        else:
            print("Hata: Geçersiz system call numarası.")

    def lw(self, operands):
   
     register_name  = operands[0]
     var_name = operands[1].strip()


   
     if var_name in DataMemory.degiskenler:
        value = self.data_memory.degiskenler[var_name]
     else:
        print(f"Hata: {var_name} adında bir değişken bulunamadı.")
        return

   
     if register_name in self.registers:
        self.registers[register_name] = value
        print(f"{register_name} register'ı {value} değişkeninin değeriyle güncellendi.")
        print(self.registers)
        self.update_register_table(self.registers)
        self.register_table_updated.emit(self.registers)
     else:
        print(f"Hata: {register_name} geçersiz bir register adı.")
        
        
    def move(self, operands):
   
     source_register = operands[0].strip() 
     destination_register = operands[1].strip() 

   
     if destination_register in self.registers:
        value = self.registers[destination_register]
     else:
        print(f"Hata: {destination_register} adında bir register bulunamadı.")
        return

   
     if source_register in self.registers:
        self.registers[source_register] = value
        print(f"{source_register} register'ı {destination_register} register'ının değeriyle güncellendi.")
       
        self.update_register_table(self.registers)
        self.register_table_updated.emit(self.registers)
     else:
        print(f"Hata: {source_register} geçersiz bir register adı.")



     






    def sw(self, operands):
   
     register_name = operands[0]  
     var_name = operands[1].strip()  

  
     if register_name in self.registers:
        value = self.registers[register_name]
        print("ALINAN REGİSTERDAKİ DEĞER:", value)
     else:
        print(f"Hata: {register_name} adında bir register bulunamadı.")
        return

   
     if var_name in self.data_memory.degisken_adresler:
        address = self.data_memory.degisken_adresler[var_name]
        print("BELLEK ADDRESİ", hex(address))
     else:
        print(f"Hata: {var_name} adında bir değişken bulunamadı.")
        return
     self.data_memory.write_memory(address, value,var_name)
     self.data_memory.memory_updated.emit(self.data_memory.memory)

   
     


   
     
     print(f"{register_name} register'ındaki değer {var_name} değişkeninin adresindeki belleğe yazıldı.")


    def add(self, operands):
   
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

   
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
       
        result = value_1 + value_2
       
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
     

   
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        print("SUB FONK DEĞERLERİ ", value_1, value_2)
      
        result = (int(value_1) - int(value_2))
       
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

   
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
       
        result = value_1 & value_2
        
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

   
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        
        result = value_1 | value_2
       
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

    
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
        
        result = 1 if value_1 < value_2 else 0
        
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

  
     if register_name_1 in self.registers:
        value_1 = self.registers[register_name_1]
        
       
        result = 1 if value_1 < immediate else 0
     
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {immediate} değerlerinin küçüklük karşılaştırması sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")    
     
    def mult(self, operands):
    
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

   
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]

        
        result = value_1 * value_2

       
        self.registers['hi'] = (result >> 32) & 0xFFFFFFFF
        self.registers['lo'] = result & 0xFFFFFFFF
        self.registers[register_name_result] = result

        print(f"Çarpım sonucu 'hi' registerına yüksek 32 bit ve 'lo' registerına düşük 32 bit olarak kaydedildi.")
     else:
        print("Hata: Geçersiz register adı.")
        
    def mul(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

    
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        
     
        result = value_1 * value_2
        
       
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının çarpımı olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")


    def div(self, operands):
  
     register_name_1 = operands[0].strip()
     register_name_2 = operands[1].strip()

    
     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]

       
        quotient = value_1 // value_2
        remainder = value_1 % value_2

       
        self.registers['hi'] = remainder
        self.registers['lo'] = quotient

        print(f"Bölme işlemi sonucu 'hi' registerına kalan, 'lo' registerına bölüm olarak kaydedildi.")
     else:
        print("Hata: Geçersiz register adı.")

    
    def jump(self, operands):
        label = operands[0].strip()
        
        
        if label in self.loop_addresses:
            address = self.loop_addresses[label]
            self.pc = address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def jump_and_link(self, operands):
        label = operands[0].strip()
        return_address_register = operands[1]
        
   
        if label in self.loop_addresses:
            address = self.loop_addresses[label]
            self.pc = address
     
            self.registers[return_address_register] = self.pc + 4
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def beq(self, operands):
        register1 = operands[0]
        register2 = operands[1].strip()
        label = operands[2].strip() 
       
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
          
            if self.registers[register1] == self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def bne(self, operands):
        register1 = operands[0]
        register2 = operands[1]
        label = operands[2].strip() 
        
        
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
           
            if self.registers[register1] != self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def blt(self, operands):
        register1 = operands[0]
        register2 = operands[1]
        label = operands[2].strip()  
        
       
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
            
            if self.registers[register1] < self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def bgt(self, operands):
        register1 = operands[0]
        register2 = operands[1]
        label = operands[2].strip() 
        
        
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
            
            if self.registers[register1] > self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def ble(self, operands):
        register1 = operands[0]
        register2 = operands[1]
        label = operands[2].strip() 
        
       
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
           
            if self.registers[register1] <= self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def bge(self, operands):
        register1 = operands[0]
        register2 = operands[1]
        label = operands[2].strip() 
        
       
        if label in self.loop_addresses:
            label_address = self.loop_addresses[label]
            
           
            if self.registers[register1] >= self.registers[register2]:
                self.pc = label_address
        else:
            print(f"Hata: {label} etiketi tanımlanmamış.")

    def li(self, operands):
     register_name = operands[0].strip() 
     immediate_value = int(operands[1].strip())  

   
     if register_name in self.registers:
        self.registers[register_name] = immediate_value
        print(f"{register_name} register'ına {immediate_value} değeri yazıldı.")
     else:
        print(f"Hata: {register_name} geçersiz bir register adı.")
        
    def addi(self, operands):
     destination_register = operands[0].strip() 
     source_register = operands[1].strip()      
     immediate_value = int(operands[2].strip())  

   
     if source_register in self.registers:
        source_value = self.registers[source_register]
        result = source_value + immediate_value

       
        if destination_register in self.registers:
            self.registers[destination_register] = result
            print(f"{immediate_value} değeri {source_register} register'ından alındı ve {result} değeri {destination_register} register'ına yazıldı.")
        else:
            print(f"Hata: {destination_register} geçersiz bir register adı.")
     else:
        print(f"Hata: {source_register} geçersiz bir register adı.")
        
    def subi(self, operands):
     destination_register = operands[0].strip()   
     source_register = operands[1].strip()       
     immediate_value = int(operands[2].strip())   

    
     if source_register in self.registers:
        source_value = self.registers[source_register]
        result = source_value - immediate_value

      
        if destination_register in self.registers:
            self.registers[destination_register] = result
            print(f"{immediate_value} değeri {source_register} register'ından çıkarıldı ve {result} değeri {destination_register} register'ına yazıldı.")
        else:
            print(f"Hata: {destination_register} geçersiz bir register adı.")
     else:
        print(f"Hata: {source_register} geçersiz bir register adı.")
        
    def xor(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        result = value_1 ^ value_2
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının XOR işlemi sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def nor(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     register_name_2 = operands[2].strip()

     if register_name_1 in self.registers and register_name_2 in self.registers:
        value_1 = self.registers[register_name_1]
        value_2 = self.registers[register_name_2]
        result = ~(value_1 | value_2)
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} ve {register_name_2} registerlarının NOR işlemi sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def jr(self, operands):
     register_name = operands[0].strip()
     if register_name in self.registers:
        address = self.registers[register_name]
        print(f"Program counter, {register_name} registerındaki adres ({address}) ile güncellendi.")
     else:
        print("Hata: Geçersiz register adı.")

    def andi(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     value = int(operands[2].strip())

     if register_name_1 in self.registers:
        value_1 = self.registers[register_name_1]
        result = value_1 & value
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} registerı ile {value} değerinin AND işlemi sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

    def ori(self, operands):
     register_name_result = operands[0].strip()
     register_name_1 = operands[1].strip()
     value = int(operands[2].strip())

     if register_name_1 in self.registers:
        value_1 = self.registers[register_name_1]
        result = value_1 | value
        if register_name_result in self.registers:
            self.registers[register_name_result] = result
            print(f"{register_name_result} register'ına {register_name_1} registerı ile {value} değerinin OR işlemi sonucu olan {result} değeri yazıldı.")
        else:
            print(f"Hata: {register_name_result} geçersiz bir register adı.")
     else:
        print("Hata: Geçersiz register adı.")

     
    
    def loop(self, operands):
        label = operands[0].strip()
        address = self.pc  
        self.loop_addresses[label] = address
        self.registers["$ra"] = address
 
     
     
    registers = {
            "$zero": 0x00000000,  
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
        
        self.registers = updated_registers

        
        self.register_table_updated.emit(self.registers)
     
     
    

        


