use std::error::Error;

pub fn parse_cents(value: &str) -> Result<i64, Box<dyn Error>> {
    let digits: String = value.chars().filter(|c| c.is_ascii_digit()).collect();
    let cents: i64 = digits.parse()?;
    Ok(if value.starts_with('-') { -cents } else { cents })
}
