from PyQt4 import QtGui #@UnresolvedImport
from PyQt4 import QtCore #@UnresolvedImport

import rospkg
import os

from modules.dashboardWidgets import DashboardWidget

class DragLed(DashboardWidget):
    updateUiSignal = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, parent = None):
        super(DragLed, self).__init__(parent)
        self.setTitle('DragLed')
        
        # Get the images from the res folder
        r = rospkg.RosPack()
        p = r.get_path('rosdashboard')
        base = os.path.join(p, 'res')
        
        redLedFile = os.path.join(base, 'red_led.png')
        self.redLedImage = QtGui.QImage(redLedFile)
        greenLedFile = os.path.join(base, 'green_led.png')
        self.greenLedImage = QtGui.QImage(greenLedFile)
        greyLedFile = os.path.join(base, 'grey_led.png')
        self.greyLedImage = QtGui.QImage(greyLedFile)
        
        #connect to the update UI signal to update the ui only in the main thread
        self.updateUiSignal.connect(self.updateUI)
        
        self.initUI()
        
        #set default size
        self.resize(100, 120)
        
        #initially set led to grey
        self.updateValue(None);
        
    def initProps(self):
        pass
        
    def initUI(self):
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setScaledContents(True);
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.imageLabel)
        
        self.setLayout(self.layout)
        
    def updateUI(self, image):
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def updateValue(self, value):
        
        if (value == None):
            self.updateUiSignal.emit(self.greyLedImage)
        elif (value == True):
            self.updateUiSignal.emit(self.greenLedImage)
        else:
            self.updateUiSignal.emit(self.redLedImage)
            
