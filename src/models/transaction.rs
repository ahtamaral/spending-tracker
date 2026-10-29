use crate::models::FinancialInstitution;
use chrono::{NaiveDate, NaiveTime};

#[derive(Debug)]
pub struct Transaction {
    pub institution: FinancialInstitution,
    pub date: NaiveDate,
    pub time: Option<NaiveTime>,
    pub description: String,
    pub amount_cents: i64,
    pub external_id: Option<String>,
    pub source_message_id: String,
    pub category: Option<String>,
}
