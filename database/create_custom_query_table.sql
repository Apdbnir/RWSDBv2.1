-- Create custom_query table for query logging (if needed by triggers)
CREATE TABLE IF NOT EXISTS public.custom_query (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    execution_time_ms INTEGER,
    result_count INTEGER
);

-- Add comment
COMMENT ON TABLE public.custom_query IS 'Query execution history log';
