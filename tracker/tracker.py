
from dataclasses import dataclass
import os

import fetcher as fetcher
import parser as parser
#import loadTransactions as lt

# Global variables
version = 0.1

if __name__ == "__main__":

    os.system("mkdir -p ../data")
    os.system("touch ../data/lastFetch.txt")
    # os.system("echo 2000-01-01 > ../data/lastFetch.txt")

    print("-----------------------\n Nubank Spending Tracker v{}".format(version))
    print("\n\tAutomatically monitor your credit and debit card spending on your Nubank account.")
    print("\tAuthor: Artur Amaral\n-----------------------")

    account_feed, card_statements, dataVeracity = fetcher.fetch()

    parser.parse(account_feed, card_statements, dataVeracity)
