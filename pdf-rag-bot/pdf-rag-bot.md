Project : "PDF Question Answering Bot (Mini RAG Project)"

This code builds a simple local RAG (Retrieval-Augmented Generation) system using:
    -> PDF as knowledge source
    -> Free embeddings (HuggingFace)
    -> FAISS vector database
    -> Local LLM via Ollama
🔹 What is Ollama?
    Ollama is a tool/software that:
        Runs LLMs locally on your computer
        Lets you download and use models like LLaMA, Mistral, etc.
        Acts like a local LLM server

---------------------------------------------------------------------------
🔹 What This Code Does (Big Picture)

    It allows you to:
        Load a PDF
        Break it into small chunks
        Convert those chunks into embeddings (vectors)
        Store them in a FAISS vector database
        Ask questions
        Retrieve the most relevant PDF chunks
        Send them to a local LLM (like Llama 3)
        Get an answer grounded in your PDF
        This is a fully local PDF chatbot.

---------------------------------------------------------------------------
🧩 Step-by-Step Explanation :
🔹 1. Load PDF
    PyPDFLoader reads your PDF file.
    It extracts text from each page.
    Output: a list of Document objects (one per page).
    documents = [
        Page1 (3000 characters),
        Page2 (2500 characters),
    ]

🔹 2. Split Into Chunks
    Why we split:
        LLMs and embedding models work better with smaller text pieces.
    What it does:
        Splits long pages into chunks of 1000 characters
        Keeps 200 characters overlapping between chunks
    Why overlap?
        To avoid cutting sentences in half and losing context.
    docs = [
        Chunk1 (1000 chars),
        Chunk2 (1000 chars),
        Chunk3 (1000 chars),
        Chunk4 (1000 chars),
        Chunk5 (500 chars),
    ]

🔹 3. Create Free Embeddings
    Embedding = converting text into numbers (vectors).
    "This is AI" → [0.123, -0.98, 0.456, ...]
    we are using all-MiniLM-L6-v2.

🔹 4. Store in FAISS
    FAISS is a vector database.
    It:
        Stores vectors
        Allows fast similarity search
    What happens here:
        Each chunk → converted to embedding
        Stored inside FAISS index
    Text chunk → Vector → Stored in FAISS

🔹 5. Load Local LLM (Ollama)

🔹 6. Create Retriever
    This turns FAISS into a search engine.
    When you ask a question:
        It converts your question into embedding
        Finds similar document chunks
        Returns the most relevant ones

🔹 7. Question (Main RAG Logic)
    This creates a chatbot loop.
    🟢 Step A: User asks question
    🟢 Step B: Retrieve relevant chunks
        What happens internally:
            Question → embedding
            Compare with stored vectors
            Find closest matches
            Return best chunks
    🟢 Step C: Combine context
        All retrieved chunks are combined into one big text block.
    🟢 Step D: Create Prompt
    🟢 Step E: Ask LLMThe 
        LLM:
        Reads context
        Reads question
        Generates answer
    🟢 Step F: Print Answer
---------------------------------------------------------------------------
Flow chart :

                ┌─────────────────────┐
                │      sample.pdf      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │   PyPDFLoader       │
                │  (Extract text)     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Text Splitter       │
                │ (Chunking 1000/200) │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ HuggingFace         │
                │ Embeddings Model    │
                │ (Text → Vectors)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ FAISS Vector Store  │
                │ (Store embeddings)  │
                └─────────────────────┘
                           │
───────────────────────────┼───────────────────────────
                           │
                           ▼
                    USER ASKS QUESTION
                           │
                           ▼
                ┌─────────────────────┐
                │ Convert Question    │
                │ → Embedding Vector  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ FAISS Similarity    │
                │ Search              │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Retrieve Relevant   │
                │ Chunks (Context)    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Create Prompt       │
                │ (Context + Question)│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Ollama (Llama3)     │
                │ Generate Answer     │
                └──────────┬──────────┘
                           │
                           ▼
                     FINAL ANSWER

---------------------------------------------------------------------------
🧠 Why This Is Powerful
Without RAG:
LLM only knows training data.

With this:
LLM answers based on YOUR PDF.