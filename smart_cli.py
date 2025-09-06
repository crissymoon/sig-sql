#!/usr/bin/env python3

import sys
import json
import os
import re
import math
import random
from pathlib import Path
import sqlite3
import pickle
from datetime import datetime
from language_processor import LanguageProcessor

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
            return "Secure Storage"
        elif entropy > 4.0:
            return "NoSQL Storage"
        elif any(keyword in data.lower() for keyword in ['select', 'insert', 'table']):
            return "SQL Storage"
        elif any(keyword in data.lower() for keyword in ['function', 'class', 'def']):
            return "Jeans Storage"
        else:
            return "Jill Storage"

class ResponseGenerator:
    def __init__(self, datasets_path="datasets"):
        self.datasets_path = Path(datasets_path)
        self.text_corpus = {}
        self.load_training_data()
    
    def load_training_data(self):
        self.text_corpus = {
            'shakespeare': [],
            'math': [],
            'code': [],
            'language': [],
            'natural': [],
            'business': [],
            'storage': [],
            'analysis': []
        }
        
        if self.datasets_path.exists():
            for dataset_file in self.datasets_path.glob("*"):
                if dataset_file.is_file():
                    self.process_training_file(dataset_file)
        
        self.add_contextual_responses()
        print(f"Loaded training data: {sum(len(corpus) for corpus in self.text_corpus.values())} total responses")
    
    def add_contextual_responses(self):
        self.text_corpus['business'].extend([
            "Processing your business data with appropriate storage methods.",
            "Employee information will be stored securely and efficiently.",
            "Payroll data requires structured storage for easy retrieval.",
            "Work hour tracking data is being analyzed for optimal storage.",
            "Personnel records need secure and organized storage systems.",
            "Time tracking information is being processed for database storage.",
            "Employee data requires careful analysis for proper backend selection."
        ])
        
        self.text_corpus['storage'].extend([
            "Selecting optimal storage backend based on data characteristics.",
            "Analyzing data patterns to determine best storage approach.",
            "Your data is being evaluated for the most suitable storage method.",
            "Running intelligence algorithms to choose appropriate backend.",
            "Data complexity analysis complete, selecting storage system.",
            "Examining data structure to recommend optimal storage solution."
        ])
        
        self.text_corpus['analysis'].extend([
            "Data analysis reveals interesting patterns in your information.",
            "The complexity of your data suggests specific storage requirements.",
            "Pattern recognition indicates this data type benefits from structured storage.",
            "Your data characteristics point toward a particular storage approach.",
            "Analysis complete, data patterns are clear and actionable."
        ])
    
    def process_training_file(self, file_path):
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            filename = file_path.name.lower()
            
            # Enhanced file type recognition for expanded datasets
            if 'shakespeare' in filename or 'hamlet' in filename or 'macbeth' in filename:
                self.extract_shakespeare_responses(content)
            elif 'english' in filename or 'grammar' in filename or 'corpus' in filename or 'words' in filename:
                self.extract_natural_responses(content)
            elif 'math' in filename or 'formula' in filename:
                self.extract_math_responses(content)
            elif 'business' in filename or 'commercial' in filename or 'payroll' in filename or 'financial' in filename:
                self.extract_business_responses(content)
            elif 'technology' in filename or 'programming' in filename or 'technical' in filename:
                self.extract_tech_responses(content)
            elif 'education' in filename or 'academic' in filename:
                self.extract_education_responses(content)
            elif 'medical' in filename or 'health' in filename:
                self.extract_medical_responses(content)
            elif 'job' in filename or 'names' in filename:
                self.extract_entity_responses(content)
            elif filename.endswith('.py') or filename.endswith('.js'):
                self.extract_code_responses(content)
            elif filename.endswith('.csv'):
                self.extract_csv_responses(content)
                
        except Exception:
            pass
    
    def extract_shakespeare_responses(self, content):
        lines = content.split('\n')
        responses = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('***') and not line.isupper():
                if any(char.isalpha() for char in line):
                    if 20 < len(line) < 120 and line.endswith(('.', '!', '?')):
                        if self.is_clean_text(line):
                            responses.append(line)
        
        if responses:
            self.text_corpus['shakespeare'].extend(responses[:50])
    
    def extract_natural_responses(self, content):
        sentences = re.split(r'[.!?]+', content)
        responses = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence.startswith('***'):
                if 15 < len(sentence) < 100 and any(char.isalpha() for char in sentence):
                    if self.is_clean_text(sentence):
                        responses.append(sentence + '.')
        
        if responses:
            self.text_corpus['natural'].extend(responses[:30])
    
    def extract_math_responses(self, content):
        lines = content.split('\n')
        responses = []
        for line in lines:
            if any(symbol in line for symbol in ['=', '+', '-', '*', '/', '^']):
                line = line.strip()
                if self.is_clean_text(line) and 5 < len(line) < 60:
                    responses.append(f"Mathematical analysis: {line}")
        
        if responses:
            self.text_corpus['math'].extend(responses[:20])
    
    def extract_business_responses(self, content):
        """Extract business-related terms and create contextual responses"""
        terms = content.split('\n') if '\n' in content else content.split()
        responses = []
        
        for term in terms:
            term = term.strip()
            if term and len(term) > 3:
                responses.append(f"Business data containing '{term}' detected, selecting appropriate storage backend.")
                responses.append(f"Processing {term} information with enhanced business logic.")
        
        if responses:
            self.text_corpus['business'].extend(responses[:40])
    
    def extract_tech_responses(self, content):
        """Extract technology-related terms and create contextual responses"""
        terms = content.split('\n') if '\n' in content else content.split()
        responses = []
        
        for term in terms:
            term = term.strip()
            if term and len(term) > 2:
                responses.append(f"Technical data type '{term}' identified, optimizing storage approach.")
                responses.append(f"Technology-related information '{term}' requires specialized processing.")
        
        if responses:
            self.text_corpus['code'].extend(responses[:40])
    
    def extract_education_responses(self, content):
        """Extract education-related terms and create contextual responses"""
        terms = content.split('\n') if '\n' in content else content.split()
        responses = []
        
        for term in terms:
            term = term.strip()
            if term and len(term) > 3:
                responses.append(f"Educational data involving '{term}' detected, applying academic storage protocols.")
                responses.append(f"Academic information '{term}' processed with educational context awareness.")
        
        if responses:
            self.text_corpus['language'].extend(responses[:30])
    
    def extract_medical_responses(self, content):
        """Extract medical terms and create healthcare-specific responses"""
        terms = content.split('\n')
        responses = []
        
        for term in terms:
            term = term.strip()
            if term and len(term) > 3:
                responses.append(f"Medical data containing '{term}' requires secure and compliant storage.")
                responses.append(f"Healthcare information '{term}' processed with privacy protocols.")
        
        if responses:
            self.text_corpus['business'].extend(responses[:35])
    
    def extract_entity_responses(self, content):
        """Extract entity names and create recognition responses"""
        entities = content.split('\n')
        responses = []
        
        for entity in entities:
            entity = entity.strip()
            if entity and len(entity) > 2:
                responses.append(f"Entity '{entity}' recognized, applying appropriate data classification.")
                responses.append(f"Named entity '{entity}' detected, enhancing storage metadata.")
        
        if responses:
            self.text_corpus['analysis'].extend(responses[:30])
    
    def extract_csv_responses(self, content):
        """Extract information from CSV files"""
        lines = content.split('\n')
        responses = []
        
        if lines:
            headers = lines[0].split(',') if lines else []
            for header in headers:
                header = header.strip()
                if header:
                    responses.append(f"CSV column '{header}' analyzed for optimal storage structure.")
        
        if responses:
            self.text_corpus['storage'].extend(responses[:20])
    
    def extract_code_responses(self, content):
        comments = re.findall(r'#\s*(.+)|//\s*(.+)', content)
        responses = []
        for comment_tuple in comments:
            comment = comment_tuple[0] or comment_tuple[1]
            if comment and self.is_clean_text(comment) and 8 < len(comment) < 60:
                responses.append(f"Code insight: {comment.strip()}")
        
        if responses:
            self.text_corpus['code'].extend(responses[:20])
    
    def is_clean_text(self, text):
        if not text:
            return False
        try:
            return all(ord(char) < 127 and (char.isalnum() or char in ' .,!?-()[]{}:;"\'') for char in text)
        except:
            return False
    
    def generate_response(self, user_input, context="general"):
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            greetings = [
                "Hello there, how can I assist you today?",
                "Greetings, I'm ready to help with your data.",
                "Hi, what would you like to do with the database?",
                "Welcome to the smart storage system.",
                "Good to see you, how may I help?"
            ]
            return random.choice(greetings)
        
        elif any(word in input_lower for word in ['payroll', 'employee', 'work', 'hours', 'salary', 'staff']):
            if self.text_corpus['business']:
                return random.choice(self.text_corpus['business'])
            return "Processing your business data with secure storage methods."
        
        elif any(word in input_lower for word in ['store', 'save', 'storage', 'backend']):
            if self.text_corpus['storage']:
                return random.choice(self.text_corpus['storage'])
            return "Analyzing your data for optimal storage solution."
        
        elif any(word in input_lower for word in ['analyze', 'analysis', 'pattern', 'examine']):
            if self.text_corpus['analysis']:
                return random.choice(self.text_corpus['analysis'])
            return "Running comprehensive analysis on your data."
        
        elif any(word in input_lower for word in ['shakespeare', 'hamlet', 'macbeth']):
            if self.text_corpus['shakespeare']:
                return random.choice(self.text_corpus['shakespeare'])
            return "Literary analysis capabilities available."
        
        elif any(word in input_lower for word in ['math', 'formula', 'equation', 'calculate']):
            if self.text_corpus['math']:
                return random.choice(self.text_corpus['math'])
            return "Mathematical computation and storage ready."
        
        elif any(word in input_lower for word in ['code', 'function', 'programming', 'algorithm']):
            if self.text_corpus['code']:
                return random.choice(self.text_corpus['code'])
            return "Code analysis and structured storage available."
        
        else:
            if self.text_corpus['natural']:
                return random.choice(self.text_corpus['natural'])
            
            fallbacks = [
                "I understand your request and will process it accordingly.",
                "Let me handle that for you with the appropriate methods.",
                "Your data is being processed with intelligent algorithms.",
                "Working on your request using advanced storage techniques.",
                "Processing your information with contextual analysis."
            ]
            return random.choice(fallbacks)

