-- PostgreSQL schema for invoice-analysis-poc task/session store
-- Applied against the postgres database on first startup.

CREATE TABLE IF NOT EXISTS invoice_poc_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_query TEXT NOT NULL,
    final_report TEXT,
    completed_at TIMESTAMP
    WITH
        TIME ZONE,
        started_at TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoice_poc_tasks (
    task_id VARCHAR(255) PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    source_agent VARCHAR(100) NOT NULL,
    target_agent VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    created_at TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inv_tasks_session ON invoice_poc_tasks (session_id);

CREATE INDEX IF NOT EXISTS idx_inv_tasks_state ON invoice_poc_tasks (state);

CREATE TABLE IF NOT EXISTS invoice_poc_messages (
    message_id VARCHAR(255) PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL REFERENCES invoice_poc_tasks (task_id),
    role VARCHAR(50) NOT NULL,
    parts_json TEXT NOT NULL,
    timestamp TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_inv_messages_task ON invoice_poc_messages (task_id);

CREATE TABLE IF NOT EXISTS invoice_poc_artifacts (
    artifact_id VARCHAR(255) PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL REFERENCES invoice_poc_tasks (task_id),
    name VARCHAR(255) NOT NULL,
    parts_json TEXT NOT NULL,
    created_at TIMESTAMP
    WITH
        TIME ZONE NOT NULL DEFAULT NOW()
);