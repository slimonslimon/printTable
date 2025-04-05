from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPaintEvent, QTextOption,QFont,QColor,QImage
from PyQt6.QtCore import Qt,QRectF

import re

class LayoutWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layoutData={ "w":100,"h":100,"componets":[] }
        self.data=[]
    

    def mm2p(self,mm, p,x):
        if x=='x':
            return mm*p.device().logicalDpiX()/25.4
        
        return mm*p.device().logicalDpiY()/25.4


    def paintEvent(self, event: QPaintEvent):      
        p = QPainter(self)
        self.setMinimumSize(int(self.mm2p(self.layoutData['w'],p,'x'))+1, int(self.mm2p(self.layoutData['h'],p,'y'))+1)
        self.draw(p)

    def processText(self,intext):
        text=intext
        for match in re.findall(r'\$(\d+)', intext):                    
            number = int(match)
            if number <= len(self.data) and number > 0:
                text = text.replace('$'+str(number), str(self.data[number-1]))
            else:
                text = text.replace('$'+str(number), '')
        return text

    def draw(self,p,x=0,y=0):
        if(self.layoutData=={}):
            return

        w=self.mm2p(self.layoutData['w'],p,'x')
        h=self.mm2p(self.layoutData['h'],p,'y')
        
        xp=self.mm2p(x,p,'x')
        yp=self.mm2p(y,p,'y')

        p.setBrush(Qt.GlobalColor.white)
        p.drawRect(int(xp), int(yp), int(w), int(h))

        for c in self.layoutData['componets']:
            if c['type']=='text':
                textOptions = QTextOption()
                textOptions.setAlignment(Qt.AlignmentFlag.AlignJustify)
                textOptions.setWrapMode(QTextOption.WrapMode.WordWrap)
                font = QFont(c['fontName'], c['fontSize'], c['fontWeight'], c['fontItalic'])
                p.setFont(font)
                #p.setPen(QColor.rgb(c['font_color'][0],c['font_color'][1],c['font_color'][2]))

                text=self.processText(c['text'])
                p.drawText(QRectF(self.mm2p(c['x']+x,p,'x'),
                                  self.mm2p(c['y']+y,p,'y'),
                                  self.mm2p(c['w'],p,'x'),
                                  self.mm2p(c['h'],p,'h')),
                           text,
                           textOptions)
            
            if c['type']=='img':
                text=self.processText(c['imgSrc'])
                if(text==""):
                    continue
                img = QImage(text)
                #img=img.scaled(int(self.mm2p(c['w'],p,'x')),int(self.mm2p(c['h'],p,'y')),Qt.AspectRatioMode.KeepAspectRatio)
                p.drawImage(QRectF(self.mm2p(c['x']+x,p,'x'),
                                  self.mm2p(c['y']+y,p,'y'),
                                  self.mm2p(c['w'],p,'x'),
                                  self.mm2p(c['h'],p,'h')),
                           img)


    def updateData(self,data):
        self.data=data
        self.update()

    def updateLayoutData(self,layoutData):
        self.layoutData=layoutData        
        self.update()

