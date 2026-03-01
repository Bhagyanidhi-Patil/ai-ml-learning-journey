from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings

def create_rag_pipeline():
    # load pdf 
    pdf_path = "OS_Concepts.pdf"
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # split the chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 400
    )
    docs = text_splitter.split_documents(documents)

    # create free embeddings
    #all-MiniLM-L6-v2 is a sentence embedding model used to convert text into numerical vectors.
    #all-MiniLM-L6-v2 is: A small transformer model
    embeddings = HuggingFaceEmbeddings(
        model_name = "all-MiniLM-L6-v2"
    )

    # store in FAISS
    vectorstore = FAISS.from_documents(docs,embeddings)

    #Load LLM (Ollama)
    llm = Ollama(model="tinyllama")

    # create Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever, llm

def ask_question(query, retriever, llm):
    relevant_docs = retriever._get_relevant_documents(query, run_manager=None)
    context = ""
    for doc in relevant_docs:
        context += doc.page_content + "\n"
    
    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {query}
    """
    answer = llm.invoke(prompt)
    # print("\nAnswer:", answer)
    return answer


#    relevant_docs = retriever.invoke(query) flow: 
    # Query → Convert to embedding vector
    #         ↓
    # Compare with stored vectors in FAISS
    #         ↓
    # Pick top similar vectors
    #         ↓
    # Return corresponding text chunks