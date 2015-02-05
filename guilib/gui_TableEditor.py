import db_components as dbc
from PyQt4 import QtGui
from PyQt4 import QtCore


class TableEditor(QtGui.QGroupBox):
# List of components with output of attributes
    def __init__(self, title, sim_inputs, parent=None):
        QtGui.QGroupBox.__init__(self, title, parent)

        self.__sim_inputs = sim_inputs

        self.comList = ComponentList(self)
        com_attributes = AttributeTable(False, self)
        self.comList.comItemSelected.connect(
            com_attributes.show_attributes)

        self._com_align = QtGui.QVBoxLayout()
        halign = QtGui.QHBoxLayout()
        halign.addWidget(self.comList)
        halign.addWidget(com_attributes)
        self._com_align.addLayout(halign)
        self.setLayout(self._com_align)

    def setData(self):
        for i in range(self.comList.count()):
            cd = self.comList.item(i).component
            if 'subs' in cd:
                if type(cd['subs']) is list:
                    for j in cd['subs']:
                        sub_dict = self.__get_sub(j)
                        cd = dict(cd.items() + sub_dict.items())
                else:
                    sub_dict = self.__get_sub(cd['subs'])
                    cd = dict(cd.items() + sub_dict.items())
                del cd['subs']
            self.__sim_inputs.append(cd)

    def __get_sub(self, com_id):
        try:
            sub_dict = dbc.get_component_by_ID(com_id, 1)
            del sub_dict['type']
        except dbc.DBError as de:
            mb = QtGui.QMessageBox(self)
            mb.setText(de.value)
            mb.exec_()
            sub_dict = {}
        return sub_dict


class ComponentEditor(TableEditor):
# List of components with output of attributes
# Additionally new components can be generated
    def __init__(self, isSub, title, parent=None):
        TableEditor.__init__(self, title, parent)

        self.__isSub = isSub

        bt_plus = QtGui.QPushButton(self)
        bt_plus.setIcon(QtGui.QIcon(QtGui.QPixmap('guilib/icons/plus.png')))
        self.connect(bt_plus, QtCore.SIGNAL('clicked()'),
                     self.__plus)

        self._com_align.insertWidget(0, bt_plus)

        self.update_com_list()

    def update_com_list(self):
        self.comList.clear()
        loc = dbc.get_component_list(self.__isSub)
        for i in range(loc.__len__()):
            if self.__isSub:
                comItem = ComponentItem(loc[i]['id'], loc[i],
                    loc[i]['fieldname'])
            else:
                comItem = ComponentItem(loc[i]['id'], loc[i], loc[i]['name'])
            del loc[i]['id']
            self.comList.addItem(comItem)

    def __plus(self):
        addcom = AddComponent(self.__isSub, self)
        if addcom.exec_():
            self.update_com_list()


class PatternEditor(TableEditor):
# List of patterns with output of attributes
# Additionally new patterns can be generated
    def __init__(self, title, parent=None):
        TableEditor.__init__(self, title, parent)

        self.__parent = parent

        bt_plus = QtGui.QPushButton(self)
        bt_plus.setIcon(QtGui.QIcon(QtGui.QPixmap('guilib/icons/plus.png')))
        self.connect(bt_plus, QtCore.SIGNAL('clicked()'),
                     self.__plus)

        self._com_align.insertWidget(0, bt_plus)

        self.update_com_list()

    def update_com_list(self):
        self.comList.clear()
        patterns = dbc.get_pattern_list()
        for i in range(patterns['count']):
            comItem = ComponentItem(patterns['pattern_fields'][i]['id'],
                patterns['pattern_fields'][i],
                str(patterns['pattern_types'][i]))
            del patterns['pattern_fields'][i]['id']
            self.comList.addItem(comItem)

    def __plus(self):
        addcom = AddPattern(self)
        if addcom.exec_():
            self.update_com_list()


