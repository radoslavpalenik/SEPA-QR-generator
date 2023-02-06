import sys

from PyQt6.QtWidgets import QApplication, QDialog, QPushButton
from PyQt6 import uic
from parser import getAccount
from parser import setAccount

class Dialog(QDialog):
    def setup(self):
        account = getAccount()

        currencyList = ['EUR','BGN','HRK','CZK','DKK',
                        'GIP','HUF','ISK','CHF','NOK',
                        'PLN','RON','SEK','CHF','GBP']
        for cur in currencyList:
            self.currency.addItem(cur)

        index = currencyList.index(account[2])


        self.IBAN.setText(account[0])
        self.SWIFT.setText(account[1])
        self.currency.setCurrentIndex(index)
    
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('dialog.ui', self) 
        
        self.updBtn.clicked.connect(self.updateAcc)
        
        self.setup()
    
    def updateAcc(self):
        setAccount(self.IBAN.text(), self.SWIFT.text(), self.currency.currentText())
        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    dialog = Dialog()
    dialog.show()

    app.exec()