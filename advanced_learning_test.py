#!/usr/bin/env python3

import json
import sqlite3
import numpy as np
from learning_test_system import AdaptiveChatSystem

class AdvancedLearningTest:
    def __init__(self):
        self.chat_system = AdaptiveChatSystem()
        self.test_iterations = 0
        self.performance_metrics = []
        
    def simulate_user_interaction(self, data, user_input, actual_preference):
        result = self.chat_system.process_interaction(data, user_input)
        
        preference_match = self.calculate_preference_match(result['storage_choice'], actual_preference)
        feedback_score = 0.3 + (preference_match * 0.7)
        success = preference_match > 0.6
        
        self.chat_system.provide_feedback(self.test_iterations + 1, feedback_score, success)
        
        self.performance_metrics.append({
            'iteration': self.test_iterations,
            'storage_choice': result['storage_choice'],
            'actual_preference': actual_preference,
            'preference_match': preference_match,
            'feedback_score': feedback_score,
            'success': success,
            'weights': result['weights_snapshot'].copy()
        })
        
        self.test_iterations += 1
        return result, feedback_score, success
    
    def calculate_preference_match(self, predicted, actual):
        mapping = {
            'enterprise_sql': ['sql', 'business', 'enterprise'],
            'technical_nosql': ['nosql', 'technical', 'code'],
            'personal_secure': ['personal', 'secure', 'private'],
            'hybrid_intelligent': ['hybrid', 'mixed', 'intelligent']
        }
        
        if actual in mapping.get(predicted, []):
            return 1.0
        
        for storage_type, keywords in mapping.items():
            if actual in keywords and storage_type != predicted:
                return 0.3
        
        return 0.1
    
    def run_continuous_learning_test(self):
        test_cases = [
            ('CREATE TABLE customers (id INT, name VARCHAR(50), revenue DECIMAL(10,2))', 'store customer data', 'sql'),
            ('def machine_learning_algorithm(data): return train_model(data)', 'save ML code', 'technical'),
            ('personal diary entry for today about family dinner', 'keep private', 'personal'),
            ('{"api_key": "secret", "database": {"host": "localhost", "port": 5432}}', 'store config', 'technical'),
            ('SELECT SUM(revenue) FROM sales WHERE quarter = 4', 'business query analysis', 'business'),
            ('my shopping list: groceries, clothes, electronics', 'private list', 'personal'),
            ('async function fetchData() { return await api.getData(); }', 'save async function', 'technical'),
            ('INSERT INTO employees (name, department, salary) VALUES ("John", "Engineering", 75000)', 'employee data', 'sql'),
            ('class DataProcessor: def __init__(self): self.data = []', 'save data class', 'technical'),
            ('personal notes about weekend plans and family activities', 'private notes', 'personal')
        ]
        
        print("Continuous Learning Test")
        print("="*60)
        
        initial_weights = self.chat_system.learning_system.weights.copy()
        print(f"Initial Weights: {initial_weights}")
        
        success_rates = []
        weight_evolution = []
        
        for i, (data, user_input, preference) in enumerate(test_cases):
            result, feedback, success = self.simulate_user_interaction(data, user_input, preference)
            
            current_weights = self.chat_system.learning_system.weights.copy()
            weight_evolution.append(current_weights)
            
            recent_successes = [m['success'] for m in self.performance_metrics[-5:]]
            success_rate = sum(recent_successes) / len(recent_successes)
            success_rates.append(success_rate)
            
            print(f"Test {i+1}: {result['storage_choice']} (wanted: {preference}) - Success: {success} - Rate: {success_rate:.2f}")
        
        self.analyze_learning_progression(success_rates, weight_evolution)
        return self.performance_metrics
    
    def analyze_learning_progression(self, success_rates, weight_evolution):
        print(f"\nLearning Analysis:")
        print(f"Initial Success Rate: {success_rates[0]:.3f}")
        print(f"Final Success Rate: {success_rates[-1]:.3f}")
        print(f"Improvement: {success_rates[-1] - success_rates[0]:.3f}")
        
        weight_stability = self.calculate_weight_stability(weight_evolution)
        print(f"Weight Stability: {weight_stability:.3f}")
        
        adaptation_speed = self.calculate_adaptation_speed(success_rates)
        print(f"Adaptation Speed: {adaptation_speed:.3f}")
        
        final_stats = self.chat_system.get_learning_stats()
        print(f"Final Average Feedback: {final_stats['avg_feedback']:.3f}")
        print(f"Total Feedback Samples: {final_stats['feedback_count']}")
    
    def calculate_weight_stability(self, weight_evolution):
        if len(weight_evolution) < 2:
            return 1.0
        
        variances = []
        for key in weight_evolution[0].keys():
            values = [w[key] for w in weight_evolution]
            variances.append(np.var(values))
        
        return 1.0 - (np.mean(variances) * 10)
    
    def calculate_adaptation_speed(self, success_rates):
        if len(success_rates) < 3:
            return 0.0
        
        improvements = []
        for i in range(1, len(success_rates)):
            improvement = success_rates[i] - success_rates[i-1]
            improvements.append(max(0, improvement))
        
        return np.mean(improvements) * 10
    
    def test_intelligent_data_selection(self):
        print(f"\nIntelligent Data Selection Test")
        print("="*40)
        
        test_data = [
            ('simple text', 'basic storage', False),
            ('complex business analytics dashboard with multiple KPIs and revenue tracking', 'enterprise solution', True),
            ('x = 5', 'store variable', False),
            ('SELECT customers.name, orders.total, products.category FROM customers JOIN orders ON customers.id = orders.customer_id JOIN products ON orders.product_id = products.id WHERE orders.date >= "2024-01-01" GROUP BY customers.name, products.category HAVING SUM(orders.total) > 1000 ORDER BY SUM(orders.total) DESC', 'complex business query', True),
        ]
        
        for data, user_input, should_learn in test_data:
            features = self.chat_system.data_selector.extract_data_features(data, user_input)
            storage_choice, score = self.chat_system.data_selector.select_storage_option(features)
            will_learn = self.chat_system.data_selector.should_store_for_learning(features, score)
            
            match = will_learn == should_learn
            print(f"Data: {data[:50]}...")
            print(f"Score: {score:.3f}, Will Learn: {will_learn}, Should Learn: {should_learn}, Match: {match}")
            
    def run_bias_weight_validation(self):
        print(f"\nBias Weight Validation")
        print("="*30)
        
        business_data = 'SELECT revenue, profit, customers FROM quarterly_business_reports WHERE year = 2024'
        technical_data = 'class NeuralNetwork: def __init__(self): self.layers = []; def train(self, data): pass'
        personal_data = 'my private diary entry about personal thoughts and family memories'
        
        business_result = self.chat_system.process_interaction(business_data, 'business analysis')
        technical_result = self.chat_system.process_interaction(technical_data, 'code storage')
        personal_result = self.chat_system.process_interaction(personal_data, 'private notes')
        
        print(f"Business Storage: {business_result['storage_choice']} (Score: {business_result['storage_score']:.3f})")
        print(f"Technical Storage: {technical_result['storage_choice']} (Score: {technical_result['storage_score']:.3f})")
        print(f"Personal Storage: {personal_result['storage_choice']} (Score: {personal_result['storage_score']:.3f})")
        
        expected_mappings = {
            business_result['storage_choice']: 'enterprise_sql',
            technical_result['storage_choice']: 'technical_nosql',
            personal_result['storage_choice']: 'personal_secure'
        }
        
        correct_predictions = sum(1 for actual, expected in expected_mappings.items() if actual == expected)
        accuracy = correct_predictions / len(expected_mappings)
        
        print(f"Bias Classification Accuracy: {accuracy:.2%}")
        return accuracy

def run_comprehensive_test():
    tester = AdvancedLearningTest()
    
    tester.run_continuous_learning_test()
    tester.test_intelligent_data_selection()
    accuracy = tester.run_bias_weight_validation()
    
    print(f"\nFinal System Performance:")
    print(f"Classification Accuracy: {accuracy:.2%}")
    print(f"Total Interactions Processed: {tester.test_iterations}")
    
    final_weights = tester.chat_system.learning_system.weights
    print(f"Learned Weight Distribution:")
    for weight_type, value in final_weights.items():
        print(f"  {weight_type}: {value:.4f}")

if __name__ == "__main__":
    run_comprehensive_test()