class AttributeTable(QtGui.QTableWidget):
# Shows attributes of given component/pattern/sub-field
    def __init__(self, editable=True, parent=None):
        QtGui.QTabWidget.__init__(self, parent)
        self.__editable = editable
        self.verticalHeader().setVisible(False)

    def show_attributes(self, com_dict):
        self.clear()
        if self.__editable:
            self.setColumnCount(3)
            self.setHorizontalHeaderLabels(['Attribute', 'Type', 'Value'])
        else:
            self.setColumnCount(2)
            self.setHorizontalHeaderLabels(['Attribute', 'Value'])
        self.setRowCount(len(com_dict))
        try:
            for i, key in enumerate(com_dict):
                wi = QtGui.QTableWidgetItem(key)
                wi.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, 0, wi)
                wi = QtGui.QTableWidgetItem(str(com_dict[key]))
                wi.setFlags(QtCore.Qt.ItemIsEnabled)
                self.setItem(i, 1, wi)
                if self.__editable:
                    self.setItem(i, 2, QtGui.QTableWidgetItem(''))
        except StandardError:
            mb = QtGui.QMessageBox(self)
            mb.setText('Unexpected values in attribute found.')
            mb.exec_()
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)

    def get_entries(self):
        com_dict = {}
        for i in range(self.rowCount()):
            key = str(self.item(i, 0).text())
            try:
                value_type = self.item(i, 1).text()
                value = self.__test_entry_type(
                    self.item(i, 2).text(), value_type)
            except TypeError as te:
                raise te
            if value[1]:
                com_dict[key] = value[0]
            else:
                raise TypeError('''Value for key "%s" is not of
                type "%s".''' % (str(key), str(value_type)))
        return com_dict

    def __test_entry_type(self, str_value, type_value):
        if type_value == 'Real' or type_value == 'Number':
            return str_value.toFloat()
        elif type_value == 'Integer':
            return str_value.toInt()
        elif type_value == 'Real[]':
            try:
                str_list = str(str_value)[1:-1]
                floats = [float(x) for x in str_list.split()]
                return (floats, True)
            except TypeError as te:
                raise te
        elif type_value == 'String':
            return (str(str_value), True)
        else:
            raise TypeError(
                'Type ' + type_value +
                ' is not a valid python type or not yet implemented.')


class AddDialog(QtGui.QDialog):
# Abstract! Provides GUI for adding new components/patterns/sub-fields
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.resize(400, 400)

        line = QtGui.QFrame(self)
        line.setGeometry(320, 150, 118, 3)
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        self._bt_okay = QtGui.QPushButton('&OK', self)
        self._bt_cancel = QtGui.QPushButton('&Cancel', self)
        self._bt_cancel.setDefault(True)
        self.connect(self._bt_cancel, QtCore.SIGNAL('clicked()'),
                     self, QtCore.SLOT('reject()'))

        halign = QtGui.QHBoxLayout()
        halign.addWidget(self._bt_okay)
        halign.addWidget(self._bt_cancel)

        valign = QtGui.QVBoxLayout()
        valign.addWidget(line)
        valign.addLayout(halign)
        self.setLayout(valign)


class AddComponent(AddDialog):
# Provides GUI for adding new components/sub-fields
    def __init__(self, isSub, parent=None):
        AddDialog.__init__(self, parent)

        self.__isSub = isSub

        self.__combo_pattern = QtGui.QComboBox(self)
        self.__patterns = dbc.get_pattern_list(isSub, 0)
        self.__combo_pattern.addItems(self.__patterns['pattern_types'])

        self.__attributes = AttributeTable(parent=self)
        self.__combo_pattern.activated.connect(self.__show_attributes)
        self.__show_attributes(0)

        self.connect(self._bt_okay, QtCore.SIGNAL('clicked()'),
            self.__add_new_component)

        self.layout().insertWidget(0, self.__combo_pattern)
        self.layout().insertWidget(1, self.__attributes)

    def __show_attributes(self, index):
        self.__attributes.show_attributes(
            self.__patterns['pattern_fields'][index])

    def __add_new_component(self):
        com_type = str(self.__combo_pattern.currentText())
        pattern_id = dbc.get_pattern_id(com_type)
        try:
            new_entry = self.__attributes.get_entries()
            new_entry['type'] = com_type
            dbc.add_component(pattern_id, new_entry, self.__isSub)
            self.accept()
        except TypeError as te:
            mb = QtGui.QMessageBox(self)
            mb.setText(te.args[0])
            mb.exec_()


