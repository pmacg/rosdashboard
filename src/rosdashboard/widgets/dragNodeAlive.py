from PyQt4 import QtGui #@UnresolvedImport
from PyQt4 import QtCore #@UnresolvedImport

import rospkg
import os
import datetime

from modules.dashboardWidgets import DashboardWidget

class DragNodeAlive(DashboardWidget):
    """
    Shows an LED which goes red if the dashboard stops receiving updates on the configured topic.
    Timeout is configurable.
    """
    def __init__(self, parent = None):
        super(DragNodeAlive, self).__init__(parent)
        self.setTitle('DragNodeAlive')
        
        # Get the images from the res folder
        r = rospkg.RosPack()
        p = r.get_path('rosdashboard')
        base = os.path.join(p, 'res')
        
        redLedFile = os.path.join(base, 'red_led.png')
        self.redLedImage = QtGui.QImage(redLedFile)
        greenLedFile = os.path.join(base, 'green_led.png')
        self.greenLedImage = QtGui.QImage(greenLedFile)

        # Keep track of when we last had an update on the topic
        self.last_update = datetime.datetime(2019, 1, 1)
        
        self.initUI()
        
        #set default size
        self.resize(100, 120)

        # Create a timer to update the UI periodically
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateUI)
        self.timer.start()

        # Fore a GUI update now
        self.updateUI()
        
    def initProps(self):
        pass
        
    def initUI(self):
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setScaledContents(True);
        
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.imageLabel)
        
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def updateUI(self):
        # Decide which LED should be displayed
        seconds_since_update = (datetime.datetime.now() - self.last_update).total_seconds()

        if seconds_since_update > 5:
            image = self.redLedImage
        else:
            image = self.greenLedImage

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def updateValue(self, value):
        self.last_update = datetime.datetime.now()            
