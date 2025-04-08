import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,QFileDialog,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QAction,QPainter,QPageSize
from PyQt6.QtCore import Qt,pyqtSignal
from layoutWidget import LayoutWidget
import csv

class TableWidget(QWidget):
    selectedDataUpdate = pyqtSignal(list)
    dataUpdate = pyqtSignal(list)

    def __init__(self,parent=None):
        super().__init__(parent)        

        self.filename=""

        layout = QVBoxLayout()

        self.tabWidget = QTableWidget(self)
        self.tabWidget.setColumnCount(2)
        self.tabWidget.setRowCount(3)
        self.tabWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabWidget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tabWidget.itemSelectionChanged.connect(self.onRowSelect)
        self.tabWidget.cellChanged.connect(self.onRowSelect)
        self.tabWidget.cellChanged.connect(self.onDataChange)
        layout.addWidget(self.tabWidget)

        #layout.addStretch(1)
        buttonLine1 = QHBoxLayout()

        addRowButton = QPushButton("Add Row", self)
        buttonLine1.addWidget(addRowButton)
        addRowButton.clicked.connect(lambda: self.tabWidget.insertRow(self.tabWidget.rowCount()))

        addColButton = QPushButton("Add Column", self)
        buttonLine1.addWidget(addColButton)
        addColButton.clicked.connect(lambda: self.tabWidget.insertColumn(self.tabWidget.columnCount()))

        layout.addLayout(buttonLine1)

        buttonLine = QHBoxLayout()        
        
        openButton = QPushButton("Import", self)
        buttonLine.addWidget(openButton)
        openButton.clicked.connect(self.importTable)

        saveButton = QPushButton("Export", self)
        buttonLine.addWidget(saveButton)
        saveButton.clicked.connect(self.exportTable)

        layout.addLayout(buttonLine)
        
        self.setLayout(layout)

    def importTable(self):
        filename = QFileDialog.getOpenFileName(self, "Open Table File", "", "Table Files (*.csv);;All Files (*)")
        if not filename[0]:
            print("No file selected")
            return
        
        with open(filename[0], 'r',encoding="utf-8") as file:
            data = file.read()
                        
            reader = csv.reader(data.splitlines(), delimiter=';')
            self.tabWidget.setRowCount(0)
            self.tabWidget.setColumnCount(0)
            for i, row in enumerate(reader):
                self.tabWidget.insertRow(i)
                for j, value in enumerate(row):
                    if j >= self.tabWidget.columnCount():
                        self.tabWidget.insertColumn(j)
                    self.tabWidget.setItem(i, j, QTableWidgetItem(value))

    def exportTable(self):
        filename = QFileDialog.getSaveFileName(self, "Save Table File", "", "Table Files (*.csv);;All Files (*)")
        if not filename[0]:
            print("No file selected")
            return
        
        with open(filename[0], 'w') as file:
            writer = csv.writer(file,delimiter=';')
            for i in range(self.tabWidget.rowCount()):
                row = []
                for j in range(self.tabWidget.columnCount()):
                    item = self.tabWidget.item(i, j)
                    if item is not None:
                        row.append(item.text())
                    else:
                        row.append("")
                writer.writerow(row)

    def onRowSelect(self):
        selected_items = self.tabWidget.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            data=[]
            for i in range(self.tabWidget.columnCount()):
                item = self.tabWidget.item(row, i)
                if item is not None:
                    data.append(item.text())
                else:
                    data.append("")
            self.selectedDataUpdate.emit(data)

    def onDataChange(self):
        data=[]
        for row in range(self.tabWidget.rowCount()):
            row_data=[]
            for i in range(self.tabWidget.columnCount()):
                item = self.tabWidget.item(row, i)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        self.dataUpdate.emit(data)
            

            
