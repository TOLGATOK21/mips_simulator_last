from PyQt5 import QtCore, QtGui, QtWidgets
from data_memory import DataMemory
from instruction_memory import InstructionMemory
from PyQt5.QtCore import QObject, pyqtSignal
import traceback
from PyQt5.QtWidgets import QFileDialog




import qdarkstyle



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Diğer sınıflardan nesneler burda.
        self.data_memory = DataMemory()
        self.instruction_memory =InstructionMemory()  
        #--------------------------------
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1332, 779)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #--------------REGİSTERS-------------------------------------------
        self.tab_register = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_register.setGeometry(QtCore.QRect(10, 100, 411, 611))
        self.tab_register.setObjectName("tab_register")
        self.tab_register1 = QtWidgets.QWidget()
        self.tab_register1.setObjectName("tab_register1")
        self.register_table = QtWidgets.QTableWidget(self.tab_register1)
        self.register_table.setGeometry(QtCore.QRect(0, 0, 401, 581))
        self.register_table.setObjectName("register_table")
        self.register_table.setColumnCount(2)
        self.register_table.setRowCount(35)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.register_table.setItem(0, 2, item)
        self.tab_register.addTab(self.tab_register1, "")
        self.populate_register_table_gui()
       

        #-------------------------------------------------------------------
        self.tabWidget_3 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_3.setGeometry(QtCore.QRect(950, 80, 361, 631))
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_memory = QtWidgets.QWidget()
        self.tab_memory.setObjectName("tab_memory")
        #-----------------DATA MEMORY TABLE-------------------------------------
        self.data_memory = DataMemory()
        self.data_memory_table = QtWidgets.QTableWidget(self.tab_memory)
        self.data_memory_table.setGeometry(QtCore.QRect(0, 20, 351, 251))
        self.data_memory_table.setObjectName("data_memory_table")
        self.data_memory_table.setColumnCount(2)
        self.data_memory_table.setRowCount(256)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.data_memory_table.setItem(0, 1, item)
        self.populate_memory_table(self.data_memory_table)
        
        self.data_memory.memory_updated.connect(self.update_table)
        self.update_table()
       
        #-----------INSTRUCTION TABLE------------------------------------------------------
        self.instruction_memory_table = QtWidgets.QTableWidget(self.tab_memory)
        self.instruction_memory_table.setGeometry(QtCore.QRect(0, 350, 351, 251))
        self.instruction_memory_table.setObjectName("instruction_memory_table")
        self.instruction_memory_table.setColumnCount(4)
        self.instruction_memory_table.setRowCount(256)
        
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        
        self.instruction_memory_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.instruction_memory_table.setItem(0, 1, item)
        self.populate_instruction_memory_table(self.instruction_memory_table)
        
        self.instruction_memory.instruction_memory_updated.connect(self.update_table_instruction)
        self.update_table_instruction()
        self.instruction_memory.register_table_updated.connect(self.update_table_registers)
       
        self.update_table_registers() 
        self.label_3 = QtWidgets.QLabel(self.tab_memory)
        self.label_3.setGeometry(QtCore.QRect(110, 320, 141, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_memory)
        self.label_4.setGeometry(QtCore.QRect(120, 0, 111, 16))
        self.label_4.setObjectName("label_4")
        self.tabWidget_3.addTab(self.tab_memory, "")
        

        
        #BUTTONLAR-----------------------------------------------------------
        self.assembleButton = QtWidgets.QPushButton(self.centralwidget)
        self.assembleButton.setGeometry(QtCore.QRect(20, 20, 101, 41))
        self.assembleButton.setObjectName("assembleButton")
        self.stepButton = QtWidgets.QPushButton(self.centralwidget)
        self.stepButton.setGeometry(QtCore.QRect(260, 20, 101, 41))
        self.stepButton.setObjectName("stepButton")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(140, 20, 101, 41))
        self.runButton.setObjectName("runButton")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(380, 20, 101, 41))
        self.saveButton.setObjectName("saveButton")
        self.code_input = Qsci.QsciScintilla(self.centralwidget)
        self.code_input.setGeometry(QtCore.QRect(450, 120, 471, 341))
        self.code_input.setToolTip("")
        self.code_input.setWhatsThis("")
        self.code_input.setObjectName("code_input")
        self.mips_messages = QtWidgets.QTabWidget(self.centralwidget)
        self.mips_messages.setGeometry(QtCore.QRect(450, 470, 471, 241))
        self.mips_messages.setObjectName("mips_messages")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser_output = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_output.setGeometry(QtCore.QRect(0, 0, 461, 211))
        self.textBrowser_output.setObjectName("textBrowser_output")
       
        
       

      

        
        self.mips_messages.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textBrowser_output_run = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_output_run.setGeometry(QtCore.QRect(0, 0, 461, 211))
        self.textBrowser_output_run.setObjectName("textBrowser_output_run")
        self.mips_messages.addTab(self.tab_2, "")
       
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(650, 100, 91, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1170, 20, 101, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1332, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_register.setCurrentIndex(0)
        self.mips_messages.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.toggle_theme)
        self.runButton.clicked.connect(self.data_process)
        self.stepButton.clicked.connect(self.instruction_memory.next_step)
        self.assembleButton.clicked.connect(self.instruction_memory.run)
        self.saveButton.clicked.connect(self.save_text)
       
        
        
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(500, 20, 101, 41))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.setText("Reset")
        self.resetButton.clicked.connect(self.reset_program)
       
        # stepButton'a tıklandığında next_step metodunu çağır
        
        self.textBrowser_output_run.setText(self.instruction_memory.syscall())
        
        self.instruction_memory.output_of_code_changed.connect(self.add_output)
        self.add_output()
        
        
        

        
    def add_output(self):
         self.textBrowser_output_run.append(str(self.instruction_memory.output_of_code))
        
    def data_process(self):
     data_lines = []
     text_lines = []

    
     code_lines = self.code_input.text().split('\n')

    
     data_section = False
     text_section = False
     for line in code_lines:
        # Boş satırları atla
        if not line.strip():
            continue
        
        if line.strip().startswith('#'):
            continue
        # Yorum kısmını ayır
        line = line.split('#')[0].strip()
        if line.strip() == '.data':
            data_section = True
            text_section = False
        elif line.strip() == '.text':
            data_section = False
            text_section = True
        elif data_section:
            data_lines.append(line)
        elif text_section:
            text_lines.append(line)

  
     for data_line in data_lines:
        self.data_memory.process_data_section(data_line)

    
     if not text_lines or text_lines[0] != 'main:':
        text_lines.insert(0, 'main:')

    
     for text_line in text_lines:
        self.instruction_memory.process_text_section(text_line)



                
    def update_table(self):
         for row, (address, value) in enumerate(self.data_memory.memory.items()):
            item_address = QtWidgets.QTableWidgetItem(hex(address))
            item_value = QtWidgets.QTableWidgetItem(format(value, '#010x'))
            self.data_memory_table.setItem(row, 0, item_address)
            self.data_memory_table.setItem(row, 1, item_value)
            
    def populate_memory_table(self, data_memory_table):
        
        row = 0
        for address, value in self.data_memory.memory.items():
            data_memory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(hex(address)))
            data_memory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(hex(value)))
            row += 1
            
    def update_table_instruction(self):
        row = 0  
        for address, instruction in self.instruction_memory.memory.items():
            opcode = instruction['opcode']
            operands = instruction['operands']
            item_address = QtWidgets.QTableWidgetItem(format(address, '#010x')) 
            item_value = QtWidgets.QTableWidgetItem("0x0000000")  
            item_source = QtWidgets.QTableWidgetItem(f"{opcode} {operands}")
            item_type = QtWidgets.QTableWidgetItem(f"{opcode}")
            self.instruction_memory_table.setItem(row, 0, item_address)
            self.instruction_memory_table.setItem(row, 1, item_value)  
            self.instruction_memory_table.setItem(row, 2, item_source)
            self.instruction_memory_table.setItem(row, 3, item_type)
            row += 1  
            
    
        

        
            
    def populate_instruction_memory_table(self, instruction_memory_table):
     address = 0x00400000
     for row in range(instruction_memory_table.rowCount()):
        
        item_address = QtWidgets.QTableWidgetItem(format(address, '#010x'))
        item_value = QtWidgets.QTableWidgetItem("0x00000000")
        instruction_memory_table.setItem(row, 0, item_address)
        instruction_memory_table.setItem(row, 1, item_value)
        
       
        address += 4
        
    def populate_register_table_gui(self):
       
        for row, (register_name, value) in enumerate(self.instruction_memory.registers.items()):
            item_name = QtWidgets.QTableWidgetItem(register_name)
            item_value = QtWidgets.QTableWidgetItem(format(value, '#010x'))
            self.register_table.setItem(row, 0, item_name)
            self.register_table.setItem(row, 1, item_value)
            
    def update_table_registers(self):
     row = 0
     for register_name, value in self.instruction_memory.registers.items():
        item_register_name = QtWidgets.QTableWidgetItem(register_name)
        item_value = QtWidgets.QTableWidgetItem(format(value, '#010x'))
        self.register_table.setItem(row, 0, item_register_name)
        self.register_table.setItem(row, 1, item_value)
        row += 1
        self.highlight_instruction_at_pc(self.instruction_memory.pc)
        
    def highlight_instruction_at_pc(self, pc):
    
     for row in range(self.instruction_memory_table.rowCount()):
        address_item = self.instruction_memory_table.item(row, 0)
        if address_item and int(address_item.text(), 16) == pc:
           
            self.instruction_memory_table.selectRow(row)
            
            self.instruction_memory_table.scrollToItem(address_item)
            break
        
    
        
