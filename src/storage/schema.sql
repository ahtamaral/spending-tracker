CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    counts_in_totals INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    institution TEXT NOT NULL,
    account_type TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT,
    description TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    external_id TEXT,
    source_message_id TEXT NOT NULL,
    category_id INTEGER REFERENCES categories(id)
);
