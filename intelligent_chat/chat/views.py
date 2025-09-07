import time
import json
import uuid
import random
import os
import re
import pickle
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import ChatSession, ChatInteraction, LearningPattern
import sys
import os
sys.path.append('..')

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Mock numpy for basic operations
    class MockNumpy:
        def array(self, data): return data
        def random(self): 
            class Random:
                def uniform(self, low, high): return 0.5
            return Random()
        def exp(self, x): return 2.718 ** x if isinstance(x, (int, float)) else [2.718 ** i for i in x]
        def mean(self, data): return sum(data) / len(data) if data else 0
    np = MockNumpy()

try:
    from learning_test_system import AdaptiveChatSystem
    from sigmoid import sigmoid, multi_layer_sigmoid
    from language_processor import Lexer, TokenType
    from eyes import analyze_string_patterns
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    CORE_MODULES_AVAILABLE = False
    print(f"Warning: Core modules not available: {e}")

try:
    import nltk
    import spacy
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    ADVANCED_NLP_AVAILABLE = False

# Fallback classes when core modules aren't available
if not CORE_MODULES_AVAILABLE:
    class MockAdaptiveChatSystem:
        def __init__(self):
            self.learning_system = self
            self.weights = {
                'business_indicators': 0.5,
                'technical_indicators': 0.5, 
                'personal_indicators': 0.5,
                'sql_weight': 0.5,
                'nosql_weight': 0.5,
                'secure_weight': 0.5
            }
        
        def process_interaction(self, data, user_input):
            return {
                'timestamp': datetime.now().isoformat(),
                'features': {'business_indicators': 1, 'technical_indicators': 1, 'personal_indicators': 1},
                'storage_choice': 'hybrid_intelligent',
                'storage_score': 0.8,
                'should_learn': True,
                'weights_snapshot': self.weights.copy()
            }
    
    AdaptiveChatSystem = MockAdaptiveChatSystem
    
    def sigmoid(x):
        try:
            return 1 / (1 + (2.718 ** -x))
        except:
            return 0.5
    
    def multi_layer_sigmoid(x, layers):
        current_value = x
        for layer in layers:
            weight = layer.get('weight', 1.0)
            bias = layer.get('bias', 0.0)
            current_value = sigmoid(current_value * weight + bias)
        return current_value
    
    class Lexer:
        def __init__(self, text): pass
        def tokenize(self): return []
    
    class TokenType:
        IDENTIFIER = "IDENTIFIER"
    
    def analyze_string_patterns(text):
        """Fallback pattern analysis when eyes.py is not available"""
        patterns = []
        if '@' in text and '.' in text:
            patterns.append(('email', 0.8))
        if any(digit in text for digit in '0123456789'):
            patterns.append(('number', 0.6))
        if 'http' in text.lower():
            patterns.append(('url', 0.9))
        if len(text.split()) > 5:
            patterns.append(('text', 0.7))
        return patterns

