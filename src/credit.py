from transactions import loadCreditTransactions, CreditTransaction

transactions = loadCreditTransactions("../data/card_statements_18-06-2022/formated.json");
currentMonth = transactions[0].date.month
totalExpenses = 0

## Fazer função estática na classe transactions para converter amount de inteiro para uma
## string legível

for i in transactions:
    
    formatedAmount = i.formatedAmount
    totalExpenses += i.amount
    if (i.date.month == currentMonth):
        print("{0: <32}{1: <10}{2: <24}".format(i.description, formatedAmount, str(i.date)))
    else:
        print("\nMonth has changed! Expenses in the month: " + str(CreditTransaction.formatAmount(totalExpenses)))
        print(50 * '-' + '\n')
        print("{0: <32}{1: <10}{2: <24}".format(i.description, formatedAmount, str(i.date)))
        currentMonth = i.date.month
        totalExpenses = 0
