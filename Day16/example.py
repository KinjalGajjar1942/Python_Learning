import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain  # For multi-step chaining

# -------------------------------
# 1. Set OpenRouter API key
# -------------------------------
os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# -------------------------------
# 2. Initialize the LLM
# -------------------------------
llm = ChatOpenAI(
    temperature=0.5,
    model="gpt-4o-mini"
)

# -------------------------------
# 3. Create prompt templates
# -------------------------------

# Step 1: Summarize the text
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following text in a concise way:\n\n{text}"
)

# Step 2: Extract keywords
keywords_prompt = PromptTemplate(
    input_variables=["summary"],
    template="Extract the most important keywords from the following summary. Provide them as a comma-separated list:\n\n{summary}"
)

# -------------------------------
# 4. Create individual chains
# -------------------------------
summary_chain = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")
keywords_chain = LLMChain(llm=llm, prompt=keywords_prompt, output_key="keywords")

# -------------------------------
# 5. Combine chains sequentially
# -------------------------------
overall_chain = SimpleSequentialChain(
    chains=[summary_chain, keywords_chain],
    input_key="text",
    output_key="keywords",
    verbose=True
)

# -------------------------------
# 6. Input text
# -------------------------------
input_text = """
Artificial Intelligence (AI) is rapidly transforming multiple industries including healthcare, finance, and transportation.
Companies are leveraging AI for automation, predictive analytics, and better decision-making. 
As AI models improve, ethical considerations and data privacy become increasingly important.
"""

# -------------------------------
# 7. Run the chain
# -------------------------------
keywords = overall_chain.run(input_text)

print("Extracted Keywords:", keywords)
