use super::money::parse_cents;
use super::parser::Parser;
use crate::models::{AccountType, FinancialInstitution, Transaction};
use chrono::NaiveDate;
use csv::StringRecord;
use std::error::Error;

pub struct NubankAccountParser;

impl Parser for NubankAccountParser {
    fn header(&self) -> &'static str {
        "Data,Valor,Identificador,Descrição"
    }

    fn row(
        &self,
        record: &StringRecord,
        source_message_id: &str,
    ) -> Result<Transaction, Box<dyn Error>> {
        Ok(Transaction {
            institution: FinancialInstitution::Nubank,
            account_type: AccountType::BankAccount,
            date: NaiveDate::parse_from_str(&record[0], "%d/%m/%Y")?,
            time: None,
            description: record[3].to_string(),
            amount_cents: parse_cents(&record[1])?,
            external_id: Some(record[2].to_string()),
            source_message_id: source_message_id.to_string(),
            category_id: None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_account_rows() {
        let csv = "Data,Valor,Identificador,Descrição\n\
                   02/10/2026,-64.50,id-1,Transferência enviada pelo Pix - FULANO\n\
                   05/10/2026,1234.00,id-2,Crédito em conta\n";
        let transactions = NubankAccountParser.parse(csv, "<msg-1>").unwrap();
        assert_eq!(transactions.len(), 2);
        assert_eq!(transactions[0].amount_cents, -6450);
        assert_eq!(transactions[0].date, NaiveDate::from_ymd_opt(2026, 10, 2).unwrap());
        assert_eq!(transactions[0].external_id.as_deref(), Some("id-1"));
        assert!(matches!(transactions[0].account_type, AccountType::BankAccount));
        assert_eq!(transactions[1].amount_cents, 123400);
    }

    #[test]
    #[ignore]
    fn parses_local_sample() {
        let csv = std::fs::read_to_string("samples/extrato_exemplo_conta_nubank.csv").unwrap();
        assert_eq!(NubankAccountParser.parse(&csv, "<msg-1>").unwrap().len(), 29);
    }
}
