from transformers import pipeline

# 1️⃣ Load summarization pipeline with BART model
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# 2️⃣ Wikipedia article (example)
article_text = """
The Apollo program, also known as Project Apollo, was the third United States human spaceflight program carried out by NASA, 
which accomplished landing the first humans on the Moon from 1969 to 1972. First conceived during Dwight D. Eisenhower's 
administration as a three-person spacecraft to follow the one-person Project Mercury which put the first Americans in space, 
Apollo was later dedicated to President John F. Kennedy's national goal of "landing a man on the Moon and returning him 
safely to the Earth" by the end of the 1960s, which he proposed in an address to Congress on May 25, 1961. Apollo was 
managed by NASA's George C. Marshall Space Flight Center, and used the Saturn family of rockets as launch vehicles.
"""

# 3️⃣ Summarize the article (max 2 sentences)
summary = summarizer(
    article_text, 
    max_length=60,   # roughly 2 sentences
    min_length=30, 
    do_sample=False
)

# 4️⃣ Print results
print("Original article length:", len(article_text.split()), "words\n")
print("Summary:")
print(summary[0]['summary_text'])
