from transformers import pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 1️⃣ Load the model locally
pipe = pipeline("text2text-generation", model="google/flan-t5-small")

# 2️⃣ Wrap in LangChain
llm = HuggingFacePipeline(pipeline=pipe)

# 3️⃣ Create a prompt
prompt = PromptTemplate(
    input_variables=["sentence"],
    template="Rewrite the following sentence politely:\n\n{sentence}\n\nPolite version:"
)

# 4️⃣ Build the chain
chain = LLMChain(llm=llm, prompt=prompt)

# 5️⃣ Test it
sentence = "Send me the file right now!"
result = chain.run(sentence)

print("📝 Original:", sentence)
print("🤖 Polite version:", result)
