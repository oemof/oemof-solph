import gui_TableEditor as guiTE
from PyQt4 import QtGui
from PyQt4 import QtCore


class GUI_Components_and_Patterns(QtGui.QWidget):
# GUI for manipulation of components, sub-fields and patterns
# Simulation-Inputs given as list can be filled with chosen components
    def __init__(self, sim_inputs, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.__scenario = GUI_ComponentSetup(sim_inputs, self)
        self.__pattern = GUI_PatternSetup(self)

        halign = QtGui.QHBoxLayout()
        halign.addWidget(self.__scenario)
        halign.addWidget(self.__pattern)
        valign = QtGui.QVBoxLayout()
        valign.addLayout(halign)
        self.setLayout(valign)

    def loadData(self):
        self.__scenario.loadData()


class GUI_Components(QtGui.QWidget):
# GUI for manipulation of components only
# Simulation-Inputs given as list can be filled with chosen components
    def __init__(self, sim_inputs, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.__scenario = GUI_ComponentSetup(sim_inputs, self)
        btLoadData = QtGui.QPushButton('&Load data into input-dictionary', self)
        self.connect(btLoadData, QtCore.SIGNAL('clicked()'),
                     self.__loadData)

        halign = QtGui.QHBoxLayout()
        halign.addWidget(self.__scenario)
        valign = QtGui.QVBoxLayout()
        valign.addLayout(halign)
        valign.addWidget(btLoadData)
        self.setLayout(valign)

    def __loadData(self):
        self.__scenario.loadData()
        self.close()


class GUI_ComponentSetup(QtGui.QWidget):
# Provides component-list and chosen-component-list
# Also new components can be generated
    def __init__(self, sim_inputs, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.__comEditor = guiTE.ComponentEditor(0, 'Components', self)
        self.__chosenEditor = guiTE.TableEditor(
            'Chosen Components', sim_inputs, self)

        bt_down = QtGui.QPushButton(self)
        bt_down.setIcon(QtGui.QIcon(QtGui.QPixmap(
            'guilib/icons/arrow_down.png')))
        self.connect(bt_down, QtCore.SIGNAL('clicked()'),
                     self.__down)
        bt_up = QtGui.QPushButton(self)
        bt_up.setIcon(QtGui.QIcon(QtGui.QPixmap('guilib/icons/arrow_up.png')))
        self.connect(bt_up, QtCore.SIGNAL('clicked()'),
                     self.__up)

        chose_align = QtGui.QHBoxLayout()
        chose_align.addWidget(bt_down)
        chose_align.addWidget(bt_up)

        v_align = QtGui.QVBoxLayout()
        v_align.addWidget(self.__comEditor)
        v_align.addLayout(chose_align)
        v_align.addWidget(self.__chosenEditor)

        self.setLayout(v_align)

    def loadData(self):
        self.__chosenEditor.setData()

    def __down(self):
        list_index = self.__comEditor.comList.currentRow()
        if not list_index == -1:
            it = self.__comEditor.comList.item(list_index)
            comItem = guiTE.ComponentItem(it.com_id, it.component,
                it.component['name'])
            self.__chosenEditor.comList.addItem(comItem)

    def __up(self):
        list_index = self.__chosenEditor.comList.currentRow()
        if not list_index == -1:
            self.__chosenEditor.comList.takeItem(list_index)


class GUI_PatternSetup(QtGui.QWidget):
# Provides list of component-patterns; new patterns can be added
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.__patternEditor = guiTE.PatternEditor('Patterns', self)
        self.__subEditor = guiTE.ComponentEditor(1, 'Sub-Fields', self)

        valign = QtGui.QVBoxLayout()
        valign.addWidget(self.__patternEditor)
        valign.addWidget(self.__subEditor)
        self.setLayout(valign)



