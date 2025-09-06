#!/usr/bin/env python3

import sys
import json
import os
import re
import math
from pathlib import Path
import sqlite3
import pickle

def calculate_entropy(data):
    if not data:
        return 0
    char_counts = {}
    for char in data:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    entropy = 0
    data_len = len(data)
    for count in char_counts.values():
        probability = count / data_len
        if probability > 0:
            entropy -= probability * math.log2(probability)
    return entropy

def deep_confidence_analysis(data):
    if not data:
        return 0.0
    
    entropy = calculate_entropy(data)
    length_factor = min(len(data) / 1000, 1.0)
    
    pattern_scores = 0
    if re.search(r'\d+', data):
        pattern_scores += 0.1
    if re.search(r'[A-Z][a-z]+', data):
        pattern_scores += 0.1
    if re.search(r'[{}()\[\]]', data):
        pattern_scores += 0.1
    
    confidence = (entropy / 10 + length_factor + pattern_scores) / 3
    return min(confidence, 1.0)

class SimpleStorage:
    def __init__(self):
        self.storage = {}
        self.db_path = "smart_cli.db"
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_store (
                key TEXT PRIMARY KEY,
                value TEXT,
                backend TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def store_data(self, key, data):
        backend = self.evaluate_storage_backend(data)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT OR REPLACE INTO data_store (key, value, backend) VALUES (?, ?, ?)',
            (key, data, backend)
        )
        conn.commit()
        conn.close()
        
        return backend
    
    def retrieve_data(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM data_store WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def evaluate_storage_backend(self, data):
        entropy = calculate_entropy(data)
        length = len(data)
        
        if length > 10000:
            return "Secure Storage (Large Data)"
        elif entropy > 4.0:
            return "NoSQL Storage (Complex Data)"
        elif any(keyword in data.lower() for keyword in ['select', 'insert', 'table']):
            return "SQL Storage (Structured)"
        elif any(keyword in data.lower() for keyword in ['function', 'class', 'def']):
            return "Jeans Storage (Code)"
        else:
            return "Jill Storage (General)"

class DatasetLearner:
    def __init__(self, datasets_path="datasets"):
        self.datasets_path = Path(datasets_path)
        self.knowledge_base = {}
        self.patterns = {}
        self.load_knowledge()
    
    def load_knowledge(self):
        if os.path.exists("knowledge_base.pkl"):
            with open("knowledge_base.pkl", "rb") as f:
                self.knowledge_base = pickle.load(f)
        else:
            self.learn_from_datasets()
            self.save_knowledge()
    
    def learn_from_datasets(self):
        for dataset_file in self.datasets_path.glob("*"):
            if dataset_file.is_file():
                self.process_dataset(dataset_file)
    
    def process_dataset(self, file_path):
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            file_type = file_path.suffix.lower()
            
            if file_type in ['.txt']:
                self.extract_text_patterns(content, file_path.name)
            elif file_type in ['.py', '.js']:
                self.extract_code_patterns(content, file_path.name)
            elif file_type in ['.sql']:
                self.extract_sql_patterns(content, file_path.name)
                
        except Exception:
            pass
    
    def extract_text_patterns(self, content, filename):
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:100]
        self.knowledge_base[f"text_{filename}"] = {
            "type": "text",
            "common_words": common_words,
            "length": len(content),
            "complexity": calculate_entropy(content)
        }
    
    def extract_code_patterns(self, content, filename):
        functions = re.findall(r'def\s+(\w+)|function\s+(\w+)', content)
        classes = re.findall(r'class\s+(\w+)', content)
        imports = re.findall(r'import\s+(\w+)|from\s+(\w+)', content)
        
        self.knowledge_base[f"code_{filename}"] = {
            "type": "code",
            "functions": [f[0] or f[1] for f in functions],
            "classes": classes,
            "imports": [i[0] or i[1] for i in imports],
            "complexity": calculate_entropy(content)
        }
    
    def extract_sql_patterns(self, content, filename):
        tables = re.findall(r'CREATE\s+TABLE\s+(\w+)', content, re.IGNORECASE)
        selects = re.findall(r'SELECT\s+.*?\s+FROM\s+(\w+)', content, re.IGNORECASE)
        
        self.knowledge_base[f"sql_{filename}"] = {
            "type": "sql",
            "tables": tables,
            "queries": selects,
            "complexity": calculate_entropy(content)
        }
    
    def save_knowledge(self):
        with open("knowledge_base.pkl", "wb") as f:
            pickle.dump(self.knowledge_base, f)
    
    def analyze_user_input(self, user_input):
        input_lower = user_input.lower()
        suggestions = []
        
        for key, knowledge in self.knowledge_base.items():
            if knowledge["type"] == "text":
                for word, freq in knowledge.get("common_words", [])[:20]:
                    if word in input_lower:
                        suggestions.append(f"Text storage recommended - similar to {key}")
                        break
            
            elif knowledge["type"] == "code":
                for func in knowledge.get("functions", []):
                    if func.lower() in input_lower:
                        suggestions.append(f"Code storage recommended - detected function patterns")
                        break
                for cls in knowledge.get("classes", []):
                    if cls.lower() in input_lower:
                        suggestions.append(f"Object storage recommended - detected class patterns")
                        break
            
            elif knowledge["type"] == "sql":
                sql_keywords = ["select", "insert", "update", "delete", "table", "database"]
                if any(keyword in input_lower for keyword in sql_keywords):
                    suggestions.append(f"SQL storage recommended - detected database operations")
                    break
        
        return list(set(suggestions))

