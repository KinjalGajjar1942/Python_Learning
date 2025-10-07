"""
LangChain Sequential Chain: Text → Summarize → Extract Keywords
This demonstrates how to chain multiple LLM operations together.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.llms import FakeListLLM

def create_summarize_and_extract_chain():
    """Creates a sequential chain: Input Text → Summarize → Extract Keywords"""
    
    # Mock responses for demonstration
    summary_responses = [
        "This article discusses the importance of artificial intelligence in modern healthcare, focusing on machine learning algorithms for medical diagnosis and patient care improvements.",
        "The text explains climate change effects on global weather patterns, including rising temperatures, melting ice caps, and extreme weather events affecting ecosystems worldwide.",
        "This content covers software development best practices, emphasizing code quality, testing methodologies, and team collaboration for successful project delivery.",
        "The passage describes renewable energy technologies, particularly solar and wind power systems, and their role in sustainable environmental solutions.",
        "This text analyzes modern educational approaches, including online learning platforms, interactive teaching methods, and technology integration in classrooms."
    ]
    
    keyword_responses = [
        "artificial intelligence, healthcare, machine learning, medical diagnosis, patient care, algorithms",
        "climate change, weather patterns, temperatures, ice caps, extreme weather, ecosystems, global warming",
        "software development, code quality, testing, collaboration, project management, best practices",
        "renewable energy, solar power, wind power, sustainability, environmental solutions, clean technology",
        "education, online learning, teaching methods, technology integration, interactive learning, digital classrooms"
    ]
    
    # Create LLMs for each step
    summarizer_llm = FakeListLLM(responses=summary_responses)
    keyword_extractor_llm = FakeListLLM(responses=keyword_responses)
    
    # Step 1: Summarization Chain
    summarize_prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Please provide a concise summary of the following text:
        
        TEXT: {text}
        
        SUMMARY:
        """
    )
    
    summarize_chain = LLMChain(
        llm=summarizer_llm,
        prompt=summarize_prompt,
        output_key="summary"  # This output becomes input for next chain
    )
    
    # Step 2: Keyword Extraction Chain
    keyword_prompt = PromptTemplate(
        input_variables=["summary"],
        template="""
        Extract the main keywords from this summary. Provide them as a comma-separated list:
        
        SUMMARY: {summary}
        
        KEYWORDS:
        """
    )
    
    keyword_chain = LLMChain(
        llm=keyword_extractor_llm,
        prompt=keyword_prompt,
        output_key="keywords"
    )
    
    # Combine into Sequential Chain
    sequential_chain = SequentialChain(
        chains=[summarize_chain, keyword_chain],
        input_variables=["text"],  # Initial input
        output_variables=["summary", "keywords"],  # Final outputs
        verbose=True  # Shows intermediate steps
    )
    
    return sequential_chain

def main():
    """Main function to demonstrate the chain"""
    
    print("🔗 LANGCHAIN SEQUENTIAL PROCESSING")
    print("Input Text → Summarize → Extract Keywords")
    print("=" * 60)
    
    # Create the chain
    chain = create_summarize_and_extract_chain()
    
    # Test texts
    sample_texts = [
        """
        Artificial Intelligence (AI) has revolutionized healthcare by enabling more accurate diagnoses 
        and personalized treatment plans. Machine learning algorithms can analyze medical images, 
        predict patient outcomes, and assist doctors in making informed decisions. AI-powered tools 
        help reduce human error, improve efficiency, and provide better patient care. From robotic 
        surgery to drug discovery, AI is transforming every aspect of modern medicine.
        """,
        
        """
        Climate change represents one of the most pressing challenges of our time. Rising global 
        temperatures are causing ice caps to melt, sea levels to rise, and weather patterns to 
        become increasingly unpredictable. These changes threaten ecosystems worldwide, affecting 
        biodiversity and human communities. Extreme weather events like hurricanes, droughts, 
        and floods are becoming more frequent and severe, requiring urgent action to mitigate 
        environmental damage.
        """,
        
        """
        Software development has evolved significantly with the adoption of agile methodologies 
        and DevOps practices. Modern development teams focus on continuous integration, automated 
        testing, and collaborative workflows. Code quality is maintained through peer reviews, 
        static analysis tools, and comprehensive testing strategies. Project success depends on 
        effective communication, proper documentation, and adherence to established coding standards 
        and best practices.
        """
    ]
    
    # Process each text through the chain
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 EXAMPLE {i}")
        print("-" * 40)
        
        try:
            # Run the sequential chain
            result = chain({"text": text.strip()})
            
            print(f"📄 Original Text (first 100 chars): {text.strip()[:100]}...")
            print(f"\n📋 Summary: {result['summary']}")
            print(f"\n🏷️  Keywords: {result['keywords']}")
            
        except Exception as e:
            print(f"❌ Error processing text: {e}")
        
        print("\n" + "=" * 60)
    
    print("✅ Sequential chain demonstration completed!")

if __name__ == "__main__":
    main()