#-----------------RESET------------------------------------------------------------------      
    def reset_program(self):
    
     self.app = QtWidgets.QApplication([])
     self.MainWindow = QtWidgets.QMainWindow()
     self.ui = Ui_MainWindow()
     self.ui.setupUi(self.MainWindow)
     self.MainWindow.show()
     MainWindow.close()
     self.ui.clear_tables()
     self.ui.populate_register_table_gui()
    def clear_tables(self):
     self.register_table.clearContents()
   

#-----------------RESET------------------------------------------------------------------ 

     
        
        
    
    
    

    
    
            
            
    

    






    #dark tema için        
    def toggle_theme(self):
       
        app = QtWidgets.QApplication.instance()
        current_style = app.styleSheet()
        if "QDarkStyle" in current_style:
            app.setStyleSheet("")
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
            
    def save_text(self):
    
     text = self.code_input.text()
     file_name, _ = QFileDialog.getSaveFileName(self.centralwidget, "Save File", "", "Text Files (*.txt);;All Files (*)")

     if file_name:
        with open(file_name, 'w') as file:
            file.write(text)

            
  

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.register_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.register_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.register_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        __sortingEnabled = self.register_table.isSortingEnabled()
        self.register_table.setSortingEnabled(False)
        item = self.register_table.item(0, 0)
        item.setText(_translate("MainWindow", "$zero"))
        item = self.register_table.item(0, 1)
        item.setText(_translate("MainWindow", "0x00000000"))
        self.register_table.setSortingEnabled(__sortingEnabled)
        self.tab_register.setTabText(self.tab_register.indexOf(self.tab_register1), _translate("MainWindow", "Registers"))
        item = self.data_memory_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.data_memory_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.data_memory_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "2"))
        item = self.data_memory_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "3"))
        item = self.data_memory_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Address"))
        item = self.data_memory_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        __sortingEnabled = self.data_memory_table.isSortingEnabled()
        self.data_memory_table.setSortingEnabled(False)
        item = self.data_memory_table.item(0, 0)
        item.setText(_translate("MainWindow", "0x10010000"))
        item = self.data_memory_table.item(0, 1)
        item.setText(_translate("MainWindow", "0x00000000"))
        self.data_memory_table.setSortingEnabled(__sortingEnabled)
        item = self.instruction_memory_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "0"))
        item = self.instruction_memory_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "1"))
        item = self.instruction_memory_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Address"))
        item = self.instruction_memory_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        item = self.instruction_memory_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Source"))
        item = self.instruction_memory_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Type"))
        __sortingEnabled = self.instruction_memory_table.isSortingEnabled()
        self.instruction_memory_table.setSortingEnabled(False)
        item = self.instruction_memory_table.item(0, 0)
        item.setText(_translate("MainWindow", "0x00400000"))
        item = self.instruction_memory_table.item(0, 1)
        item.setText(_translate("MainWindow", "0x00000000"))
        self.instruction_memory_table.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(_translate("MainWindow", "Instruction Memory"))
        self.label_4.setText(_translate("MainWindow", "Data Memory"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_memory), _translate("MainWindow", "Memory"))
        self.assembleButton.setText(_translate("MainWindow", "Run"))
        self.stepButton.setText(_translate("MainWindow", "Step"))
        self.runButton.setText(_translate("MainWindow", "Assemble"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.mips_messages.setTabText(self.mips_messages.indexOf(self.tab), _translate("MainWindow", "MIPS Messages"))
        self.mips_messages.setTabText(self.mips_messages.indexOf(self.tab_2), _translate("MainWindow", "Run I/O"))
        self.label.setText(_translate("MainWindow", "Code Area"))
        self.pushButton.setText(_translate("MainWindow", "Dark Theme"))
from PyQt5 import Qsci


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())