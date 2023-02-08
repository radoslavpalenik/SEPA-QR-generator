import sys

from PyQt6.QtWidgets import QApplication, QDialog, QPushButton
from PyQt6 import uic
from parser import getAccount
from parser import setAccount

class Dialog(QDialog):
    currencyList = ['EUR','BGN','HRK','CZK','DKK',
                    'GIP','HUF','ISK','CHF','NOK',
                    'PLN','RON','SEK','CHF','GBP']

   
    def setup(self):
        account = getAccount()

        self.IBAN.setText(account[0])

        self.SWIFT.setText(account[1])

        actualCurrencies = self.currencyList.copy()

        storedCurrency =  account[2]
        
        #If config holds invalid currency, invalidate it in the next account update
        if storedCurrency not in actualCurrencies:
            self.invalidate(self.currency)
            self.currency.addItem(storedCurrency)
            actualCurrencies.insert(0, storedCurrency)

        #Gets list of supported currencies
        for cur in self.currencyList:
            self.currency.addItem(cur)

        index = actualCurrencies.index(storedCurrency)
        self.currency.setCurrentIndex(index)
    
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('dialog.ui', self) 

        self.updBtn.clicked.connect(self.updateAcc)
        self.IBAN.textChanged.connect(self.ipnutChecker)
        self.SWIFT.textChanged.connect(self.ipnutChecker)
        self.currency.currentIndexChanged.connect(self.ipnutChecker)

        self.setup()
        
        
    #Updates Account config
    def updateAcc(self):
        setAccount(self.IBAN.text(), self.SWIFT.text(), self.currency.currentText())
        self.close()

    #Checks if any of input data are invalid
    def ipnutChecker(self):

        ibanLen = len(self.IBAN.text())
        swiftLen = len(self.SWIFT.text())
        curType = self.currency.currentText()

        
        if ibanLen < 15 or swiftLen < 8 or swiftLen > 11 or curType not in self.currencyList:
            if ibanLen < 15:
                self.invalidate(self.IBAN)
            else:
                self.IBAN.setStyleSheet("border :none")
            if curType not in self.currencyList:
                self.invalidate(self.currency)
            else:
                self.currency.setStyleSheet("border :none")
            if swiftLen < 8 or swiftLen > 11:
                self.invalidate(self.SWIFT)
            else:
                self.SWIFT.setStyleSheet("border :none")
        else:
            #Fixes deleting border of the last invalid element after change
            self.IBAN.setStyleSheet("border :none")
            self.SWIFT.setStyleSheet("border :none")
            self.currency.setStyleSheet("border :none")

            self.updBtn.setStyleSheet("background-color: #00ADB5;color: #EEEEEE;")
            self.updBtn.setDisabled(False)

    #Forbids updating config while some of input data are not valid    
    def invalidate(self, field):
        field.setStyleSheet("border :3px solid red")
        self.updBtn.setStyleSheet("background-color: #303841;color: #7d7d7d")
        self.updBtn.setDisabled(True)
        
        
        


if __name__ == '__main__':

    app = QApplication(sys.argv)

    dialog = Dialog()
    dialog.show()

    app.exec()