class AddPattern(AddDialog):
# Provides GUI for adding new patterns
    def __init__(self, parent=None):
        AddDialog.__init__(self, parent)
        patternName = QtGui.QGroupBox('Name of new Pattern:', self)
        patternName.setFixedHeight(100)
        self.__name = QtGui.QLineEdit('', patternName)
        self.__isSub = QtGui.QCheckBox('is Subfield?', patternName)
        align = QtGui.QVBoxLayout()
        align.addWidget(self.__name)
        align.addWidget(self.__isSub)
        patternName.setLayout(align)

        self.connect(self._bt_okay, QtCore.SIGNAL('clicked()'),
            self.__addNewPattern)

        self.__attributeGroup = QtGui.QGroupBox('Attributes:', self)
        btPlus = QtGui.QPushButton(self.__attributeGroup)
        btPlus.setIcon(QtGui.QIcon(QtGui.QPixmap('guilib/icons/plus.png')))
        self.connect(btPlus, QtCore.SIGNAL('clicked()'),
                     self.__addAttribute)

        grid = QtGui.QGridLayout()
        grid.addWidget(btPlus, 0, 0, 1, 0)
        grid.addWidget(
            QtGui.QLabel('Name:', self.__attributeGroup), 1, 0)
        grid.addWidget(
            QtGui.QLabel('Type:', self.__attributeGroup), 1, 1)
        self.__attributeGroup.setLayout(grid)

        self.__attributeList = []
        self.__addAttribute()

        self.layout().insertWidget(0, patternName)
        self.layout().insertWidget(1, self.__attributeGroup)

    def __addAttribute(self):
        cr = len(self.__attributeList) + 2
        le = QtGui.QLineEdit('', self.__attributeGroup)
        cb = QtGui.QComboBox(self.__attributeGroup)
        cb.addItems(['Real', 'Integer', 'String', 'Real[]'])
        self.__attributeList.append((le, cb))
        self.__attributeGroup.layout().addWidget(le, cr, 0)
        self.__attributeGroup.layout().addWidget(cb, cr, 1)

    def __addNewPattern(self):
        try:
            name, pat_dict, isSub = self.__checkEntries()
            dbc.add_pattern(name, pat_dict, isSub)
            self.accept()
        except NameError as ne:
            mb = QtGui.QMessageBox(self)
            mb.setText(ne.args[0])
            mb.exec_()
        except dbc.DBError as de:
            mb = QtGui.QMessageBox(self)
            mb.setText('Database-Error: ' + de.value)
            mb.exec_()

    def __checkEntries(self):
        pat_dict = {}
        if self.__name.text() == '':
            raise NameError('Unvalid pattern-name.')
        for i in range(len(self.__attributeList)):
            attName = str(self.__attributeList[i][0].text())
            if not attName == '':
                pat_dict[attName] = (
                    str(self.__attributeList[i][1].currentText()))
            else:
                raise NameError(
                    'Could not read attribute #' + str(i + 1) + '.')
        if self.__isSub.isChecked():
            pat_dict['fieldname'] = 'String'
        else:
            pat_dict['name'] = 'String'
        return (str(self.__name.text()), pat_dict,
            int(self.__isSub.isChecked()))


class ComponentItem(QtGui.QListWidgetItem):
# Special QListWidgetItem holding component-ID and -data
    def __init__(self, com_id, component, itemName):
        itemText = com_id + ': ' + itemName
        QtGui.QListWidgetItem.__init__(self, itemText)
        self.__component = component
        self.__com_id = com_id

    @property
    def component(self):
        return self.__component

    @property
    def com_id(self):
        return self.__com_id


class ComponentList(QtGui.QListWidget):
# Special QListWidget using ComponentItems
    comItemSelected = QtCore.pyqtSignal(dict)

    def __init__(self, parent):
        QtGui.QListWidget.__init__(self, parent)
        self.currentRowChanged.connect(self.connect_and_emit_ItemSelected)

    def connect_and_emit_ItemSelected(self, index):
        if not index == -1:
            self.comItemSelected.emit(self.item(index).component)