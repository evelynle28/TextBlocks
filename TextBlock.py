# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QIcon, QPixmap, QImage
from db_manager import DbManager

addr = 'http://localhost:5000'
upload_url = addr + '/upload'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        MainWindow.setWindowTitle("TextBlock Application")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.db = DbManager('text_block')

        self.setStyle(MainWindow)
        self.setMenubar(MainWindow)
        self.setHeaderText()
        self.setButtons()
        self.setIOLayout()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setStyle(self, MainWindow):
        '''
        Set up font and color for labels in the MainWindow
        '''
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(44, 45, 44, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 53, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 53, 56, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 45, 44, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 53, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(53, 53, 56, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)

    def setMenubar(self, MainWindow):
        '''
        Set up options in the menubar
        '''
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)


        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionClose.triggered.connect(MainWindow.close)

        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

    def setHeaderText(self):
        '''
        Set Up Label on the topleft screen
        '''

        self.appName = QtWidgets.QLabel(self.centralwidget)
        self.appName.setGeometry(QtCore.QRect(130, 20, 341, 81))

        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(40)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)

        self.appName.setFont(font)
        self.appName.setFocusPolicy(QtCore.Qt.NoFocus)
        self.appName.setTextFormat(QtCore.Qt.MarkdownText)
        self.appName.setScaledContents(True)
        self.appName.setObjectName("appName")

        self.appDescription = QtWidgets.QLabel(self.centralwidget)
        self.appDescription.setGeometry(QtCore.QRect(130, 90, 331, 31))

        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)

        self.appDescription.setFont(font)
        self.appDescription.setScaledContents(True)
        self.appDescription.setObjectName("appDescription")


        # self.width = self.inputImg.frameGeometry().width()
        # self.height = self.inputImg.frameGeometry().height()

    def setButtons(self):
        '''
        Set up the position and style of the Upload and Delete buttons
        '''
        self.UploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.UploadButton.setGeometry(QtCore.QRect(410, 92, 112, 32))

        self.DeleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteButton.setGeometry(QtCore.QRect(1230, 790, 101, 32))

        self.ShowAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.ShowAllButton.setGeometry(QtCore.QRect(1119, 790, 101, 32))

        self.DefaultButton = QtWidgets.QPushButton(self.centralwidget)
        self.DefaultButton.setGeometry(QtCore.QRect(1008, 790, 101, 32))

        #Set up style and font of text inside buttons
        font = QtGui.QFont()
        font.setFamily("Helvetica Neue")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)


        self.UploadButton.setFont(font)
        self.UploadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UploadButton.setMouseTracking(True)
        self.UploadButton.setObjectName("UploadButton")
        self.UploadButton.clicked.connect(self.browseImage)

        self.DeleteButton.setFont(font)
        self.DeleteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DeleteButton.setMouseTracking(True)
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(self.clearData)

        self.ShowAllButton.setFont(font)
        self.ShowAllButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ShowAllButton.setMouseTracking(True)
        self.ShowAllButton.setObjectName("ShowAllButton")
        self.ShowAllButton.clicked.connect(self.showAllData)

        self.DefaultButton.setFont(font)
        self.DefaultButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DefaultButton.setMouseTracking(True)
        self.DefaultButton.setObjectName("Default")
        self.DefaultButton.clicked.connect(self.showCurrentData)

    def setIOLayout(self):
        '''
        Set up the layout for the input/output images and
        the database showing the text in the input image
        '''
        self.inputImage = QtWidgets.QLabel(self.centralwidget)
        self.inputImage.setEnabled(True)
        self.inputImage.setGeometry(QtCore.QRect(130, 140, 591, 390))
        self.inputImage.setText("")
        self.inputImage.setObjectName("inputImage")

        self.currentImgID = ''
        self.outputImage = QtWidgets.QLabel(self.centralwidget)
        self.outputImage.setEnabled(True)
        self.outputImage.setGeometry(QtCore.QRect(740, 140, 591, 390))
        self.outputImage.setText("")
        self.outputImage.setObjectName("outImage")

        self.databaseDisplay = QtWidgets.QTableWidget(self.centralwidget)
        self.databaseDisplay.setEnabled(True)
        self.databaseDisplay.setGeometry(QtCore.QRect(130, 560, 1201, 220))
        self.databaseDisplay.setMinimumSize(QtCore.QSize(1201, 0))
        self.databaseDisplay.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)


        self.databaseDisplay.setAlternatingRowColors(True)
        self.databaseDisplay.setObjectName("databaseDisplay")
        self.databaseDisplay.setColumnCount(5)
        self.databaseDisplay.horizontalHeader().setVisible(False)
        self.databaseDisplay.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers);


        for col in range(5):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.databaseDisplay.setHorizontalHeaderItem(col, item)

    def browseImage(self):
        '''
        Let users browse their file directories and specify
        upload file type (images only - .jpg, .png) and pass
        the input image for processing
        '''
        dialog = QFileDialog()
        filename, _ = dialog.getOpenFileName(self.UploadButton,\
                                             "Import Image","", \
                                             "Image files (*.JPEG *.JPG *.PNG)")

        if filename != '':
            img = QPixmap(filename).scaled(591, 390, Qt.KeepAspectRatio,Qt.SmoothTransformation)

            self.inputImage.setPixmap(img)
            self.inputImage.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


            inferred_img = self.inferImage(filename)

            self.currentImgID = inferred_img['id']
            self.renderOutput(inferred_img['img'])
            self.updateDatabase(inferred_img['id'], \
                                inferred_img['blocks'])
            self.showCurrentData()

    def inferImage(self, filename):
        '''
        Perform inference on the server
        '''
        img = open(filename, 'rb').read()
        response = requests.post(upload_url, data=img)
        return response.json()

    def renderOutput(self,img):
        '''
        Render output image  grasped from the server
        '''
        #Decode image data received from server

        bin_img = base64.b64decode(img)

        qImg = QImage.fromData(bin_img)

        pix = QPixmap.fromImage(qImg)

        self.outputImage.setPixmap(pix.scaled(591, 390,\
                                                Qt.KeepAspectRatio, \
                                                Qt.SmoothTransformation))

        self.outputImage.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)

    def updateDatabase(self, img_id, blocks):
        # query = QtSql.QSqlQuery()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS image_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id TEXT NOT NULL,
                image_path TEXT NOT NULL,
                box_id INTEGER NOT NULL,
                position TEXT NOT NULL,
                box_content TEXT
            );'''

        try:
            self.db.exec(create_table_query)
            # query.exec(create_table_query)
        except:
            return None

        path = os.getcwd() + '/outputs/' +str(img_id) + '.png'

        insert_template = ("""
            INSERT INTO image_data
                (image_id, image_path, box_id, position, box_content)
            VALUES
                ('{}','{}',{},'{}','{}')""")

        for block in blocks:
            try:
                insert_query = insert_template.format(img_id,\
                                                path,\
                                                block['id'],\
                                                json.dumps(block['coors']),\
                                                block['content'])
                self.db.exec(insert_query)
            except Exception as e:
                return None

    def queryData(self, img_id):
        '''
        Query data from the img_database to display properly
        '''
        # query = QtSql.QSqlQuery()
        select_query = """ SELECT image_id, box_id, position,
                                    box_content, image_path
                            FROM image_data """

        if img_id != None:
            select_query +=  "WHERE image_id = '{}'".format(str(img_id))

        try:
            cursor = self.db.exec(select_query)
        except Exception as e:
            return None
        else:
            results = []
            while(cursor.next()):
                results.append([str(cursor.value(0)),\
                                    str(cursor.value(1)),\
                                    str(cursor.value(2)),
                                    str(cursor.value(3)),
                                    str(cursor.value(4))])
            return results

    def showAllData(self):
        try:
            data = self.queryData(None)
            self.displayData(data)
        except:
            return

    def showCurrentData(self):
        try:
            data = self.queryData(self.currentImgID)
            self.displayData(data)
        except:
            return

    def displayData(self, results):
        if (results == None or len(results) == 0):
            return

        self.databaseDisplay.setRowCount(0)
        self.databaseDisplay.horizontalHeader().setVisible(True)

        curRowNum = 0
        self.databaseDisplay.setRowCount(len(results))

        record = self.databaseDisplay.verticalHeader()

        for row_data in results:
            # self.databaseDisplay.insertRow(row_id)
            for col_id, data in enumerate(row_data):
                self.databaseDisplay.setItem(curRowNum, col_id, QtWidgets.QTableWidgetItem(str(data)))
            record.setSectionResizeMode(curRowNum, QtWidgets.QHeaderView.ResizeToContents)
            curRowNum += 1

        header = self.databaseDisplay.horizontalHeader()

        for i in range(5):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

    def clearData (self):
        confirm = QMessageBox()
        confirm.setText("Do you want to delete the database?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        confirm = confirm.exec()

        if confirm == QMessageBox.Yes:
            query = QtSql.QSqlQuery()
            try:
                query.exec("DROP TABLE image_data")
            except:
                return
            finally:
                self.databaseDisplay.setRowCount(0)
                self.databaseDisplay.horizontalHeader().setVisible(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TextBlock Detection"))
        self.UploadButton.setText(_translate("MainWindow", "Upload"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete All"))
        self.ShowAllButton.setText(_translate("MainWindow", "Show All"))
        self.DefaultButton.setText(_translate("MainWindow", "Default"))
        self.appName.setText(_translate("MainWindow", "TEXTBLOCK"))
        self.appDescription.setText(_translate("MainWindow", "Retrieve Text From Your Image"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        item = self.databaseDisplay.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Image ID"))
        item = self.databaseDisplay.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Bounding Box ID"))
        item = self.databaseDisplay.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Position"))
        item = self.databaseDisplay.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Content"))
        item = self.databaseDisplay.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Image Path"))

class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self,event):
        close = QtWidgets.QMessageBox.question(self, "QUIT", \
                                         "Are you sure to quit?",\
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel, \
                                        QtWidgets.QMessageBox.Cancel)

        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    import requests
    import json
    import os
    import base64

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

