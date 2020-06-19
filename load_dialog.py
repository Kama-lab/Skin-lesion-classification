from PyQt5 import QtCore, QtGui, QtWidgets
import classifier
import re

class dialog(QtWidgets.QWidget):
    def __init__(self):
        self.model_path = ""
        self.weights_path = ""
        QtWidgets.QWidget.__init__(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(0, 150, 441, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.setObjectName("buttonBox")
        self.upload_model_button = QtWidgets.QPushButton(self)
        self.upload_model_button.setGeometry(QtCore.QRect(20, 10, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.upload_model_button.setFont(font)
        self.upload_model_button.setObjectName("upload_model_button")
        self.upload_weights_button = QtWidgets.QPushButton(self)
        self.upload_weights_button.setGeometry(QtCore.QRect(20, 50, 121, 31))
        self.upload_model_button.clicked.connect(self.upload_model)
        self.upload_weights_button.clicked.connect(self.upload_weights)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.upload_weights_button.setFont(font)
        self.upload_weights_button.setObjectName("upload_weights_button")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 60, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(150, 20, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.model_name_input = QtWidgets.QPlainTextEdit(self)
        self.model_name_input.setGeometry(QtCore.QRect(70, 100, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.model_name_input.setFont(font)
        self.model_name_input.setObjectName("model_name_input")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.upload_model_path = QtWidgets.QLabel(self)
        self.upload_model_path.setGeometry(QtCore.QRect(200, 20, 241, 16))
        self.upload_model_path.setText("")
        self.upload_model_path.setObjectName("upload_model_path")
        self.upload_weights_path = QtWidgets.QLabel(self)
        self.upload_weights_path.setGeometry(QtCore.QRect(200, 60, 241, 21))
        self.upload_weights_path.setText("")
        self.upload_weights_path.setObjectName("upload_weights_path")
        self.upload_model_button.setText("upload model")
        self.upload_weights_button.setText("upload weights")
        self.label.setText("Path:")
        self.label_2.setText("Path:")
        self.label_3.setText("Name")


        self.warning = QtWidgets.QLabel(self)
        self.warning.setGeometry(QtCore.QRect(20, 150, 200, 13))
        self.warning.setObjectName("warning")

    def upload_model(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None,'Open file','','Images (*.json)')
        self.upload_model_path.setText(file_name[0])
        self.model_path = file_name[0]

    def upload_weights(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None,'Open file','','Images (*.h5)')
        self.upload_weights_path.setText(file_name[0])
        self.weights_path = file_name[0]

    def accept(self):
        name_shown = self.model_name_input.toPlainText()
        valid_name = re.match("^[A-Za-z0-9_-]*$", name_shown)
        if not(valid_name):
            self.warning.setText("Invalid input of name")
        elif name_shown != "" and self.model_path != "" and self.weights_path != "":
            result = classifier.add_model(self.model_path,self.weights_path,name_shown)
            if result == 0:
                self.warning.setText("Successfully uploaded")
                self.close()
            else:
                self.warning.setText(result)
        else:
            self.warning.setText("All fields are required")


    def reject(self):
        self.close()
