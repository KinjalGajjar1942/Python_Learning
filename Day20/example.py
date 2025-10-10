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
# Set your OpenAI API key
# ----------------------
os.environ["OPENAI_API_KEY"] = "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"  # Replace with your key

# ----------------------
# Initialize FastAPI
# ----------------------
app = FastAPI(title="PDF Q&A Bot")

# ----------------------
# Pydantic model for POST query
# ----------------------
class QARequest(BaseModel):
    query: str

# ----------------------
# Endpoint: POST /upload-pdf
# Upload PDF and create FAISS index
# ----------------------
faiss_index = None  # Global variable to store FAISS index

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global faiss_index
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # 1️⃣ Read PDF content
        pdf = PdfReader(file.file)
        texts = []
        for page in pdf.pages:
            texts.append(page.extract_text())

        # 2️⃣ Wrap texts as Document objects
        docs = [Document(page_content=t, metadata={"source": f"page_{i}"}) for i, t in enumerate(texts)]

        # 3️⃣ Split text into smaller chunks
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = []
        for doc in docs:
            chunks = splitter.split_text(doc.page_content)
            for chunk in chunks:
                split_docs.append(Document(page_content=chunk, metadata=doc.metadata))

        # 4️⃣ Create embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # 5️⃣ Store in FAISS
        faiss_index = FAISS.from_documents(split_docs, embeddings)

        return {"message": f"PDF '{file.filename}' uploaded and indexed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------
# Endpoint: POST /qa
# Ask question from loaded PDF
# ----------------------
@app.post("/qa")
def ask_question(request: QARequest):
    global faiss_index
    if faiss_index is None:
        raise HTTPException(status_code=400, detail="No PDF uploaded yet")

    try:
        # 1️⃣ Create retrieval QA chain
        retriever = faiss_index.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            retriever=retriever
        )

        # 2️⃣ Run query
        answer = qa_chain.run(request.query)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
