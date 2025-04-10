from PyQt6.QtWidgets import QWidget,QVBoxLayout, QHBoxLayout,QPushButton,QComboBox,QSpinBox,QLabel,QFileDialog,QCheckBox
from PyQt6.QtGui import QPainter, QPaintEvent, QTextOption,QFont,QColor
from PyQt6.QtCore import Qt,QRectF
from PyQt6.QtGui import QAction,QPainter,QPageSize
from PyQt6.QtPrintSupport import QPrinter,QPrinterInfo

from pageWidget import PageWidget

class PrintWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.printers=[]
        self.printerCombo = QComboBox(self)

        layout = QVBoxLayout()

        self.pageWidget = PageWidget(self)
        self.pageWidget.setMinimumSize(100, 100)
        self.pageWidget.setPage(0)
        self.pageWidget.setRowCount(2)
        self.pageWidget.setColumnCount(2)
        self.pageWidget.setOffsetX(10)
        self.pageWidget.setOffsetY(10)
        self.pageWidget.setPageSize(210,297) # A4 size in mm

        layout.addWidget(self.pageWidget)

        layout.addStretch(1)                
        buttonLine1 = QHBoxLayout() 

        rowL=QLabel("Rows:", self)
        buttonLine1.addWidget(rowL)
        rowSpin = QSpinBox(self)
        rowSpin.setMinimum(1)
        #rowSpin.setMaximum(10)
        rowSpin.setValue(2)
        rowSpin.valueChanged.connect(self.pageWidget.setRowCount)
        buttonLine1.addWidget(rowSpin)

        buttonLine1.addSpacing(10)

        colL=QLabel("Columns:", self)
        buttonLine1.addWidget(colL)
        colSpin = QSpinBox(self)
        colSpin.setMinimum(1)
        #colSpin.setMaximum(10)
        colSpin.setValue(2)
        colSpin.valueChanged.connect(self.pageWidget.setColumnCount)
        buttonLine1.addWidget(colSpin)

        buttonLine1.addSpacing(10)

        pageL=QLabel("Page:", self)
        buttonLine1.addWidget(pageL)
        pageSpin = QSpinBox(self)
        pageSpin.setMinimum(0)
        #pageSpin.setMaximum(10)
        pageSpin.setValue(0)
        pageSpin.valueChanged.connect(self.pageWidget.setPage)
        buttonLine1.addWidget(pageSpin)
        buttonLine1.addSpacing(10)

        buttonLine1.addStretch(1)
        layout.addLayout(buttonLine1)

        buttonLine2 = QHBoxLayout()

        offsetXL=QLabel("Offset X:", self)
        buttonLine2.addWidget(offsetXL)
        offsetXSpin = QSpinBox(self)
        offsetXSpin.setMinimum(0)
        #offsetXSpin.setMaximum(100)
        offsetXSpin.setValue(10)
        offsetXSpin.valueChanged.connect(self.pageWidget.setOffsetX)
        buttonLine2.addWidget(offsetXSpin)
        buttonLine2.addSpacing(10)

        offsetYL=QLabel("Offset Y:", self)
        buttonLine2.addWidget(offsetYL)
        offsetYSpin = QSpinBox(self)
        offsetYSpin.setMinimum(0)
        #offsetYSpin.setMaximum(100)
        offsetYSpin.setValue(10)
        offsetYSpin.valueChanged.connect(self.pageWidget.setOffsetY)
        buttonLine2.addWidget(offsetYSpin)
        buttonLine2.addSpacing(10)

        self.allPagesCheckBox = QCheckBox("All Pages", self)
        self.allPagesCheckBox.setChecked(True)
        buttonLine2.addWidget(self.allPagesCheckBox)
        

        buttonLine2.addStretch(1)   
        layout.addLayout(buttonLine2)

        buttonLine = QHBoxLayout()        
        buttonLine.addWidget(self.printerCombo)
        
        refreshButton = QPushButton("Refresh", self)
        buttonLine.addWidget(refreshButton)
        refreshButton.clicked.connect(self.refreshPrinters)

        printButton = QPushButton("Print", self)
        buttonLine.addWidget(printButton)
        printButton.clicked.connect(self.printLayout)

        pdfButton = QPushButton("Print PDF", self)
        buttonLine.addWidget(pdfButton)
        pdfButton.clicked.connect(self.printLayoutPDF)

        layout.addLayout(buttonLine)
        
        self.setLayout(layout)

        self.refreshPrinters()
    

    def mm2p(self,mm, p,x):
        if x=='x':
            return mm*p.device().logicalDpiX()/25.4
        
        return mm*p.device().logicalDpiY()/25.4

    def printLayoutPDF(self):
        filename= QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf);;All Files (*)")
        if not filename[0]:
            print("No file selected")
            return

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)        
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setFullPage(True)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(filename[0])

        self.doPrint(printer)     

    def printLayout(self):
        selected_printer = None
        for pi in self.printers:
            if self.printerCombo.currentText()==pi.printerName():
                selected_printer = pi
                break

        if selected_printer is None:
            print("No printer selected")
            return

        printer = QPrinter(selected_printer,QPrinter.PrinterMode.HighResolution)        
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setFullPage(True)
        printer.setOutputFormat(QPrinter.OutputFormat.NativeFormat)
        
        self.doPrint(printer)
    
    def doPrint(self,printer):
        
        painter = QPainter(printer)

        if self.allPagesCheckBox.isChecked():
            pageCoutn = int(len(self.pageWidget.data)/(self.pageWidget.columnCount*self.pageWidget.rowCount))+1
    
            for page in range(pageCoutn):
                if page>0:
                    printer.newPage()
                self.pageWidget.setPage(page)
                self.pageWidget.draw(painter)    
        else:
            self.pageWidget.draw(painter)
                        
        painter.end()

    def refreshPrinters(self):
        self.printerCombo.clear()
        self.printers = QPrinterInfo.availablePrinters()
        for printer in self.printers:
            self.printerCombo.addItem(printer.printerName())

    def updateData(self,data):
        self.pageWidget.updateData(data)        

    def updateLayoutData(self,layoutData):
        self.pageWidget.updateLayoutData(layoutData)        

