import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,QFileDialog,QGroupBox,QFontComboBox,QSpinBox,QScrollArea
from PyQt6.QtGui import QFont 
from PyQt6.QtCore import Qt,pyqtSignal
from layoutWidget import LayoutWidget
import json

class TextComponentEditor(QWidget):
    dataUpdate = pyqtSignal(dict)
    def __init__(self,componentData,parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        posLine=QHBoxLayout(self)
        fontLine=QHBoxLayout(self)

        self.xe=QSpinBox(self)
        self.xe.setValue(componentData['x'])
        self.xe.valueChanged.connect(self.onDataChange)
        posLine.addWidget(self.xe)

        self.ye=QSpinBox(self)
        self.ye.setValue(componentData['y'])        
        self.ye.valueChanged.connect(self.onDataChange)
        posLine.addWidget(self.ye)

        self.w=QSpinBox(self)
        self.w.setValue(componentData['w'])        
        self.w.valueChanged.connect(self.onDataChange)
        posLine.addWidget(self.w)

        self.h=QSpinBox(self)
        self.h.setValue(componentData['h'])
        self.h.valueChanged.connect(self.onDataChange)
        posLine.addWidget(self.h)

        self.fontName=QFontComboBox(self)
        self.fontName.setCurrentFont(QFont(componentData['fontName']))
        self.fontName.currentFontChanged.connect(self.onDataChange)
        fontLine.addWidget(self.fontName)

        self.fontSize=QSpinBox(self)
        self.fontSize.setValue(componentData['fontSize'])
        self.fontSize.valueChanged.connect(self.onDataChange)
        fontLine.addWidget(self.fontSize)

        self.fontWeight=QSpinBox(self)
        self.fontWeight.setValue(componentData['fontWeight'])
        self.fontWeight.valueChanged.connect(self.onDataChange)
        fontLine.addWidget(self.fontWeight)

        self.fontItalic=QSpinBox(self)
        self.fontItalic.setValue(componentData['fontItalic'])
        self.fontItalic.valueChanged.connect(self.onDataChange)
        fontLine.addWidget(self.fontItalic)
        
        self.textEdit = QLineEdit(componentData['text'],self)        
        self.textEdit.textChanged.connect(self.onDataChange)
        posLine.addWidget(self.textEdit)
        posLine.addStretch(1)
        
        layout.addLayout(posLine)
        layout.addLayout(fontLine)
        

        self.setLayout(layout)

    def onDataChange(self):
        self.dataUpdate.emit(
            self.getData())
        
    def getData(self):
        return {
                "type":"text",
                "text":self.textEdit.text(),
                "x":self.xe.value(),
                "y":self.ye.value(),
                "w":self.w.value(),
                "h":self.h.value(),
                "fontName":self.fontName.currentFont().family(),
                "fontSize":self.fontSize.value(),
                "fontWeight":self.fontWeight.value(),
                "fontItalic":self.fontItalic.value(),
                
            }

class ImgComponentEditor(QWidget):
    dataUpdate = pyqtSignal(dict)
    def __init__(self,componentData,parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.xe=QSpinBox(self)
        self.xe.setValue(componentData['x'])
        self.xe.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.xe)

        self.ye=QSpinBox(self)
        self.ye.setValue(componentData['y'])        
        self.ye.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.ye)

        self.w=QSpinBox(self)
        self.w.setValue(componentData['w'])        
        self.w.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.w)

        self.h=QSpinBox(self)
        self.h.setValue(componentData['h'])
        self.h.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.h)

        self.imgSrc = QLineEdit(componentData['imgSrc'],self)        
        self.imgSrc.textChanged.connect(self.onDataChange)
        layout.addWidget(self.imgSrc)
        layout.addStretch(1)
        
        self.setLayout(layout)

    def onDataChange(self):
        self.dataUpdate.emit(
            self.getData())
        
    def getData(self):
        return {
                "type":"img",
                "imgSrc":self.imgSrc.text(),
                "x":self.xe.value(),
                "y":self.ye.value(),
                "w":self.w.value(),
                "h":self.h.value()
            }
    
