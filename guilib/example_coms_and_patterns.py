import sys
import gui_components as gc
from PyQt4 import QtGui

sim_inputs = []

app = QtGui.QApplication(sys.argv)
widget = gc.GUI_Components_and_Patterns(sim_inputs)
widget.setGeometry(20, 20, 2400, 1200)
widget.show()
app.exec_()
print sim_inputs