#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from os import listdir, remove
from os.path import isfile, join

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.bind_views()
        self.reload_files()
        self.setWindowTitle('Api-proxy GUI')
        self.show()

    def bind_views(self):
        self.override_checkbox.stateChanged.connect(self.override_checked)
        self.qlist.itemSelectionChanged.connect(self.item_click)
        self.reload_text_button.clicked.connect(self.item_click)
        self.reload_button.clicked.connect(self.reload_files)
        self.save_button.clicked.connect(self.save_text_to_file)

    def _get_files_in_directory(self, directory):
        return [f for f in listdir(directory) if isfile(join(directory, f))]

    def reload_files(self):
        self.qlist.clear()
        files = sum([self._get_files_in_directory(d) for d in ["output", "override"]], [])
        map(self.qlist.addItem, files)

    def override_checked(self):
        if len(self.qlist.selectedItems()) == 1:
            item = self.qlist.selectedItems()[0]
            path = "override/" + item.text()
            if self.override_checkbox.isChecked():
                text_file = open(path, "w")
                text_file.write(self.textbox.toPlainText())
                text_file.close()
            elif isfile(path):
                remove(path)

            self.save_button.setEnabled(self.override_checkbox.isChecked())

    def save_text_to_file(self):
            item = self.qlist.selectedItems()[0]
            path = "override/" + item.text()
            text_file = open(path, "w")
            text_file.write(self.textbox.toPlainText())
            text_file.close()

    def item_click(self):
            if len(self.qlist.selectedItems()) == 1:
                item = self.qlist.selectedItems()[0]
                path = "override/" + item.text()
                if not isfile(path):
                    path = "output/" + item.text()

                with open(path, 'rb') as f:
                    content = f.read()
                    self.textbox.setText(content)
                self.override_checkbox.setChecked(isfile("override/" + item.text()))

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.qlist = QtGui.QListWidget()
        self.qlist.setWindowTitle('Example List')
        self.qlist.setMinimumSize(100, 600)
        self.qlist.setFixedWidth(200)
        self.qlist.setSortingEnabled(True);  

        self.reload_button = QtGui.QPushButton('Reload')
        self.reload_button.setFixedWidth(200)

        self.textbox = QtGui.QTextEdit()
        self.textbox.setMinimumSize(800, 600)

        self.override_checkbox = QtGui.QCheckBox("Override Response")
        self.save_button = QtGui.QPushButton('Save')
        self.save_button.setFixedWidth(200)

        self.reload_text_button = QtGui.QPushButton('Reload Text')
        self.reload_text_button.setFixedWidth(200)

        listVbox = QtGui.QVBoxLayout()
        listVbox.addWidget(self.qlist)
        listVbox.addWidget(self.reload_button)

        actionshbox = QtGui.QHBoxLayout()
        actionshbox.addWidget(self.override_checkbox)
        actionshbox.addWidget(self.reload_text_button)
        actionshbox.addWidget(self.save_button)

        textboxVbox = QtGui.QVBoxLayout()
        textboxVbox.addWidget(self.textbox)
        textboxVbox.addLayout(actionshbox)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(listVbox)
        hbox.addLayout(textboxVbox)
        self.setLayout(hbox)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
