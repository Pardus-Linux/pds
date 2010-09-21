# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from pds.gui import PMessageBox

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(743, 487)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtGui.QLineEdit(Form)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.button = QtGui.QPushButton(Form)
        self.button.setObjectName("button")
        self.gridLayout.addWidget(self.button, 0, 2, 1, 1)
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setUrl(QtCore.QUrl("http://developer.pardus.org.tr/"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 1, 0, 1, 3)

        self.retranslateUi(Form)

        self.info = PMessageBox(Form, enable_overlay = True)
        self.button.clicked.connect(lambda: self.info.showMessage(self.line.text()))
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.line.setText(QtGui.QApplication.translate("Form", "This is a test message from PDS GUI !", None, QtGui.QApplication.UnicodeUTF8))
        self.button.setText(QtGui.QApplication.translate("Form", "Show Message", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