class SmartCLI:
    def __init__(self):
        self.db_manager = SimpleStorage()
        self.learner = DatasetLearner()
        self.session_history = []
    
    def start(self):
        print("Smart Database CLI - Intelligent Storage Assistant")
        print("Type 'help' for commands, 'quit' to exit")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.startswith('store '):
                    self.handle_store(user_input[6:])
                elif user_input.startswith('retrieve '):
                    self.handle_retrieve(user_input[9:])
                elif user_input.startswith('search '):
                    self.handle_search(user_input[7:])
                elif user_input.startswith('analyze '):
                    self.handle_analyze(user_input[8:])
                else:
                    self.handle_general_query(user_input)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        print("\nCommands:")
        print("store <data>     - Store data with intelligent backend selection")
        print("retrieve <key>   - Retrieve stored data")
        print("search <term>    - Search across stored data")
        print("analyze <data>   - Analyze data characteristics")
        print("help            - Show this help")
        print("quit            - Exit CLI")
    
    def handle_store(self, data):
        suggestions = self.learner.analyze_user_input(data)
        
        if suggestions:
            print("Intelligence Suggestions:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        confidence = deep_confidence_analysis(data)
        print(f"Data Analysis Complete - Confidence: {confidence:.2f}")
        
        try:
            result = self.db_manager.store_data("user_data", data)
            print(f"Stored successfully using: {result}")
            self.session_history.append(("store", data, result))
        except Exception as e:
            print(f"Storage failed: {e}")
    
    def handle_retrieve(self, key):
        try:
            result = self.db_manager.retrieve_data(key)
            if result:
                print(f"Retrieved: {result}")
                
                analysis = self.learner.analyze_user_input(str(result))
                if analysis:
                    print("Related patterns found in knowledge base")
            else:
                print("No data found for key")
        except Exception as e:
            print(f"Retrieval failed: {e}")
    
    def handle_search(self, term):
        print(f"Searching for: {term}")
        
        found_in_knowledge = []
        for key, knowledge in self.learner.knowledge_base.items():
            if term.lower() in str(knowledge).lower():
                found_in_knowledge.append(key)
        
        if found_in_knowledge:
            print("Found in knowledge base:")
            for item in found_in_knowledge[:5]:
                print(f"  - {item}")
        
        for action, data, backend in self.session_history:
            if term.lower() in data.lower():
                print(f"Found in session: {data[:100]}... (stored via {backend})")
    
    def handle_analyze(self, data):
        entropy = calculate_entropy(data)
        confidence = deep_confidence_analysis(data)
        suggestions = self.learner.analyze_user_input(data)
        
        print(f"Data Entropy: {entropy:.3f}")
        print(f"Confidence Score: {confidence:.3f}")
        print(f"Data Length: {len(data)} characters")
        
        if suggestions:
            print("Storage Recommendations:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        
        backend_recommendation = self.db_manager.evaluate_storage_backend(data)
        print(f"Recommended Backend: {backend_recommendation}")
    
    def handle_general_query(self, query):
        suggestions = self.learner.analyze_user_input(query)
        
        if suggestions:
            print("Based on learned patterns:")
            for suggestion in suggestions:
                print(f"  - {suggestion}")
        else:
            print("No specific patterns detected. Use 'help' for available commands.")
            
        if any(word in query.lower() for word in ['shakespeare', 'hamlet', 'macbeth']):
            print("Literary content detected - consider text storage with high compression")
        elif any(word in query.lower() for word in ['function', 'class', 'algorithm']):
            print("Code content detected - structured storage recommended")
        elif any(word in query.lower() for word in ['math', 'formula', 'equation']):
            print("Mathematical content detected - precise storage recommended")

if __name__ == "__main__":
    cli = SmartCLI()
    cli.start()
