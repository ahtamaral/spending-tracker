INSERT INTO categories (name, counts_in_totals)
SELECT name, counts_in_totals FROM (
    SELECT 'Mercado' AS name, 1 AS counts_in_totals
    UNION ALL SELECT 'Bares e restaurantes', 1
    UNION ALL SELECT 'Transporte', 1
    UNION ALL SELECT 'Compras', 1
    UNION ALL SELECT 'Lazer e eventos', 1
    UNION ALL SELECT 'Saúde e bem-estar', 1
    UNION ALL SELECT 'Viagem', 1
    UNION ALL SELECT 'Dívidas e encargos', 0
    UNION ALL SELECT 'Transferência interna', 0
    UNION ALL SELECT 'Receita', 1
    UNION ALL SELECT 'Outros', 1
)
WHERE NOT EXISTS (SELECT 1 FROM categories);
