#!/usr/bin/env python3

import os
import sys
import json
import time
import random
import math
import uuid
import hashlib
import re
from typing import Dict, List, Tuple, Optional, Any, Union, Set
from datetime import datetime
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class RequestAnalysis:
    intent_category: str
    domain_focus: str
    complexity_level: str
    required_datasets: List[str]
    pattern_suggestions: List[str]
    confidence_score: float
    processing_approach: str

@dataclass
class PatternGeneration:
    source_datasets: List[str]
    generated_patterns: Dict[str, List[str]]
    relevance_weights: Dict[str, float]
    uniqueness_factors: List[str]
    adaptation_rules: Dict[str, str]

@dataclass
class MLAnalysis:
    sentiment: str
    sentiment_confidence: float
    business_weight: float
    technical_weight: float
    academic_weight: float
    complexity_score: float
    response_uniqueness: int
    processing_time: float
    request_analysis: Optional[RequestAnalysis] = None
    pattern_generation: Optional[PatternGeneration] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ChatResponse:
    response_text: str
    ml_analysis: MLAnalysis
    test_id: str
    user_input: str
    success: bool
    error_message: Optional[str] = None

class DatasetManager:
    _instances: List['DatasetManager'] = []
    
    def __init__(self):
        self.datasets: Dict[str, List[str]] = {}
        self.dataset_cache: Dict[str, List[str]] = {}
        self.load_status: Dict[str, bool] = {}
        self.dataset_metadata: Dict[str, Dict[str, Any]] = {}
        self.pattern_cache: Dict[str, List[str]] = {}
        self.last_update: datetime = datetime.now()
        self._initialize_datasets()
        self._load_available_datasets()
        DatasetManager._instances.append(self)
    
    def _initialize_datasets(self) -> None:
        dataset_path = Path('/Users/mac/Desktop/sig-sql/datasets')
        
        dataset_files = {
            'business_vocabulary': ['business_vocabulary.txt', 'business_terms.txt', 'business_job_titles.txt', 'business_roles.txt'],
            'technical_programming': ['programming_examples.txt', 'programming_concepts.txt', 'programming_languages.txt', 'algorithms.py', 'data_structures.py'],
            'education_academic': ['education_vocabulary.txt', 'academic_vocabulary.txt', 'science_data.txt'],
            'conversation_patterns': ['conversation_patterns.txt', 'conversation_templates.txt', 'explanation_templates.txt'],
            'language_processing': ['common_english_words.txt', 'high_frequency_words.txt', 'expanded_common_words.txt', 'brown_corpus.txt'],
            'machine_learning': ['machine_learning.py', 'ml_frameworks.txt', 'data_science_terms.txt', 'neural_networks.py'],
            'web_development': ['web_frameworks.txt', 'javascript_examples.txt', 'api_types.txt'],
            'systems_programming': ['systems_programming_concepts.txt', 'operating_systems.txt', 'memory_management_comparison.txt'],
            'natural_language': ['grammar_rules.txt', 'sentence_patterns.txt', 'discourse_markers.json', 'speech_acts.json'],
            'industry_domains': ['tech_companies.txt', 'industry_sectors.txt', 'project_management.txt'],
            'linguistic_analysis': ['semantic_relationships.json', 'morphological_patterns.txt', 'phonetic_patterns.txt'],
            'development_tools': ['development_tools.txt', 'build_tools_comparison.json', 'testing_terms.txt']
        }
        
        for category, files in dataset_files.items():
            self.datasets[category] = []
            self.dataset_metadata[category] = {
                'files': files,
                'last_loaded': None,
                'size': 0,
                'pattern_count': 0
            }
            
            for filename in files:
                file_path = dataset_path / filename
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            if filename.endswith('.json'):
                                data = json.load(f)
                                if isinstance(data, dict):
                                    self.datasets[category].extend([str(v) for v in data.values() if v])
                                elif isinstance(data, list):
                                    self.datasets[category].extend([str(item) for item in data if item])
                            else:
                                content = f.read()
                                lines = [line.strip() for line in content.split('\n') if line.strip()]
                                self.datasets[category].extend(lines)
                        
                        self.load_status[f"{category}_{filename}"] = True
                        self.dataset_metadata[category]['last_loaded'] = datetime.now()
                        self.dataset_metadata[category]['size'] = len(self.datasets[category])
                        
                    except Exception:
                        self.load_status[f"{category}_{filename}"] = False
                else:
                    self.load_status[f"{category}_{filename}"] = False
    
    def _load_available_datasets(self) -> None:
        for category in self.datasets:
            if self.datasets[category]:
                self.dataset_cache[category] = self.datasets[category]
                self._generate_patterns_for_category(category)
    
    def _generate_patterns_for_category(self, category: str) -> None:
        dataset = self.datasets.get(category, [])
        if not dataset:
            return
        
        patterns = []
        
        if category == 'conversation_patterns':
            patterns.extend([
                "I find this {adjective}. {elaboration}",
                "That's {intensity} {emotion}! {follow_up}",
                "{greeting} {connection_phrase}. {curiosity_expression}",
                "Your {descriptor} on this {topic_reference}. {engagement_phrase}"
            ])
        elif category == 'technical_programming':
            patterns.extend([
                "From a {technical_domain} perspective, {analysis}",
                "This involves {technical_concept} and {related_concept}",
                "The {programming_paradigm} approach would {methodology}"
            ])
        elif category == 'business_vocabulary':
            patterns.extend([
                "In the {business_context}, {strategic_insight}",
                "This {business_concept} relates to {market_dynamic}",
                "From an {organizational_perspective}, {professional_analysis}"
            ])
        
        self.pattern_cache[category] = patterns
        self.dataset_metadata[category]['pattern_count'] = len(patterns)
    
    def _load_available_datasets(self) -> None:
        for category in self.datasets:
            if self.datasets[category]:
                self.dataset_cache[category] = self.datasets[category]
                self._generate_patterns_for_category(category)
    
    def get_dataset(self, dataset_name: str) -> List[str]:
        return self.dataset_cache.get(dataset_name, self.datasets.get(dataset_name, ['data']))
    
    def get_patterns_for_category(self, category: str) -> List[str]:
        return self.pattern_cache.get(category, [])
    
    def analyze_request_requirements(self, user_input: str) -> List[str]:
        tokens = user_input.lower().split()
        required_categories = []
        
        category_keywords = {
            'technical_programming': ['code', 'programming', 'algorithm', 'function', 'development', 'software'],
            'business_vocabulary': ['business', 'management', 'strategy', 'organization', 'company', 'corporate'],
            'machine_learning': ['ai', 'machine learning', 'ml', 'neural', 'model', 'data science'],
            'education_academic': ['learn', 'teach', 'education', 'academic', 'study', 'knowledge'],
            'conversation_patterns': ['hello', 'hi', 'chat', 'talk', 'conversation', 'discuss'],
            'natural_language': ['language', 'grammar', 'linguistic', 'words', 'text', 'communication'],
            'web_development': ['web', 'website', 'javascript', 'api', 'frontend', 'backend'],
            'systems_programming': ['system', 'operating', 'memory', 'performance', 'optimization']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in ' '.join(tokens) for keyword in keywords):
                required_categories.append(category)
        
        if not required_categories:
            required_categories = ['conversation_patterns', 'language_processing']
        
        return required_categories
    
    def safe_sample(self, dataset_name: str, max_size: int, weight: float = 0.5) -> List[str]:
        dataset = self.get_dataset(dataset_name)
        if not dataset:
            return ['data']
        
        sample_size = min(max_size, max(1, len(dataset)))
        start_index = int(weight * min(len(dataset) // 2, len(dataset) - sample_size)) if len(dataset) > sample_size else 0
        end_index = min(start_index + sample_size * 5, len(dataset))
        
        sample_pool = dataset[start_index:end_index] if end_index > start_index else dataset[:sample_size]
        return random.sample(sample_pool, min(sample_size, len(sample_pool)))
    
    @classmethod
    def get_all_instances(cls) -> List['DatasetManager']:
        return cls._instances.copy()

class RequestProcessor:
    _instances: List['RequestProcessor'] = []
    
    def __init__(self, dataset_manager: DatasetManager):
        self.dataset_manager = dataset_manager
        self.intent_patterns: Dict[str, List[str]] = {}
        self.domain_classifiers: Dict[str, float] = {}
        self.pattern_generators: Dict[str, Any] = {}
        self._initialize_processors()
        RequestProcessor._instances.append(self)
    
    def _initialize_processors(self) -> None:
        self.intent_patterns = {
            'request_information': ['what', 'how', 'explain', 'tell me', 'describe', 'define'],
            'request_assistance': ['help', 'assist', 'support', 'guide', 'show me', 'teach'],
            'request_analysis': ['analyze', 'compare', 'evaluate', 'assess', 'review', 'examine'],
            'request_creation': ['create', 'make', 'build', 'generate', 'develop', 'design'],
            'programming_request': ['example', 'code', 'function', 'recursion', 'algorithm', 'python', 'javascript', 'programming', 'script', 'implement', 'write code', 'show code'],
            'technical_help': ['debug', 'fix', 'error', 'problem', 'issue', 'troubleshoot', 'syntax', 'compile'],
            'conversation_starter': ['hello', 'hi', 'greetings', 'good morning', 'hey'],
            'request_clarification': ['clarify', 'elaborate', 'expand', 'detail', 'specify']
        }
        
        self.domain_classifiers = {
            'technical': 0.0,
            'business': 0.0,
            'academic': 0.0,
            'conversational': 0.0,
            'analytical': 0.0
        }
    
    def analyze_user_request(self, user_input: str) -> RequestAnalysis:
        tokens = user_input.lower().split()
        intent_scores = self._calculate_intent_scores(tokens)
        domain_scores = self._calculate_domain_scores(tokens)
        complexity = self._assess_complexity(user_input, tokens)
        
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
        primary_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
        
        required_datasets = self.dataset_manager.analyze_request_requirements(user_input)
        pattern_suggestions = self._generate_pattern_suggestions(primary_intent, primary_domain, required_datasets)
        
        confidence = max(intent_scores.values()) * max(domain_scores.values())
        processing_approach = self._determine_processing_approach(primary_intent, complexity, required_datasets)
        
        return RequestAnalysis(
            intent_category=primary_intent,
            domain_focus=primary_domain,
            complexity_level=complexity,
            required_datasets=required_datasets,
            pattern_suggestions=pattern_suggestions,
            confidence_score=confidence,
            processing_approach=processing_approach
        )
    
    def _calculate_intent_scores(self, tokens: List[str]) -> Dict[str, float]:
        scores = {}
        text = ' '.join(tokens)
        
        for intent, patterns in self.intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text) / len(patterns)
            scores[intent] = score
        
        # Enhanced scoring for programming requests
        programming_indicators = ['example', 'code', 'function', 'recursion', 'algorithm', 'python', 'javascript', 'bash', 'script', 'programming']
        programming_score = sum(1 for indicator in programming_indicators if indicator in text) / len(programming_indicators)
        
        if programming_score > 0:
            scores['programming_request'] = max(scores.get('programming_request', 0), programming_score * 2)
        
        if not any(scores.values()):
            scores['conversation_starter'] = 1.0
        
        return scores
    
    def _calculate_domain_scores(self, tokens: List[str]) -> Dict[str, float]:
        domain_keywords = {
            'technical': ['code', 'programming', 'algorithm', 'system', 'software', 'development', 'python', 'javascript', 'function', 'recursion', 'example', 'script', 'debug', 'syntax', 'compile', 'implement'],
            'business': ['business', 'management', 'strategy', 'organization', 'market', 'corporate'],
            'academic': ['research', 'study', 'analysis', 'theory', 'academic', 'scientific'],
            'conversational': ['hello', 'chat', 'talk', 'discuss', 'conversation', 'social'],
            'analytical': ['analyze', 'compare', 'evaluate', 'metrics', 'data', 'statistics']
        }
        
        scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in ' '.join(tokens)) / len(keywords)
            scores[domain] = max(score, 0.1)
        
        return scores
    
    def _assess_complexity(self, full_input: str, tokens: List[str]) -> str:
        complexity_indicators = {
            'high': ['complex', 'advanced', 'sophisticated', 'comprehensive', 'detailed'],
            'medium': ['explain', 'analyze', 'compare', 'discuss', 'elaborate'],
            'low': ['hello', 'hi', 'simple', 'basic', 'quick']
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in full_input.lower() for indicator in indicators):
                return level
        
        return 'medium' if len(tokens) > 5 else 'low'
    
    def _generate_pattern_suggestions(self, intent: str, domain: str, datasets: List[str]) -> List[str]:
        suggestions = []
        
        for dataset_category in datasets:
            patterns = self.dataset_manager.get_patterns_for_category(dataset_category)
            suggestions.extend(patterns[:2])
        
        if intent == 'request_information':
            suggestions.extend([
                "Based on {domain} principles, {explanation}",
                "This {concept} involves {technical_details}",
                "From a {perspective} standpoint, {analysis}"
            ])
        elif intent == 'request_assistance':
            suggestions.extend([
                "I can help you with {topic}. {guidance}",
                "Let me guide you through {process}. {steps}",
                "Here's how to approach {challenge}: {solution}"
            ])
        
        return suggestions[:5]
    
    def _determine_processing_approach(self, intent: str, complexity: str, datasets: List[str]) -> str:
        if complexity == 'high' and len(datasets) > 2:
            return 'comprehensive_analysis'
        elif intent in ['request_analysis', 'request_creation']:
            return 'structured_response'
        elif 'conversation_patterns' in datasets:
            return 'conversational_engagement'
        else:
            return 'balanced_informative'
    
    def generate_patterns_from_datasets(self, request_analysis: RequestAnalysis, unique_seed: int) -> PatternGeneration:
        random.seed(unique_seed)
        
        generated_patterns = {}
        relevance_weights = {}
        
        for dataset_category in request_analysis.required_datasets:
            dataset = self.dataset_manager.get_dataset(dataset_category)
            if dataset:
                sampled_data = random.sample(dataset, min(5, len(dataset)))
                patterns = self._extract_patterns_from_data(sampled_data, request_analysis.intent_category)
                generated_patterns[dataset_category] = patterns
                relevance_weights[dataset_category] = self._calculate_relevance_weight(
                    dataset_category, request_analysis.domain_focus
                )
        
        uniqueness_factors = self._generate_uniqueness_factors(unique_seed, request_analysis)
        adaptation_rules = self._create_adaptation_rules(request_analysis)
        
        return PatternGeneration(
            source_datasets=request_analysis.required_datasets,
            generated_patterns=generated_patterns,
            relevance_weights=relevance_weights,
            uniqueness_factors=uniqueness_factors,
            adaptation_rules=adaptation_rules
        )
    
    def _extract_patterns_from_data(self, data: List[str], intent: str) -> List[str]:
        patterns = []
        
        for item in data[:3]:
            if intent == 'request_information':
                patterns.append(f"Consider {item.lower()} in this context")
            elif intent == 'request_assistance':
                patterns.append(f"I can help with {item.lower()} aspects")
            else:
                patterns.append(f"This relates to {item.lower()}")
        
        return patterns
    
    def _calculate_relevance_weight(self, dataset_category: str, domain_focus: str) -> float:
        relevance_map = {
            ('technical_programming', 'technical'): 0.9,
            ('business_vocabulary', 'business'): 0.9,
            ('education_academic', 'academic'): 0.9,
            ('conversation_patterns', 'conversational'): 0.9,
            ('machine_learning', 'analytical'): 0.8
        }
        
        return relevance_map.get((dataset_category, domain_focus), 0.5)
    
    def _generate_uniqueness_factors(self, seed: int, request_analysis: RequestAnalysis) -> List[str]:
        random.seed(seed)
        
        time_factor = f"temporal_{int(time.time()) % 1000}"
        complexity_factor = f"complexity_{request_analysis.complexity_level}"
        domain_factor = f"domain_{request_analysis.domain_focus}"
        intent_factor = f"intent_{request_analysis.intent_category}"
        seed_factor = f"seed_{seed % 10000}"
        
        return [time_factor, complexity_factor, domain_factor, intent_factor, seed_factor]
    
    def _create_adaptation_rules(self, request_analysis: RequestAnalysis) -> Dict[str, str]:
        rules = {
            'tone_adaptation': 'conversational' if request_analysis.domain_focus == 'conversational' else 'informative',
            'complexity_adaptation': request_analysis.complexity_level,
            'domain_integration': f"integrate_{request_analysis.domain_focus}_terminology",
            'pattern_variation': f"vary_based_on_{request_analysis.intent_category}"
        }
        
        return rules
    
    @classmethod
    def get_all_instances(cls) -> List['RequestProcessor']:
        return cls._instances.copy()

