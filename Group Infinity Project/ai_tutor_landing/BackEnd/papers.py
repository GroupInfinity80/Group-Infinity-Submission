import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
from typing import Dict, List, Optional
import hashlib

# For AI capabilities (choose one)
import openai  # pip install openai
# OR use free alternatives:
from transformers import pipeline  # pip install transformers torch

class IndianEducationChatbot:
    def __init__(self, use_openai=False, openai_api_key=None):
        """Initialize the chatbot with database and AI model"""
        self.setup_database()
        self.use_openai = use_openai
        
        # Setup AI model
        if use_openai and openai_api_key:
            openai.api_key = openai_api_key
            self.model_type = "openai"
        else:
            # Use free local model (requires downloading)
            print("Loading free AI model (first time may take a while)...")
            self.chatbot = pipeline("text-generation", 
                                   model="microsoft/DialoGPT-small")
            self.model_type = "local"
    
    def setup_database(self):
        """Create SQLite database to store papers and syllabus"""
        self.conn = sqlite3.connect('education_data.db')
        cursor = self.conn.cursor()
        
        # Table for syllabus
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS syllabus (
                id INTEGER PRIMARY KEY,
                board TEXT,
                class_level TEXT,
                subject TEXT,
                year INTEGER,
                content TEXT,
                url TEXT,
                fetched_at TIMESTAMP
            )
        ''')
        
        # Table for question papers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_papers (
                id INTEGER PRIMARY KEY,
                board TEXT,
                class_level TEXT,
                subject TEXT,
                year INTEGER,
                paper_type TEXT,
                content TEXT,
                url TEXT,
                fetched_at TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def fetch_cbse_resources(self, class_level: str, subject: str, year: int):
        """Fetch CBSE syllabus and papers from official website"""
        resources = []
        
        # CBSE Academic website
        base_url = "https://cbseacademic.nic.in"
        
        # Syllabus URL pattern (example)
        syllabus_url = f"{base_url}/syllabus_{class_level}_{year}.html"
        
        # Question papers URL (example - actual URLs differ)
        paper_url = f"{base_url}/question_papers/class_{class_level}/{subject}_{year}.pdf"
        
        # Try to fetch syllabus
        try:
            response = requests.get(syllabus_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Extract text content (simplified)
                content = soup.get_text()[:5000]  # Limit size
                
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO syllabus (board, class_level, subject, year, content, url, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', ('CBSE', class_level, subject, year, content, syllabus_url, datetime.now()))
                self.conn.commit()
                resources.append({"type": "syllabus", "content": content[:500]})
        except Exception as e:
            print(f"Error fetching syllabus: {e}")
        
        return resources
    
    def fetch_ncert_resources(self, class_level: str, subject: str):
        """Fetch NCERT textbooks and resources"""
        base_url = "https://ncert.nic.in/textbook.php"
        # Implementation similar to above
        pass
    
    def search_local_db(self, query: str) -> List[Dict]:
        """Search locally stored resources"""
        cursor = self.conn.cursor()
        
        # Search in syllabus
        cursor.execute('''
            SELECT board, class_level, subject, year, content 
            FROM syllabus 
            WHERE content LIKE ? 
            LIMIT 5
        ''', (f'%{query}%',))
        
        syllabus_results = cursor.fetchall()
        
        # Search in question papers
        cursor.execute('''
            SELECT board, class_level, subject, year, paper_type, content 
            FROM question_papers 
            WHERE content LIKE ? 
            LIMIT 5
        ''', (f'%{query}%',))
        
        paper_results = cursor.fetchall()
        
        results = []
        for res in syllabus_results:
            results.append({
                "type": "syllabus",
                "board": res[0],
                "class": res[1],
                "subject": res[2],
                "year": res[3],
                "preview": res[4][:200]
            })
        
        return results
    
    def get_ai_response(self, user_query: str, context: str = "") -> str:
        """Generate AI response based on user query and available context"""
        
        prompt = f"""You are an AI assistant for Indian education system. 
        You have access to CBSE, ICSE, and state board syllabi and previous year papers.
        
        Context from available resources: {context[:1000]}
        
        User question: {user_query}
        
        Please provide a helpful, accurate response about Indian education syllabus or exam papers.
        If the specific information isn't in the context, suggest how to find it.
        """
        
        if self.model_type == "openai":
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an Indian education system expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
        
        else:
            # Local model response
            response = self.chatbot(prompt, max_length=300, num_return_sequences=1)
            return response[0]['generated_text']
    
    def chat(self):
        """Interactive chat interface"""
        print("\n🤖 Indian Education AI Chatbot 🤖")
        print("="*50)
        print("I can help you with:")
        print("- CBSE/ICSE/State board syllabus")
        print("- Previous year question papers")
        print("- Exam patterns and marking schemes")
        print("- Study resources and references")
        print("\nType 'exit' to quit")
        print("Type 'fetch' to download new resources")
        print("="*50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                print("Goodbye! 📚")
                break
            
            elif user_input.lower() == 'fetch':
                print("\nFetching latest resources...")
                self.fetch_cbse_resources("10", "Mathematics", 2023)
                print("Resources fetched and stored locally!")
                continue
            
            # Search local database first
            local_results = self.search_local_db(user_input)
            
            if local_results:
                context = "\n".join([f"{r['type']}: {r['preview']}" for r in local_results[:3]])
                print("\n📚 Found relevant resources in database!")
            else:
                context = "No specific resources found in local database. Provide general guidance."
                print("\n🔍 Searching general knowledge...")
            
            # Get AI response
            response = self.get_ai_response(user_input, context)
            print(f"\n🤖 Assistant: {response}")
            
            # Show local results if available
            if local_results:
                print("\n📖 Related resources:")
                for i, res in enumerate(local_results[:3], 1):
                    print(f"{i}. {res['board']} Class {res['class']} {res['subject']} - {res['type']} ({res['year']})")

def main():
    """Main function to run the chatbot"""
    
    # Option 1: Use free local AI (no API key needed)
    chatbot = IndianEducationChatbot(use_openai=False)
    
    # Option 2: Use OpenAI (requires API key)
    # api_key = os.getenv("OPENAI_API_KEY")  # Set your key in environment
    # if api_key:
    #     chatbot = IndianEducationChatbot(use_openai=True, openai_api_key=api_key)
    # else:
    #     print("OpenAI API key not found. Using local AI model.")
    #     chatbot = IndianEducationChatbot(use_openai=False)
    
    # Start chatting
    chatbot.chat()

if __name__ == "__main__":
    main()