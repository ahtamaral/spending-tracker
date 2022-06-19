import gspread
import datetime
import transactions as t
import utils

# Carrega as transações nas duas listas.
# Cria uma lista do mês desejado -> Por exemplo, 06, junta os gastos de débito e crédito em uma lista só.
# Ordena os gastos em ordem crescente de dia.
# Cria uma worksheet do mês e escreve os dados formatados nela.

card_statements_filename = "../data/card_statements_18-06-2022/raw.json"
account_feed_filename = "../data/account_feed_18-06-2022/raw.json"
myTransactions = t.getMyTransactions(card_statements_filename, account_feed_filename);


sa = gspread.service_account()
sh = sa.open("Pynubank")

yearList = [2020, 2021, 2022]
month = 5

# Creating all worksheets
for year in yearList:
    for month in range(1,13):
        currentMonth = datetime.date(year,month,1).month
        currentYear = datetime.date(year,month,1).year
        currentMonthName = utils.getMonthString(month)
        wksTitle = str(year) + "/" + currentMonthName
        try:
            1+1
            #wks = sh.add_worksheet(title=wksTitle, rows="200", cols="20")
        except:
            print("Worksheet already exists.")
            #wks = sh.worksheet(wksTitle)
        print(wksTitle)

# Ordering transactions by month
        monthlyTransactions = []

        for i in myTransactions["credit"]:
            if (i.date.year == currentYear) and (i.date.month == currentMonth):
                monthlyTransactions += [i]

        for i in myTransactions["debit"]:
            if (i.date.year == currentYear) and (i.date.month == currentMonth):
                monthlyTransactions += [i]

        monthlyTransactions.sort(key = lambda x: x.date, reverse=False)

        spreadData = []
        transactionData = []

        for i in monthlyTransactions:
            if str(type(i)) == "<class 'transactions.CreditTransaction'>":
                #print("[CREDITO] " + str(i.date))
                transactionData = [i.description, "Crédito",  i.amount, str(i.date)]
            else:
                #print("[DEBITO] " + str(i.date))
                transactionData = ["[" + i.typename + "] " + i.title, "Débito", i.detail, str(i.date)]
                spreadData += [transactionData]
            print(transactionData)  
        nRows = len(spreadData)
        spreadRange = "A1:D" + str(nRows)
        print(spreadRange)
        print("------------------")

'''
spreadData = []
transactionData = []

for i in monthlyTransactions:
    if str(type(i)) == "<class 'transactions.CreditTransaction'>":
        transactionData = [i.description, "Crédito",  i.amount, str(i.date)]
    else:
        transactionData = ["[" + i.typename + "] " + i.title, "Débito", i.detail, str(i.date)]
    spreadData += [transactionData]
    print(transactionData)

nRows = len(spreadData)
spreadRange = "A1:D" + str(nRows)
print(spreadRange)

#wks.update(spreadRange, spreadData)'''