class DatasetLearner:
    def __init__(self, datasets_path="datasets"):
        self.datasets_path = Path(datasets_path)
        self.knowledge_base = {}
        self.load_knowledge()
    
    def load_knowledge(self):
        if os.path.exists("knowledge_base.pkl"):
            try:
                with open("knowledge_base.pkl", "rb") as f:
                    self.knowledge_base = pickle.load(f)
            except:
                self.learn_from_datasets()
                self.save_knowledge()
        else:
            self.learn_from_datasets()
            self.save_knowledge()
    
    def learn_from_datasets(self):
        if self.datasets_path.exists():
            for dataset_file in self.datasets_path.glob("*"):
                if dataset_file.is_file():
                    self.process_dataset(dataset_file)
    
    def process_dataset(self, file_path):
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            filename = file_path.name
            file_type = file_path.suffix.lower()
            
            if file_type == '.txt':
                self.extract_text_patterns(content, filename)
            elif file_type in ['.py', '.js']:
                self.extract_code_patterns(content, filename)
            elif file_type == '.sql':
                self.extract_sql_patterns(content, filename)
                
        except Exception:
            pass
    
    def extract_text_patterns(self, content, filename):
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]
        self.knowledge_base[filename] = {
            "type": "text",
            "words": [word for word, freq in common_words],
            "complexity": calculate_entropy(content)
        }
    
    def extract_code_patterns(self, content, filename):
        functions = re.findall(r'def\s+(\w+)|function\s+(\w+)', content)
        classes = re.findall(r'class\s+(\w+)', content)
        
        self.knowledge_base[filename] = {
            "type": "code",
            "functions": [f[0] or f[1] for f in functions],
            "classes": classes,
            "complexity": calculate_entropy(content)
        }
    
    def extract_sql_patterns(self, content, filename):
        tables = re.findall(r'CREATE\s+TABLE\s+(\w+)', content, re.IGNORECASE)
        
        self.knowledge_base[filename] = {
            "type": "sql",
            "tables": tables,
            "complexity": calculate_entropy(content)
        }
    
    def save_knowledge(self):
        try:
            with open("knowledge_base.pkl", "wb") as f:
                pickle.dump(self.knowledge_base, f)
        except:
            pass
    
    def analyze_input(self, user_input):
        suggestions = []
        input_lower = user_input.lower()
        
        for filename, knowledge in self.knowledge_base.items():
            if knowledge["type"] == "text":
                for word in knowledge.get("words", [])[:5]:
                    if word in input_lower:
                        suggestions.append(f"Text patterns found in {filename}")
                        break
            elif knowledge["type"] == "code":
                for func in knowledge.get("functions", []):
                    if func.lower() in input_lower:
                        suggestions.append(f"Code patterns detected in {filename}")
                        break
            elif knowledge["type"] == "sql":
                if any(word in input_lower for word in ['select', 'table', 'database']):
                    suggestions.append(f"SQL patterns recognized in {filename}")
                    break
        
        return suggestions[:2]

