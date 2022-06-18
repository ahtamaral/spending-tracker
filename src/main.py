import transactions as t

myTransactions = t.getMyTransactions();

for i in myTransactions["credit"]:
    print(i.description)
    print(i.amount)
    print(i.date)
    print("-----\n")

for i in myTransactions["debit"]:
    print(i.typename)
    print(i.title)
    print(i.detail)
    print(i.date)
    print("-----\n")

print(len(myTransactions["debit"]))
print(len(myTransactions["credit"]))