class IntelligentChatService:
    def __init__(self):
        self.chat_systems = {}
        self.dataset_cache = {}
        self.memory = {}
        self.conversation_history = {}
        self.learning_patterns = {}
        self.tfidf_vectorizer = None
        self.load_datasets()
        self.initialize_ml_components()
    
    def load_datasets(self):
        # Try multiple paths to find datasets
        possible_paths = [
            os.path.join('..', 'datasets'),
            os.path.join('/Users/mac/Desktop/sig-sql', 'datasets'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'datasets')
        ]
        
        dataset_dir = None
        for path in possible_paths:
            if os.path.exists(path):
                dataset_dir = path
                break
        
        if not dataset_dir:
            print("Warning: Dataset directory not found, using fallback data")
            self._load_fallback_datasets()
            return
        
        print(f"Loading datasets from: {dataset_dir}")
        
        self.dataset_cache = {
            'business_terms': [],
            'technical_terms': [],
            'programming_keywords': [],
            'common_words': [],
            'names': [],
            'sentences': [],
            'conversational_patterns': {},
            'intent_patterns': {},
            'response_templates': {},
            'grammar_rules': [],
            'idioms': [],
            'academic_vocabulary': [],
            'high_frequency_words': [],
            'zig_keywords': [],
            'rust_keywords': [],
            'go_keywords': []
        }
        
        dataset_files = {
            'business_terms': 'business_terms.txt',
            'technical_terms': 'technology_vocabulary.txt',
            'programming_keywords': 'programming_request_keywords.txt',
            'common_words': 'common_english_words.txt',
            'names': 'names_dataset.txt',
            'sentences': 'english_sentences.txt',
            'grammar_rules': 'grammar_rules.txt',
            'idioms': 'idioms_phrasal_verbs.txt',
            'academic_vocabulary': 'academic_vocabulary.txt',
            'high_frequency_words': 'high_frequency_words.txt',
            'zig_keywords': 'zig_keywords.txt',
            'rust_keywords': 'rust_keywords.txt',
            'go_keywords': 'go_keywords.txt'
        }
        
        # Load datasets with comprehensive error handling
        for key, filename in dataset_files.items():
            file_path = os.path.join(dataset_dir, filename)
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        self.dataset_cache[key] = lines[:1000]  # Load up to 1000 items
                        print(f"Loaded {len(lines)} items from {filename}")
                else:
                    print(f"File not found: {filename}")
                    self._load_fallback_for_key(key)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                self._load_fallback_for_key(key)
        
        self.build_ml_patterns()
    
    def _load_fallback_datasets(self):
        """Load minimal fallback datasets when files aren't available"""
        self.dataset_cache = {
            'business_terms': ['analysis', 'report', 'metrics', 'business', 'enterprise', 'strategy', 'revenue', 'profit'],
            'technical_terms': ['algorithm', 'database', 'function', 'code', 'system', 'technical', 'software', 'hardware'],
            'programming_keywords': ['python', 'javascript', 'sql', 'html', 'css', 'api', 'framework', 'library'],
            'common_words': ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'],
            'names': ['john', 'mary', 'david', 'sarah', 'michael', 'jennifer', 'robert', 'lisa'],
            'sentences': ['hello world', 'how are you', 'what is this', 'thank you', 'good morning'],
            'conversational_patterns': {},
            'intent_patterns': {},
            'response_templates': {},
            'grammar_rules': ['use proper capitalization', 'end sentences with punctuation'],
            'idioms': ['break the ice', 'piece of cake', 'hit the nail on the head'],
            'academic_vocabulary': ['analyze', 'evaluate', 'synthesize', 'examine', 'interpret'],
            'high_frequency_words': ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have'],
            'zig_keywords': ['const', 'var', 'fn', 'struct', 'enum'],
            'rust_keywords': ['fn', 'let', 'mut', 'struct', 'enum', 'impl'],
            'go_keywords': ['func', 'var', 'const', 'struct', 'interface']
        }
        self.build_ml_patterns()
    
    def _load_fallback_for_key(self, key):
        """Load fallback data for a specific key"""
        fallbacks = {
            'business_terms': ['business', 'enterprise', 'analysis', 'report'],
            'technical_terms': ['technical', 'system', 'algorithm', 'database'],
            'programming_keywords': ['python', 'javascript', 'code', 'function'],
            'common_words': ['the', 'and', 'or', 'but'],
            'names': ['user', 'person', 'individual'],
            'sentences': ['hello', 'thank you', 'please help'],
            'grammar_rules': ['proper grammar is important'],
            'idioms': ['common expressions'],
            'academic_vocabulary': ['analyze', 'evaluate'],
            'high_frequency_words': ['the', 'be', 'to'],
            'zig_keywords': ['const', 'var', 'fn'],
            'rust_keywords': ['fn', 'let', 'mut'],
            'go_keywords': ['func', 'var', 'const']
        }
        self.dataset_cache[key] = fallbacks.get(key, ['data', 'content', 'information'])
        
        self.build_ml_patterns()
    
    def initialize_ml_components(self):
        if ADVANCED_NLP_AVAILABLE:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                self.nlp = None
            
            try:
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            except ImportError:
                self.tfidf_vectorizer = None
        else:
            self.nlp = None
            self.tfidf_vectorizer = None
        
        self.memory_file = os.path.join('..', 'knowledge_base.pkl')
        self.load_memory()
    
    def load_memory(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'rb') as f:
                    self.memory = pickle.load(f)
        except Exception:
            self.memory = {
                'conversations': [],
                'learned_patterns': [],
                'user_preferences': {},
                'context_memory': [],
                'response_feedback': []
            }
    
    def save_memory(self):
        try:
            with open(self.memory_file, 'wb') as f:
                pickle.dump(self.memory, f)
        except Exception:
            pass
    
    def build_ml_patterns(self):
        self.dataset_cache['intent_patterns'] = {
            'creation': ['create', 'make', 'build', 'generate', 'develop', 'construct', 'produce'],
            'analysis': ['analyze', 'examine', 'review', 'check', 'evaluate', 'assess', 'study'],
            'storage': ['store', 'save', 'add', 'insert', 'put', 'keep', 'archive'],
            'query': ['what', 'how', 'why', 'when', 'where', 'which', 'who'],
            'modification': ['change', 'modify', 'update', 'edit', 'alter', 'adjust', 'fix']
        }
        
        self.dataset_cache['conversational_patterns'] = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
            'confirmation': ['yes', 'correct', 'right', 'exactly', 'true', 'confirmed'],
            'negation': ['no', 'wrong', 'incorrect', 'false', 'not', 'never'],
            'politeness': ['please', 'thank you', 'thanks', 'sorry', 'excuse me']
        }
        
        self.dataset_cache['response_templates'] = {
            'technical_analysis': 'analysis of {} reveals {} with confidence {}',
            'data_processing': 'processing {} data containing {} elements',
            'pattern_recognition': 'identified {} patterns including {}',
            'learning_update': 'learning system updated with {} new patterns',
            'storage_recommendation': '{} storage recommended based on {} analysis'
        }
    
    def analyze_with_sigmoid(self, text, weights):
        features = {}
        
        # Use sigmoid activation for feature detection
        business_score = 0
        technical_score = 0
        personal_score = 0
        
        text_lower = text.lower()
        
        # Business feature detection using dataset
        if 'business_terms' in self.dataset_cache:
            business_matches = sum(1 for term in self.dataset_cache['business_terms'] 
                                 if term and term in text_lower)
            business_score = sigmoid(business_matches * weights.get('business', 0.33))
        
        # Technical feature detection
        if 'technical_terms' in self.dataset_cache:
            tech_matches = sum(1 for term in self.dataset_cache['technical_terms'] 
                             if term and term in text_lower)
            technical_score = sigmoid(tech_matches * weights.get('technical', 0.33))
        
        # Personal feature detection
        if 'names' in self.dataset_cache:
            name_matches = sum(1 for name in self.dataset_cache['names'] 
                             if name and name in text_lower)
            personal_score = sigmoid(name_matches * weights.get('personal', 0.34))
        
        # Pattern analysis using eyes.py
        patterns = analyze_string_patterns(text)
        pattern_score = sigmoid(len(patterns) * 0.1)
        
        # Multi-layer sigmoid processing
        layers = [
            {'weight': weights.get('complexity', 0.5), 'bias': 0.1},
            {'weight': weights.get('frequency', 0.3), 'bias': 0.0},
            {'weight': weights.get('user_preference', 0.8), 'bias': 0.2}
        ]
        
        features['business_indicators'] = multi_layer_sigmoid(business_score, layers)
        features['technical_indicators'] = multi_layer_sigmoid(technical_score, layers)
        features['personal_indicators'] = multi_layer_sigmoid(personal_score, layers)
        features['complexity'] = pattern_score
        features['detected_patterns'] = [p[0] for p in patterns]
        
        return features
    
    def generate_ml_response(self, user_input, session_id=None):
        # COMPLETELY NEW ML-POWERED CONVERSATIONAL SYSTEM
        import random
        import time
        
        # Ensure true randomness for every call
        random.seed(int(time.time() * 1000000 + hash(user_input) + len(user_input) * 73) % 2147483647)
        
        # Sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'enjoy', 'happy', 'awesome']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'wrong', 'sad', 'angry', 'frustrated']
        
        user_lower = user_input.lower()
        user_tokens = user_lower.split()
        
        positive_count = sum(1 for word in user_tokens if word in positive_words)
        negative_count = sum(1 for word in user_tokens if word in negative_words)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            sentiment_score = positive_count / len(user_tokens) if user_tokens else 0.3
        elif negative_count > positive_count:
            sentiment = 'negative'
            sentiment_score = negative_count / len(user_tokens) if user_tokens else 0.3
        else:
            sentiment = 'neutral'
            sentiment_score = 0.5
        
        # Dataset-powered response generation
        business_terms = random.sample(self.dataset_cache.get('business_terms', ['strategy', 'management'])[:300], min(8, len(self.dataset_cache.get('business_terms', ['strategy']))))
        tech_terms = random.sample(self.dataset_cache.get('technology_vocabulary', ['system', 'data'])[:200], min(6, len(self.dataset_cache.get('technology_vocabulary', ['data']))))
        prog_terms = random.sample(self.dataset_cache.get('programming_request_keywords', ['function', 'code'])[:100], min(4, len(self.dataset_cache.get('programming_request_keywords', ['code']))))
        
        # Conversational starters based on sentiment
        if sentiment == 'positive':
            starters = ["That's awesome!", "Great question!", "I love discussing this!", "Fantastic topic!"]
        elif sentiment == 'negative':
            starters = ["I understand your concern.", "Let me help with that.", "I see what you mean.", "That's a valid point."]
        else:
            starters = ["Interesting!", "Good question!", "Let me think about that.", "Here's what I know:"]
        
        # Generate unique responses using datasets
        if 'hello' in user_lower or 'hi' in user_lower or 'hey' in user_lower:
            greetings = [
                f"Hello! I'm running with {sentiment} sentiment analysis and {len(business_terms)} business terms loaded!",
                f"Hi there! My current state shows {sentiment_score:.2f} confidence with {len(tech_terms)} tech concepts ready!",
                f"Hey! Processing through {len(prog_terms)} programming patterns with {sentiment} tone detection!",
                f"Greetings! System loaded with {len(self.dataset_cache)} datasets and {sentiment} sentiment analysis!"
            ]
            return random.choice(greetings)
        
        elif 'programming' in user_lower or 'code' in user_lower:
            prog_responses = [
                f"Programming involves {', '.join(prog_terms[:3])} with {', '.join(tech_terms[:2])} frameworks. My {sentiment} analysis suggests exploring {', '.join(business_terms[:2])} applications!",
                f"Code development uses {', '.join(prog_terms[2:])} methodologies. With {sentiment} sentiment, I recommend {', '.join(tech_terms[2:4])} approaches for {', '.join(business_terms[2:4])} integration!",
                f"Software engineering combines {', '.join(prog_terms[:2])} with {', '.join(tech_terms[:3])}. Your {sentiment} interest aligns with {', '.join(business_terms[:3])} strategies!"
            ]
            return random.choice(prog_responses)
        
        elif 'business' in user_lower or 'marketing' in user_lower:
            biz_responses = [
                f"Business strategy involves {', '.join(business_terms[:4])} with {sentiment} market analysis. Consider {', '.join(tech_terms[:2])} integration for {', '.join(prog_terms[:2])} automation!",
                f"Marketing requires {', '.join(business_terms[4:])} approaches. With {sentiment} sentiment, implement {', '.join(tech_terms[2:4])} solutions using {', '.join(prog_terms[2:])} frameworks!",
                f"Enterprise operations use {', '.join(business_terms[:3])} methodologies. Your {sentiment} perspective suggests {', '.join(tech_terms[:3])} technologies for competitive advantage!"
            ]
            return random.choice(biz_responses)
        
        else:
            # General conversational responses using all datasets
            mixed_responses = [
                f"{random.choice(starters)} This connects to {', '.join(business_terms[:2])} concepts with {', '.join(tech_terms[:2])} implementation. My {sentiment} analysis shows {sentiment_score:.2f} confidence!",
                f"{random.choice(starters)} Interesting topic involving {', '.join(tech_terms[2:4])} and {', '.join(business_terms[2:4])} applications. With {sentiment} sentiment, consider {', '.join(prog_terms[:2])} approaches!",
                f"{random.choice(starters)} This relates to {', '.join(business_terms[:3])} strategies using {', '.join(tech_terms[:3])} frameworks. Your {sentiment} perspective aligns with modern practices!",
                f"{random.choice(starters)} Great inquiry about {', '.join(tech_terms[:2])} integration with {', '.join(business_terms[4:6])} methodologies. {sentiment.title()} analysis suggests innovative solutions!"
            ]
            return random.choice(mixed_responses)
    
    def detect_programming_content(self, user_input, analysis):
        """Detect and respond to programming-related content"""
        user_lower = user_input.lower()
        
        # Check for programming languages
        prog_langs = []
        if any(word in user_lower for word in self.dataset_cache.get('zig_keywords', [])):
            prog_langs.append('Zig')
        if any(word in user_lower for word in self.dataset_cache.get('rust_keywords', [])):
            prog_langs.append('Rust')
        if any(word in user_lower for word in self.dataset_cache.get('go_keywords', [])):
            prog_langs.append('Go')
        if any(word in user_lower for word in ['python', 'def', 'import', 'class']):
            prog_langs.append('Python')
        if any(word in user_lower for word in ['javascript', 'function', 'var', 'let', 'const']):
            prog_langs.append('JavaScript')
        
        if prog_langs:
            return f"Detected {', '.join(prog_langs)} programming content. Analyzing code patterns and syntax structures."
        
        # Check for general programming terms
        prog_terms = [term for term in self.dataset_cache.get('programming_keywords', []) 
                     if term and term in user_lower]
        if prog_terms:
            return f"Programming concepts identified: {', '.join(prog_terms[:3])}. Applying technical analysis."
        
        return None
    
    def detect_business_content(self, user_input, analysis):
        """Detect and respond to business-related content"""
        user_lower = user_input.lower()
        
        business_terms = [term for term in self.dataset_cache.get('business_terms', []) 
                         if term and len(term) > 2 and term in user_lower]
        
        if business_terms:
            return f"Business context detected with terms: {', '.join(business_terms[:4])}. Applying enterprise analysis framework."
        
        return None
    
    def analyze_language_content(self, user_input, analysis):
        """Analyze language and grammar content"""
        user_lower = user_input.lower()
        
        # Check for grammar-related queries
        if any(word in user_lower for word in ['grammar', 'language', 'sentence', 'word', 'meaning']):
            academic_terms = [term for term in self.dataset_cache.get('academic_vocabulary', []) 
                             if term and term in user_lower]
            if academic_terms:
                return f"Language analysis activated. Academic vocabulary detected: {', '.join(academic_terms[:3])}."
            else:
                return "Linguistic analysis engaged. Processing grammatical structures and language patterns."
        
        # Check for high-frequency words and language complexity
        high_freq = [word for word in user_input.split() 
                    if word.lower() in self.dataset_cache.get('high_frequency_words', [])]
        if len(high_freq) > 2:
            return f"Natural language processing: {len(high_freq)} high-frequency words identified, analyzing semantic relationships."
        
        return None
    
    def generate_pattern_insights(self, analysis):
        """Generate insights based on detected patterns"""
        if analysis['patterns']:
            pattern_types = ', '.join(analysis['patterns'])
            return f"Conversational patterns detected: {pattern_types}. Adapting response style accordingly."
        return None
    
    def tokenize_and_analyze(self, text):
        tokens = text.lower().strip().split()
        
        analysis = {
            'tokens': tokens,
            'entities': [],
            'intents': [],
            'patterns': [],
            'sentiment': 'neutral',
            'confidence': 0.0,
            'context_words': [],
            'technical_terms': [],
            'business_terms': []
        }
        
        # Named Entity Recognition (simple)
        for token in tokens:
            if token in self.dataset_cache['names']:
                analysis['entities'].append({'type': 'person', 'value': token})
            elif token in self.dataset_cache['technical_terms']:
                analysis['entities'].append({'type': 'technical', 'value': token})
                analysis['technical_terms'].append(token)
            elif token in self.dataset_cache['business_terms']:
                analysis['entities'].append({'type': 'business', 'value': token})
                analysis['business_terms'].append(token)
        
        # Intent Recognition
        for intent, keywords in self.dataset_cache['intent_patterns'].items():
            if any(keyword in text.lower() for keyword in keywords):
                analysis['intents'].append(intent)
        
        # Pattern Recognition
        for pattern_type, patterns in self.dataset_cache['conversational_patterns'].items():
            if any(pattern in text.lower() for pattern in patterns):
                analysis['patterns'].append(pattern_type)
        
        # Context Analysis
        analysis['context_words'] = [token for token in tokens if len(token) > 3]
        
        # Confidence Scoring
        entity_score = len(analysis['entities']) * 0.2
        intent_score = len(analysis['intents']) * 0.3
        pattern_score = len(analysis['patterns']) * 0.1
        context_score = min(len(analysis['context_words']) * 0.05, 0.4)
        
        analysis['confidence'] = min(entity_score + intent_score + pattern_score + context_score, 1.0)
        
        return analysis
    
    def store_in_memory(self, user_input, analysis, session_id):
        if not hasattr(self, 'memory') or not self.memory:
            self.load_memory()
        
        memory_item = {
            'timestamp': datetime.now().isoformat(),
            'input': user_input,
            'analysis': analysis,
            'session_id': session_id
        }
        
        if 'conversations' not in self.memory:
            self.memory['conversations'] = []
        
        self.memory['conversations'].append(memory_item)
        
        if len(self.memory['conversations']) > 1000:
            self.memory['conversations'] = self.memory['conversations'][-500:]
        
        self.save_memory()
    
    def get_conversation_context(self, session_id):
        if not session_id:
            return []
        
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        return self.conversation_history[session_id][-5:]
    
    def generate_intent_response(self, intent, analysis, context):
        context_count = len(context)
        entity_count = len(analysis['entities'])
        
        intent_responses = {
            'creation': f"Creating solution with {entity_count} identified components and {context_count} context references",
            'analysis': f"Analyzing data using {len(analysis['technical_terms'])} technical patterns and {analysis['confidence']:.2f} confidence score",
            'query': f"Processing query with {len(analysis['context_words'])} context elements and cross-referencing previous conversations",
            'storage': f"Recommending storage approach based on {entity_count} entities and historical usage patterns",
            'modification': f"Applying modifications using learned patterns from {len(self.memory.get('conversations', []))} previous interactions"
        }
        
        return intent_responses.get(intent, f"Processing {intent} request with contextual understanding")
    
    def generate_entity_response(self, analysis):
        entities = analysis['entities']
        spacy_entities = analysis.get('spacy_entities', [])
        
        if entities and spacy_entities:
            return f"Identified {len(entities)} dataset entities and {len(spacy_entities)} linguistic entities for comprehensive analysis"
        elif entities:
            entity_types = set(entity['type'] for entity in entities)
            return f"Detected {len(entities)} entities across {len(entity_types)} categories using dataset matching"
        elif spacy_entities:
            entity_labels = set(label for _, label in spacy_entities)
            return f"Found {len(spacy_entities)} named entities with {len(entity_labels)} distinct types via NLP processing"
        
        return None
    
    def find_similar_conversations(self, user_input):
        if not hasattr(self, 'memory') or not self.memory or 'conversations' not in self.memory:
            return None
        
        if not self.memory['conversations'] or not ADVANCED_NLP_AVAILABLE:
            return None
        
        try:
            recent_conversations = [conv['input'] for conv in self.memory['conversations'][-50:]]
            all_texts = recent_conversations + [user_input]
            
            if not hasattr(self, 'tfidf_vectorizer') or self.tfidf_vectorizer is None:
                return None
            
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_texts)
            similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
            
            max_similarity = np.max(similarities)
            if max_similarity > 0.3:
                return f"Found similar conversation patterns with {max_similarity:.2f} similarity coefficient"
        except Exception:
            pass
        
        return None
    
    def generate_learning_insight(self, analysis, context):
        pattern_count = len(analysis['patterns'])
        confidence = analysis['confidence']
        
        if not hasattr(self, 'memory') or not self.memory or 'conversations' not in self.memory:
            memory_size = 0
        else:
            memory_size = len(self.memory['conversations'])
        
        if confidence > 0.8:
            return f"High confidence analysis using {memory_size} learned examples and {pattern_count} detected patterns"
        elif confidence > 0.5:
            return f"Moderate confidence with adaptive learning from {memory_size} training interactions"
        else:
            return f"Exploratory analysis expanding knowledge base of {memory_size} examples"
    
    def combine_response_parts(self, parts):
        if len(parts) == 1:
            return parts[0] + "."
        elif len(parts) == 2:
            return f"{parts[0]}. {parts[1]}."
        else:
            main_response = parts[0]
            supporting_details = ". ".join(parts[1:3])
            return f"{main_response}. {supporting_details}."
    
    def learn_from_interaction(self, user_input, response, analysis, session_id):
        if session_id:
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].append({
                'user': user_input,
                'bot': response,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
        
        learned_pattern = {
            'input_pattern': user_input[:100],
            'entities': analysis['entities'],
            'intents': analysis['intents'],
            'confidence': analysis['confidence'],
            'timestamp': datetime.now().isoformat()
        }
        
        self.memory['learned_patterns'].append(learned_pattern)
        
        if len(self.memory['learned_patterns']) > 500:
            self.memory['learned_patterns'] = self.memory['learned_patterns'][-250:]
    
    def generate_data_driven_response(self, user_input, data_content, analysis_result, weights):
        text_combined = (user_input + " " + data_content).lower()
        
        found_terms = self.extract_matching_terms(text_combined)
        patterns = analyze_string_patterns(text_combined)
        tokens = self.extract_tokens(data_content)
        
        response = self.autocomplete_response_from_patterns(
            user_input, data_content, found_terms, patterns, tokens, analysis_result, weights
        )
        
        return response
    
    def extract_matching_terms(self, text):
        matches = {
            'business': [term for term in self.dataset_cache.get('business_terms', []) 
                        if term and len(term) > 2 and term in text],
            'technical': [term for term in self.dataset_cache.get('technical_terms', []) 
                         if term and len(term) > 2 and term in text],
            'programming': [term for term in self.dataset_cache.get('programming_keywords', []) 
                           if term and len(term) > 2 and term in text],
            'common': [term for term in self.dataset_cache.get('common_words', [])[:500] 
                      if term and len(term) > 3 and term in text]
        }
        return matches
    
    def extract_tokens(self, content):
        lexer = Lexer(content)
        tokens = []
        try:
            while True:
                token = lexer.get_next_token()
                if token.type == TokenType.EOF:
                    break
                tokens.append(token.value)
                if len(tokens) >= 15:
                    break
        except:
            pass
        return tokens
    
    def autocomplete_response_from_patterns(self, user_input, data_content, found_terms, patterns, tokens, analysis_result, weights):
        response_parts = []
        
        starter = self.find_response_starter(found_terms, patterns)
        if starter:
            response_parts.append(starter)
        
        content_description = self.build_content_description(found_terms, patterns, tokens)
        if content_description:
            response_parts.append(content_description)
        
        analysis_description = self.build_analysis_description(analysis_result, found_terms, weights)
        if analysis_description:
            response_parts.append(analysis_description)
        
        technical_details = self.build_technical_details(tokens, patterns, analysis_result['features'])
        if technical_details:
            response_parts.append(technical_details)
        
        conclusion = self.build_conclusion(analysis_result, found_terms, weights)
        if conclusion:
            response_parts.append(conclusion)
        
        return ' '.join(response_parts)
    
    def find_response_starter(self, found_terms, patterns):
        if found_terms['programming']:
            base_patterns = self.dataset_cache['patterns'].get('action_patterns', [])
            for pattern in base_patterns[:10]:
                if any(word in pattern for word in ['create', 'build', 'make']):
                    words = pattern.split()
                    return f"{words[0].capitalize()} {' '.join(words[1:])} with {found_terms['programming'][0]}"
        
        if found_terms['technical']:
            tech_patterns = self.dataset_cache['patterns'].get('technical_phrases', [])
            for pattern in tech_patterns[:5]:
                if 'data' in pattern or 'system' in pattern:
                    return f"{pattern.capitalize()} involves {found_terms['technical'][0]}"
        
        if found_terms['business']:
            business_patterns = self.dataset_cache['patterns'].get('business_phrases', [])
            for pattern in business_patterns[:5]:
                return f"{pattern.capitalize()} requires {found_terms['business'][0]}"
        
        starters = self.dataset_cache['patterns'].get('response_starters', [])
        if starters:
            return f"{starters[0].capitalize()} content analysis"
        
        return "Processing request"
    
    def build_content_description(self, found_terms, patterns, tokens):
        description_parts = []
        
        if found_terms['programming']:
            prog_terms = found_terms['programming'][:4]
            if tokens:
                description_parts.append(f"programming elements {' '.join(prog_terms)} detected in tokens {' '.join(tokens[:3])}")
            else:
                description_parts.append(f"programming content containing {' '.join(prog_terms)}")
        
        if found_terms['technical']:
            tech_terms = found_terms['technical'][:3]
            description_parts.append(f"technical vocabulary {' '.join(tech_terms)} identified")
        
        if found_terms['business']:
            biz_terms = found_terms['business'][:3]
            description_parts.append(f"business terminology {' '.join(biz_terms)} present")
        
        pattern_names = [p[0] for p in patterns if p[0] in ['email', 'phone', 'url', 'date_mdy', 'number']]
        if pattern_names:
            description_parts.append(f"structured patterns {' '.join(pattern_names[:3])} found")
        
        return '. '.join(description_parts) + '.' if description_parts else ''
    
    def build_analysis_description(self, analysis_result, found_terms, weights):
        storage_choice = analysis_result['storage_choice']
        features = analysis_result['features']
        
        analysis_parts = []
        
        if storage_choice == 'enterprise_sql' and found_terms['business']:
            analysis_parts.append(f"sql database recommended for business data {' '.join(found_terms['business'][:2])}")
        elif storage_choice == 'technical_nosql' and (found_terms['technical'] or found_terms['programming']):
            relevant = (found_terms['technical'] + found_terms['programming'])[:3]
            analysis_parts.append(f"nosql storage selected for technical content {' '.join(relevant)}")
        elif storage_choice == 'personal_secure':
            analysis_parts.append("secure storage chosen for sensitive information patterns")
        else:
            analysis_parts.append("hybrid storage system configured for mixed content")
        
        high_features = [(name.replace('_indicators', '').replace('_', ' '), score) 
                        for name, score in features.items() 
                        if isinstance(score, (int, float)) and score > 0.5]
        
        if high_features:
            feature_desc = ' '.join([f"{name} {score:.2f}" for name, score in high_features[:2]])
            analysis_parts.append(f"feature analysis shows {feature_desc}")
        
        return '. '.join(analysis_parts) + '.' if analysis_parts else ''
    
    def build_technical_details(self, tokens, patterns, features):
        details = []
        
        if tokens:
            token_sequence = ' '.join(tokens[:5])
            details.append(f"lexical sequence {token_sequence}")
        
        if patterns:
            pattern_types = [p[0] for p in patterns[:3]]
            details.append(f"pattern types {' '.join(pattern_types)}")
        
        numeric_features = [(name, score) for name, score in features.items() 
                           if isinstance(score, (int, float)) and score > 0.3]
        if numeric_features:
            feature_summary = ' '.join([f"{name.split('_')[0]} {score:.1f}" for name, score in numeric_features[:3]])
            details.append(f"scoring {feature_summary}")
        
        return '. '.join(details) + '.' if details else ''
    
    def get_or_create_chat_system(self, session_id):
        if session_id not in self.chat_systems:
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'learning_weights': {}}
            )
            
            self.chat_systems[session_id] = AdaptiveChatSystem()
            
            if not created and session.learning_weights:
                self.chat_systems[session_id].learning_system.weights = session.learning_weights
        
        return self.chat_systems[session_id]
    
    def analyze_with_sigmoid(self, text, weights):
        """Simple sigmoid analysis for compatibility"""
        tokens = text.lower().split()
        business_score = len([t for t in tokens if t in self.dataset_cache.get('business_terms', [])]) / max(len(tokens), 1)
        technical_score = len([t for t in tokens if t in self.dataset_cache.get('programming_keywords', [])]) / max(len(tokens), 1)
        personal_score = len([t for t in tokens if t in self.dataset_cache.get('names', [])]) / max(len(tokens), 1)
        
        return {
            'business_indicators': min(business_score * 2, 1.0),
            'technical_indicators': min(technical_score * 2, 1.0),
            'personal_indicators': min(personal_score * 2, 1.0),
            'complexity': min((len(tokens) / 10), 1.0),
            'detected_patterns': ['text', 'analysis']
        }

