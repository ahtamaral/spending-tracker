use crate::models::Transaction;
use rusqlite::{Connection, params};
use std::error::Error;

pub fn insert(connection: &Connection, transaction: &Transaction) -> Result<(), Box<dyn Error>> {
    connection.execute(
        "INSERT INTO transactions
            (institution, account_type, date, time, description, amount_cents, external_id, source_message_id, category_id)
         VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9)",
        params![
            format!("{:?}", transaction.institution),
            format!("{:?}", transaction.account_type),
            transaction.date.to_string(),
            transaction.time.map(|time| time.to_string()),
            transaction.description,
            transaction.amount_cents,
            transaction.external_id,
            transaction.source_message_id,
            transaction.category_id,
        ],
    )?;
    Ok(())
}
