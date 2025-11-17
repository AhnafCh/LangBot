-- Supabase Database Setup for RAG System with pgvector
-- Run this in your Supabase SQL Editor

-- 1. Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create documents table
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    document_id TEXT UNIQUE NOT NULL,
    filename TEXT NOT NULL,
    file_hash TEXT UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    chunk_count INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create document_chunks table with vector column
CREATE TABLE IF NOT EXISTS document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(document_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI embeddings are 1536 dimensions
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);

-- 4. Create index on embedding column for faster similarity search
CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx 
ON document_chunks 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 5. Create index on document_id for faster joins
CREATE INDEX IF NOT EXISTS document_chunks_document_id_idx 
ON document_chunks(document_id);

-- 6. Create index on file_hash for duplicate detection
CREATE INDEX IF NOT EXISTS documents_file_hash_idx 
ON documents(file_hash);

-- 7. Create function for similarity search
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding vector(1536),
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id BIGINT,
    document_id TEXT,
    chunk_index INTEGER,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        document_chunks.id,
        document_chunks.document_id,
        document_chunks.chunk_index,
        document_chunks.content,
        document_chunks.metadata,
        1 - (document_chunks.embedding <=> query_embedding) AS similarity
    FROM document_chunks
    ORDER BY document_chunks.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 8. Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. Create trigger for auto-updating updated_at
CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 10. Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

-- 11. Create policies for authenticated access
-- Allow all operations for authenticated users (adjust based on your needs)
CREATE POLICY "Enable all operations for authenticated users on documents"
ON documents FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "Enable all operations for authenticated users on document_chunks"
ON document_chunks FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

-- 12. Create policies for service role (your backend)
CREATE POLICY "Enable all operations for service role on documents"
ON documents FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Enable all operations for service role on document_chunks"
ON document_chunks FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- 13. Grant permissions
GRANT ALL ON documents TO authenticated, service_role;
GRANT ALL ON document_chunks TO authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated, service_role;

-- Verification queries (optional - run these to check setup)
-- SELECT COUNT(*) FROM documents;
-- SELECT COUNT(*) FROM document_chunks;
-- SELECT * FROM pg_extension WHERE extname = 'vector';
