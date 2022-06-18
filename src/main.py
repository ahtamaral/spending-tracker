from parse import loadTransactions, Transaction

transactions = loadTransactions("../data/real-data.json");
currentMonth = transactions[0].date.month
totalExpenses = 0
print(currentMonth)

## Fazer função estática na classe transactions para converter amount de inteiro para uma
## string legível

for i in transactions:

    formatedAmount = i.formatedAmount
    print("{0: <32}{1: <10}{2: <24}".format(i.description, formatedAmount, str(i.date)))
    totalExpenses += i.amount
    if (i.date.month != currentMonth):
        print(str(i.date.month) + "!=" + str(currentMonth))
        print("Month has changed! Expenses in the month: " + str(Transaction.formatAmount(totalExpenses)))
        print(50 * '-' + '\n')
        currentMonth = i.date.month
        totalExpenses = 0
