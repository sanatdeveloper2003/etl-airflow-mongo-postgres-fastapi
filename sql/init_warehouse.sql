CREATE TABLE IF NOT EXISTS public.items (
  id SERIAL PRIMARY KEY,
  name TEXT,
  value NUMERIC,
  loaded_at TIMESTAMP DEFAULT now()
);
