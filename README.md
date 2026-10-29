# spending-tracker
Automatic ingestion of bank statements and categorization of expenses.

## Setup

1. Install [Rust](https://rustup.rs) and, on Ubuntu, `sudo apt install libssl-dev pkg-config`.
2. Create a Gmail [app password](https://myaccount.google.com/apppasswords) (requires 2-step verification).
3. Create a `.env` in the project root:

```
GMAIL_PESSOAL_USER=you@gmail.com
GMAIL_PESSOAL_APP_PASSWORD=xxxx xxxx xxxx xxxx
NUBANK_MAILBOX=GMAIL_PESSOAL
FLASH_MAILBOX=GMAIL_PESSOAL
```

Each `*_MAILBOX` names the mailbox (`<NAME>_USER` / `<NAME>_APP_PASSWORD`) where that institution's statements arrive.

## Run

```
cargo run     # fetch statements and print transactions
cargo test    # unit tests
```
