from pynubank import Nubank, MockHttpClient
import os

CPF = os.getenv('CPF')
NU_PASS = os.getenv('NU_PASS')
CERT_PATH = os.getenv('CERT_PATH')

nu = Nubank(MockHttpClient())
#nu = Nubank()

nu.authenticate_with_cert(CPF, NU_PASS, CERT_PATH)

account_balance = nu.get_account_balance()
card_statements = nu.get_card_statements()

print(account_balance)
print(card_statements)

# Essa linha funciona porque não estamos chamando o servidor do Nubank.

# Qualquer método chamado não passará pelo Nubank e terá o retorno instantâneo.
