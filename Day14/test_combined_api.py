#!/usr/bin/env python3
"""
Test script for the Enhanced Text Analysis API with 3 endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8001"

def test_api_endpoints():
    """Test all three API endpoints"""
    
    print("🤖 Testing Enhanced Text Analysis API")
    print("=" * 50)
    
    # Wait for server to be ready
    time.sleep(2)
    
    # Test data
    test_texts = [
        {
            "text": "I absolutely love this new smartphone! The camera quality is amazing and the battery life is fantastic. It's definitely worth the money.",
            "description": "Positive Product Review (Long)"
        },
        {
            "text": "This service is terrible!",
            "description": "Negative Review (Short)"
        },
        {
            "text": "The meeting went well today. We discussed the quarterly results and the team seemed satisfied with the progress. The new project timeline looks achievable and everyone is excited about the upcoming challenges. We also reviewed the budget allocations for next month and made some important decisions regarding resource management.",
            "description": "Neutral Business Text (Long)"
        }
    ]
    
    # Test root endpoint
    try:
        print("🏠 Testing Root Endpoint:")
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API: {data['message']}")
            print(f"   📊 Version: {data['version']}")
            print(f"   📚 Documentation: {BASE_URL}{data['docs']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # Test each endpoint for each text
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n🧪 TEST CASE {i}: {test_case['description']}")
        print(f"📝 Text: '{test_case['text']}'")
        print("-" * 50)
        
        # Test 1: Sentiment Only
        print("1️⃣  SENTIMENT ANALYSIS:")
        try:
            response = requests.post(
                f"{BASE_URL}/sentiment",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                sentiment = data['sentiment'][0]
                emoji = "😊" if sentiment['label'] == 'POSITIVE' else "😢"
                print(f"   {emoji} Sentiment: {sentiment['label']} ({sentiment['score']:.1%})")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Summary Only
        print("\n2️⃣  SUMMARIZATION:")
        try:
            response = requests.post(
                f"{BASE_URL}/summary",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                summary = data['summary']
                print(f"   📄 Summary: {summary}")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Combined Analysis (NEW!)
        print("\n3️⃣  🆕 COMBINED ANALYSIS:")
        try:
            response = requests.post(
                f"{BASE_URL}/analyze",
                json={"text": test_case['text']},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                
                # Display comprehensive results
                print(f"   📊 Word Count: {data['word_count']} words")
                
                sentiment = data['sentiment']
                emoji = "😊" if sentiment['label'] == 'POSITIVE' else "😢"
                print(f"   {emoji} Sentiment: {sentiment['label']} ({sentiment['confidence']})")
                print(f"   🎯 Confidence Level: {data['analysis']['confidence_level']}")
                
                summary_info = data['summary']
                if summary_info['summary_length'] > 0:
                    print(f"   📄 Summary: {summary_info['text']}")
                    print(f"   📏 Compression: {summary_info['original_length']} → {summary_info['summary_length']} chars")
                else:
                    print(f"   📄 Summary: {summary_info['text']}")
                
                print(f"   💡 Recommendation: {data['analysis']['recommended_action']}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 50)

def interactive_mode():
    """Interactive testing mode"""
    print("\n🎮 Interactive Mode - Test Your Own Text!")
    print("Enter text to analyze (type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        text = input("\n📝 Enter your text: ").strip()
        
        if text.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not text:
            continue
        
        try:
            # Use the combined analysis endpoint
            response = requests.post(
                f"{BASE_URL}/analyze",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n🎯 ANALYSIS RESULTS:")
                print(f"   📊 Length: {data['word_count']} words")
                
                sentiment = data['sentiment']
                emoji = "😊" if sentiment['label'] == 'POSITIVE' else "😢"
                print(f"   {emoji} Sentiment: {sentiment['label']} ({sentiment['confidence']})")
                
                if data['summary']['summary_length'] > 0:
                    print(f"   📄 Summary: {data['summary']['text']}")
                
                print(f"   💡 Recommendation: {data['analysis']['recommended_action']}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Enhanced Text Analysis API Tester")
    print("Choose testing mode:")
    print("1. Run automated tests")
    print("2. Interactive mode")
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        test_api_endpoints()
    elif choice == "2":
        interactive_mode()
    else:
        print("Invalid choice. Running automated tests...")
        test_api_endpoints()
    
    print(f"\n🌐 API Documentation available at: {BASE_URL}/docs")
    print(f"🔧 Interactive API testing at: {BASE_URL}/redoc")