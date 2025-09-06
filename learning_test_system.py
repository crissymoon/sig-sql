#!/usr/bin/env python3

import json
import os
import sqlite3
import numpy as np
from datetime import datetime
import pickle

class LearningWeightSystem:
    def __init__(self):
        self.weights = {
            'business': 0.33,
            'technical': 0.33,
            'personal': 0.34,
            'complexity': 0.5,
            'frequency': 0.3,
            'success_rate': 0.7,
            'user_preference': 0.8
        }
        self.bias_factors = {
            'time_decay': 0.95,
            'interaction_boost': 1.2,
            'failure_penalty': 0.8,
            'context_similarity': 1.5
        }
        self.learning_rate = 0.1
        self.interaction_history = []
        self.storage_patterns = {}
        self.user_feedback_scores = []
        
    def update_weights(self, feedback_score, context_type, storage_choice, success):
        adjustment = self.learning_rate * (feedback_score - 0.5)
        
        if context_type in self.weights:
            self.weights[context_type] += adjustment
            self.weights[context_type] = max(0.1, min(0.9, self.weights[context_type]))
        
        if success:
            self.weights['success_rate'] *= self.bias_factors['interaction_boost']
            if storage_choice in self.storage_patterns:
                self.storage_patterns[storage_choice] *= 1.1
        else:
            self.weights['success_rate'] *= self.bias_factors['failure_penalty']
            if storage_choice in self.storage_patterns:
                self.storage_patterns[storage_choice] *= 0.9
        
        self.normalize_weights()
        
    def normalize_weights(self):
        total = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] /= total
    
    def calculate_storage_score(self, data_features, storage_type):
        base_score = 0.5
        
        business_score = data_features.get('business_indicators', 0) * self.weights['business']
        technical_score = data_features.get('technical_indicators', 0) * self.weights['technical']
        personal_score = data_features.get('personal_indicators', 0) * self.weights['personal']
        complexity_score = data_features.get('complexity', 0) * self.weights['complexity']
        
        pattern_bonus = self.storage_patterns.get(storage_type, 1.0)
        
        final_score = (base_score + business_score + technical_score + 
                      personal_score + complexity_score) * pattern_bonus
        
        return min(1.0, max(0.0, final_score))
    
    def apply_time_decay(self):
        for key in self.weights:
            if key != 'user_preference':
                self.weights[key] *= self.bias_factors['time_decay']
        self.normalize_weights()

