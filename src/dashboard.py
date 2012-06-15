#!/usr/bin/env python
import roslib; roslib.load_manifest('rosdashboard')
import rospy

import sys
from PyQt4 import QtGui, QtCore

from modules.props import DashboardProperties, WidgetProperties
from modules.widgets import DragButton, DragDial

"""
def callback(data, l):
    l.setText(data.data)
    l.resize(l.sizeHint())
    rospy.loginfo(rospy.get_name()+"I heard %s",data.data)
"""


class Dashboard(QtGui.QGroupBox):
    """ canvas where widgets can be positioned """ 
    
    #selectionChanged = QtCore.pyqtSignal()
      
    def __init__(self, parent):
        super(Dashboard, self).__init__(parent)

        self.initUI()
        self.initProperties()
        
    def initUI(self):

        self.setTitle('Dashboard')
        self.setAcceptDrops(True)

        self.button = DragButton('Button', self)
        self.button.move(100, 65)
        
        self.button.rightClicked.connect(self.selectionChanged)
        
        self.dial = DragDial(self)
        self.dial.move(100, 150)
        
        self.dial.rightClicked.connect(self.selectionChanged)
        
        #self.multiple = Multiple('multi', self)
        #self.multiple.move(100, 100)
        
    def initProperties(self):
        self.props = DashboardProperties()
        widgetProps = WidgetProperties()
        widgetProps.setProperty('datasource', '/turtle1/pose')
        widgetProps.setProperty('datafield', 'linear_velocity')
        self.props.setProperties(1, widgetProps)
        
    def selectionChanged(self):
        print('selection changed from ' + str(self.sender()))
        #TODO: lookup widget (by id?) and update currentWidget (and properties?)
        
    def dragEnterEvent(self, e):
        
        e.accept()

    def dropEvent(self, e):

        e.source().move(e.pos())

        e.setDropAction(QtCore.Qt.MoveAction)
        e.accept()
        
        
def main():
    
    rospy.init_node('dashboard', anonymous=True)
    
    app = QtGui.QApplication(sys.argv)
    
    w = QtGui.QWidget()
    w.resize(800, 600)
    w.move(100, 100)
    w.setWindowTitle('Dashboard')
    
    layout = QtGui.QHBoxLayout()
    
    dashboard = Dashboard(w)
    layout.addWidget(dashboard)
    
    #dashboard.selectionChanged.connect(properties.widgetSelected)
    
    w.setLayout(layout)
    w.show()

    #rospy.Subscriber("chatter", String, callback, l)
    #rospy.spin()
    
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
