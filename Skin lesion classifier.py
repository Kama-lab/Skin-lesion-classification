from PyQt5 import QtCore, QtGui, QtWidgets
import classifier
import copy
from load_dialog import dialog
from threading import Thread

models = []
for model in classifier.get_models().keys():
    models.append(model)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.imported_picture = QtWidgets.QLabel(self.centralwidget)
        self.imported_picture.setGeometry(QtCore.QRect(7, 7, 350, 250))
        self.imported_picture.setAcceptDrops(True)
        self.imported_picture.setAutoFillBackground(True)
        self.imported_picture.setText("")
        self.imported_picture.setObjectName("imported_picture")

        self.imported_picture.setPixmap(QtGui.QPixmap("res/placeholder-image.jpg").scaled(350,350,QtCore.Qt.KeepAspectRatio))
        
        self.import_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_button.setGeometry(QtCore.QRect(380, 10, 71, 31))
        self.import_button.setObjectName("import_button")

        self.import_button.clicked.connect(self.import_image)
        
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(530, 10, 60, 30))
        self.save_button.setObjectName("save_button")

        self.save_button.clicked.connect(self.save_file)

        self.classify_button = QtWidgets.QPushButton(self.centralwidget)
        self.classify_button.setGeometry(QtCore.QRect(380, 190, 101, 31))
        self.classify_button.setAutoFillBackground(True)
        self.classify_button.setObjectName("classify_button")

        self.classify_button.clicked.connect(self.predict)

        self.warning_label = QtWidgets.QLabel(self.centralwidget)
        self.warning_label.setGeometry(QtCore.QRect(380, 220, 160, 16))
        self.warning_label.setObjectName("warning_label")
        self.warning_label.setStyleSheet("color:red")
        
        self.save_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.save_combobox.setGeometry(QtCore.QRect(600, 12, 50, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_combobox.setFont(font)
        self.save_combobox.setObjectName("save_combobox")
        self.save_combobox.addItem("")
        self.save_combobox.addItem("")
        self.model_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.model_combobox.setGeometry(QtCore.QRect(560, 190, 91, 31))
        self.model_combobox.setObjectName("model_combobox")
        for model in range(len(models)):
            self.model_combobox.addItem("")
        self.model_combobox.view().pressed.connect(self.update_list)

        self.upload_button = QtWidgets.QPushButton(self.centralwidget)
        self.upload_button.setGeometry(QtCore.QRect(525, 190, 31, 31))
        self.upload_button.setObjectName("upload_button")
        self.upload_button.setText("+")
        self.upload_button.clicked.connect(self.open_upload_dialog)

        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setGeometry(QtCore.QRect(630, 221, 21, 21))
        self.update_button.setObjectName("update_button")
        self.update_button.setIcon(QtGui.QIcon(QtGui.QPixmap("res/update_icon.png")))
        self.update_button.clicked.connect(self.update_list)

        self.predicted_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted_label.setGeometry(QtCore.QRect(380, 240, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)

        font_small = QtGui.QFont()
        font_small.setPointSize(8)

        self.predicted_label.setFont(font)
        self.predicted_label.setObjectName("predicted_label")
        self.predicted2_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted2_label.setGeometry(QtCore.QRect(380, 280, 135, 16))
        self.predicted2_label.setObjectName("predicted2_label")
        self.predicted3_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted3_label.setGeometry(QtCore.QRect(380, 310, 135, 16))
        self.predicted3_label.setObjectName("predicted3_label")
        self.predicted4_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted4_label.setGeometry(QtCore.QRect(380, 340, 135, 16))
        self.predicted4_label.setObjectName("predicted4_label")
        self.predicted5_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted5_label.setGeometry(QtCore.QRect(520, 280, 135, 16))
        self.predicted5_label.setObjectName("predicted5_label")
        self.predicted6_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted6_label.setGeometry(QtCore.QRect(520, 310, 135, 16))
        self.predicted6_label.setObjectName("predicted6_label")
        self.predicted7_label = QtWidgets.QLabel(self.centralwidget)
        self.predicted7_label.setGeometry(QtCore.QRect(520, 340, 135, 16))
        self.predicted7_label.setObjectName("predicted7_label")
        self.predicted2_label.setFont(font_small)
        self.predicted3_label.setFont(font_small)
        self.predicted4_label.setFont(font_small)
        self.predicted5_label.setFont(font_small)
        self.predicted6_label.setFont(font_small)
        self.predicted7_label.setFont(font_small)
        
        self.listView = QtWidgets.QListWidget(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(380, 50, 271, 131))
        self.listView.setObjectName("listView")
        self.listView.setSelectionMode(QtWidgets.QListWidget.MultiSelection)

        self.resized_image = QtWidgets.QLabel(self.centralwidget)
        self.resized_image.setGeometry(QtCore.QRect(7, 260, 112, 112))
        self.resized_image.setAutoFillBackground(True)
        self.resized_image.setText("")
        self.resized_image.setObjectName("resized_image")

        self.resized_image.setPixmap(QtGui.QPixmap("res/placeholder-image.jpg").scaled(112,112))
        
        self.size_label = QtWidgets.QLabel(self.centralwidget)
        self.size_label.setGeometry(QtCore.QRect(130, 300, 120, 16))
        self.size_label.setObjectName("size_label")
        self.resized_label = QtWidgets.QLabel(self.centralwidget)
        self.resized_label.setGeometry(QtCore.QRect(130, 320, 101, 16))
        self.resized_label.setObjectName("resized_label")
        self.filename_label = QtWidgets.QLabel(self.centralwidget)
        self.filename_label.setGeometry(QtCore.QRect(130, 260, 211, 16))
        self.filename_label.setObjectName("filename_label")
        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setGeometry(QtCore.QRect(130, 280, 211, 16))
        self.path_label.setObjectName("path_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 642, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.save_button.setText(_translate("MainWindow", "Save as"))
        self.classify_button.setText(_translate("MainWindow", "Classify"))
        self.save_combobox.setItemText(0, _translate("MainWindow", "csv"))
        self.save_combobox.setItemText(1, _translate("MainWindow", "xlsx"))
        for model in models:
            self.model_combobox.setItemText(models.index(model), _translate("MainWindow", model))
        
        self.predicted_label.setText(_translate("MainWindow", ""))
        self.predicted2_label.setText(_translate("MainWindow", ""))
        self.predicted3_label.setText(_translate("MainWindow", ""))
        self.predicted4_label.setText(_translate("MainWindow", ""))
        self.predicted5_label.setText(_translate("MainWindow", ""))
        self.predicted6_label.setText(_translate("MainWindow", ""))
        self.predicted7_label.setText(_translate("MainWindow", ""))
        self.warning_label.setText(_translate("MainWindow", ""))
        self.size_label.setText(_translate("MainWindow", "Original size:"))
        self.resized_label.setText(_translate("MainWindow", "Resized to:"))
        self.filename_label.setText(_translate("MainWindow", "Filename:"))
        self.path_label.setText(_translate("MainWindow", "Path:"))
        self.listView.itemClicked.connect(self.show_item_info)
        self.threadpool_progressBar = QtCore.QThreadPool()
        self.threadpool_predict = QtCore.QThreadPool()

    
    def import_image(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(None,'Open file','','Images (*.jpg)')
        if file_name[0]:
            image_name = classifier.add_image(file_name[0])
            if image_name:
                self.imported_picture.setPixmap(QtGui.QPixmap(file_name[0]).scaled(340,340,QtCore.Qt.KeepAspectRatio))
                self.listView.addItem(image_name)
                self.show_info_box(image_name)
                self.warning_label.setText("")
                self.warning_label.setStyleSheet("color:red")
            else:
                self.warning_label.setText("Unknown image format")

    def save_file(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(None,'Save file','',f"file (*.{self.save_combobox.currentText()})")
        try:
            classifier.save(file_name,self.save_combobox.currentText())
            self.warning_label.setStyleSheet("color:black")
            self.warning_label.setText("file is saved")
        except FileNotFoundError:
            self.warning_label.setText("file is not saved")



    def predict(self):
        selected_items = self.listView.selectedItems()
        if len(selected_items) == 1:
            probs = classifier.predict_image(selected_items[0].text(),self.model_combobox.currentText())
            self.show_predictions_info(probs)
            self.show_info_box(selected_items[0].text())
            self.show_item_info(selected_items[0])
        elif len(selected_items) > 1:
            probs = classifier.predict_images([i.text() for i in selected_items],self.model_combobox.currentText())
            self.warning_label.setText("")
            self.warning_label.setStyleSheet("color:red")
            self.show_predictions_info(probs)
            self.show_info_box(selected_items[-1].text())
            self.show_item_info(selected_items[-1])
        else:
            self.warning_label.setText("Image is not selected")

        


    def show_item_info(self,clicked_item):
        loc,size,probs,crop_size,image = classifier.get_image_info(clicked_item.text())
        if probs:
            self.show_predictions_info(probs)
            self.resized_image.setPixmap(QtGui.QPixmap(QtGui.QImage(image)).scaled(112,112,QtCore.Qt.KeepAspectRatio))
        else:
            self.clear_item_info()
        self.imported_picture.setPixmap(QtGui.QPixmap(loc).scaled(340,340,QtCore.Qt.KeepAspectRatio))
        self.show_info_box(clicked_item)
        self.warning_label.setText("")
        self.warning_label.setStyleSheet("color:red")

    def clear_item_info(self):
        self.predicted_label.setText("")
        for i in _labels:
            i.setText("")

    def show_predictions_info(self,pred_probs):
        probs = copy.deepcopy(pred_probs)
        max_value = max(probs.values())
        n = list(probs.values()).index(max_value)
        max_prob_type = list(probs.keys())[n]
        self.predicted_label.setText(f"{max_prob_type}: {max_value}%")
        del probs[max_prob_type]
        nLabel = 0
        for i in probs:
            _labels[nLabel].setText(f"{i}: {probs[i]}%")
            nLabel += 1
        self.warning_label.setText("")
        self.warning_label.setStyleSheet("color:red")

    def show_info_box(self,item):
        item_name = item
        if not isinstance(item,str):
            item_name = item.text()

        path, size, info, resized_to, _ = classifier.get_image_info(item_name)
        self.filename_label.setText(f"file name:{item_name}.jpg")
        self.size_label.setText(f"Original size:{size}")
        self.resized_label.setText(f"Resized to:{resized_to}")
        self.path_label.setText(f"location:{path}")

    def open_upload_dialog(self):
        _prev_combo_list_num = classifier.models.keys()
        self.w = dialog()
        self.w.setGeometry(400,200,455,185)
        #self.w.setFixedSize(455,185)
        self.w.show()
        
    def update_list(self):
        _new_combo_list_num = classifier.models.keys()
        if len(_new_combo_list_num) > len(_prev_combo_list_num):
            new_item = list(set(_new_combo_list_num)^set(_prev_combo_list_num))[0]
            self.model_combobox.addItem(new_item)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setFixedSize(662,400)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    _labels = [ui.predicted2_label,
                ui.predicted3_label,
                ui.predicted4_label,
                ui.predicted5_label,
                ui.predicted6_label,
                ui.predicted7_label]

    list_copy = copy.deepcopy(classifier.models)
    _prev_combo_list_num = list_copy.keys()
    _new_combo_list_num = 0
    MainWindow.show()

    sys.exit(app.exec_())
    if app.exec_():
        w.reject()
