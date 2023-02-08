from configparser import ConfigParser
import os.path

#Opens config file for further manipulation
def openConfig():
    file='config.ini'
    cfg = ConfigParser()
    cfg.read(file)
    return cfg, file

#Returns details of stored account
def getAccount():

    cfg, file = openConfig()

    accName = 'Account'
    details = [ cfg[accName]['iban'],
                cfg[accName]['swift'],
                cfg[accName]['currency']
              ]    
    return details

#Updates config file with given data
def setAccount(IBAN, SWIFT, cur):

    accName = 'Account'

    cfg, file = openConfig()
   
    cfg.set(accName, 'iban', IBAN)
    cfg.set(accName, 'swift', SWIFT)
    cfg.set(accName, 'currency', cur)

    with open(file, 'w') as config:
        cfg.write(config)

#Updates config with default data (if file is missing or corrupted)
def writeDefaultConfig(cfg):
    
    cfg['Account'] = {
        'iban' : 'SK8011000000002934476335',
        'swift' : 'TATRSKBX',
        'currency' : 'EUR'
    }

    with open("config.ini", "w") as f:
        cfg.write(f)

#Checks if config data are present and valid
def configChecker():

    if  not os.path.exists('config.ini'):

        cfg = ConfigParser()
        writeDefaultConfig(cfg)
        return 1
        
    else:

        cfg, file = openConfig()
        accName = "Account"

        if not cfg.has_section(accName):
            writeDefaultConfig(cfg)
            return 2

        elif not cfg.has_option(accName,'iban') or not cfg.has_option(accName,'swift') or not cfg.has_option(accName,'currency'): 
            writeDefaultConfig(cfg)
            return 2

    return 0