class QRcodeComponentEditor(QWidget):
    dataUpdate = pyqtSignal(dict)
    def __init__(self,componentData,parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.xe=QSpinBox(self)
        self.xe.setValue(componentData['x'])
        self.xe.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.xe)

        self.ye=QSpinBox(self)
        self.ye.setValue(componentData['y'])        
        self.ye.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.ye)

        self.w=QSpinBox(self)
        self.w.setValue(componentData['w'])        
        self.w.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.w)

        self.h=QSpinBox(self)
        self.h.setValue(componentData['h'])
        self.h.valueChanged.connect(self.onDataChange)
        layout.addWidget(self.h)

        self.data = QLineEdit(componentData['data'],self)        
        self.data.textChanged.connect(self.onDataChange)
        layout.addWidget(self.data)
        layout.addStretch(1)
        
        self.setLayout(layout)

    def onDataChange(self):
        self.dataUpdate.emit(
            self.getData())
        
    def getData(self):
        return {
                "type":"qrcode",
                "data":self.data.text(),
                "x":self.xe.value(),
                "y":self.ye.value(),
                "w":self.w.value(),
                "h":self.h.value()
            }

class ComponentEditor(QWidget):
    dataUpdate = pyqtSignal(dict)
    deleteComponent = pyqtSignal(int)
    moveUpComponent = pyqtSignal(int)
    moveDownComponent = pyqtSignal(int)
    def __init__(self,componetData,index,parent=None):
        super().__init__(parent)
        self.index=index
        self.editor=None
        if componetData['type']=='text':
            self.editor=TextComponentEditor(componetData,self)            
        
        if componetData['type']=='img':
            self.editor=ImgComponentEditor(componetData,self)

        if componetData['type']=='qrcode':
            self.editor=QRcodeComponentEditor(componetData,self)

        if self.editor is not None:            
            self.editor.dataUpdate.connect(self.subdataUpdate)

        box=QGroupBox(self)
        layout = QVBoxLayout(self)
        layout.addWidget(box)

        boxLayout = QVBoxLayout(box)
        box.setLayout(boxLayout)
        boxLayout.addWidget(self.editor)
        
        buttonLine = QHBoxLayout()
        boxLayout.addLayout(buttonLine)

        removeButton = QPushButton("Del", self)
        removeButton.clicked.connect(lambda : self.deleteComponent.emit(self.index))
        buttonLine.addWidget(removeButton)

        moveUpButton = QPushButton("Up", self)
        moveUpButton.clicked.connect(lambda : self.moveUpComponent.emit(self.index))
        buttonLine.addWidget(moveUpButton)

        moveDownButton = QPushButton("Down", self)
        moveDownButton.clicked.connect(lambda : self.moveDownComponent.emit(self.index))
        buttonLine.addWidget(moveDownButton)

        self.setLayout(layout)


    def subdataUpdate(self,data):
        self.dataUpdate.emit(data)

    def getData(self):
        if self.editor is not None:
            return self.editor.getData()
        return {}


