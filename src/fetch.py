'''
* Pede login para o usuário: CPF, senha e path do certificado.
* Verifica a última vez que a API foi chamada para a conta real.
    * Lê arquivo lastFetch.txt
    * Se for menor que 1 dia, barra a requisição.
* Cria a seguinte estrutura de diretórios:
    - data
        - 2022-06-21
            - account_feed
                - raw.json
                - formated.json
            - card_statements
                - raw.json
                - formated.json


# Por enquanto, a operação de fetch vai ser desacoplada do carregamento em memória dos dados.
# TBD:
    * Como automatizar a passagem do nome dos novos arquivos para o consumidor?
    * Como formatar o Json? ("Pretty print") -> Provavelmente não vale a pena agora.
'''

import getpass, datetime, os
from pynubank import Nubank, MockHttpClient

f = open("lastFetch.txt", "r")
lastFetchStr = f.read()
f.close()

date = lastFetchStr.split('-')                      
lastFetch = datetime.date(int(date[0]),int(date[1]),int(date[2]))
today = datetime.date.today()
timeDelta = today - lastFetch 

print("Last fetch: " + str(lastFetch))
print("Today:" + str(today))
print("Time since last fetch: " + str(timeDelta))

if timeDelta.days < 2:
    print("Ultimo fetch foi muito recente. Abortaremos por segurança.")
    exit()

print("Insira seu CPF: ", end="")
cpf = input()
nu_pass = getpass.getpass("Insira sua senha: ")
print("Insira o path do certificado: ", end="")
cert_path = input()

nu = Nubank(MockHttpClient())
#nu = Nubank()

nu.authenticate_with_cert(cpf, nu_pass, cert_path)

f = open("lastFetch.txt", "w")
# Descomentar linha de baixo quando for utilizar pra valer.
#f.write(str(today))
f.write(str(today-datetime.timedelta(days=7)))
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

print(account_feed)
print(card_statements)

print(account_feed_filename)
print(card_statements_filename)


os.system("echo " + str(account_feed) + " > " + account_feed_filename)
os.system("echo " + str(card_statements) + " > " + card_statements_filename)
