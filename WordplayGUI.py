#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
from PySide import QtGui
from wordplay import Wordplay


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.wordplay = Wordplay()
        self.wordplay.open("french.sqlite")

        self.__init_gui()


    def __init_gui(self):
        self.setWindowTitle("Wordplay")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        tabWidget = QtGui.QTabWidget(self)
        layout.addWidget(tabWidget)

        self.__init_tab_dictionary(tabWidget)
        self.__init_tab_anagrams(tabWidget)
        self.__init_tab_3words(tabWidget)
        self.__init_tab_quatro(tabWidget)


    def __init_tab_dictionary(self, tabWidget):
        tab = QtGui.QWidget(tabWidget)
        tabWidget.addTab(tab, "Dictionnaire")

        layout = QtGui.QVBoxLayout()
        tab.setLayout(layout)

        entry = QtGui.QLineEdit(self)
        layout.addWidget(entry)

        listView = QtGui.QListView(self)
        layout.addWidget(listView)

        model = QtGui.QStandardItemModel(listView)
        listView.setModel(model)

        entry.editingFinished.connect(lambda: self.__dictionary_updated(entry.text(), model))


    def __init_tab_anagrams(self, tabWidget):
        tab = QtGui.QWidget(tabWidget)
        tabWidget.addTab(tab, "Annagrames")

        layout = QtGui.QVBoxLayout()
        tab.setLayout(layout)

        entry = QtGui.QLineEdit(self)
        layout.addWidget(entry)

        listView = QtGui.QListView(self)
        layout.addWidget(listView)

        model = QtGui.QStandardItemModel(listView)
        listView.setModel(model)

        entry.editingFinished.connect(lambda: self.__anagram_updated(entry.text(), model))


    def __init_tab_3words(self, tabWidget):
        tab = QtGui.QWidget(tabWidget)
        tabWidget.addTab(tab, "Lettres pour 3 mots")

        layout = QtGui.QVBoxLayout()
        tab.setLayout(layout)

        sub_layout = QtGui.QHBoxLayout()
        layout.addLayout(sub_layout)

        prefix1 = QtGui.QLineEdit(self)
        sub_layout.addWidget(prefix1)

        prefix2 = QtGui.QLineEdit(self)
        sub_layout.addWidget(prefix2)

        prefix3 = QtGui.QLineEdit(self)
        sub_layout.addWidget(prefix3)

        suffixLength = QtGui.QSpinBox(self)
        sub_layout.addWidget(suffixLength)
        suffixLength.setValue(3)

        pushButton = QtGui.QPushButton("OK", self)
        sub_layout.addWidget(pushButton)

        listView = QtGui.QListView(self)
        layout.addWidget(listView)

        model = QtGui.QStandardItemModel(listView)
        listView.setModel(model)

        pushButton.clicked.connect(lambda: self.__3words_updated(prefix1.text(), prefix2.text(), prefix3.text(), suffixLength.value(), model))


    def __init_tab_quatro(self, tabWidget):
        tab = QtGui.QWidget(tabWidget)
        tabWidget.addTab(tab, "Quatro")

        layout = QtGui.QVBoxLayout()
        tab.setLayout(layout)


        sub_layout = QtGui.QHBoxLayout()
        layout.addLayout(sub_layout)

        prefix1 = QtGui.QLineEdit(self)
        sub_layout.addWidget(prefix1)

        suffix1 = QtGui.QLineEdit(self)
        sub_layout.addWidget(suffix1)

        sub_layout = QtGui.QHBoxLayout()
        layout.addLayout(sub_layout)

        prefix2 = QtGui.QLineEdit(self)
        sub_layout.addWidget(prefix2)

        suffix2 = QtGui.QLineEdit(self)
        sub_layout.addWidget(suffix2)

        sub_layout = QtGui.QHBoxLayout()
        layout.addLayout(sub_layout)

        middleLength = QtGui.QSpinBox(self)
        sub_layout.addWidget(middleLength)
        middleLength.setValue(1)

        pushButton = QtGui.QPushButton("OK", self)
        sub_layout.addWidget(pushButton)


        listView = QtGui.QListView(self)
        layout.addWidget(listView)

        model = QtGui.QStandardItemModel(listView)
        listView.setModel(model)

        pushButton.clicked.connect(lambda: self.__quatro_updated(prefix1.text(), suffix1.text(), prefix2.text(), suffix2.text(), middleLength.value(), model))


    def __dictionary_updated(self, text, model):
        model.clear()
        for word in self.wordplay.search_words(text):
            item = QtGui.QStandardItem(word)
            item.setEditable(False)
            model.appendRow(item)


    def __anagram_updated(self, text, model):
        model.clear()
        for word in self.wordplay.search_anagrams(text):
            item = QtGui.QStandardItem(word)
            item.setEditable(False)
            model.appendRow(item)


    def __3words_updated(self, prefix1, prefix2, prefix3, suffix_len, model):
        model.clear()
        for suffix in self.wordplay.letters_for_three_words(prefix1, prefix2, prefix3, suffix_len):
            item = QtGui.QStandardItem("{0} ({1}{0}, {2}{0}, {3}{0})".format(suffix, prefix1, prefix2, prefix3))
            item.setEditable(False)
            model.appendRow(item)


    def __quatro_updated(self, prefix1, suffix1, prefix2, suffix2, middleLength, model):
        model.clear()
        for middle in self.wordplay.quatro(prefix1, suffix1, prefix2, suffix2, middleLength):
            item = QtGui.QStandardItem("{0} ({1}{0}{2}, {3}{0}{4})".format(middle, prefix1, suffix1, prefix2, suffix2))
            item.setEditable(False)
            model.appendRow(item)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
