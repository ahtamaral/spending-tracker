mod ingestion;
mod models;
mod parsing;
mod storage;

use models::{FinancialInstitution, Statement, Transaction};
use std::error::Error;
use storage::Connection;

fn transactions(statement: &Statement) -> Result<Vec<Transaction>, Box<dyn Error>> {
    let mut all = Vec::new();
    for attachment in &statement.attachments {
        if !attachment.name.ends_with(".csv") {
            continue;
        }
        let csv_text = std::str::from_utf8(&attachment.content)?;
        match parsing::parse(csv_text, &statement.message_id) {
            Ok(parsed) => all.extend(parsed),
            Err(e) => eprintln!("ignorado {}: {e}", attachment.name),
        }
    }
    Ok(all)
}

fn ingest(db: &Connection, institution: FinancialInstitution) -> Result<(), Box<dyn Error>> {
    for statement in ingestion::fetch_statements(institution)? {
        for t in transactions(&statement)? {
            storage::insert(db, &t)?;
            println!(
                "{:?} | {} | {:>9.2} | {}",
                t.institution,
                t.date,
                t.amount_cents as f64 / 100.0,
                t.description
            );
        }
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    let db = storage::open()?;
    for institution in [FinancialInstitution::Nubank, FinancialInstitution::Flash] {
        ingest(&db, institution)?;
    }
    Ok(())
}
