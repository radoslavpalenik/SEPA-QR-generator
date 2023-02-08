import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QImage, QClipboard
import qrcode
import pay_by_square
from PIL import ImageQt
from PyQt6 import uic, QtWidgets
from dialog import Dialog
from parser import getAccount
from parser import configChecker

class UI(QMainWindow):
    #Opens dialog window
    def openDialog(self):
        self.window = QtWidgets.QDialog()
        self.ui = Dialog()
        self.ui.setModal(True)
        self.ui.show()



    def __init__(self):
        super(UI, self).__init__() 
        uic.loadUi('GUI.ui', self) 

        self.copyBtn.clicked.connect(self.copyQR)
        self.saveBtn.clicked.connect(self.saveQR)
        self.settingsBtn.clicked.connect(lambda: self.openDialog())

        self.copyBtn.setVisible(False)
        self.saveBtn.setVisible(False)

        self.labelQR = self.findChild(QLabel,'labelQR')
        
        self.generateBtn.clicked.connect(self.generate)

        self.show()

    #Generates QR code from given values and stored account in config file
    def generate(self):

        account = getAccount()        
        code = pay_by_square.generate(  
            iban=account[0],
            swift=account[1],
            currency=account[2],
            amount=self.value.value(),
            variable_symbol= self.inputVS.text(),
            specific_symbol= self.inputSS.text(),
            constant_symbol= self.inputCS.text(),
        )

        img = qrcode.make(code)

        image = ImageQt.ImageQt(img)
        self.imgQR = QImage(image)
        self.pixmap = QPixmap.fromImage(self.imgQR)
        self.labelQR.setPixmap(self.pixmap)

        self.copyBtn.setVisible(True)
        self.saveBtn.setVisible(True)

       
    def copyQR(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.pixmap)
    
    def saveQR(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;All Files(*.*) ")
        if filePath == "":
            return
        self.pixmap.save(filePath)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #Checks if config file is not missing and whether it contains valid options
    errCode = configChecker()

    if errCode > 0:
        msg = QMessageBox()
        msg.setWindowTitle("Missing config data")
        if errCode == 1:
            msg.setText("Config file was not found.\n A new config file has been created.")
        elif errCode == 2:
            msg.setText("Some (or all) of config data not found.\n Account data were updated to default settings.")
        x = msg.exec() 

    window = UI()

    app.exec()