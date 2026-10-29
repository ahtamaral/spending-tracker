use crate::models::Attachment;

pub struct Statement {
    pub message_id: String,
    pub date: String,
    pub subject: String,
    pub attachments: Vec<Attachment>,
}
