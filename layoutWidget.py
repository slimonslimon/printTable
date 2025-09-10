from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPaintEvent, QTextOption,QFont,QColor,QImage
from PyQt6.QtCore import Qt,QRectF

import re
import qrcode

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

        p.setPen(QColor(0, 0, 0))
        p.setBrush(QColor(255, 255, 255))
        p.drawRect(int(xp), int(yp), int(w), int(h))

        for c in self.layoutData['componets']:
            if c['type']=='text':
                textOptions = QTextOption()
                textOptions.setAlignment(Qt.AlignmentFlag.AlignLeft)
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
                if img.isNull():
                    continue
                if img.width()==0 or img.height()==0:
                    continue
                w=c['w']
                h=c['h']
                xo=0
                yo=0
                if c['center']:
                    if img.width()/img.height()>c['w']/c['h']:
                        h=img.height()*c['w']/img.width()
                        w=c['w']
                        xo=0;
                        yo=(c['h']-h)/2
                    else:
                        w=img.width()*c['h']/img.height()
                        h=c['h']
                        xo=(c['w']-w)/2
                        yo=0
        
                #img=img.scaled(int(self.mm2p(c['w'],p,'x')),int(self.mm2p(c['h'],p,'y')),Qt.AspectRatioMode.KeepAspectRatio)
                if c['frame']:
                    p.drawRect(QRectF(self.mm2p(c['x']+x,p,'x'),
                                    self.mm2p(c['y']+y,p,'y'),
                                    self.mm2p(c['w'],p,'x'),
                                    self.mm2p(c['h'],p,'h')))
                p.drawImage(QRectF(self.mm2p(c['x']+xo+x,p,'x'),
                                  self.mm2p(c['y']+yo+y,p,'y'),
                                  self.mm2p(w,p,'x'),
                                  self.mm2p(h,p,'h')),
                           img)
                
            if c['type']=='qrcode':
                text=self.processText(c['data'])
                if(text==""):
                    continue
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(text)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img.save('qrcode.png')
                img = QImage('qrcode.png')
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

