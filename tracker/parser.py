import pandas as pd
import datetime
import matplotlib.pyplot as plt
import transaction as t
import math
import os


def parse(account_feed, card_statements, dataVeracity):
    # print(account_feed)
    # print(card_statements)

    dfDebit = pd.DataFrame(account_feed)
    dfCredit = pd.DataFrame(card_statements)

    transactions = []

    # # DEBITO
    for row in range(len(dfDebit)):
        de = dfDebit.iloc[row]

        d = de["postDate"].split("-")
        date = datetime.date(int(d[0]),int(d[1]),int(d[2]))

        if math.isnan(de["amount"]):
            # DEFINIR VALUE POR REGEX

            valueIndex = str(de["detail"]).find("R$")
            if valueIndex != -1:
                value = float(str(de["detail"])[valueIndex + 2:].strip(" ").replace(".", "").replace(",","."))
            else:
                value = 0.0
        else:
            value = float(de["amount"])

        i = de["detail"].find("R$")
        type = ""
        description = ""


        account = True
        if i < 2 and i >= 0:
            type = "Revenue"
            description = de["title"]
            if description == "Dinheiro resgatado" or description == "Dinheiro guardado":
                # print("Neutral transaction.")
                account = False

        else:
            type = "Debit expense"
            description=de["detail"]
        # print(value)

        dt = t.transaction(description, type, value, date)
        # ct.print()
        if account:
            transactions += [dt]

    # CREDITO   
    for row in range(len(dfCredit)):
        ce = dfCredit.iloc[row]
        date = datetime.date(int(ce["time"].split("-")[0]),int(ce["time"].split("-")[1]),int(ce["time"].split("-")[2].split("T")[0]))

        value = float(str(ce["amount"])[0:-2] + "." + str(ce["amount"])[-2:])

        ct = t.transaction(ce["description"], "Credit expense", value, date)
        # dt.print("row")
        transactions += [ct]

    soma = 0.0
    
    today = datetime.date.today()
    filename = "../data/" + str(today) + "/" + dataVeracity + "/csv"
    os.system("mkdir -p " + filename)
    filename += "/history.csv"

    with open(filename, "w") as fp:
        print("Writing CSV history to " + filename)
        for tr in transactions:
            # tr.print("csv")

            # print("{0},{1},{2},{3}".format(tr.description, tr.type, tr.value, tr.date))
            fp.write("{0}?{1}?{2}?{3}\n".format(tr.description, tr.type, str(tr.value).replace(".",","), tr.date))

            # soma += tr.value
        # print(soma)
        