class IntelligentDataSelector:
    def __init__(self, learning_system):
        self.learning_system = learning_system
        self.data_categories = {
            'high_value': [],
            'medium_value': [],
            'low_value': [],
            'learned_patterns': []
        }
        self.selection_criteria = {
            'relevance_threshold': 0.7,
            'novelty_factor': 0.3,
            'frequency_weight': 0.4,
            'success_correlation': 0.6
        }
    
    def extract_data_features(self, data, user_input):
        features = {
            'length': len(data),
            'complexity': self.calculate_complexity(data),
            'business_indicators': self.count_business_terms(data),
            'technical_indicators': self.count_technical_terms(data),
            'personal_indicators': self.count_personal_terms(data),
            'language_diversity': self.count_languages(data),
            'structure_type': self.identify_structure(data),
            'user_intent_strength': self.analyze_intent(user_input)
        }
        return features
    
    def calculate_complexity(self, data):
        factors = [
            len(data) / 1000,
            data.count('{') + data.count('['),
            len(data.split('\n')),
            len(set(data.lower().split()))
        ]
        return min(1.0, sum(factors) / len(factors))
    
    def count_business_terms(self, data):
        business_terms = ['company', 'business', 'revenue', 'profit', 'customer', 'client', 'enterprise', 'corporate', 'sales', 'marketing']
        count = sum(1 for term in business_terms if term in data.lower())
        return min(1.0, count / 10)
    
    def count_technical_terms(self, data):
        technical_terms = ['function', 'variable', 'algorithm', 'database', 'system', 'code', 'technical', 'engineering', 'api', 'framework']
        count = sum(1 for term in technical_terms if term in data.lower())
        return min(1.0, count / 10)
    
    def count_personal_terms(self, data):
        personal_terms = ['personal', 'private', 'my', 'purchase', 'expense', 'diary', 'note', 'family', 'friend', 'home']
        count = sum(1 for term in personal_terms if term in data.lower())
        return min(1.0, count / 10)
    
    def count_languages(self, data):
        language_indicators = {
            'python': ['def ', 'import ', 'class '],
            'javascript': ['function ', 'var ', 'const '],
            'sql': ['SELECT ', 'INSERT ', 'CREATE '],
            'json': ['{', '":', 'null'],
            'csv': [',', 'header', 'row']
        }
        detected = 0
        for lang, indicators in language_indicators.items():
            if any(ind in data for ind in indicators):
                detected += 1
        return min(1.0, detected / 5)
    
    def identify_structure(self, data):
        if '{' in data and '"' in data:
            return 'json'
        elif 'SELECT' in data.upper() or 'INSERT' in data.upper():
            return 'sql'
        elif 'def ' in data or 'class ' in data:
            return 'code'
        elif ',' in data and '\n' in data:
            return 'tabular'
        else:
            return 'text'
    
    def analyze_intent(self, user_input):
        intent_keywords = {
            'store': 0.9,
            'save': 0.9,
            'analyze': 0.8,
            'process': 0.7,
            'organize': 0.8,
            'search': 0.6,
            'find': 0.6,
            'learn': 0.9
        }
        max_intent = 0
        for keyword, strength in intent_keywords.items():
            if keyword in user_input.lower():
                max_intent = max(max_intent, strength)
        return max_intent
    
    def select_storage_option(self, features):
        storage_options = {
            'enterprise_sql': {
                'business_weight': 0.9,
                'complexity_threshold': 0.7,
                'structure_types': ['sql', 'tabular']
            },
            'technical_nosql': {
                'technical_weight': 0.8,
                'structure_types': ['json', 'code'],
                'complexity_threshold': 0.6
            },
            'personal_secure': {
                'personal_weight': 0.9,
                'complexity_threshold': 0.3,
                'structure_types': ['text']
            },
            'hybrid_intelligent': {
                'language_diversity_threshold': 0.5,
                'complexity_threshold': 0.8
            }
        }
        
        best_option = 'hybrid_intelligent'
        best_score = 0
        
        for option, criteria in storage_options.items():
            score = self.learning_system.calculate_storage_score(features, option)
            
            if 'business_weight' in criteria and features['business_indicators'] >= criteria['business_weight']:
                score *= 1.3
            if 'technical_weight' in criteria and features['technical_indicators'] >= criteria['technical_weight']:
                score *= 1.3
            if 'personal_weight' in criteria and features['personal_indicators'] >= criteria['personal_weight']:
                score *= 1.3
            if 'structure_types' in criteria and features['structure_type'] in criteria['structure_types']:
                score *= 1.2
            if 'complexity_threshold' in criteria and features['complexity'] >= criteria['complexity_threshold']:
                score *= 1.1
            if 'language_diversity_threshold' in criteria and features['language_diversity'] >= criteria['language_diversity_threshold']:
                score *= 1.2
            
            if score > best_score:
                best_score = score
                best_option = option
        
        return best_option, best_score
    
    def should_store_for_learning(self, features, storage_score):
        if storage_score >= self.selection_criteria['relevance_threshold']:
            return True
        if features['user_intent_strength'] >= 0.8:
            return True
        if features['complexity'] >= 0.7 and features['language_diversity'] >= 0.4:
            return True
        return False

