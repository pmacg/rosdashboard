from PyQt4 import QtGui #@UnresolvedImport

from modules.props import WidgetProperty
from modules.dashboardWidgets import DashboardWidget
from PyQt4.Qwt5 import Qwt

class DragKnob(DashboardWidget):
    
    MIN = 'minimum'
    MAX = 'maximum'
    
    def __init__(self, parent = None):
        super(DragKnob, self).__init__(parent)
        self.setTitle('DragKnob')
        self.initUI()
        
    def initUI(self):
        self.layout = QtGui.QVBoxLayout()
        self.qwtKnob = Qwt.QwtKnob(self)
        self.qwtKnob.setRange(-5,5)
        self.qwtKnob.setDisabled(True)
        
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.qwtKnob.valueChanged.connect(self.lcd.display)
        
        self.layout.addWidget(self.qwtKnob)
        self.layout.addWidget(self.lcd)
        
        #initial size
        self.resize(150,180)
        
        #update widget according to properties
        self.updateWidget()
        
        self.setLayout(self.layout)
        
    def initProps(self):
        self.props[self.MIN] = WidgetProperty('numeric', -4)
        self.props[self.MAX] = WidgetProperty('numeric', 4)
    
    def propertiesDialogAccepted(self):
        self.updateWidget()
        
    def updateWidget(self):
        #update the widget properties
        self.qwtKnob.setRange(self.props[self.MIN].value,
                              self.props[self.MAX].value)
        
    def updateValue(self, value):
        self.qwtKnob.setValue(float(value))
