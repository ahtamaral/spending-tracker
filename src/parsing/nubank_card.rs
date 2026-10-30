use super::money::parse_cents;
use super::parser::Parser;
use crate::models::{AccountType, FinancialInstitution, Transaction};
use chrono::NaiveDate;
use csv::StringRecord;
use std::error::Error;

pub struct NubankCardParser;

impl Parser for NubankCardParser {
    fn header(&self) -> &'static str {
        "date,title,amount"
    }

    fn row(
        &self,
        record: &StringRecord,
        source_message_id: &str,
    ) -> Result<Transaction, Box<dyn Error>> {
        Ok(Transaction {
            institution: FinancialInstitution::Nubank,
            account_type: AccountType::CreditCard,
            date: NaiveDate::parse_from_str(&record[0], "%Y-%m-%d")?,
            time: None,
            description: record[1].to_string(),
            amount_cents: -parse_cents(&record[2])?,
            external_id: None,
            source_message_id: source_message_id.to_string(),
            category_id: None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_card_rows_with_inverted_sign() {
        let csv = "date,title,amount\n\
                   2026-10-25,Metro Rj,\"7,90\"\n\
                   2026-10-15,Pagamento recebido,\"- 1.528,26\"\n\
                   2026-10-11,Lojas Americanas,\"1.414,97\"\n";
        let transactions = NubankCardParser.parse(csv, "<msg-1>").unwrap();
        assert_eq!(transactions.len(), 3);
        assert_eq!(transactions[0].amount_cents, -790);
        assert_eq!(transactions[0].date, NaiveDate::from_ymd_opt(2026, 10, 25).unwrap());
        assert_eq!(transactions[1].amount_cents, 152826);
        assert_eq!(transactions[2].amount_cents, -141497);
        assert_eq!(transactions[0].source_message_id, "<msg-1>");
        assert!(matches!(transactions[0].account_type, AccountType::CreditCard));
    }

    #[test]
    #[ignore]
    fn parses_local_sample() {
        let csv = std::fs::read_to_string("samples/extrato_exemplo_cartao_nubank.csv").unwrap();
        assert_eq!(NubankCardParser.parse(&csv, "<msg-1>").unwrap().len(), 39);
    }
}
