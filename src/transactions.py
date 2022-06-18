import json
import datetime

class CreditTransaction:

    def __init__(self, description, amount, date):
        self.description = description
        self.amount = amount
        self.formatedAmount = self.formatedAmount(amount)
        self.date = date

    @staticmethod
    def formatAmount(amount):
        amountStr = str(amount)
        reais = amountStr[:len(amountStr)-2]
        centavos = amountStr[len(amountStr)-1:]
        if len(centavos) < 2:
            centavos += '0'
        formatedAmount = "R${},{}".format(reais, centavos)
        return formatedAmount 
    
    def formatedAmount(self, amount):
        amountStr = str(amount)
        reais = amountStr[:len(amountStr)-2]
        centavos = amountStr[len(amountStr)-1:]
        if len(centavos) < 2:
            centavos += '0'
        formatedAmount = "R${},{}".format(reais, centavos)
        return formatedAmount 

class DebitTransaction:

    def __init__(self, typename, title, detail, date):
        self.typename = typename
        self.title = title
        self.detail = detail
        self.date = date
        
# Parses json file into a array of json strings.
# IN: The name of a file containing an array of Json Objects.
# OUT: A list of transaction objects.
'''
def loadCreditTransactions(transactionsFileName):

    chavesCount = 0
    transactions = []
    buff = ""
    appendChar = False
   
    transactionsFile = open(transactionsFileName, 'r')
    transactionsString = transactionsFile.read()
    transactionsFile.close()

    for char in transactionsString:
         
        if char == "{":
            chavesCount += 1
        if char == "}":
            chavesCount -= 1

        if chavesCount > 0:
            appendChar = True
        else:
            appendChar = False

        if appendChar:
            buff += char
        else:
            #print(buff)
            buff += '}' # Meio gambiarrado, mas funciona
            if len(buff) > 32:
                buff = buff.replace("'", '"').replace("True", "true").replace("False", "false")
                transaction = json.loads(buff)
                date = transaction["time"][:10].split('-')
                d = datetime.date(int(date[0]),int(date[1]),int(date[2])) 
                t = CreditTransaction(transaction["description"], transaction["amount"] ,d)
                transactions += [t]
            buff = ""

    return transactions
'''

def loadTransactions(transactionsFileName):

    chavesCount = 0
    transactions = []
    buff = ""
    appendChar = False
   
    transactionsFile = open(transactionsFileName, 'r')
    transactionsString = transactionsFile.read()
    transactionsFile.close()
    
    for char in transactionsString:
        if char == "{":
            chavesCount += 1
        if char == "}":
            chavesCount -= 1

        if chavesCount > 0:
            appendChar = True
        else:
            appendChar = False
        
        if appendChar:
            buff += char
        else:
            buff += "}"
            if len(buff) > 32:
                buff = buff.replace("'", '"').replace("\\xa","").replace("None", '"None"').replace("True", "true").replace("False", "false")
                #print(buff + "\n\n")
                try:
                    transaction = json.loads(buff)
                    transactions += [transaction]
                except:
                    print("Error converting string to Json. The transactions list will be incomplete.")
            buff = ""
            
    return transactions

def getMyTransactions():

    creditTransactions = []
    transactions = loadTransactions("../data/card_statements_18-06-2022/formated.json")

    for t in transactions:
        date = t["time"][:10].split('-')                      
        d = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        ct = CreditTransaction(t["description"], t["amount"], d) 
        creditTransactions += [ct]


    debitTransactions = []
    transactions = loadTransactions("../data/account_feed_18-06-2022/raw.json")
    for t in transactions:
        date = t["postDate"].split('-')                      
        d = datetime.date(int(date[0]),int(date[1]),int(date[2]))
        dt = DebitTransaction(t["__typename"], t["title"], t["detail"], d)
        debitTransactions += [dt]

    myTransactions = {
        "credit": creditTransactions,
        "debit": debitTransactions
    }

    return myTransactions
