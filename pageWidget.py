from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPaintEvent, QTextOption,QFont,QColor
from PyQt6.QtCore import Qt,QRectF

from layoutWidget import LayoutWidget

class PageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data=[]
        self.layoutData={}
    
    def mm2p(self,mm, p,x):
        if x=='x':
            return mm*p.device().logicalDpiX()/25.4
        
        return mm*p.device().logicalDpiY()/25.4

    def paintEvent(self, event: QPaintEvent):      
        p = QPainter(self)
        scale=0.5
        p.scale(scale,scale)
        self.setMinimumSize(int(scale*self.mm2p(self.pageWidth,p,'x'))+1, int(scale*self.mm2p(self.pageHeight,p,'y'))+1)
        self.draw(p)

    def draw(self,p):
        #draw page background
        
        p.setBrush(Qt.GlobalColor.white)
        p.drawRect(0, 0, int(self.mm2p(self.pageWidth,p,'x')), int(self.mm2p(self.pageHeight,p,'y')))

        for r in range(self.rowCount):
            for c in range(self.columnCount):
                x=self.offsetX+c*(self.pageWidth-2*self.offsetX)/self.columnCount
                y=self.offsetY+r*(self.pageHeight-2*self.offsetY)/self.rowCount
                i=self.page*self.rowCount*self.columnCount+r*self.columnCount+c
                data=[]
                if i<len(self.data):
                    data=self.data[i]
                w=LayoutWidget(None)
                w.updateLayoutData(self.layoutData)
                w.updateData(data)
                w.draw(p,x,y)

                

    def setRowCount(self,rowCount):
        self.rowCount=rowCount
        self.update()

    def setColumnCount(self,columnCount):
        self.columnCount=columnCount
        self.update()
    
    def setOffsetX(self,x):
        self.offsetX=x
        self.update()

    def setOffsetY(self,y):
        self.offsetY=y
        self.update()

    def setPageSize(self,w,h):
        self.pageWidth=w
        self.pageHeight=h
        self.update()

    def setPage(self,page):
        self.page=page
        self.update()

    def updateData(self,data):
        self.data=data
        self.update()
    
    def updateLayoutData(self,layoutData):
        self.layoutData=layoutData
        self.update()
     

     
