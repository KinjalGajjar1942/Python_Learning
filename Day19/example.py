from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize FastAPI
app = FastAPI(title="Q&A API")

# Request model
class QARequest(BaseModel):
    text: str

# Response model
class QAResponse(BaseModel):
    answer: str

# Initialize LLM
llm = OpenAI(temperature=0)  # Make sure OPENAI_API_KEY is set in env

# Define prompt template
prompt = PromptTemplate(
    input_variables=["context"],
    template="Answer the following question based on the text:\n\n{context}\n\nAnswer:"
)

# Create LangChain chain
qa_chain = LLMChain(llm=llm, prompt=prompt)

# API endpoint
@app.post("/qa", response_model=QAResponse)
async def qa_endpoint(request: QARequest):
    answer = qa_chain.run(request.text)
    return QAResponse(answer=answer)
