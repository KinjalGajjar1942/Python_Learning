import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import PyPDF2

# -------------------------------
# 1. Set OpenRouter API key
# -------------------------------
os.environ["OPENAI_API_KEY"] = "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"  # Your OpenRouter key
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# -------------------------------
# 2. Load PDF text
# -------------------------------
pdf_file_path = "example.pdf"  # Replace with your PDF path
pdf_text = ""

with open(pdf_file_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        pdf_text += page.extract_text() + "\n"

# -------------------------------
# 3. Create summarization prompt
# -------------------------------
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text in a concise and clear manner:\n\n{text}"
)

# -------------------------------
# 4. Initialize Chat LLM
# -------------------------------
llm = ChatOpenAI(
    temperature=0.5,
    model="gpt-4o-mini"
)

# -------------------------------
# 5. Create LLMChain
# -------------------------------
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# -------------------------------
# 6. Run the summarization
# -------------------------------
summary = summary_chain.invoke({"text": pdf_text})

# -------------------------------
# 7. Print results
# -------------------------------
print("PDF Summary:\n", summary)
