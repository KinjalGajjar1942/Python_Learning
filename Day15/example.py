
import os

# Replace with your actual OpenRouter key
os.environ["OPENAI_API_KEY"] = "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"

# OpenRouter endpoint
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Prompt for polite rewriting
prompt = PromptTemplate(
    input_variables=["sentence"],
    template="Rewrite the following sentence politely:\n\n'{sentence}'"
)

# Initialize the LLM
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini"
)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# Input sentence
if __name__ == "__main__":
    input_sentence = "Give me that report now."

    # Use invoke() instead of run() (deprecated)
    polite_sentence = chain.invoke({"sentence": input_sentence})

    print("Original:", input_sentence)
    print("Polite:", polite_sentence)
