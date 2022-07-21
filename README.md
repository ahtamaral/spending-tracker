# Spending-tracker

* Programa que automatiza o gerenciamento da minha vida financeira utilizando a API do Nubank para Python.

# Objetivos

* O principal objetivo desse projeto é automatizar o trabalho que eu fazia ao carregar
meus gastos mensais numa planilha do google sheets.
* A princípio, gostaria de acompanhar em tempo real o quanto eu já gastei no mês, tanto
no crédito quanto no débito.
* Os gastos serão divididos por mês, estritamente. Os meses que já se passaram
ficarão estáticos como um histórico. Os dados do mês atual serão sempre atualizados
ao dar um fetch na API.
* Isso serve tanto para crédito quanto para débito.

# Schema da transação.

(description, type, value, date)

* "description": String descritiva do que foi a transação. Dífícil de tratar, pois o modelo varia
bastante entre as transações.
* "type": Descreve qual a natureza da transação. Assume os seguintes valores:
    * "debit expense"
    * "credit expense"
    * "revenue"
* "value": Valor da transação. São armazenados como inteiros para fazer as contas sem perda de precisão.
Porem na hora de renderizar o inteiro é formatado para leitura humana como "R$123,45".
* "date": Data da transação. Utilizada para categorizá-las em meses diferentes.

# Componentes

* Fetcher [?]:
    * input: CPF, senha e certificado P2. 
    * output: Arquivo com outputs das transações (Crédito e débito).
    * Funcionamento:
        * Recebe CPF, senha e certificado do usuário para realizar autenticação na API.
        * Verifica quando foi a última chamada da API. Medida de segurança para não bloquear a nuconta do usuário.
        * Realiza a chamada da API para pegar todas as transações. Esses dados estão desorganizados, por isso serão
    passados para o parser formatar no esquema de transação definido.
* Parser [?]:
    * input: Arquivo com outputs das transações (Crédito e débito).
    * output: Lista com objetos "transaction", que seguem o schema definido acima.
    * Funcionamento:    
        * Recebe o arquivo cru com o JSON de transações. Usando bibliotecas, faz o parse para do JSON em memória.
        * Outra parte desse código recebe esse JSON e realiza o tratamento para ficar no formato definido no schema.
* Tracker [?]:
    * input:  Lista com objetos "transaction".
    * output: Análise da lista de gastos recebida.

# Considerações:

* O idioma servido para o usuário será inglês.
* O código será escrito em inglês.