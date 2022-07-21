
import fetcher as fetcher
import os

# Global variables
version = 0.1

if __name__ == "__main__":

    os.system("mkdir -p ../data")

    print("-----------------------\n Nubank Spending Tracker v{}".format(version))
    print("\n\tAutomatically monitor your credit and debit card spending on your Nubank account.")
    print("\tAuthor: Artur Amaral\n-----------------------")

    fetcher.fetch()