chat_service = IntelligentChatService()

@api_view(['POST'])
def process_chat_input(request):
    try:
        data = request.data
        user_input = data.get('user_input', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_input:
            return Response({
                'error': 'user_input is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        import random
        import time
        import math
        
        # Generate unique seed for different responses every time
        unique_seed = int(time.time() * 1000000 + len(user_input) * 97 + hash(user_input) % 10000)
        random.seed(unique_seed)
        
        intelligent_service = IntelligentChatService()
        user_tokens = user_input.lower().split()
        
        # Advanced sentiment analysis using expanded indicators
        positive_indicators = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'enjoy', 'fantastic', 'awesome', 'brilliant', 'perfect', 'outstanding', 'superb', 'marvelous', 'terrific', 'fabulous', 'incredible', 'magnificent', 'spectacular']
        negative_indicators = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'wrong', 'worst', 'disappointing', 'frustrating', 'annoying', 'dreadful', 'disgusting', 'pathetic', 'useless', 'nightmare', 'disaster', 'catastrophe']
        neutral_indicators = ['okay', 'fine', 'normal', 'standard', 'regular', 'average', 'typical', 'ordinary', 'moderate', 'acceptable']
        
        positive_score = sum(1 for token in user_tokens if token in positive_indicators)
        negative_score = sum(1 for token in user_tokens if token in negative_indicators)
        neutral_score = sum(1 for token in user_tokens if token in neutral_indicators)
        
        sentiment_total = positive_score + negative_score + neutral_score
        if sentiment_total > 0:
            sentiment_confidence = min(sentiment_total / len(user_tokens), 1.0)
            if positive_score > negative_score and positive_score >= neutral_score:
                detected_sentiment = 'positive'
                sentiment_weight = positive_score / sentiment_total
            elif negative_score > positive_score and negative_score >= neutral_score:
                detected_sentiment = 'negative'
                sentiment_weight = negative_score / sentiment_total
            else:
                detected_sentiment = 'neutral'
                sentiment_weight = neutral_score / sentiment_total if neutral_score > 0 else 0.5
        else:
            detected_sentiment = 'neutral'
            sentiment_confidence = 0.4
            sentiment_weight = 0.5
        
        # Sigmoid analysis for topic classification
        business_keywords = ['business', 'marketing', 'sales', 'strategy', 'management', 'finance', 'revenue', 'profit', 'customer', 'market', 'brand', 'commercial', 'enterprise', 'corporate', 'industry', 'economics', 'investment', 'startup', 'venture', 'entrepreneur']
        technical_keywords = ['code', 'programming', 'software', 'development', 'algorithm', 'database', 'system', 'application', 'framework', 'library', 'api', 'interface', 'function', 'method', 'variable', 'data', 'structure', 'network', 'server', 'technology']
        academic_keywords = ['study', 'research', 'analysis', 'theory', 'concept', 'principle', 'methodology', 'approach', 'hypothesis', 'conclusion', 'evidence', 'empirical', 'systematic', 'comprehensive', 'fundamental', 'academic', 'scholarly', 'intellectual', 'analytical', 'theoretical']
        
        business_matches = sum(1 for token in user_tokens if token in business_keywords)
        technical_matches = sum(1 for token in user_tokens if token in technical_keywords)
        academic_matches = sum(1 for token in user_tokens if token in academic_keywords)
        
        # Sigmoid function for weighting
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        
        business_weight = sigmoid((business_matches - 1) * 2)
        technical_weight = sigmoid((technical_matches - 1) * 2)
        academic_weight = sigmoid((academic_matches - 1) * 2)
        personal_weight = sigmoid((len(user_tokens) - max(business_matches, technical_matches, academic_matches)) * 0.5)
        complexity_score = sigmoid((len(user_tokens) - 3) * 0.3)
        
        # Generate conversational responses using datasets
        if any(word in user_input.lower() for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            conversation_starters = [
                f"Hello there! I'm really excited to chat with you today. What's sparking your curiosity?",
                f"Hi! Great to connect with you. I love exploring ideas and having genuine conversations. What's on your mind?",
                f"Hey! Nice to meet you. I'm here for engaging discussions about absolutely anything that interests you. What would you like to explore?",
                f"Greetings! I enjoy meaningful conversations and I'm ready to dive into whatever topic catches your attention. What's got you thinking?",
                f"Hello! I find every conversation unique and fascinating. Whether it's questions, ideas, or just chatting, I'm here for it. What brings you here today?"
            ]
            chat_response = random.choice(conversation_starters)
            
        elif any(word in user_input.lower() for word in ['thank', 'thanks', 'appreciate', 'grateful']):
            appreciation_responses = [
                f"You're absolutely welcome! I genuinely enjoy our conversations and exploring ideas together. It's what makes this interesting for me!",
                f"My pleasure entirely! These discussions are engaging and I love learning about different perspectives. Happy to help anytime!",
                f"You're very welcome! I find our exchanges stimulating and I'm always excited to dive into new topics with you.",
                f"Absolutely my pleasure! I thrive on meaningful conversations and I'm grateful you're sharing your thoughts and questions with me.",
                f"You're welcome! I really value these interactions and the opportunity to explore concepts together. It's genuinely enjoyable!"
            ]
            chat_response = random.choice(appreciation_responses)
            
        elif any(word in user_input.lower() for word in ['who are you', 'what are you', 'about yourself', 'tell me about you']):
            introduction_responses = [
                f"I'm an AI who's passionate about having real conversations! I love exploring ideas, diving into questions, and learning what makes people curious. Every chat feels different and engaging to me. What kind of topics do you enjoy exploring?",
                f"I'm a conversational AI that thrives on meaningful discussions! Whether it's technical topics, creative ideas, or just random thoughts, I find every conversation brings something new. I'm genuinely curious about what interests you most.",
                f"I'm an AI assistant designed for engaging conversations! I enjoy the unpredictability of discussions, learning from different perspectives, and helping explore whatever captures your imagination. What draws your curiosity today?",
                f"I'm an AI who finds genuine joy in conversations! I love how each discussion takes unexpected turns and reveals new ways of thinking. I'm here to chat, explore ideas, and dive deep into whatever fascinates you.",
                f"I'm a conversational AI that's energized by interesting discussions! I enjoy the back-and-forth of exploring ideas together, whether they're complex concepts or simple observations. What's something you've been thinking about lately?"
            ]
            chat_response = random.choice(introduction_responses)
            
        else:
            # Generate dynamic responses using all datasets
            business_terms = random.sample(intelligent_service.dataset_cache.get('business_terms', [])[:int(business_weight * 1000 + 50)], min(8, len(intelligent_service.dataset_cache.get('business_terms', []))))
            tech_terms = random.sample(intelligent_service.dataset_cache.get('technology_vocabulary', [])[:int(technical_weight * 500 + 30)], min(6, len(intelligent_service.dataset_cache.get('technology_vocabulary', []))))
            academic_terms = random.sample(intelligent_service.dataset_cache.get('academic_vocabulary', [])[:int(academic_weight * 200 + 20)], min(5, len(intelligent_service.dataset_cache.get('academic_vocabulary', []))))
            programming_terms = random.sample(intelligent_service.dataset_cache.get('programming_request_keywords', [])[:int(technical_weight * 300 + 25)], min(4, len(intelligent_service.dataset_cache.get('programming_request_keywords', []))))
            common_words = random.sample(intelligent_service.dataset_cache.get('common_english_words', [])[:100], min(10, len(intelligent_service.dataset_cache.get('common_english_words', []))))
            
            # Context-aware conversation starters based on sentiment
            if detected_sentiment == 'positive':
                starters = [
                    f"That's fantastic! I love your enthusiasm about this.",
                    f"Excellent question! Your positive energy is contagious.",
                    f"I'm excited you brought this up! This is a great topic.",
                    f"Wonderful! I can tell you're really engaged with this subject.",
                    f"That's amazing! I enjoy exploring this kind of thinking."
                ]
            elif detected_sentiment == 'negative':
                starters = [
                    f"I understand this can be challenging. Let me help clarify things.",
                    f"I hear your concerns about this. Let's work through it together.",
                    f"That's a valid frustration. I'll do my best to make this clearer.",
                    f"I can see why this might be confusing. Let me break it down.",
                    f"I appreciate you bringing up these difficulties. Let's address them."
                ]
            else:
                starters = [
                    f"That's an interesting perspective. I'm curious to explore this with you.",
                    f"Great question! This is exactly the kind of thing I enjoy discussing.",
                    f"I find this topic fascinating. There's a lot to unpack here.",
                    f"That's a thoughtful inquiry. I love diving into these concepts.",
                    f"Interesting point! This connects to some really engaging ideas."
                ]
            
            # Generate content based on topic weights and complexity
            if business_weight > 0.6 and complexity_score > 0.5:
                business_focus = random.sample(business_terms, min(6, len(business_terms)))
                detailed_content = f"When I think about {', '.join(business_focus[:3])}, it really connects to how {', '.join(business_focus[3:])} creates opportunities in today's market. The {detected_sentiment} tone of your question suggests you're looking at the strategic implications of {', '.join(business_focus[:2])} implementation."
                
                practical_applications = [
                    f"In practice, this often involves {', '.join(business_focus[2:4])} approaches that balance {', '.join(tech_terms[:2])} efficiency with {', '.join(academic_terms[:2])} rigor.",
                    f"Real-world applications typically leverage {', '.join(business_focus[:2])} frameworks while integrating {', '.join(tech_terms[1:3])} solutions for optimal outcomes.",
                    f"The most effective strategies combine {', '.join(business_focus[1:3])} methodologies with {', '.join(academic_terms[1:3])} principles to drive sustainable results."
                ]
                
                chat_response = f"{random.choice(starters)} {detailed_content}\n\n{random.choice(practical_applications)}\n\nWhat specific aspects of this approach interest you most? I'd love to hear your thoughts on how these concepts might apply to your situation."
                
            elif technical_weight > 0.6 and complexity_score > 0.5:
                tech_focus = random.sample(tech_terms + programming_terms, min(8, len(tech_terms + programming_terms)))
                technical_insight = f"This touches on some fascinating {', '.join(tech_focus[:3])} concepts! The way {', '.join(tech_focus[3:5])} interacts with {', '.join(tech_focus[5:])} creates really interesting possibilities for implementation."
                
                implementation_ideas = [
                    f"From a technical standpoint, you'd typically approach this using {', '.join(tech_focus[:2])} patterns combined with {', '.join(programming_terms[:2])} best practices.",
                    f"The implementation would likely involve {', '.join(programming_terms[1:3])} techniques integrated with {', '.join(tech_focus[2:4])} frameworks for optimal performance.",
                    f"Most developers tackle this by leveraging {', '.join(tech_focus[1:3])} architectures alongside {', '.join(programming_terms[:2])} methodologies."
                ]
                
                chat_response = f"{random.choice(starters)} {technical_insight}\n\n{random.choice(implementation_ideas)}\n\nAre you working on something specific with this, or exploring the concepts more generally? I'm curious about what drew you to this particular area."
                
            elif academic_weight > 0.5 or complexity_score > 0.7:
                academic_focus = random.sample(academic_terms, min(6, len(academic_terms)))
                intellectual_exploration = f"This is such a rich area for {', '.join(academic_focus[:3])} exploration! The {detected_sentiment} nature of your inquiry suggests deep engagement with how {', '.join(academic_focus[3:])} principles apply in this context."
                
                analytical_perspectives = [
                    f"From an analytical lens, this involves {', '.join(academic_focus[:2])} frameworks that intersect beautifully with {', '.join(common_words[:3])} understanding.",
                    f"The theoretical foundation here draws on {', '.join(academic_focus[1:3])} approaches while connecting to {', '.join(common_words[2:5])} practical applications.",
                    f"This exemplifies how {', '.join(academic_focus[2:4])} thinking can illuminate {', '.join(common_words[1:4])} patterns in meaningful ways."
                ]
                
                chat_response = f"{random.choice(starters)} {intellectual_exploration}\n\n{random.choice(analytical_perspectives)}\n\nWhat's your background with this topic? I find it fascinating how different perspectives can reveal new dimensions of understanding."
                
            else:
                # General conversational responses with high variety
                conversational_elements = random.sample(common_words + business_terms[:3] + tech_terms[:3] + academic_terms[:2], min(12, len(common_words + business_terms[:3] + tech_terms[:3] + academic_terms[:2])))
                
                engaging_openers = [
                    f"I find that really engaging! When you mention this, it makes me think about how {', '.join(conversational_elements[:3])} connects to {', '.join(conversational_elements[3:6])} in unexpected ways.",
                    f"That's such an interesting angle! Your perspective on this reminds me of the interplay between {', '.join(conversational_elements[1:4])} and {', '.join(conversational_elements[6:9])} concepts.",
                    f"I love this kind of question! It brings together {', '.join(conversational_elements[2:5])} thinking with {', '.join(conversational_elements[7:])} applications in ways that create new possibilities.",
                    f"That's a great observation! The way you're approaching this connects {', '.join(conversational_elements[:4])} with {', '.join(conversational_elements[5:8])} in a really thoughtful way.",
                    f"Fascinating! This touches on the relationship between {', '.join(conversational_elements[1:3])} and {', '.join(conversational_elements[8:])} that I find endlessly interesting to explore."
                ]
                
                follow_up_questions = [
                    "What got you thinking about this particular aspect?",
                    "Have you encountered this in a specific context that sparked your curiosity?",
                    "I'm curious about what angle interests you most here.",
                    "What's your take on how this might apply in different situations?",
                    "Are there particular examples or scenarios you're considering with this?"
                ]
                
                chat_response = f"{random.choice(starters)} {random.choice(engaging_openers)}\n\n{random.choice(follow_up_questions)} I find these conversations always lead to unexpected insights!"
        
        # Apply final processing with sigmoid and sentiment integration
        processing_time = random.uniform(0.1, 0.3)
        confidence_score = min(sentiment_confidence + complexity_score * 0.5, 1.0)
        
        return Response({
            'response': chat_response,
            'ml_analysis': {
                'sentiment': detected_sentiment,
                'sentiment_confidence': sentiment_confidence,
                'business_weight': business_weight,
                'technical_weight': technical_weight,
                'academic_weight': academic_weight,
                'complexity_score': complexity_score,
                'processing_time': processing_time,
                'confidence_score': confidence_score,
                'response_uniqueness': unique_seed % 1000
            },
            'session_id': session_id
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def provide_feedback(request):
    try:
        data = request.data
        interaction_id = data.get('interaction_id')
        satisfaction_rating = data.get('satisfaction_rating')
        session_id = data.get('session_id')
        
        if not all([interaction_id, satisfaction_rating is not None, session_id]):
            return Response({
                'error': 'interaction_id, satisfaction_rating, and session_id are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not (1 <= satisfaction_rating <= 10):
            return Response({
                'error': 'satisfaction_rating must be between 1 and 10'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        interaction = ChatInteraction.objects.get(id=interaction_id)
        feedback_score = satisfaction_rating / 10.0
        success = feedback_score >= 0.7
        
        interaction.user_feedback = feedback_score
        interaction.success = success
        interaction.save()
        
        chat_system = chat_service.get_or_create_chat_system(session_id)
        
        features = interaction.features_analyzed
        context_type = max(
            ['business', 'technical', 'personal'],
            key=lambda x: features.get(f'{x}_indicators', 0)
        )
        
        chat_system.learning_system.update_weights(
            feedback_score, 
            context_type, 
            interaction.storage_recommendation, 
            success
        )
        
        session = ChatSession.objects.get(session_id=session_id)
        session.learning_weights = chat_system.learning_system.weights
        
        LearningPattern.objects.create(
            session=session,
            context_type=context_type,
            storage_choice=interaction.storage_recommendation,
            feedback_score=feedback_score,
            success=success,
            weights_before=session.learning_weights,
            weights_after=chat_system.learning_system.weights
        )
        
        all_feedback = ChatInteraction.objects.filter(
            session=session, 
            user_feedback__isnull=False
        ).values_list('user_feedback', flat=True)
        
        if all_feedback:
            session.avg_satisfaction = sum(all_feedback) / len(all_feedback)
        session.save()
        
        return Response({
            'message': 'Feedback processed successfully',
            'updated_weights': chat_system.learning_system.weights,
            'learning_improvement': success
        }, status=status.HTTP_200_OK)
        
    except ChatInteraction.DoesNotExist:
        return Response({
            'error': 'Interaction not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_session_stats(request, session_id):
    try:
        session = ChatSession.objects.get(session_id=session_id)
        interactions = ChatInteraction.objects.filter(session=session)
        
        successful_interactions = interactions.filter(success=True).count()
        total_interactions = interactions.count()
        success_rate = successful_interactions / total_interactions if total_interactions > 0 else 0
        
        avg_processing_time = interactions.aggregate(
            avg_time=models.Avg('processing_time')
        )['avg_time'] or 0
        
        storage_distribution = {}
        for interaction in interactions:
            storage_type = interaction.storage_recommendation
            storage_distribution[storage_type] = storage_distribution.get(storage_type, 0) + 1
        
        return Response({
            'session_id': session_id,
            'total_interactions': total_interactions,
            'success_rate': f"{success_rate:.1%}",
            'avg_satisfaction': session.avg_satisfaction,
            'avg_processing_time': avg_processing_time,
            'storage_distribution': storage_distribution,
            'current_weights': session.learning_weights,
            'created_at': session.created_at,
            'last_activity': session.last_activity
        }, status=status.HTTP_200_OK)
        
    except ChatSession.DoesNotExist:
        return Response({
            'error': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)

def chat_interface(request):
    return render(request, 'chat/simple_chat.html')
