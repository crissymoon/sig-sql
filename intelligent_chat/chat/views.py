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
    
    def multi_layer_sigmoid(x):
        return sigmoid(x)
    
    class Lexer:
        def __init__(self, text): pass
        def tokenize(self): return []
    
    class TokenType:
        IDENTIFIER = "IDENTIFIER"
    
    def analyze_string_patterns(text):
        return {'patterns': [], 'complexity': 0.5}

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
        dataset_dir = os.path.join('..', 'datasets')
        
        self.dataset_cache = {
            'business_terms': [],
            'technical_terms': [],
            'programming_keywords': [],
            'common_words': [],
            'names': [],
            'sentences': [],
            'conversational_patterns': {},
            'intent_patterns': {},
            'response_templates': {}
        }
        
        dataset_files = {
            'business_terms': 'business_terms.txt',
            'technical_terms': 'technology_vocabulary.txt',
            'programming_keywords': 'programming_request_keywords.txt',
            'common_words': 'common_english_words.txt',
            'names': 'names_dataset.txt',
            'sentences': 'english_sentences.txt'
        }
        
        # Load datasets with fallback
        for key, filename in dataset_files.items():
            file_path = os.path.join(dataset_dir, filename)
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f.readlines() if line.strip()]
                        self.dataset_cache[key] = lines[:500]  # Limit to prevent memory issues
                else:
                    # Fallback data
                    if key == 'business_terms':
                        self.dataset_cache[key] = ['analysis', 'report', 'metrics', 'business', 'enterprise', 'strategy']
                    elif key == 'technical_terms':
                        self.dataset_cache[key] = ['algorithm', 'database', 'function', 'code', 'system', 'technical']
                    elif key == 'programming_keywords':
                        self.dataset_cache[key] = ['python', 'javascript', 'sql', 'html', 'css', 'api']
                    else:
                        self.dataset_cache[key] = ['data', 'information', 'content', 'text', 'input', 'output']
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                self.dataset_cache[key] = ['data', 'content', 'information']
            'business_terms': 'business_vocabulary.txt',
            'technical_terms': 'technology_vocabulary.txt', 
            'programming_keywords': 'programming_request_keywords.txt',
            'common_words': 'common_english_words.txt',
            'names': 'names_dataset.txt',
            'sentences': 'english_sentences.txt'
        }
        
        for key, filename in dataset_files.items():
            filepath = os.path.join(dataset_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        self.dataset_cache[key] = content.lower().split('\n')
                except Exception as e:
                    self.dataset_cache[key] = []
        
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
        analysis = self.tokenize_and_analyze(user_input)
        
        self.store_in_memory(user_input, analysis, session_id)
        
        context = self.get_conversation_context(session_id)
        
        response_parts = []
        
        if ADVANCED_NLP_AVAILABLE and self.nlp:
            try:
                doc = self.nlp(user_input)
                entities = [(ent.text, ent.label_) for ent in doc.ents]
                analysis['spacy_entities'] = entities
            except:
                analysis['spacy_entities'] = []
        
        if analysis['intents']:
            primary_intent = analysis['intents'][0]
            context_response = self.generate_intent_response(primary_intent, analysis, context)
            response_parts.append(context_response)
        
        if analysis['entities'] or (ADVANCED_NLP_AVAILABLE and analysis.get('spacy_entities')):
            entity_response = self.generate_entity_response(analysis)
            if entity_response:
                response_parts.append(entity_response)
        
        similarity_response = self.find_similar_conversations(user_input)
        if similarity_response:
            response_parts.append(similarity_response)
        
        learning_insight = self.generate_learning_insight(analysis, context)
        if learning_insight:
            response_parts.append(learning_insight)
        
        if not response_parts:
            response_parts.append(f"Processing input with {len(analysis['tokens'])} tokens using advanced ML algorithms")
            response_parts.append("Learning from conversation patterns to improve future responses")
        
        final_response = self.combine_response_parts(response_parts)
        
        self.learn_from_interaction(user_input, final_response, analysis, session_id)
        
        return final_response
    
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

chat_service = IntelligentChatService()

@api_view(['POST'])
def process_chat_input(request):
    try:
        data = request.data
        user_input = data.get('user_input', '')
        data_content = data.get('data_content', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_input or not data_content:
            return Response({
                'error': 'user_input and data_content are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        chat_system = chat_service.get_or_create_chat_system(session_id)
        
        start_time = time.time()
        result = chat_system.process_interaction(data_content, user_input)
        processing_time = time.time() - start_time
        
        # Enhanced analysis with sigmoid features
        enhanced_features = chat_service.analyze_with_sigmoid(
            data_content + " " + user_input, 
            chat_system.learning_system.weights
        )
        result['features'].update(enhanced_features)
        
        confidence_score = min(result['storage_score'], 1.0)
        
        chat_response = chat_service.generate_ml_response(user_input, session_id)
        
        session = ChatSession.objects.get(session_id=session_id)
        session.total_interactions += 1
        session.learning_weights = chat_system.learning_system.weights
        session.save()
        
        interaction = ChatInteraction.objects.create(
            session=session,
            user_input=user_input,
            data_content=data_content,
            storage_recommendation=result['storage_choice'],
            confidence_score=confidence_score,
            features_analyzed=result['features'],
            processing_time=processing_time
        )
        
        if result['should_learn']:
            context_type = max(
                ['business', 'technical', 'personal'],
                key=lambda x: result['features'].get(f'{x}_indicators', 0)
            )
            LearningPattern.objects.create(
                session=session,
                context_type=context_type,
                storage_choice=result['storage_choice'],
                feedback_score=None,
                success=None,
                weights_before=session.learning_weights,
                weights_after=session.learning_weights
            )
        
        storage_descriptions = {
            'enterprise_sql': {
                'name': 'Enterprise SQL Database',
                'description': 'Structured business data with complex queries',
                'features': ['ACID compliance', 'Business intelligence', 'Reporting']
            },
            'technical_nosql': {
                'name': 'Technical NoSQL Storage',
                'description': 'Flexible schema for code and JSON data',
                'features': ['Document storage', 'Scalability', 'Developer tools']
            },
            'personal_secure': {
                'name': 'Personal Secure Storage',
                'description': 'Encrypted private data storage',
                'features': ['Encryption', 'Access control', 'Privacy protection']
            },
            'hybrid_intelligent': {
                'name': 'Hybrid Intelligent Storage',
                'description': 'AI-optimized multi-format storage',
                'features': ['Multi-format', 'AI optimization', 'Adaptive indexing']
            }
        }
        
        storage_info = storage_descriptions.get(
            result['storage_choice'], 
            storage_descriptions['hybrid_intelligent']
        )
        
        return Response({
            'session_id': session_id,
            'interaction_id': interaction.id,
            'chat_response': chat_response,
            'storage_recommendation': {
                'type': result['storage_choice'],
                'name': storage_info['name'],
                'description': storage_info['description'],
                'features': storage_info['features'],
                'confidence': f"{confidence_score:.1%}"
            },
            'features_analyzed': result['features'],
            'should_learn': result['should_learn'],
            'processing_time': processing_time,
            'weights': chat_system.learning_system.weights
        }, status=status.HTTP_200_OK)
        
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
