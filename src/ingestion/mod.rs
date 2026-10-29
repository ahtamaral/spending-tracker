mod rules;

use crate::models::{Attachment, FinancialInstitution, Statement};
use mailparse::{DispositionType, MailHeaderMap, ParsedMail, parse_mail};
use std::env;
use std::error::Error;

const HOST: &str = "imap.gmail.com";

fn attachments(mail: &ParsedMail) -> Result<Vec<Attachment>, Box<dyn Error>> {
    let mut found = Vec::new();
    for part in &mail.subparts {
        found.extend(attachments(part)?);
    }
    let disposition = mail.get_content_disposition();
    if disposition.disposition == DispositionType::Attachment {
        found.push(Attachment {
            name: disposition.params.get("filename").cloned().unwrap_or_default(),
            content: mail.get_body_raw()?,
        });
    }
    Ok(found)
}

pub fn fetch_statements(institution: FinancialInstitution) -> Result<Vec<Statement>, Box<dyn Error>> {
    dotenvy::dotenv()?;
    let mailbox = env::var(rules::mailbox_var(institution))?;
    let user = env::var(format!("{mailbox}_USER"))?;
    let password = env::var(format!("{mailbox}_APP_PASSWORD"))?.replace(' ', "");

    let tls = native_tls::TlsConnector::builder().build()?;
    let client = imap::connect((HOST, 993), HOST, &tls)?;
    let mut session = client.login(user, password).map_err(|e| e.0)?;
    session.select("INBOX")?;

    let ids = session.search(rules::query(institution))?;
    if ids.is_empty() {
        session.logout()?;
        return Ok(Vec::new());
    }

    let seq: Vec<String> = ids.iter().map(|id| id.to_string()).collect();
    let mut statements = Vec::new();
    for message in session.fetch(seq.join(","), "BODY.PEEK[]")?.iter() {
        let Some(body) = message.body() else {
            continue;
        };
        let mail = parse_mail(body)?;
        statements.push(Statement {
            message_id: mail.headers.get_first_value("Message-ID").unwrap_or_default(),
            date: mail.headers.get_first_value("Date").unwrap_or_default(),
            subject: mail.headers.get_first_value("Subject").unwrap_or_default(),
            attachments: attachments(&mail)?,
        });
    }

    session.logout()?;
    Ok(statements)
}
