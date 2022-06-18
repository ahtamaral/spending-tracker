import transactions as t

card_statements_filename = "../data/card_statements_18-06-2022/raw.json"
account_feed_filename = "../data/account_feed_18-06-2022/raw.json"
myTransactions = t.getMyTransactions(card_statements_filename, account_feed_filename);

for i in myTransactions["credit"]:
    print("{0: <32}{1: <10}{2: <24}".format(i.description, i.amount, str(i.date)))
print("-----\n")

for i in myTransactions["debit"]:
    print("{0: <32}{1: <32}{2: <40}{3: <8}".format(i.typename, i.title, i.detail ,str(i.date)))

print(len(myTransactions["debit"]))
print(len(myTransactions["credit"]))
