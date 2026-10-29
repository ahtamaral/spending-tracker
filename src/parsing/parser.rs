use crate::models::Transaction;
use csv::StringRecord;
use std::error::Error;

pub trait Parser {
    fn header(&self) -> &'static str;

    fn row(
        &self,
        record: &StringRecord,
        source_message_id: &str,
    ) -> Result<Transaction, Box<dyn Error>>;

    fn parse(
        &self,
        csv_text: &str,
        source_message_id: &str,
    ) -> Result<Vec<Transaction>, Box<dyn Error>> {
        let mut reader = csv::Reader::from_reader(csv_text.as_bytes());
        let mut transactions = Vec::new();
        for record in reader.records() {
            transactions.push(self.row(&record?, source_message_id)?);
        }
        Ok(transactions)
    }
}
