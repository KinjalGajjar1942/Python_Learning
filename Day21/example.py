import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# ----------------------
# Set OpenAI API key
# ----------------------
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your key

# ----------------------
# Initialize FastAPI
# ----------------------
app = FastAPI(title="PDF Q&A Bot")

# ----------------------
# Pydantic model for queries
# ----------------------
class QARequest(BaseModel):
    query: str

# ----------------------
# Global FAISS index
# ----------------------
faiss_index = None

# ----------------------
# 1️⃣ Upload PDF → store embeddings
# ----------------------
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global faiss_index
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Read PDF
        pdf = PdfReader(file.file)
        texts = [page.extract_text() for page in pdf.pages]

        # Convert to Document objects
        docs = [Document(page_content=t, metadata={"source": f"page_{i}"}) for i, t in enumerate(texts)]

        # Split text into chunks
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = []
        for doc in docs:
            chunks = splitter.split_text(doc.page_content)
            for chunk in chunks:
                split_docs.append(Document(page_content=chunk, metadata=doc.metadata))

        # Create embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Store in FAISS
        faiss_index = FAISS.from_documents(split_docs, embeddings)

        return {"message": f"PDF '{file.filename}' uploaded and indexed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# 2️⃣ Ask question → get context-based answer
# ----------------------
@app.post("/qa")
def ask_question(request: QARequest):
    global faiss_index
    if faiss_index is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet")

    try:
        retriever = faiss_index.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            retriever=retriever
        )

        answer = qa_chain.run(request.query)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