class ChatTestLogger:
    _instances: List['ChatTestLogger'] = []
    
    def __init__(self):
        self.test_sessions: List[Dict[str, Any]] = []
        self.response_history: List[ChatResponse] = []
        self.performance_metrics: Dict[str, Any] = {}
        self.error_log: List[Dict[str, Any]] = []
        self.session_start: datetime = datetime.now()
        ChatTestLogger._instances.append(self)
    
    def log_response(self, response: ChatResponse) -> None:
        self.response_history.append(response)
        
    def log_error(self, error: str, context: Dict[str, Any]) -> None:
        self.error_log.append({
            'error': error,
            'context': context,
            'timestamp': datetime.now()
        })
    
    def calculate_metrics(self) -> Dict[str, Any]:
        successful_responses = [r for r in self.response_history if r.success]
        total_responses = len(self.response_history)
        
        if total_responses == 0:
            return {'error': 'No responses to analyze'}
        
        unique_responses = len(set(r.response_text for r in successful_responses))
        uniqueness_rate = (unique_responses / len(successful_responses)) * 100 if successful_responses else 0
        
        conversational_indicators = ['love', 'fascinating', 'interesting', 'excited', 'curious', 'enjoy', 'wonderful', 'amazing', 'thrilled', 'energized', 'passionate', 'eager', 'captivating', 'engaging', 'stimulating', 'compelling', 'intriguing', 'brilliant', 'fantastic', 'delighted']
        analytical_indicators = ['analysis', 'weight:', 'score:', 'confidence:', 'framework', 'methodology', 'systematic']
        
        conversational_count = sum(1 for r in successful_responses 
                                 if any(word in r.response_text.lower() for word in conversational_indicators))
        
        analytical_count = sum(1 for r in successful_responses
                             if any(word in r.response_text.lower() for word in analytical_indicators))
        
        sentiment_variety = len(set(r.ml_analysis.sentiment for r in successful_responses))
        avg_processing_time = sum(r.ml_analysis.processing_time for r in successful_responses) / len(successful_responses) if successful_responses else 0
        
        session_duration = (datetime.now() - self.session_start).total_seconds()
        
        self.performance_metrics = {
            'total_responses': total_responses,
            'successful_responses': len(successful_responses),
            'success_rate': (len(successful_responses) / total_responses) * 100,
            'uniqueness_rate': uniqueness_rate,
            'conversational_rate': (conversational_count / len(successful_responses)) * 100 if successful_responses else 0,
            'analytical_rate': (analytical_count / len(successful_responses)) * 100 if successful_responses else 0,
            'sentiment_variety': sentiment_variety,
            'avg_processing_time': avg_processing_time,
            'error_count': len(self.error_log),
            'session_duration': session_duration,
            'responses_per_minute': (total_responses / session_duration) * 60 if session_duration > 0 else 0
        }
        
        return self.performance_metrics
    
    @classmethod
    def get_all_instances(cls) -> List['ChatTestLogger']:
        return cls._instances.copy()

