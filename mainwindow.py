import sys
from PyQt6.QtWidgets import QMainWindow, QToolBar,  QComboBox, QPushButton, QFileDialog,QWidget,QSplitter,QTableWidget


from layoutEditorWidget import LayoutEditorWidget
from tableWidget import TableWidget
from printWidget import PrintWidget

import csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
            
        self.tabWidget = TableWidget(self)

        self.layoutEditorWidget = LayoutEditorWidget(self)
        self.tabWidget.selectedDataUpdate.connect(self.layoutEditorWidget.updateData)

        self.printWidget = PrintWidget(self)        
        self.tabWidget.dataUpdate.connect(self.printWidget.updateData)
        self.layoutEditorWidget.layoutUpdate.connect(self.printWidget.updateLayoutData)
        
        self.initUI()

        

    def initUI(self):

        central=QSplitter(self)
        central.addWidget(self.tabWidget)
        central.addWidget(self.layoutEditorWidget)
        central.addWidget(self.printWidget)
 

        self.setCentralWidget(central)
        self.setWindowTitle("TablePrint")





