CREATE TABLE IF NOT EXISTS tickets (
    id                 BIGSERIAL PRIMARY KEY,
    ticket_id          TEXT UNIQUE NOT NULL,
    customer           TEXT,
    text               TEXT NOT NULL,
    intent             TEXT,
    confidence         NUMERIC(5, 4),
    priority           TEXT CHECK (priority IN ('High', 'Medium', 'Low')),
    needs_human_review BOOLEAN NOT NULL DEFAULT FALSE,
    route              TEXT NOT NULL,
    draft_reply        TEXT,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets (created_at);

CREATE OR REPLACE VIEW daily_summary AS
SELECT date_trunc('day', created_at) AS day,
       COALESCE(priority, 'Unclassified') AS priority,
       COUNT(*) AS tickets,
       SUM(CASE WHEN needs_human_review THEN 1 ELSE 0 END) AS sent_to_human_review,
       ROUND(AVG(confidence), 3) AS avg_confidence
FROM tickets
GROUP BY 1, 2
ORDER BY 1 DESC, 2;