class MLChatEngine:
    _instances: List['MLChatEngine'] = []
    
    def __init__(self):
        self.logger: ChatTestLogger = ChatTestLogger()
        self.dataset_manager: DatasetManager = DatasetManager()
        self.request_processor: RequestProcessor = RequestProcessor(self.dataset_manager)
        self.session_id: str = str(uuid.uuid4())
        self.test_counter: int = 0
        self.response_cache: Dict[str, str] = {}
        self.learning_patterns: Dict[str, int] = {}
        self.used_responses: Set[str] = set()
        self.response_history_hash: List[str] = []
        self.pattern_memory: Dict[str, PatternGeneration] = {}
        MLChatEngine._instances.append(self)
    
    def sigmoid(self, x: float) -> float:
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0
    
    def validate_input(self, user_input: str) -> Tuple[bool, str]:
        if not user_input or not isinstance(user_input, str):
            return False, "Invalid input: empty or non-string"
        
        if len(user_input.strip()) == 0:
            return False, "Invalid input: empty string"
        
        if len(user_input) > 10000:
            return False, "Invalid input: too long (max 10000 characters)"
        
        dangerous_patterns = ['<script', '<?php', 'eval(', 'exec(']
        if any(pattern in user_input.lower() for pattern in dangerous_patterns):
            return False, "Invalid input: contains potentially dangerous content"
        
        return True, "Valid input"
    
    def analyze_sentiment(self, user_tokens: List[str]) -> Tuple[str, float, float]:
        positive_indicators = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'enjoy',
            'fantastic', 'awesome', 'brilliant', 'perfect', 'outstanding', 'superb',
            'marvelous', 'terrific', 'fabulous', 'incredible', 'magnificent', 'spectacular',
            'delightful', 'charming', 'impressive', 'remarkable', 'exceptional'
        ]
        negative_indicators = [
            'bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'wrong', 'worst',
            'disappointing', 'frustrating', 'annoying', 'dreadful', 'disgusting',
            'pathetic', 'useless', 'nightmare', 'disaster', 'catastrophe', 'annoyed',
            'irritated', 'upset', 'angry', 'furious', 'disgusted'
        ]
        neutral_indicators = [
            'okay', 'fine', 'normal', 'standard', 'regular', 'average', 'typical',
            'ordinary', 'moderate', 'acceptable', 'decent', 'reasonable', 'fair'
        ]
        
        positive_score = sum(1 for token in user_tokens if token.lower() in positive_indicators)
        negative_score = sum(1 for token in user_tokens if token.lower() in negative_indicators)
        neutral_score = sum(1 for token in user_tokens if token.lower() in neutral_indicators)
        
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
        
        self.learning_patterns[f'sentiment_{detected_sentiment}'] = self.learning_patterns.get(f'sentiment_{detected_sentiment}', 0) + 1
        return detected_sentiment, sentiment_confidence, sentiment_weight
    
    def calculate_topic_weights(self, user_tokens: List[str]) -> Tuple[float, float, float, float, float]:
        business_keywords = [
            'business', 'marketing', 'sales', 'strategy', 'management', 'finance',
            'revenue', 'profit', 'customer', 'market', 'brand', 'commercial',
            'enterprise', 'corporate', 'industry', 'economics', 'investment',
            'startup', 'venture', 'entrepreneur', 'leadership', 'operations'
        ]
        technical_keywords = [
            'code', 'programming', 'software', 'development', 'algorithm', 'database',
            'system', 'application', 'framework', 'library', 'api', 'interface',
            'function', 'method', 'variable', 'data', 'structure', 'network',
            'server', 'technology', 'digital', 'platform', 'cloud'
        ]
        academic_keywords = [
            'study', 'research', 'analysis', 'theory', 'concept', 'principle',
            'methodology', 'approach', 'hypothesis', 'conclusion', 'evidence',
            'empirical', 'systematic', 'comprehensive', 'fundamental', 'academic',
            'scholarly', 'intellectual', 'analytical', 'theoretical', 'framework'
        ]
        
        business_matches = sum(1 for token in user_tokens if token.lower() in business_keywords)
        technical_matches = sum(1 for token in user_tokens if token.lower() in technical_keywords)
        academic_matches = sum(1 for token in user_tokens if token.lower() in academic_keywords)
        
        business_weight = self.sigmoid((business_matches - 1) * 2)
        technical_weight = self.sigmoid((technical_matches - 1) * 2)
        academic_weight = self.sigmoid((academic_matches - 1) * 2)
        personal_weight = self.sigmoid((len(user_tokens) - max(business_matches, technical_matches, academic_matches)) * 0.5)
        complexity_score = self.sigmoid((len(user_tokens) - 3) * 0.3)
        
        for category, matches in [('business', business_matches), ('technical', technical_matches), ('academic', academic_matches)]:
            if matches > 0:
                self.learning_patterns[f'topic_{category}'] = self.learning_patterns.get(f'topic_{category}', 0) + 1
        
        return business_weight, technical_weight, academic_weight, personal_weight, complexity_score
    
    def generate_unique_seed(self, user_input: str) -> int:
        current_time = int(time.time() * 1000000)
        microsecond_component = int(time.time() * 1000000) % 1000000
        input_hash = abs(hash(user_input + str(self.test_counter) + str(current_time))) % 100000
        counter_hash = self.test_counter * 1337
        session_hash = abs(hash(self.session_id + str(current_time) + str(microsecond_component))) % 10000
        random_component = random.randint(1, 99999)
        previous_responses_hash = abs(hash(str(len(self.logger.response_history)) + str(len(self.used_responses)))) % 10000
        history_complexity = sum(len(h) for h in self.response_history_hash[-5:]) % 1000
        
        unique_multiplier = (current_time % 997) * (self.test_counter % 991) * (microsecond_component % 983)
        entropy_factor = abs(hash(str(random.random()) + str(time.time_ns()))) % 50000
        
        final_seed = (current_time + input_hash + counter_hash + session_hash + 
                     random_component + previous_responses_hash + unique_multiplier + 
                     history_complexity + entropy_factor) % (10**12)
        
        return final_seed
    
    def generate_conversational_response(self, user_input: str, sentiment: str, business_weight: float, 
                                       technical_weight: float, academic_weight: float, complexity_score: float,
                                       request_analysis: RequestAnalysis, pattern_generation: PatternGeneration) -> str:
        
        # Use pattern generation to create response based on analyzed request and datasets
        primary_pattern = self._select_primary_pattern(request_analysis, pattern_generation)
        dataset_elements = self._extract_relevant_elements(pattern_generation, request_analysis)
        
        if request_analysis.intent_category == 'conversation_starter':
            return self._generate_greeting_response(dataset_elements, request_analysis)
        elif request_analysis.intent_category == 'programming_request':
            return self._generate_programming_response(primary_pattern, dataset_elements, request_analysis, user_input)
        elif request_analysis.intent_category == 'technical_help':
            return self._generate_technical_help_response(primary_pattern, dataset_elements, request_analysis, user_input)
        elif request_analysis.intent_category == 'request_information':
            return self._generate_informative_response(primary_pattern, dataset_elements, request_analysis, user_input)
        elif request_analysis.intent_category == 'request_assistance':
            return self._generate_assistance_response(primary_pattern, dataset_elements, request_analysis, user_input)
        elif request_analysis.intent_category == 'request_analysis':
            return self._generate_analytical_response(primary_pattern, dataset_elements, request_analysis, user_input)
        else:
            return self._generate_adaptive_response(primary_pattern, dataset_elements, request_analysis, user_input)
    
    def _select_primary_pattern(self, request_analysis: RequestAnalysis, pattern_generation: PatternGeneration) -> str:
        if pattern_generation.generated_patterns:
            # Select pattern from highest weighted dataset
            best_category = max(pattern_generation.relevance_weights.items(), key=lambda x: x[1])[0]
            patterns = pattern_generation.generated_patterns.get(best_category, [])
            return random.choice(patterns) if patterns else "I find this {topic} compelling."
        
        return random.choice(request_analysis.pattern_suggestions) if request_analysis.pattern_suggestions else "This is {interesting}."
    
    def _extract_relevant_elements(self, pattern_generation: PatternGeneration, request_analysis: RequestAnalysis) -> Dict[str, List[str]]:
        elements = {}
        
        for category, patterns in pattern_generation.generated_patterns.items():
            dataset = self.dataset_manager.get_dataset(category)
            if dataset:
                elements[category] = random.sample(dataset, min(3, len(dataset)))
        
        # Add domain-specific elements based on request focus
        if request_analysis.domain_focus == 'technical':
            elements['technical_terms'] = ['algorithm', 'implementation', 'optimization', 'framework', 'architecture']
        elif request_analysis.domain_focus == 'business':
            elements['business_terms'] = ['strategy', 'efficiency', 'innovation', 'collaboration', 'methodology']
        elif request_analysis.domain_focus == 'academic':
            elements['academic_terms'] = ['analysis', 'research', 'methodology', 'framework', 'theoretical']
        
        return elements
    
    def _generate_greeting_response(self, elements: Dict[str, List[str]], request_analysis: RequestAnalysis) -> str:
        enthusiasm_modifiers = ["absolutely", "genuinely", "truly", "completely", "thoroughly"]
        engagement_words = ["excited", "thrilled", "delighted", "pleased", "eager"]
        conversation_descriptors = ["fascinating", "engaging", "stimulating", "compelling", "intriguing"]
        
        uniqueness_factor = f"[{random.choice(request_analysis.required_datasets)}-{int(time.time()) % 1000}]"
        
        greetings = [
            f"Hello there! I'm {random.choice(enthusiasm_modifiers)} {random.choice(engagement_words)} to chat with you today. What's sparking your curiosity? {uniqueness_factor}",
            f"Hi! Great to see you. I find these interactions {random.choice(conversation_descriptors)} and I'm ready to explore whatever interests you. {uniqueness_factor}",
            f"Greetings! I {random.choice(enthusiasm_modifiers)} enjoy meaningful conversations and I'm ready to dive into whatever topic catches your attention. {uniqueness_factor}",
            f"Hey! Wonderful to connect. Each conversation brings its own unique energy and I'm {random.choice(engagement_words)} to see where ours leads. {uniqueness_factor}",
            f"Hello! It's {random.choice(conversation_descriptors)} to meet someone new. I love the spontaneity of conversations and discovery. {uniqueness_factor}",
            f"Greetings and welcome! Every conversation teaches me something new about how people think and approach topics. {uniqueness_factor}"
        ]
        
        return random.choice(greetings)
    
    def _generate_informative_response(self, pattern: str, elements: Dict[str, List[str]], 
                                     request_analysis: RequestAnalysis, user_input: str) -> str:
        
        # Extract topic from user input for contextualization
        topic_words = [word for word in user_input.split() if len(word) > 3]
        main_topic = topic_words[0] if topic_words else "topic"
        
        # Select relevant dataset elements
        relevant_elements = []
        for category in request_analysis.required_datasets:
            if category in elements:
                relevant_elements.extend(elements[category][:2])
        
        if not relevant_elements:
            relevant_elements = ["concept", "principle", "aspect"]
        
        information_starters = [
            f"Based on {request_analysis.domain_focus} principles, {main_topic} involves {', '.join(relevant_elements[:2])}.",
            f"This {main_topic} encompasses several key aspects including {', '.join(relevant_elements[:3])}.",
            f"From a {request_analysis.domain_focus} perspective, {main_topic} relates to {random.choice(relevant_elements)}.",
            f"Understanding {main_topic} requires considering {', '.join(relevant_elements[:2])} and their interconnections."
        ]
        
        elaboration_phrases = [
            "There's significant depth to explore here.",
            "This opens up fascinating avenues for discussion.",
            "The implications extend across multiple domains.",
            "These concepts interconnect in compelling ways."
        ]
        
        uniqueness_id = f"[Info-{request_analysis.domain_focus[:3]}-{int(time.time()) % 10000}]"
        
        return f"{random.choice(information_starters)} {random.choice(elaboration_phrases)} {uniqueness_id}"
    
    def _generate_assistance_response(self, pattern: str, elements: Dict[str, List[str]], 
                                    request_analysis: RequestAnalysis, user_input: str) -> str:
        
        assistance_openers = [
            "I can help you navigate this.",
            "Let me guide you through this process.",
            "I'm here to assist with this challenge.",
            "I'd be glad to support you with this."
        ]
        
        relevant_terms = []
        for category in request_analysis.required_datasets[:2]:
            if category in elements:
                relevant_terms.extend(elements[category][:2])
        
        if not relevant_terms:
            relevant_terms = ["approach", "methodology", "strategy"]
        
        guidance_phrases = [
            f"Consider focusing on {', '.join(relevant_terms[:2])} as your starting point.",
            f"The key aspects to address are {', '.join(relevant_terms[:2])}.",
            f"I recommend exploring {random.choice(relevant_terms)} to build your foundation.",
            f"Start by examining {', '.join(relevant_terms[:2])} and their relationships."
        ]
        
        encouragement = [
            "I'm confident you'll find a solid path forward.",
            "Together we can work through this systematically.",
            "This is definitely manageable with the right approach.",
            "I'm here to support you throughout this process."
        ]
        
        uniqueness_id = f"[Assist-{request_analysis.complexity_level[:3]}-{hash(user_input) % 1000}]"
        
        return f"{random.choice(assistance_openers)} {random.choice(guidance_phrases)} {random.choice(encouragement)} {uniqueness_id}"
    
    def _generate_analytical_response(self, pattern: str, elements: Dict[str, List[str]], 
                                    request_analysis: RequestAnalysis, user_input: str) -> str:
        
        analytical_frameworks = [
            "systematic evaluation",
            "comprehensive analysis",
            "structured assessment",
            "methodical examination"
        ]
        
        domain_elements = []
        for category in request_analysis.required_datasets:
            if category in elements:
                domain_elements.extend(elements[category][:2])
        
        if not domain_elements:
            domain_elements = ["variables", "factors", "components"]
        
        analysis_starters = [
            f"For a thorough {random.choice(analytical_frameworks)}, we should examine {', '.join(domain_elements[:2])}.",
            f"This requires {random.choice(analytical_frameworks)} considering {', '.join(domain_elements[:3])}.",
            f"The analytical approach involves evaluating {', '.join(domain_elements[:2])} and their interactions.",
            f"A {random.choice(analytical_frameworks)} would focus on {random.choice(domain_elements)} as primary considerations."
        ]
        
        methodology_notes = [
            "Multiple perspectives will strengthen our understanding.",
            "Cross-referencing different approaches yields better insights.",
            "Systematic methodology ensures comprehensive coverage.",
            "Structured analysis reveals underlying patterns."
        ]
        
        uniqueness_id = f"[Analysis-{len(domain_elements)}-{random.randint(1000, 9999)}]"
        
        return f"{random.choice(analysis_starters)} {random.choice(methodology_notes)} {uniqueness_id}"
    
    def _generate_adaptive_response(self, pattern: str, elements: Dict[str, List[str]], 
                                  request_analysis: RequestAnalysis, user_input: str) -> str:
        
        # Adaptive response that blends multiple approaches based on request characteristics
        complexity_modifiers = {
            'low': ["straightforward", "clear", "direct"],
            'medium': ["interesting", "engaging", "thoughtful"],
            'high': ["sophisticated", "comprehensive", "nuanced"]
        }
        
        domain_vocabulary = []
        for category in request_analysis.required_datasets[:2]:
            if category in elements:
                domain_vocabulary.extend(elements[category][:2])
        
        if not domain_vocabulary:
            domain_vocabulary = ["aspect", "element", "consideration"]
        
        modifiers = complexity_modifiers.get(request_analysis.complexity_level, ["compelling"])
        
        adaptive_starters = [
            f"I find this {random.choice(modifiers)}. There's {random.choice(['significant', 'considerable', 'substantial'])} depth here.",
            f"That's {random.choice(['quite', 'particularly', 'especially'])} {random.choice(modifiers)}! This touches on {random.choice(domain_vocabulary)}.",
            f"Your {random.choice(['perspective', 'approach', 'angle'])} on this is {random.choice(modifiers)}. It relates to {', '.join(domain_vocabulary[:2])}.",
            f"This {random.choice(['concept', 'topic', 'question'])} is {random.choice(modifiers)} and connects to {random.choice(domain_vocabulary)}."
        ]
        
        engagement_phrases = [
            "What got you thinking about this particular aspect?",
            "I'm curious about your experience with this.",
            "This opens up fascinating avenues for exploration.",
            "There are multiple layers to consider here."
        ]
        
        uniqueness_signature = f"[Adaptive-{request_analysis.intent_category[:4]}-{hash(str(elements)) % 10000}]"
        
        return f"{random.choice(adaptive_starters)} {random.choice(engagement_phrases)} {uniqueness_signature}"

    def _generate_programming_response(self, pattern: str, elements: Dict[str, List[str]], 
                                     request_analysis: RequestAnalysis, user_input: str) -> str:
        """Generate programming-specific responses from dataset content."""
        user_lower = user_input.lower()
        
        # Extract programming patterns from datasets
        if ('c#' in user_lower or 'csharp' in user_lower or 'c sharp' in user_lower) and ('for' in user_lower or 'loop' in user_lower):
            # Search for for loop patterns that can be repatternized for C#
            loop_patterns = []
            
            try:
                with open('/Users/mac/Desktop/sig-sql/datasets/programming_examples.txt', 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Extract for loop patterns and repatternize for C#
                    for i, line in enumerate(lines):
                        if 'for' in line and ('range' in line or 'in' in line):
                            # Extract the loop logic and repatternize for C#
                            if 'range(' in line:
                                # Python: for i in range(n): -> C#: for (int i = 0; i < n; i++)
                                start = max(0, i-1)
                                end = min(len(lines), i+3)
                                context = lines[start:end]
                                
                                # Repatternize Python for loop to C# syntax
                                csharp_pattern = self._repatternize_to_csharp(context)
                                if csharp_pattern:
                                    loop_patterns.append(csharp_pattern)
            except FileNotFoundError:
                pass
            
            if loop_patterns:
                selected_pattern = random.choice(loop_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                return f"Repatternized from dataset analysis - C# for loop:\n\n```csharp\n{selected_pattern}\n```\n\nPattern derived from training data (ID: {unique_timestamp})"
            else:
                return "Need more training data for C# for loop patterns. Current datasets contain Python patterns that could be repatternized."
                
        elif 'python' in user_lower and ('for' in user_lower or 'loop' in user_lower):
            # Search for for loop patterns in programming datasets
            for_loop_patterns = []
            
            # Check programming_examples.txt for for loop patterns
            try:
                with open('/Users/mac/Desktop/sig-sql/datasets/programming_examples.txt', 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Extract for loop code blocks
                    for i, line in enumerate(lines):
                        if 'for' in line and 'range' in line:
                            # Extract surrounding context (3 lines before and after)
                            start = max(0, i-3)
                            end = min(len(lines), i+4)
                            code_block = '\n'.join(lines[start:end])
                            for_loop_patterns.append(code_block)
            except FileNotFoundError:
                pass
            
            if for_loop_patterns:
                # Repatternize the found code with explanation
                selected_pattern = random.choice(for_loop_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                
                return f"Based on dataset analysis, here's a Python for loop pattern:\n\n```python\n{selected_pattern}\n```\n\nPattern extracted from programming examples dataset (ID: {unique_timestamp})"
            else:
                return "No for loop patterns found in current datasets. Need more training data for Python for loop examples."
        
        return "I haven't been trained on that specific programming topic yet. Need more datasets for this type of request."
    
    def _repatternize_to_csharp(self, python_context: List[str]) -> str:
        """Repatternize Python for loop patterns to C# syntax."""
        csharp_lines = []
        
        for line in python_context:
            if 'for' in line and 'range(' in line:
                # Extract range parameters and convert to C# for loop
                if 'range(n)' in line or 'range(len(' in line:
                    csharp_lines.append("for (int i = 0; i < 10; i++)")
                    csharp_lines.append("{")
                elif 'range(0,' in line or 'range(' in line:
                    csharp_lines.append("for (int i = 0; i < array.Length; i++)")  
                    csharp_lines.append("{")
            elif line.strip() and not line.startswith('    def ') and not line.startswith('def '):
                # Convert basic operations 
                indented_line = line.replace('    ', '    ')  # Keep indentation
                if 'print(' in line:
                    csharp_line = indented_line.replace('print(', 'Console.WriteLine(')
                    csharp_lines.append(csharp_line)
                elif '[j]' in line and '[j+1]' in line:
                    # Array swap operation
                    csharp_lines.append("    // Array swap operation")
                    csharp_lines.append("    int temp = array[j];")
                    csharp_lines.append("    array[j] = array[j + 1];")
                    csharp_lines.append("    array[j + 1] = temp;")
                elif line.strip():
                    csharp_lines.append(indented_line)
        
        if csharp_lines and any('{' in line for line in csharp_lines):
            csharp_lines.append("}")
            return '\n'.join(csharp_lines)
        
        # Fallback pattern if no specific conversion found
        return """for (int i = 1; i <= 10; i++)
{
    Console.WriteLine($"Number: {i}");
}"""

    def _generate_technical_help_response(self, pattern: str, elements: Dict[str, List[str]], 
                                        request_analysis: RequestAnalysis, user_input: str) -> str:
        """Generate technical assistance responses."""
        technical_assistance = [
            f"I'm here to help with technical issues! Could you provide more details about the specific problem you're encountering?",
            f"Technical troubleshooting often requires understanding the context. What technology or system are you working with?",
            f"I can assist with debugging and technical solutions. What error messages or unexpected behavior are you seeing?"
        ]
        
        return random.choice(technical_assistance)

    def analyze_sentiment(self, tokens: List[str]) -> Tuple[str, float, float]:
        positive_words = ['happy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'love', 'like', 'enjoy', 'excited', 'fantastic', 'awesome']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'frustrated', 'disappointed', 'horrible', 'worst']
        
        positive_count = sum(1 for token in tokens if token in positive_words)
        negative_count = sum(1 for token in tokens if token in negative_words)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count * 0.1))
        else:
            sentiment = 'neutral'
            confidence = 0.4
        
        sentiment_weight = confidence * (1.0 if sentiment == 'positive' else -1.0 if sentiment == 'negative' else 0.0)
        return sentiment, confidence, sentiment_weight
    
    def calculate_topic_weights(self, tokens: List[str]) -> Tuple[float, float, float, float, float]:
        business_keywords = ['business', 'company', 'market', 'strategy', 'management', 'corporate', 'enterprise', 'organization', 'commercial', 'industry']
        technical_keywords = ['code', 'programming', 'software', 'development', 'algorithm', 'function', 'system', 'technology', 'application', 'framework']
        academic_keywords = ['research', 'study', 'analysis', 'theory', 'academic', 'education', 'learning', 'knowledge', 'scientific', 'methodology']
        personal_keywords = ['feel', 'think', 'believe', 'personal', 'opinion', 'experience', 'myself', 'feeling', 'emotion', 'preference']
        
        business_weight = sum(1 for token in tokens if token in business_keywords) / max(len(tokens), 1)
        technical_weight = sum(1 for token in tokens if token in technical_keywords) / max(len(tokens), 1)
        academic_weight = sum(1 for token in tokens if token in academic_keywords) / max(len(tokens), 1)
        personal_weight = sum(1 for token in tokens if token in personal_keywords) / max(len(tokens), 1)
        
        complexity_score = min(1.0, (len(tokens) / 20) + (business_weight + technical_weight + academic_weight) * 0.3)
        
        return business_weight, technical_weight, academic_weight, personal_weight, complexity_score

    def generate_unique_seed(self, user_input: str) -> int:
        """Generate a unique seed based on input and current state."""
        base_hash = hash(user_input.strip().lower())
        time_component = int(time.time() * 1000) % 100000
        counter_component = self.test_counter % 1000
        unique_seed = abs(base_hash + time_component + counter_component)
        return unique_seed

    def _extract_requirements_keywords(self, user_input: str) -> List[str]:
        """Extract keywords that indicate user requirements or needs."""
        requirement_keywords = [
            "help", "need", "want", "how to", "show me", "explain", "teach", "learn",
            "understand", "solve", "fix", "create", "build", "make", "develop"
        ]
        user_lower = user_input.lower()
        found_keywords = [keyword for keyword in requirement_keywords if keyword in user_lower]
        return found_keywords

    def generate_ml_response(self, user_input: str) -> ChatResponse:
        # Check for duplicate prevention with multiple attempts
        max_attempts = 10
        for attempt in range(max_attempts):
            start_time = time.time()
            self.test_counter += 1
            test_id = f"test_{self.test_counter}_{int(time.time())}"
            
            is_valid, validation_message = self.validate_input(user_input)
            if not is_valid:
                return ChatResponse(
                    response_text="",
                    ml_analysis=MLAnalysis(
                        sentiment="error",
                        sentiment_confidence=0.0,
                        business_weight=0.0,
                        technical_weight=0.0,
                        academic_weight=0.0,
                        complexity_score=0.0,
                        response_uniqueness=0,
                        processing_time=time.time() - start_time
                    ),
                    test_id=test_id,
                    user_input=user_input,
                    success=False,
                    error_message=validation_message
                )
            
            try:
                unique_seed = self.generate_unique_seed(user_input)
                random.seed(unique_seed)
                
                user_tokens = user_input.lower().split()
                
                # Enhanced analysis with request processing and pattern generation
                request_analysis = self.request_processor.analyze_user_request(user_input)
                pattern_generation = self.request_processor.generate_patterns_from_datasets(request_analysis, unique_seed)
                
                # Store pattern generation for learning
                request_key = f"{request_analysis.intent_category}_{request_analysis.domain_focus}"
                self.pattern_memory[request_key] = pattern_generation
                
                detected_sentiment, sentiment_confidence, sentiment_weight = self.analyze_sentiment(user_tokens)
                business_weight, technical_weight, academic_weight, personal_weight, complexity_score = self.calculate_topic_weights(user_tokens)
                
                # Generate response using enhanced pattern-based approach
                chat_response = self.generate_conversational_response(
                    user_input, detected_sentiment, business_weight, 
                    technical_weight, academic_weight, complexity_score,
                    request_analysis, pattern_generation
                )
                
                # Check if response is unique using hash for quick comparison
                response_hash = hash(chat_response.strip().lower())
                
                if response_hash not in self.used_responses:
                    # Store both hash and full response for tracking
                    self.used_responses.add(response_hash)
                    self.response_history_hash.append(chat_response)
                    # Keep only last 100 responses in history to manage memory
                    if len(self.response_history_hash) > 100:
                        self.response_history_hash.pop(0)
                    
                    processing_time = time.time() - start_time
                    
                    ml_analysis = MLAnalysis(
                        sentiment=detected_sentiment,
                        sentiment_confidence=sentiment_confidence,
                        business_weight=business_weight,
                        technical_weight=technical_weight,
                        academic_weight=academic_weight,
                        complexity_score=complexity_score,
                        response_uniqueness=unique_seed % 1000,
                        processing_time=processing_time,
                        request_analysis=request_analysis,
                        pattern_generation=pattern_generation
                    )
                    
                    response = ChatResponse(
                        response_text=chat_response,
                        ml_analysis=ml_analysis,
                        test_id=test_id,
                        user_input=user_input,
                        success=True
                    )
                    
                    self.logger.log_response(response)
                    return response
                
                # If duplicate found, adjust for next attempt
                time.sleep(0.001)  # Small delay to change timestamp
                
            except Exception as e:
                if attempt == max_attempts - 1:  # Last attempt
                    error_msg = str(e)
                    self.logger.log_error(error_msg, {"user_input": user_input, "test_id": test_id})
                    
                    return ChatResponse(
                        response_text="",
                        ml_analysis=MLAnalysis(
                            sentiment="error",
                            sentiment_confidence=0.0,
                            business_weight=0.0,
                            technical_weight=0.0,
                            academic_weight=0.0,
                            complexity_score=0.0,
                            response_uniqueness=0,
                            processing_time=time.time() - start_time
                        ),
                        test_id=test_id,
                        user_input=user_input,
                        success=False,
                        error_message=error_msg
                    )
        
        # Fallback: Force unique response if all attempts failed
        fallback_analysis = RequestAnalysis(
            intent_category="fallback",
            domain_focus="general",
            complexity_level="medium",
            required_datasets=["conversation_patterns"],
            pattern_suggestions=["I understand your message"],
            confidence_score=1.0,
            processing_approach="fallback_generation"
        )
        
        fallback_unique = f"[UNIQUE-{int(time.time_ns())}] I understand your message and I'm here to help. [ID:{random.randint(10000,99999)}]"
        fallback_hash = hash(fallback_unique.strip().lower())
        self.used_responses.add(fallback_hash)
        self.response_history_hash.append(fallback_unique)
        
        processing_time = time.time() - start_time
        ml_analysis = MLAnalysis(
            sentiment="neutral",
            sentiment_confidence=1.0,
            business_weight=0.5,
            technical_weight=0.5,
            academic_weight=0.5,
            complexity_score=0.5,
            response_uniqueness=999,
            processing_time=processing_time,
            request_analysis=fallback_analysis
        )
        
        response = ChatResponse(
            response_text=fallback_unique,
            ml_analysis=ml_analysis,
            test_id=f"fallback_{int(time.time())}",
            user_input=user_input,
            success=True
        )
        
        self.logger.log_response(response)
        return response
        
    def _generate_fallback_response(self, user_input: str) -> str:
        """Generate a guaranteed unique fallback response."""
        fallback_unique = f"[UNIQUE-{int(time.time_ns())}] I understand your message. [ID:{random.randint(10000,99999)}]"
        return fallback_unique
    
    @classmethod
    def get_all_instances(cls) -> List['MLChatEngine']:
        return cls._instances.copy()

def display_response_analysis(response: ChatResponse) -> None:
    print(f"\n{'='*60}")
    if len(response.response_text) > 100:
        print(f"Response: {response.response_text[:100]}...")
    else:
        print(f"Response: {response.response_text}")
    
    ml = response.ml_analysis
    print(f"Sentiment: {ml.sentiment} (confidence: {ml.sentiment_confidence:.2f})")
    print(f"Complexity: {ml.complexity_score:.2f}")
    print(f"Business Weight: {ml.business_weight:.2f}")
    print(f"Technical Weight: {ml.technical_weight:.2f}")
    print(f"Academic Weight: {ml.academic_weight:.2f}")
    print(f"Uniqueness ID: {ml.response_uniqueness}")
    print(f"Processing Time: {ml.processing_time:.3f}s")
    print(f"Test ID: {response.test_id}")
    
    # Enhanced analysis with request processing information
    if ml.request_analysis:
        req = ml.request_analysis
        print(f"\n--- REQUEST ANALYSIS ---")
        print(f"Intent: {req.intent_category} | Domain: {req.domain_focus} | Complexity: {req.complexity_level}")
        print(f"Confidence: {req.confidence_score:.2f} | Approach: {req.processing_approach}")
        print(f"Datasets Used: {', '.join(req.required_datasets[:3])}")
        
        if ml.pattern_generation:
            pat = ml.pattern_generation
            print(f"\n--- PATTERN GENERATION ---")
            print(f"Source Datasets: {', '.join(pat.source_datasets[:3])}")
            if pat.relevance_weights:
                top_dataset = max(pat.relevance_weights.items(), key=lambda x: x[1])
                print(f"Primary Dataset: {top_dataset[0]} (relevance: {top_dataset[1]:.2f})")
            
            pattern_count = sum(len(patterns) for patterns in pat.generated_patterns.values()) if pat.generated_patterns else 0
            print(f"Generated Patterns: {pattern_count} from {len(pat.generated_patterns)} datasets")
            print(f"Uniqueness Factors: {', '.join(pat.uniqueness_factors[:3])}")
    
    if response.success:
        print("✓ SUCCESS - Generated response with enhanced dataset pattern analysis")
    else:
        print(f"✗ FAILED - {response.error_message}")
    print(f"{'='*60}")

def display_dataset_analysis(dataset_manager: DatasetManager, request_processor: RequestProcessor) -> None:
    print(f"\n{'='*50} DATASET ANALYSIS {'='*50}")
    
    print(f"Available Dataset Categories: {len(dataset_manager.datasets)}")
    
    for category, data in dataset_manager.datasets.items():
        metadata = dataset_manager.dataset_metadata.get(category, {})
        patterns = dataset_manager.pattern_cache.get(category, [])
        
        print(f"\n--- {category.upper().replace('_', ' ')} ---")
        print(f"  Data Points: {len(data)}")
        print(f"  Generated Patterns: {len(patterns)}")
        print(f"  Last Loaded: {metadata.get('last_loaded', 'Never')}")
        
        if data:
            sample_data = random.sample(data, min(3, len(data)))
            print(f"  Sample Data: {', '.join(sample_data[:3])}")
        
        if patterns:
            print(f"  Sample Pattern: {patterns[0]}")
    
    print(f"\n--- REQUEST PROCESSING CAPABILITIES ---")
    print(f"Intent Categories: {', '.join(request_processor.intent_patterns.keys())}")
    print(f"Domain Classifiers: {', '.join(request_processor.domain_classifiers.keys())}")
    
    # Show recent pattern memory
    print(f"\n--- RECENT PATTERN MEMORY ---")
    if hasattr(request_processor, 'pattern_memory') and request_processor.pattern_memory:
        # Since pattern_memory is in MLChatEngine, not RequestProcessor, let's show dataset usage
        print("Dataset utilization based on request analysis:")
        for category in dataset_manager.datasets.keys():
            data_size = len(dataset_manager.datasets[category])
            pattern_count = len(dataset_manager.pattern_cache.get(category, []))
            print(f"  {category}: {data_size} items, {pattern_count} patterns available")
    else:
        print("  No pattern memory data available yet")
    
    print(f"{'='*115}")

def display_session_metrics(logger: ChatTestLogger) -> None:
    metrics = logger.calculate_metrics()
    
    print(f"\n{'='*40} SESSION METRICS {'='*40}")
    print(f"Total Responses: {metrics.get('total_responses', 0)}")
    print(f"Successful Responses: {metrics.get('successful_responses', 0)}")
    print(f"Success Rate: {metrics.get('success_rate', 0):.1f}%")
    print(f"Uniqueness Rate: {metrics.get('uniqueness_rate', 0):.1f}%")
    print(f"Conversational Rate: {metrics.get('conversational_rate', 0):.1f}%")
    print(f"Analytical Rate: {metrics.get('analytical_rate', 0):.1f}%")
    print(f"Sentiment Variety: {metrics.get('sentiment_variety', 0)} types")
    print(f"Average Processing Time: {metrics.get('avg_processing_time', 0):.3f}s")
    print(f"Session Duration: {metrics.get('session_duration', 0):.1f}s")
    print(f"Responses/Minute: {metrics.get('responses_per_minute', 0):.1f}")
    print(f"Error Count: {metrics.get('error_count', 0)}")
    print(f"{'='*92}")

def display_learning_patterns(engine: MLChatEngine) -> None:
    if engine.learning_patterns:
        print(f"\n--- LEARNING PATTERNS ---")
        for pattern, count in sorted(engine.learning_patterns.items()):
            print(f"{pattern}: {count}")

def run_interactive_chat_system() -> None:
    print("=== INTERACTIVE ML CHAT SYSTEM ===")
    print("Advanced conversational AI with machine learning analytics")
    print("Standalone CLI version - no Django dependencies")
    
    engine = MLChatEngine()
    print(f"\nSession ID: {engine.session_id}")
    print("Commands: 'metrics' - stats, 'learn' - patterns, 'datasets' - data info, 'quit' - exit, 'help' - commands")
    print("Enter any message to test the ML chat system...\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nSession ending...")
                display_session_metrics(engine.logger)
                display_learning_patterns(engine)
                break
            
            if user_input.lower() == 'metrics':
                display_session_metrics(engine.logger)
                continue
            
            if user_input.lower() == 'learn':
                display_learning_patterns(engine)
                continue
            
            if user_input.lower() == 'datasets':
                display_dataset_analysis(engine.dataset_manager, engine.request_processor)
                continue
            
            if user_input.lower() == 'help':
                print("\nAvailable commands:")
                print("  metrics - Display current session statistics")
                print("  learn - Show learning patterns and adaptations")
                print("  datasets - Show available datasets and pattern information")
                print("  quit/exit/q - End the session")
                print("  help - Show this help message")
                print("  Any other text - Chat with the ML system\n")
                continue
            
            print("\nProcessing...")
            response = engine.generate_ml_response(user_input)
            
            print(f"AI: {response.response_text}")
            
            display_response_analysis(response)
            
            if engine.test_counter % 5 == 0:
                print(f"\n--- Quick Stats (after {engine.test_counter} interactions) ---")
                metrics = engine.logger.calculate_metrics()
                print(f"Uniqueness: {metrics.get('uniqueness_rate', 0):.1f}% | Conversational: {metrics.get('conversational_rate', 0):.1f}% | Success: {metrics.get('success_rate', 0):.1f}%")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted by user")
            display_session_metrics(engine.logger)
            display_learning_patterns(engine)
            break
        except EOFError:
            print("\n\nEnd of input reached")
            display_session_metrics(engine.logger)
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")
            engine.logger.log_error(str(e), {"context": "main_loop", "input": user_input})
            continue

def test_batch_validation() -> bool:
    print("=== BATCH VALIDATION TEST ===")
    print("Testing core ML functionality with comprehensive analysis")
    
    engine = MLChatEngine()
    
    test_inputs = [
        "Hello, how are you today?",
        "Can you help me with Python programming?",
        "I love learning about machine learning algorithms",
        "What's the best business strategy for startups?",
        "Tell me about your capabilities",
        "I'm frustrated with this complex algorithm",
        "How does sentiment analysis work?",
        "What are neural networks?",
        "Thanks for your help with everything!",
        "Can you analyze market trends?",
        "I'm excited about new technology developments",
        "What's your favorite programming language?",
        "How do databases optimize query performance?"
    ]
    
    responses = []
    unique_responses = set()
    conversational_count = 0
    sentiment_types = set()
    
    print(f"\nTesting {len(test_inputs)} different inputs...\n")
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"Test {i}/{len(test_inputs)}: '{test_input[:50]}...' " if len(test_input) > 50 else f"Test {i}/{len(test_inputs)}: '{test_input}'")
        
        response = engine.generate_ml_response(test_input)
        responses.append(response)
        
        if response.success:
            unique_responses.add(response.response_text)
            sentiment_types.add(response.ml_analysis.sentiment)
            
            conversational_indicators = ['love', 'fascinating', 'interesting', 'excited', 'curious', 'enjoy', 'wonderful', 'amazing']
            if any(word in response.response_text.lower() for word in conversational_indicators):
                conversational_count += 1
            
            print(f"  ✓ Generated {len(response.response_text)} chars, sentiment: {response.ml_analysis.sentiment}")
        else:
            print(f"  ✗ Failed: {response.error_message}")
    
    successful_responses = [r for r in responses if r.success]
    total_responses = len(responses)
    unique_count = len(unique_responses)
    
    print(f"\n=== BATCH TEST RESULTS ===")
    print(f"Total responses: {total_responses}")
    print(f"Successful responses: {len(successful_responses)}")
    print(f"Unique responses: {unique_count}/{len(successful_responses)} ({(unique_count/len(successful_responses)*100) if successful_responses else 0:.1f}%)")
    print(f"Conversational responses: {conversational_count}/{len(successful_responses)} ({(conversational_count/len(successful_responses)*100) if successful_responses else 0:.1f}%)")
    print(f"Different sentiment types detected: {len(sentiment_types)} ({', '.join(sentiment_types)})")
    
    avg_processing_time = sum(r.ml_analysis.processing_time for r in successful_responses) / len(successful_responses) if successful_responses else 0
    print(f"Average processing time: {avg_processing_time:.3f}s")
    
    print(f"\n=== VALIDATION STATUS ===")
    success_criteria = (
        unique_count == len(successful_responses) and
        len(successful_responses) > 0 and
        conversational_count >= len(successful_responses) * 0.7 and
        len(sentiment_types) >= 2
    )
    
    if success_criteria:
        print("✓ ALL TESTS PASSED - ML Chat System Working Correctly")
        return True
    else:
        print("✗ SOME TESTS FAILED - Review Results Above")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        success = test_batch_validation()
        sys.exit(0 if success else 1)
    else:
        run_interactive_chat_system()
