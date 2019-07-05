from PyQt4 import QtCore #@UnresolvedImport

#import xml.dom.minidom as minidom
import os
import json

#TODO: the widgets should be imported automatically from a plugin folder
from widgets.dragDial import DragDial
from widgets.dragKnob import DragKnob
from widgets.dragCompass import DragCompass
from widgets.dragThermo import DragThermo
from widgets.dragString import DragString
from widgets.dragLed import DragLed
from widgets.dragNodeAlive import DragNodeAlive

from modules.props import WidgetProperty

class Persistance(object):
    def __init__(self, dashboard):
        self.dashboard = dashboard
        
    def loadDashboard(self, filename):
        # clear old dashboard
        self.dashboard.clearDashboard()
        
        # get file data
        _file = open(filename,'r')
        filedata = _file.read()
        _file.close()
        
        # Parse file data. Always parse as json
        self.loadFromJSON(filedata)
            
    def saveDashboard(self, filename):
        # Always save as JSON
        data = self.saveToJSON()

        # Write to file
        _file = open(filename,'w')
        _file.write(data)
        _file.close()
        
    def loadFromJSON(self, filedata):
        data = json.loads(filedata)
        for widget in data["widgets"]:
            
            # load properties
            props = dict()
            for prop in widget["properties"]:
                propName = str(prop["name"])
                propType = str(prop["type"])
                propValue = prop["value"]
                props[propName] = WidgetProperty(propType, propValue)
            
            # load subscription
            topic = widget["subscription"]["topic"]
            datafield = widget["subscription"]["datafield"]
            regex = widget["subscription"]["regex"]
            
            # load geometry
            height = widget["height"]
            width = widget["width"]
            
            # load widget class
            typename = str(widget["type"])
            constructor = globals()[typename]
            instance = constructor()
            
            instance.setProperties(props)
            instance.setSubscription(topic, datafield, regex)
            instance.setWidgetName(widget["name"])
            instance.resize(width, height)
            
            x = widget["posX"]
            y = widget["posY"]
            position = QtCore.QPoint(x, y)

            self.dashboard.addWidget(instance, position, False)
            
    def saveToJSON(self):
        widgets = list()
        for widget in self.dashboard.widgets:
            widgetType = widget.__class__.__name__
            widgetName = widget.getWidgetName()
            widgetX = widget.x()
            widgetY = widget.y()
            widgetHeight = widget.height()
            widgetWidth = widget.width()
            subscription = {"topic": widget.topic, "datafield": widget.datafield, "regex": widget.regex}
            
            #fill properties
            props = list()
            for propKey, prop  in widget.getProperties().iteritems():
                props.append({"name": propKey, "type": prop.propertyType, "value": prop.value})
                
            widgets.append({"type": widgetType, "name": widgetName, "height": widgetHeight,
                            "width": widgetWidth, "posX": widgetX, "posY":widgetY,
                            "subscription": subscription, "properties": props})
            
        return json.dumps({"widgets": widgets})