class LayoutEditorWidget(QWidget):
    layoutUpdate = pyqtSignal(dict)

    def __init__(self,parent=None):
        super().__init__(parent)

        self.layoutData={ "w":100,"h":100,"componets":[] }
        self.filename=""

        layout = QVBoxLayout()

        self.layoutWidget = LayoutWidget(self)
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutWidget.setMinimumSize(100, 100)

        layout.addWidget(self.layoutWidget)

  

        #layout.addStretch(1)
        sizeLine = QHBoxLayout()

        self.widthW=QSpinBox(self)
        self.widthW.setValue(self.layoutData['w'])
        self.widthW.setMinimum(1)
        self.widthW.setMaximum(1000)
        self.widthW.valueChanged.connect(self.setWidth)
        sizeLine.addWidget(self.widthW)

        self.heightW=QSpinBox(self)
        self.heightW.setValue(self.layoutData['h'])
        self.heightW.setMinimum(1)
        self.heightW.setMaximum(1000)
        self.heightW.valueChanged.connect(self.setHeight)
        sizeLine.addWidget(self.heightW)

        layout.addLayout(sizeLine)

        

        self.components=QWidget(self)
        self.componentsLayout=QVBoxLayout(self.components)
        self.components.setLayout(self.componentsLayout)
        #layout.addWidget(self.components)
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.components)

        layout.addWidget(scrollArea)

        buttonLine = QHBoxLayout()        
            
        openButton = QPushButton("Open", self)
        buttonLine.addWidget(openButton)
        openButton.clicked.connect(self.openFile)

        saveButton = QPushButton("Save", self)
        buttonLine.addWidget(saveButton)
        saveButton.clicked.connect(self.saveFile)

        addTextButton = QPushButton("Add Text", self)
        buttonLine.addWidget(addTextButton)
        addTextButton.clicked.connect(self.addTextComponent)

        addImgButton = QPushButton("Add Img", self)
        buttonLine.addWidget(addImgButton)
        addImgButton.clicked.connect(self.addImgComponent)

        addQRButton = QPushButton("Add QR", self)
        buttonLine.addWidget(addQRButton)
        addQRButton.clicked.connect(self.addQRComponent)

        layout.addLayout(buttonLine)

        self.setLayout(layout)
        self.buildEditor()

    def buildEditor(self):
        #clean up old editors
        for i in reversed(range(self.componentsLayout.count())):
            widget = self.componentsLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        for i in range(len(self.layoutData['componets'])):
            editor=ComponentEditor(self.layoutData['componets'][i],i,self.components)
            editor.dataUpdate.connect(self.updateEditorData)
            editor.deleteComponent.connect(self.removeComponent)
            editor.moveUpComponent.connect(self.moveUpComponent)
            editor.moveDownComponent.connect(self.moveDownComponent)
            self.componentsLayout.addWidget(editor)
        self.componentsLayout.addStretch(1)

    def removeComponent(self,i):
        if i>=0 and i<len(self.layoutData['componets']):
            self.layoutData['componets'].pop(i)
            self.layoutWidget.updateLayoutData(self.layoutData)
            self.layoutUpdate.emit(self.layoutData)
            self.buildEditor()

    def moveUpComponent(self,i):
        if i>0 and i<len(self.layoutData['componets']):
            self.layoutData['componets'][i],self.layoutData['componets'][i-1]=self.layoutData['componets'][i-1],self.layoutData['componets'][i]
            self.layoutWidget.updateLayoutData(self.layoutData)
            self.layoutUpdate.emit(self.layoutData)
            self.buildEditor()
    
    def moveDownComponent(self,i):
        if i>=0 and i<len(self.layoutData['componets'])-1:
            self.layoutData['componets'][i],self.layoutData['componets'][i+1]=self.layoutData['componets'][i+1],self.layoutData['componets'][i]
            self.layoutWidget.updateLayoutData(self.layoutData)
            self.layoutUpdate.emit(self.layoutData)
            self.buildEditor()
            
        
    def addTextComponent(self):
        self.layoutData['componets'].append({
                "type":"text",
                "text":"New Component",
                "x":10,
                "y":10,
                "w":50,
                "h":50,
                "fontName":"Arial",
                "fontSize":12,
                "fontWeight":0,
                "fontItalic":0
            })
        self.buildEditor()
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def addImgComponent(self):
        self.layoutData['componets'].append({
                "type":"img",
                "imgSrc":"",
                "x":10,
                "y":10,
                "w":50,
                "h":50,                
            })
        self.buildEditor()
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def addQRComponent(self):
        self.layoutData['componets'].append({
                "type":"qrcode",
                "data":"",
                "x":10,
                "y":10,
                "w":50,
                "h":50,                
            })
        self.buildEditor()
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def setWidth(self,w):
        self.layoutData['w']=w
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def setHeight(self,h):
        self.layoutData['h']=h
        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def updateEditorData(self,data):
        self.layoutData['componets']=[]
        for i in range(self.componentsLayout.count()):
            widget = self.componentsLayout.itemAt(i).widget()
            if widget is not None:
                self.layoutData['componets'].append(widget.getData())


        self.layoutWidget.updateLayoutData(self.layoutData)
        self.layoutUpdate.emit(self.layoutData)

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open Layout File", "", "Layout Files (*.layout);;All Files (*)")
        if not filename[0]:
            print("No file selected")
            return
        
        with open(filename[0], 'r') as file:
            data = file.read()
            self.layoutData = json.loads(data)
            self.layoutWidget.updateLayoutData(self.layoutData)
            self.layoutUpdate.emit(self.layoutData)
            self.filename=filename[0]
            self.heightW.setValue(self.layoutData['h'])
            self.widthW.setValue(self.layoutData['w'])
            self.buildEditor()

    def saveFile(self):
        
        filename = QFileDialog.getSaveFileName(self, "Save Layout File", "", "Layout Files (*.layout);;All Files (*)")
        if not filename[0]:
            print("No file selected")
            return
        self.filename=filename[0]
        
        with open(self.filename, 'w') as file:
            json.dump(self.layoutData, file, indent=4)
        
    def updateData(self,data):
        self.layoutWidget.updateData(data)