class AdaptiveChatSystem:
    def __init__(self):
        self.learning_system = LearningWeightSystem()
        self.data_selector = IntelligentDataSelector(self.learning_system)
        self.conversation_context = []
        self.learning_database = "adaptive_learning.db"
        self.setup_database()
    
    def setup_database(self):
        conn = sqlite3.connect(self.learning_database)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                user_input TEXT,
                data_features TEXT,
                storage_choice TEXT,
                storage_score REAL,
                user_feedback REAL,
                success INTEGER
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY,
                pattern_type TEXT,
                pattern_data TEXT,
                effectiveness_score REAL,
                usage_count INTEGER,
                last_updated TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def process_interaction(self, data, user_input):
        features = self.data_selector.extract_data_features(data, user_input)
        storage_choice, storage_score = self.data_selector.select_storage_option(features)
        
        should_learn = self.data_selector.should_store_for_learning(features, storage_score)
        
        interaction_result = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'storage_choice': storage_choice,
            'storage_score': storage_score,
            'should_learn': should_learn,
            'weights_snapshot': self.learning_system.weights.copy()
        }
        
        if should_learn:
            self.store_learning_data(interaction_result, data, user_input)
        
        return interaction_result
    
    def store_learning_data(self, interaction_result, data, user_input):
        conn = sqlite3.connect(self.learning_database)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interactions 
            (timestamp, user_input, data_features, storage_choice, storage_score, user_feedback, success)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            interaction_result['timestamp'],
            user_input,
            json.dumps(interaction_result['features']),
            interaction_result['storage_choice'],
            interaction_result['storage_score'],
            0.5,
            1
        ))
        conn.commit()
        conn.close()
    
    def provide_feedback(self, interaction_id, feedback_score, success):
        self.learning_system.user_feedback_scores.append(feedback_score)
        
        conn = sqlite3.connect(self.learning_database)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT storage_choice, data_features FROM interactions WHERE id = ?
        ''', (interaction_id,))
        result = cursor.fetchone()
        
        if result:
            storage_choice, features_json = result
            features = json.loads(features_json)
            context_type = self.determine_context_type(features)
            
            self.learning_system.update_weights(feedback_score, context_type, storage_choice, success)
            
            cursor.execute('''
                UPDATE interactions SET user_feedback = ?, success = ? WHERE id = ?
            ''', (feedback_score, 1 if success else 0, interaction_id))
        
        conn.commit()
        conn.close()
    
    def determine_context_type(self, features):
        scores = {
            'business': features['business_indicators'],
            'technical': features['technical_indicators'],
            'personal': features['personal_indicators']
        }
        return max(scores, key=scores.get)
    
    def get_learning_stats(self):
        return {
            'current_weights': self.learning_system.weights,
            'bias_factors': self.learning_system.bias_factors,
            'storage_patterns': self.learning_system.storage_patterns,
            'feedback_count': len(self.learning_system.user_feedback_scores),
            'avg_feedback': np.mean(self.learning_system.user_feedback_scores) if self.learning_system.user_feedback_scores else 0
        }

def run_learning_test():
    chat_system = AdaptiveChatSystem()
    
    test_scenarios = [
        {
            'data': 'SELECT revenue, profit FROM quarterly_reports WHERE year = 2024 ORDER BY quarter',
            'user_input': 'store this business query for quarterly analysis',
            'expected_feedback': 0.9
        },
        {
            'data': 'def calculate_fibonacci(n): return n if n <= 1 else calculate_fibonacci(n-1) + calculate_fibonacci(n-2)',
            'user_input': 'save this algorithm for learning purposes',
            'expected_feedback': 0.8
        },
        {
            'data': 'my personal grocery list: milk, bread, eggs, cheese, apples',
            'user_input': 'keep this private shopping list',
            'expected_feedback': 0.7
        },
        {
            'data': '{"users": [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "user"}]}',
            'user_input': 'process this user configuration data',
            'expected_feedback': 0.85
        }
    ]
    
    print("Learning System Test Results")
    print("="*50)
    
    interaction_ids = []
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\nScenario {i+1}:")
        
        result = chat_system.process_interaction(scenario['data'], scenario['user_input'])
        
        print(f"Storage Choice: {result['storage_choice']}")
        print(f"Storage Score: {result['storage_score']:.3f}")
        print(f"Should Learn: {result['should_learn']}")
        print(f"Features: {result['features']}")
        
        interaction_ids.append(i+1)
        chat_system.provide_feedback(i+1, scenario['expected_feedback'], True)
    
    print("\nLearning Stats After Feedback:")
    stats = chat_system.get_learning_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\nTesting Weight Adaptation:")
    
    for i in range(3):
        chat_system.learning_system.apply_time_decay()
        new_result = chat_system.process_interaction(
            test_scenarios[0]['data'], 
            test_scenarios[0]['user_input']
        )
        print(f"Iteration {i+1} - Storage Score: {new_result['storage_score']:.3f}")
    
    final_stats = chat_system.get_learning_stats()
    print(f"\nFinal Weights: {final_stats['current_weights']}")

if __name__ == "__main__":
    run_learning_test()
