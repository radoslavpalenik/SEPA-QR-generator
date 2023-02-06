from configparser import ConfigParser

def openConfig():
    file='config.ini'
    cfg = ConfigParser()
    cfg.read(file)
    return cfg, file


def getAccount():

    cfg, file = openConfig()

    accName = 'Account'
    details = [ cfg[accName]['iban'],
                cfg[accName]['swift'],
                cfg[accName]['currency']
              ]    
    return details

def setAccount(IBAN, SWIFT, cur):

    print(IBAN)
    print(SWIFT)
    print(cur)

    accName = 'Account'

    cfg, file = openConfig()
   
    cfg.set(accName, 'iban', IBAN)
    cfg.set(accName, 'swift', SWIFT)
    cfg.set(accName, 'currency', cur)

    with open(file, 'w') as config:
        cfg.write(config)