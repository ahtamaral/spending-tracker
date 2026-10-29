use super::money::parse_cents;
use super::parser::Parser;
use crate::models::{FinancialInstitution, Transaction};
use chrono::{NaiveDate, NaiveTime};
use csv::StringRecord;
use std::error::Error;

pub struct FlashParser;

impl Parser for FlashParser {
    fn header(&self) -> &'static str {
        "Data,Hora,Movimentação,Valor,Meio de Pagamento,Saldo"
    }

    fn row(
        &self,
        record: &StringRecord,
        source_message_id: &str,
    ) -> Result<Transaction, Box<dyn Error>> {
        Ok(Transaction {
            institution: FinancialInstitution::Flash,
            date: NaiveDate::parse_from_str(&record[0], "%d/%m/%Y")?,
            time: Some(NaiveTime::parse_from_str(&record[1], "%H:%M")?),
            description: record[2].to_string(),
            amount_cents: parse_cents(&record[3])?,
            external_id: None,
            source_message_id: source_message_id.to_string(),
            category: None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_flash_rows() {
        let csv = "Data,Hora,Movimentação,Valor,Meio de Pagamento,Saldo\n\
                   25/10/2026,01:35,PONTES PETISCO RIO DE JANEIR BRA,\"-R$ 51,15\",Cartão,\"R$ 350,39\"\n\
                   03/10/2026,23:20,CREDITO,\"R$ 1.200,00\",Cartão,\"R$ 1.067,74\"\n";
        let transactions = FlashParser.parse(csv, "<msg-1>").unwrap();
        assert_eq!(transactions.len(), 2);
        assert_eq!(transactions[0].source_message_id, "<msg-1>");
        assert_eq!(transactions[0].amount_cents, -5115);
        assert_eq!(transactions[0].date, NaiveDate::from_ymd_opt(2026, 10, 25).unwrap());
        assert_eq!(transactions[1].amount_cents, 120000);
    }

    #[test]
    #[ignore]
    fn parses_local_sample() {
        let csv = std::fs::read_to_string("samples/extrato_exemplo_flash.csv").unwrap();
        assert_eq!(FlashParser.parse(&csv, "<msg-1>").unwrap().len(), 22);
    }
}
