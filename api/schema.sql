-- Highscores table schema for Vercel Postgres
-- Run this in your Vercel Postgres Query tab

-- Create the highscores table
CREATE TABLE IF NOT EXISTS highscores (
    id SERIAL PRIMARY KEY,
    level_name VARCHAR(100) NOT NULL,
    player_name VARCHAR(50) NOT NULL,
    total_score INTEGER NOT NULL,
    time_score INTEGER NOT NULL,
    trophy_score INTEGER NOT NULL,
    damage_score INTEGER NOT NULL,
    life_score INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries by level and score
CREATE INDEX IF NOT EXISTS idx_highscores_level_score 
ON highscores(level_name, total_score DESC);

-- Create index for timestamp queries
CREATE INDEX IF NOT EXISTS idx_highscores_timestamp 
ON highscores(timestamp DESC);

-- Verify the table was created
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'highscores' 
ORDER BY ordinal_position;
