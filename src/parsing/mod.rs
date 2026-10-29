mod flash;
mod money;
mod nubank_account;
mod nubank_card;
mod parser;

use crate::models::Transaction;
use flash::FlashParser;
use nubank_account::NubankAccountParser;
use nubank_card::NubankCardParser;
use parser::Parser;
use std::error::Error;

const PARSERS: &[&dyn Parser] = &[&FlashParser, &NubankCardParser, &NubankAccountParser];

pub fn parse(csv_text: &str, source_message_id: &str) -> Result<Vec<Transaction>, Box<dyn Error>> {
    let header = csv_text.trim_start_matches('\u{feff}').lines().next().unwrap_or_default();
    let Some(parser) = PARSERS.iter().find(|p| p.header() == header) else {
        return Err(format!("formato de CSV desconhecido: {header}").into());
    };
    parser.parse(csv_text, source_message_id)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn picks_parser_by_header() {
        let csv = "date,title,amount\n2026-10-25,Metro Rj,\"7,90\"\n";
        assert_eq!(parse(csv, "<msg-1>").unwrap()[0].amount_cents, -790);
    }

    #[test]
    fn rejects_unknown_header() {
        assert!(parse("foo,bar\n1,2\n", "<msg-1>").is_err());
    }
}
