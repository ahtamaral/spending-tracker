use crate::models::{AccountType, FinancialInstitution};
use chrono::{NaiveDate, NaiveTime};

#[derive(Debug)]
pub struct Transaction {
    pub institution: FinancialInstitution,
    pub account_type: AccountType,
    pub date: NaiveDate,
    pub time: Option<NaiveTime>,
    pub description: String,
    pub amount_cents: i64,
    pub external_id: Option<String>,
    pub source_message_id: String,
    pub category_id: Option<i64>,
}
