use crate::models::FinancialInstitution;

struct FetchRule {
    from: &'static str,
    subjects: &'static [&'static str],
}

fn rule(institution: FinancialInstitution) -> FetchRule {
    match institution {
        FinancialInstitution::Nubank => FetchRule {
            from: "nubank",
            subjects: &["Extrato da fatura", "Extrato da sua conta do Nubank"],
        },
        FinancialInstitution::Flash => FetchRule {
            from: "flash",
            subjects: &["Seu extrato Flash chegou!"],
        },
    }
}

pub fn query(institution: FinancialInstitution) -> String {
    let rule = rule(institution);
    let mut subjects = rule.subjects.iter().rev().map(|s| format!("SUBJECT \"{s}\""));
    let mut criteria = subjects.next().unwrap_or_default();
    for subject in subjects {
        criteria = format!("OR {subject} {criteria}");
    }
    format!("FROM \"{}\" {criteria}", rule.from)
}

pub fn mailbox_var(institution: FinancialInstitution) -> &'static str {
    match institution {
        FinancialInstitution::Nubank => "NUBANK_MAILBOX",
        FinancialInstitution::Flash => "FLASH_MAILBOX",
    }
}
