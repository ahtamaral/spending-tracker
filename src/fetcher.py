''' Fetcher logic:

* Checa se existe o arquivo "../data/cert.p12"
    Se não existe, invoca o processo de criá-lo.
    Se existe, usa-o como parametro para fazer o fetch dos dados
* Checa data do último fetch.
    Se arquivo não existe, considera que nunca foi feito um fetch.
    Se fetch foi feito a menos de 2 dias, impede a operação.
    Se não, realiza o fetch e disponibiliza os dados na pasta data.

'''

from pynubank import Nubank, MockHttpClient
import datetime, os, getpass

def fetch():

    print("Calling fetch().")

    # ---
    # Checking for p12 certificate

    print("Searching for p12 certificate as ../data/cert.p12...")

    if (os.path.exists("../data/cert.p12")):
        print("Found certificate!")
    else:
        print("Certificate not found. Please generate one thoroug pynubank CLI.")

    # ---


    # ---
    # Checking last fetch date.
    print("reading file ../data/lastFetch.txt")
    f = open("../data/lastFetch.txt", "r")
    lastFetchStr = f.read()
    f.close()
    print("Last Fetch: " + lastFetchStr)

    date = lastFetchStr.split('-')                      
    lastFetch = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    today = datetime.date.today()
    timeDelta = today - lastFetch 

    if timeDelta.days < 2:
        print("The last fetch was performed less than 2 days ago.")
        exit("Very recurring accesses to your account can block it for 72 hours. We will not proceed for safety.")

    # ---

    validCpf = False

    while not validCpf:
        print("Enter you CPF (Just numbers): ", end="")
        cpf = input()
        if len(cpf) != 11:
            print("Invalid CPF length. Try again.")
        else:
            if not cpf.isnumeric():
                print("Non numeric CPF. Try again.")
            else:
                print("Valid CPF.")
                validCpf = True

    nu_pass = getpass.getpass("Insira sua senha: ")

    # Fetching Nubank server.

    nu = Nubank(MockHttpClient())
    nu.authenticate_with_cert(cpf, nu_pass, "../data/cert.p12")
    
    f = open("../data/lastFetch.txt", "w")
    # Descomentar linha de baixo quando for utilizar pra valer.
    #f.write(str(today))
    f.write(str(today-datetime.timedelta(days=7))) # last fetch setado para 7 dias atrás. Para debug.
    f.close()

    account_feed = nu.get_account_feed()
    card_statements = nu.get_card_statements()

    account_feed_filename = "../data/" + str(today) + "/account_feed"
    card_statements_filename = "../data/" + str(today) + "/card_statements"

    os.system("mkdir -p " + account_feed_filename)
    os.system("mkdir -p " + card_statements_filename)

    account_feed_filename += "/raw.json"
    card_statements_filename += "/raw.json"

    os.system("touch " + account_feed_filename)
    os.system("touch " + card_statements_filename)

    # print(account_feed)
    # print(card_statements)

    print(account_feed_filename)
    print(card_statements_filename)

    os.system("echo " + str(account_feed) + " > " + account_feed_filename)
    os.system("echo " + str(card_statements) + " > " + card_statements_filename)

    return account_feed, card_statements