mod transactions;

pub use rusqlite::Connection;
pub use transactions::insert;
use std::env;
use std::error::Error;

const DEFAULT_PATH: &str = "spending-tracker.db";

pub fn open() -> Result<Connection, Box<dyn Error>> {
    dotenvy::dotenv().ok();
    let path = env::var("DATABASE_PATH").unwrap_or_else(|_| DEFAULT_PATH.to_string());
    let connection = Connection::open(path)?;
    connection.pragma_update(None, "foreign_keys", true)?;
    connection.execute_batch(include_str!("schema.sql"))?;
    connection.execute_batch(include_str!("seed_categories.sql"))?;
    Ok(connection)
}