class SmartCLI:
    def __init__(self):
        self.storage = SimpleStorage()
        self.learner = DatasetLearner()
        self.response_gen = ResponseGenerator()
        self.language_processor = LanguageProcessor()
        self.session_data = []
    
    def start(self):
        welcome = self.response_gen.generate_response("welcome hello")
        print(f"Smart Database CLI")
        print(f"{welcome}")
        print("Commands: store, retrieve, search, analyze, help, quit")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    farewell = self.response_gen.generate_response("goodbye farewell")
                    print(farewell)
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                elif user_input.startswith('store '):
                    self.handle_store(user_input[6:])
                elif user_input.startswith('add '):
                    self.handle_store(user_input[4:])
                elif user_input.startswith('retrieve '):
                    self.handle_retrieve(user_input[9:])
                elif user_input.startswith('search '):
                    self.handle_search(user_input[7:])
                elif user_input.startswith('analyze '):
                    self.handle_analyze(user_input[8:])
                else:
                    self.handle_conversation(user_input)
                    
            except KeyboardInterrupt:
                print("\nGoodbye")
                break
            except Exception as e:
                error_msg = self.response_gen.generate_response("error problem")
                print(f"{error_msg}: {e}")
    
    def show_help(self):
        help_msg = self.response_gen.generate_response("help assistance")
        print(f"\n{help_msg}")
        print("Available commands:")
        print("  store <data>     - Store data intelligently")
        print("  add <data>       - Add data (same as store)")
        print("  retrieve <key>   - Get stored data")
        print("  search <term>    - Search data")
        print("  analyze <data>   - Analyze data patterns")
        print("  help            - Show commands")
        print("  quit            - Exit")
    
    def handle_store(self, data):
        processed = self.language_processor.process(data)
        domain = processed['parsed'].get('domain', 'general')
        
        response = self.response_gen.generate_response(f"store {data[:50]}", "storage")
        print(response)
        
        print(f"Data type detected: {processed['parsed']['data_type']}")
        print(f"Domain classified as: {domain}")
        
        if processed['parsed']['entities']:
            print("Extracted entities:")
            for key, value in processed['parsed']['entities'].items():
                if value is not None:
                    print(f"  {key}: {value}")
        
        if processed['parsed']['relationships']:
            for rel in processed['parsed']['relationships']:
                if rel['type'] == 'calculation':
                    print(f"  Calculated {rel['formula']} = {rel['result']}")
        
        storage_type = processed['structured']['storage_recommendation']
        print(f"Storage recommendation: {storage_type}")
        
        try:
            # Create a more detailed data record
            record_data = {
                'original_input': data,
                'timestamp': datetime.now().isoformat(),
                'entities': processed['parsed']['entities'],
                'domain': domain,
                'data_type': processed['parsed']['data_type']
            }
            
            structured_data = json.dumps(record_data)
            record_key = f"data_{len(self.session_data)}_{domain}"
            backend = self.storage.store_data(record_key, structured_data)
            
            success_responses = [
                f"Data structured and stored using {backend.title()} Storage",
                f"Successfully processed {domain} domain data and saved to {backend.title()}",
                f"Intelligent processing complete, {domain} data stored in {backend.title()} backend",
                f"Domain-aware storage complete - {backend.title()} selected for {domain} data"
            ]
            print(random.choice(success_responses))
            
            # Store in session for easy retrieval
            processed['storage_info'] = {
                'key': record_key,
                'backend': backend,
                'timestamp': record_data['timestamp']
            }
            self.session_data.append(processed)
            
            print(f"Record stored with key: {record_key}")
            
        except Exception as e:
            error_msg = self.response_gen.generate_response("error failed", "error")
            print(f"{error_msg}: {e}")
    
    def handle_retrieve(self, key):
        try:
            result = self.storage.retrieve_data(key)
            if result:
                found_msg = self.response_gen.generate_response("found retrieved")
                print(f"{found_msg}: {result}")
            else:
                not_found_msg = self.response_gen.generate_response("not found missing")
                print(not_found_msg)
        except Exception as e:
            error_msg = self.response_gen.generate_response("error problem")
            print(f"{error_msg}: {e}")
    
    def handle_search(self, term):
        search_msg = self.response_gen.generate_response(f"searching {term}")
        print(search_msg)
        
        found_count = 0
        for i, data in enumerate(self.session_data):
            if term.lower() in data.lower():
                print(f"  Found in session {i}: {data[:60]}...")
                found_count += 1
        
        if found_count == 0:
            none_msg = self.response_gen.generate_response("nothing found")
            print(none_msg)
    
    def handle_analyze(self, data):
        processed = self.language_processor.process(data)
        
        analysis_msg = self.response_gen.generate_response(f"analyzing {data[:20]}", "analysis")
        print(analysis_msg)
        
        print("Lexical analysis:")
        for token in processed['tokens'][:10]:
            print(f"  {token['type']}: '{token['value']}'")
        
        print(f"\nSemantic analysis:")
        print(f"  Data type: {processed['parsed']['data_type']}")
        print(f"  Confidence: {processed['parsed']['metadata'].get('confidence', 0):.2f}")
        
        if processed['parsed']['entities']:
            print(f"  Entities found: {len(processed['parsed']['entities'])}")
        
        entropy = calculate_entropy(data)
        confidence = deep_confidence_analysis(data)
        backend = self.storage.evaluate_storage_backend(data)
        
        print(f"\nTechnical metrics:")
        print(f"  Data entropy: {entropy:.3f}")
        print(f"  Pattern confidence: {confidence:.3f}")
        print(f"  Recommended backend: {backend}")
        print(f"  Storage type: {processed['structured']['storage_recommendation']}")
        
        if processed['structured']['indexing_strategy']:
            print(f"  Indexing strategy: {', '.join(processed['structured']['indexing_strategy'])}")
    
    def handle_conversation(self, user_input):
        """Enhanced conversation handling with programming request detection and data retrieval"""
        # Check for data retrieval requests first
        if self.is_data_retrieval_request(user_input):
            self.handle_data_retrieval(user_input)
            return
            
        # Detect programming requests
        programming_keywords = ['make', 'create', 'generate', 'build', 'write', 'develop', 'implement', 'show', 'example', 'pull', 'information']
        code_keywords = ['python', 'javascript', 'c', 'algorithm', 'function', 'class', 'sort', 'search', 'linked list', 'array', 'tree', 'file']
        
        user_lower = user_input.lower()
        is_programming_request = any(keyword in user_lower for keyword in programming_keywords)
        is_code_related = any(keyword in user_lower for keyword in code_keywords)
        
        if is_programming_request and is_code_related:
            self.handle_programming_request(user_input)
            return
        
        response = self.response_gen.generate_response(user_input)
        print(response)
        
        suggestions = self.learner.analyze_input(user_input)
        if suggestions:
            suggest_msg = self.response_gen.generate_response("suggestions recommendations")
            print(f"Based on training data: {random.choice(suggestions)}")
    
    def is_data_retrieval_request(self, user_input):
        """Check if user is requesting to retrieve stored data"""
        retrieval_keywords = ['pull', 'get', 'find', 'search', 'list', 'show', 'display', 'retrieve']
        info_keywords = ['information', 'info', 'data', 'about', 'details', 'records']
        
        user_lower = user_input.lower()
        has_retrieval = any(keyword in user_lower for keyword in retrieval_keywords)
        has_info = any(keyword in user_lower for keyword in info_keywords)
        
        return has_retrieval and has_info
    
    def handle_data_retrieval(self, user_input):
        """Handle data retrieval requests using prolist search functions"""
        from prolist import linear_search, find_all_occurrences, search_by_pattern
        
        user_lower = user_input.lower()
        
        # Extract search terms with better pattern matching
        search_terms = self.extract_search_terms(user_lower)
        
        print(f"Searching for: {', '.join(search_terms) if search_terms else 'all stored data'}")
        print("=" * 60)
        
        # Search in stored session data
        session_results = self.search_session_data(search_terms)
        
        # Search in database
        db_results = self.search_database(search_terms)
        
        # Search in training datasets for relevant examples
        dataset_examples = self.search_datasets(search_terms)
        
        # Display comprehensive results
        total_found = len(session_results) + len(db_results)
        
        if total_found > 0:
            print(f"Found {total_found} matching records:")
            print()
            
            # Display session data with improved formatting
            for idx, (session_idx, data) in enumerate(session_results, 1):
                print(f"Session Record #{idx}:")
                self.display_formatted_data(data)
                print()
            
            # Display database results with enhanced details
            for idx, record in enumerate(db_results, len(session_results) + 1):
                print(f"Database Record #{idx}:")
                self.display_database_record(record)
                print()
                
            # Show relevant examples from datasets
            if dataset_examples:
                print("Relevant examples from training data:")
                for example in dataset_examples[:3]:  # Show top 3 examples
                    print(f"  - {example}")
                print()
                
            # Provide programming examples if requested
            if any(lang in user_lower for lang in ['python', 'javascript', 'c']):
                self.provide_code_export_example(session_results, db_results, user_lower)
                
        else:
            print("No matching data found.")
            print("Available data categories:")
            self.show_available_categories()
            print()
            print("Try these example searches:")
            print("  - pull employee information")
            print("  - list customer data")
            print("  - show project records")
            print("  - get medical information")
    
    def extract_search_terms(self, user_input):
        """Extract meaningful search terms from user input"""
        # Remove common words and extract meaningful terms
        stop_words = {'pull', 'get', 'find', 'search', 'list', 'show', 'display', 'retrieve',
                      'any', 'information', 'info', 'data', 'about', 'details', 'records',
                      'the', 'and', 'or', 'from', 'for', 'with', 'by'}
        
        words = user_input.lower().split()
        meaningful_terms = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Add specific domain terms if detected
        domain_terms = []
        if 'employee' in user_input or 'staff' in user_input:
            domain_terms.append('employee')
        if 'customer' in user_input or 'client' in user_input:
            domain_terms.append('customer')
        if 'patient' in user_input or 'medical' in user_input:
            domain_terms.append('patient')
        if 'project' in user_input or 'development' in user_input:
            domain_terms.append('project')
        if 'student' in user_input or 'course' in user_input:
            domain_terms.append('student')
        
        return list(set(meaningful_terms + domain_terms))
    
    def search_session_data(self, search_terms):
        """Search through session data with improved matching"""
        found_data = []
        
        for i, session_item in enumerate(self.session_data):
            if self.matches_search_criteria(session_item, search_terms):
                found_data.append((i, session_item))
        
        return found_data
    
    def search_datasets(self, search_terms):
        """Search through training datasets for relevant examples"""
        examples = []
        dataset_dir = 'datasets'
        
        if not os.path.exists(dataset_dir) or not search_terms:
            return examples
        
        try:
            for filename in os.listdir(dataset_dir):
                if not filename.endswith(('.txt', '.py', '.js', '.sql')):
                    continue
                    
                filepath = os.path.join(dataset_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                    # Check if any search terms match the content
                    if any(term.lower() in content for term in search_terms):
                        # Extract relevant lines
                        lines = content.split('\n')
                        for line in lines:
                            if any(term.lower() in line for term in search_terms) and len(line.strip()) > 10:
                                examples.append(f"{filename}: {line.strip()[:100]}")
                                if len(examples) >= 10:  # Limit examples
                                    break
                except:
                    continue
        except:
            pass
        
        return examples
    
    def display_database_record(self, record):
        """Display database record with enhanced formatting"""
        key, value, backend = record
        
        print(f"   Key: {key}")
        print(f"   Backend: {backend}")
        
        try:
            # Try to parse JSON data
            data = json.loads(value)
            print(f"   Data Type: {data.get('data_type', 'Unknown')}")
            print(f"   Domain: {data.get('domain', 'General')}")
            print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            
            if 'entities' in data and data['entities']:
                print("   Entities:")
                for ent_key, ent_value in data['entities'].items():
                    if ent_value is not None:
                        print(f"      {ent_key}: {ent_value}")
        except:
            # Fallback for non-JSON data
            print(f"   Data: {value[:100]}{'...' if len(value) > 100 else ''}")
    
    def show_available_categories(self):
        """Show available data categories in the database"""
        try:
            conn = sqlite3.connect(self.storage.db_path)
            cursor = conn.cursor()
            
            # Get sample of stored keys to show categories
            cursor.execute('SELECT DISTINCT key FROM data_store LIMIT 10')
            keys = [row[0] for row in cursor.fetchall()]
            
            if keys:
                print("Stored data categories:")
                categories = set()
                for key in keys:
                    if '_' in key:
                        category = key.split('_')[-1]  # Get domain from key
                        categories.add(category)
                
                for category in sorted(categories):
                    cursor.execute('SELECT COUNT(*) FROM data_store WHERE key LIKE ?', (f'%_{category}',))
                    count = cursor.fetchone()[0]
                    print(f"  {category}: {count} records")
            
            conn.close()
        except Exception as e:
            print(f"Could not retrieve categories: {e}")
    
    def provide_code_export_example(self, session_data, db_data, user_input):
        """Provide language-specific code examples for data export"""
        
        if 'python' in user_input:
            print("Python code to export this data:")
            print(self.generate_python_export_code(session_data, db_data))
        elif 'javascript' in user_input:
            print("JavaScript code to process this data:")
            print(self.generate_javascript_export_code(session_data, db_data))
        elif 'c' in user_input:
            print("C code structure for this data:")
            print(self.generate_c_export_code(session_data, db_data))
    
    def generate_python_export_code(self, session_data, db_data):
        """Generate Python code example for exporting found data"""
        return '''
import json
import sqlite3
from datetime import datetime

def export_search_results():
    # Session data found
    session_records = []'''+ (f'''
    # Sample from {len(session_data)} session records
    for record in session_data:
        session_records.append(record['parsed']['entities'])
    ''' if session_data else '') + f'''
    
    # Database records found  
    db_records = []'''+ (f'''
    # Sample from {len(db_data)} database records
    for key, value, backend in db_records:
        try:
            data = json.loads(value)
            db_records.append({{
                'key': key,
                'backend': backend,
                'data': data
            }})
        except:
            db_records.append({{'key': key, 'raw_value': value}})
    ''' if db_data else '') + '''
    
    # Export combined results
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'session_count': len(session_records),
        'database_count': len(db_records),
        'session_data': session_records,
        'database_data': db_records
    }
    
    with open('search_results.json', 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print("Search results exported to search_results.json")

export_search_results()
'''
    
    def generate_javascript_export_code(self, session_data, db_data):
        """Generate JavaScript code example"""
        return f'''
// JavaScript code to process search results
const searchResults = {{
    sessionData: {len(session_data)} records,
    databaseData: {len(db_data)} records,
    exportTimestamp: new Date().toISOString()
}};

function processSearchResults(results) {{
    console.log(`Found ${{results.sessionData}} session records`);
    console.log(`Found ${{results.databaseData}} database records`);
    
    // Process and display results
    return {{
        totalRecords: results.sessionData + results.databaseData,
        timestamp: results.exportTimestamp
    }};
}}

const processed = processSearchResults(searchResults);
console.log(processed);
'''
    
    def generate_c_export_code(self, session_data, db_data):
        """Generate C code structure example"""
        return f'''
// C structure for search results
#include <stdio.h>
#include <stdlib.h>

typedef struct {{
    int session_count;
    int database_count;
    char timestamp[64];
}} SearchResults;

int main() {{
    SearchResults results = {{
        .session_count = {len(session_data)},
        .database_count = {len(db_data)},
        .timestamp = "2024-09-06"
    }};
    
    printf("Search Results:\\n");
    printf("Session records: %d\\n", results.session_count);
    printf("Database records: %d\\n", results.database_count);
    printf("Total found: %d\\n", results.session_count + results.database_count);
    
    return 0;
}}
'''
    
    def matches_search_criteria(self, data_item, search_terms):
        """Check if a data item matches search criteria"""
        if not search_terms:
            return True
            
        # Convert data to searchable string
        searchable_text = json.dumps(data_item, default=str).lower()
        
        return any(term.lower() in searchable_text for term in search_terms)
    
    def search_database(self, search_terms):
        """Search the SQLite database for matching records"""
        try:
            conn = sqlite3.connect(self.storage.db_path)
            cursor = conn.cursor()
            
            if search_terms:
                # Search for any of the terms in the value field
                placeholders = ' OR '.join(['value LIKE ?' for _ in search_terms])
                query = f'SELECT key, value, backend FROM data_store WHERE {placeholders}'
                params = [f'%{term}%' for term in search_terms]
                cursor.execute(query, params)
            else:
                # Return all records
                cursor.execute('SELECT key, value, backend FROM data_store')
            
            results = cursor.fetchall()
            conn.close()
            return results
            
        except Exception as e:
            print(f"Database search error: {e}")
            return []
    
    def display_formatted_data(self, data_item):
        """Display data in a formatted, readable way"""
        if 'parsed' in data_item:
            parsed = data_item['parsed']
            
            print(f"   Data Type: {parsed.get('data_type', 'Unknown')}")
            print(f"   Domain: {parsed.get('domain', 'General')}")
            
            if parsed.get('entities'):
                print("   Extracted Information:")
                for key, value in parsed['entities'].items():
                    if value is not None:
                        print(f"      - {key}: {value}")
            
            if parsed.get('relationships'):
                print("   Relationships:")
                for rel in parsed['relationships']:
                    if rel.get('type') == 'calculation':
                        print(f"      - {rel.get('formula', '')} = {rel.get('result', '')}")
        
        if 'structured' in data_item:
            storage_rec = data_item['structured'].get('storage_recommendation', 'Unknown')
            print(f"   Storage: {storage_rec}")
    
    def show_data_export_example(self, session_data, db_data):
        """Show Python code example to export the found data"""
        print("""
```python
import json
import sqlite3
from datetime import datetime

def export_found_data():
    # Session data
    session_records = [""")
        
        for _, data in session_data[:2]:  # Show first 2 records as example
            entities = data.get('parsed', {}).get('entities', {})
            print(f"        {json.dumps(entities, indent=8)},")
        
        print("""    ]
    
    # Export to JSON file
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'total_records': len(session_records),
        'records': session_records
    }
    
    with open('exported_data.json', 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print("Data exported to exported_data.json")

# Run the export
export_found_data()
```""")
        print()
    
    def handle_programming_request(self, user_input):
        """Handle specific programming requests with relevant code examples"""
        user_lower = user_input.lower()
        
        if 'python' in user_lower and 'file' in user_lower:
            print(self.provide_python_file_example())
        elif 'python' in user_lower and ('information' in user_lower or 'data' in user_lower):
            print(self.provide_python_data_example())
        elif 'animation' in user_lower and 'c' in user_lower:
            print(self.provide_c_animation_example())
        elif 'c' in user_lower and 'terminal' in user_lower:
            print(self.provide_c_terminal_example())
        elif 'sort' in user_lower and 'linked list' in user_lower:
            print(self.provide_linked_list_sort_example())
        elif 'javascript' in user_lower and 'math' in user_lower:
            print(self.provide_javascript_math_example())
        elif 'javascript' in user_lower and 'function' in user_lower:
            print(self.provide_javascript_examples())
        elif 'c' in user_lower and ('program' in user_lower or 'example' in user_lower):
            print(self.provide_c_examples())
        elif 'sort' in user_lower:
            print(self.provide_sort_examples())
        elif 'search' in user_lower:
            print(self.provide_search_examples())
        elif 'linked list' in user_lower:
            print(self.provide_linked_list_examples())
        elif 'python' in user_lower and 'example' in user_lower:
            print(self.provide_python_examples())
        else:
            print("I can help you with programming examples. Try asking for specific algorithms like 'sort linked list', 'binary search', 'javascript math functions', 'C terminal animation', 'python file operations', or 'python examples'.")
    
    def provide_python_file_example(self):
        """Provide Python file writing example"""
        return """Here's a Python example to write data to a file:

```python
import json
import csv
from datetime import datetime

def write_person_data_to_file(person_info, filename="person_data.txt"):
    '''
    Write person information to various file formats
    '''
    
    # Example person data
    if not person_info:
        person_info = {
            "name": "Crissy Deutsch", 
            "occupation": "Software Developer",
            "skills": ["Python", "JavaScript", "Database Design"],
            "experience_years": 5,
            "last_updated": datetime.now().isoformat()
        }
    
    # 1. Write to text file
    with open(f"{filename}.txt", 'w') as f:
        f.write("=== PERSON INFORMATION ===\\n")
        for key, value in person_info.items():
            f.write(f"{key.upper()}: {value}\\n")
    
    # 2. Write to JSON file  
    with open(f"{filename}.json", 'w') as f:
        json.dump(person_info, f, indent=2)
    
    # 3. Write to CSV file
    with open(f"{filename}.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Field', 'Value'])  # Header
        for key, value in person_info.items():
            writer.writerow([key, value])
    
    print(f"Data written to {filename}.txt, {filename}.json, and {filename}.csv")
    return f"Files created successfully for {person_info.get('name', 'Unknown')}"

# Usage examples:
if __name__ == "__main__":
    # Example 1: Write sample data
    sample_data = {
        "name": "Crissy Deutsch",
        "location": "Tech Hub",
        "projects": ["Smart Database CLI", "NLP Processor", "Backend Systems"],
        "expertise": "Full-stack Development"
    }
    
    result = write_person_data_to_file(sample_data, "crissy_info")
    print(result)
    
    # Example 2: Read and display the data
    with open("crissy_info.json", 'r') as f:
        loaded_data = json.load(f)
        print("\\nLoaded data:", loaded_data)
```

**Key Features:**
• Multiple file format support (TXT, JSON, CSV)
• Error handling and validation
• Structured data organization
• Easy to modify and extend
• Professional file naming conventions"""
    
    def provide_python_data_example(self):
        """Provide Python data handling example"""
        return """Here's a comprehensive Python example for data handling and file operations:

```python
import json
import sqlite3
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class PersonInfo:
    name: str
    skills: List[str]
    experience: int
    projects: List[str]
    
class DataManager:
    def __init__(self, db_path="people.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                data TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def save_person(self, person: PersonInfo):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        person_data = {
            'skills': person.skills,
            'experience': person.experience,
            'projects': person.projects
        }
        
        cursor.execute('''
            INSERT OR REPLACE INTO people (name, data) 
            VALUES (?, ?)
        ''', (person.name, json.dumps(person_data)))
        
        conn.commit()
        conn.close()
        
        # Also write to file
        self.write_to_file(person)
        
        return f"Saved {person.name} to database and file"
    
    def write_to_file(self, person: PersonInfo):
        filename = f"{person.name.lower().replace(' ', '_')}_data.json"
        
        data = {
            'name': person.name,
            'skills': person.skills,
            'experience_years': person.experience,
            'projects': person.projects,
            'file_created': True
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"File created: {filename}")

# Example usage:
if __name__ == "__main__":
    # Create data manager
    dm = DataManager()
    
    # Create person info
    crissy = PersonInfo(
        name="Crissy Deutsch",
        skills=["Python", "Database Design", "NLP", "Backend Development"],
        experience=5,
        projects=["Smart CLI", "Language Processor", "Multi-Backend Storage"]
    )
    
    # Save the data
    result = dm.save_person(crissy)
    print(result)
```

This example demonstrates professional data handling, database storage, and file operations."""
    
    def provide_c_animation_example(self):
        """Provide a cool C terminal animation example"""
        return """Here's a cool C terminal animation - Matrix Rain Effect:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

void matrix_rain() {
    char matrix[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*";
    int cols = 80, rows = 24;
    srand(time(NULL));
    
    printf("\\033[2J\\033[H"); // Clear screen and move cursor to top
    printf("\\033[32m"); // Green color
    
    for (int frame = 0; frame < 100; frame++) {
        printf("\\033[H"); // Move cursor to top
        
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (rand() % 8 == 0) {
                    // Bright green for new characters
                    printf("\\033[1;32m%c\\033[0;32m", matrix[rand() % strlen(matrix)]);
                } else if (rand() % 25 == 0) {
                    // Dim green for fading characters
                    printf("\\033[2;32m%c\\033[0;32m", matrix[rand() % strlen(matrix)]);
                } else {
                    printf(" ");
                }
            }
            printf("\\n");
        }
        
        usleep(100000); // 100ms delay
    }
    
    printf("\\033[0m"); // Reset color
    printf("\\033[2J\\033[H"); // Clear screen
}

int main() {
    printf("Starting Matrix Rain Animation...\\n");
    sleep(1);
    matrix_rain();
    printf("Animation complete!\\n");
    return 0;
}
```

**Compile and run:**
```bash
gcc -o matrix matrix.c
./matrix
```

**Features:**
• Uses ANSI escape codes for colors and cursor control
• Random character generation for authentic matrix effect
• Adjustable frame rate with usleep()
• Green terminal styling like the movie
• Cross-platform compatible (Unix/Linux/macOS)

**Other cool animations you can try:**
• Bouncing ball physics simulation
• ASCII fire effect with flickering
• Starfield 3D depth simulation
• Snake game with real-time movement
• Progress bars with color gradients"""
    
    def provide_c_terminal_example(self):
        """Provide C terminal programming examples"""
        return """Here are cool C terminal programming techniques:

**1. Colors and Formatting:**
```c
printf("\\033[31mRed text\\033[0m\\n");        // Red
printf("\\033[32mGreen text\\033[0m\\n");      // Green  
printf("\\033[33mYellow text\\033[0m\\n");     // Yellow
printf("\\033[1mBold text\\033[0m\\n");        // Bold
printf("\\033[4mUnderlined\\033[0m\\n");       // Underline
```

**2. Cursor Control:**
```c
printf("\\033[H");        // Move to top-left
printf("\\033[10;5H");    // Move to row 10, col 5
printf("\\033[2J");       // Clear entire screen
printf("\\033[K");        // Clear line from cursor
```

**3. Simple Animation Loop:**
```c
for (int i = 0; i < 50; i++) {
    printf("\\r[");
    for (int j = 0; j < i; j++) printf("=");
    for (int j = i; j < 50; j++) printf(" ");
    printf("] %d%%", i * 2);
    fflush(stdout);
    usleep(100000);
}
```

**Advanced terminal control available for interactive games and animations!**"""
    
    def provide_c_examples(self):
        return "C programming examples I can provide:\n• Terminal animations and graphics\n• Data structures (linked lists, trees, stacks)\n• Algorithms (sorting, searching, recursion)\n• Memory management and pointers\n• File I/O and system programming\n• Game development and simulations\n\nWhat specific C topic interests you?"
    
    def provide_javascript_math_example(self):
        """Provide JavaScript math operations example"""
        return """Here's a comprehensive JavaScript function with all math operations:

function allMathOperations(a, b) {
    return {
        // Basic Operations
        addition: a + b,
        subtraction: a - b,
        multiplication: a * b,
        division: b !== 0 ? a / b : 'Division by zero',
        modulus: a % b,
        exponentiation: Math.pow(a, b),
        
        // Advanced Operations
        squareRoot: Math.sqrt(a),
        cubeRoot: Math.cbrt(a),
        absolute: Math.abs(a),
        ceiling: Math.ceil(a),
        floor: Math.floor(a),
        round: Math.round(a),
        
        // Trigonometric Functions
        sine: Math.sin(a),
        cosine: Math.cos(a),
        tangent: Math.tan(a),
        
        // Logarithmic Functions
        naturalLog: Math.log(a),
        log10: Math.log10(a),
        log2: Math.log2(a),
        
        // Random & Constants
        random: Math.random(),
        pi: Math.PI,
        e: Math.E
    };
}

// Usage example:
const result = allMathOperations(10, 3);
console.log(result.addition);     // 13
console.log(result.division);     // 3.333...
console.log(result.squareRoot);   // 3.162..."""
    
    def provide_javascript_examples(self):
        return "JavaScript examples I can provide:\n• Math operations and calculations\n• Array manipulation methods\n• Object-oriented programming\n• Async/await and Promises\n• DOM manipulation\n• ES6+ features\n\nWhat specific JavaScript topic interests you?"
    
    def provide_linked_list_sort_example(self):
        """Provide a complete linked list sorting example"""
        return """Here's a Python implementation to sort a linked list using merge sort:

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sort_linked_list(head):
    if not head or not head.next:
        return head
    
    # Find the middle point to split the list
    slow = fast = head
    prev = None
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    
    # Split the list into two halves
    prev.next = None
    
    # Recursively sort both halves
    left = sort_linked_list(head)
    right = sort_linked_list(slow)
    
    # Merge the sorted halves
    return merge_sorted_lists(left, right)

def merge_sorted_lists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 or l2
    return dummy.next

# Time Complexity: O(n log n)
# Space Complexity: O(log n) due to recursion stack"""
    
    def provide_sort_examples(self):
        return "Popular sorting algorithms:\n• Bubble Sort: O(n²) - Simple but inefficient\n• Merge Sort: O(n log n) - Stable and consistent\n• Quick Sort: O(n log n) average - Fast in practice\n• Heap Sort: O(n log n) - In-place sorting\n\nWhich algorithm would you like to see implemented?"
    
    def provide_search_examples(self):
        return "Search algorithms:\n• Linear Search: O(n) - Works on unsorted data\n• Binary Search: O(log n) - Requires sorted data\n• Hash Table Lookup: O(1) average - Uses extra space\n\nWhich search algorithm interests you?"
    
    def provide_linked_list_examples(self):
        return "Common linked list operations:\n• Insertion at head/tail: O(1)\n• Deletion by value: O(n)\n• Reverse list: O(n)\n• Find middle node: O(n)\n• Detect cycle: O(n)\n\nWhat specific operation would you like to see?"
    
    def provide_python_examples(self):
        return "I can provide Python examples for:\n• Data structures: lists, dicts, sets, trees\n• Algorithms: sorting, searching, graph traversal\n• OOP concepts: classes, inheritance, polymorphism\n• File handling, APIs, databases\n\nWhat topic interests you most?"

if __name__ == "__main__":
    cli = SmartCLI()
    cli.start()
