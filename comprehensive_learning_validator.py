#!/usr/bin/env python3

import json
import numpy as np
import time
from learning_test_system import AdaptiveChatSystem

class ComprehensiveLearningValidator:
    def __init__(self):
        self.chat_system = AdaptiveChatSystem()
        self.validation_results = {}
        
    def test_weight_adaptation_speed(self):
        initial_weights = self.chat_system.learning_system.weights.copy()
        
        training_data = [
            ('SELECT * FROM business_analytics', 'business query', 'business'),
            ('def algorithm(): pass', 'technical code', 'technical'),
            ('my personal notes', 'private storage', 'personal')
        ] * 10
        
        weight_changes = []
        for i, (data, input_text, expected_type) in enumerate(training_data):
            self.chat_system.process_interaction(data, input_text)
            
            feedback_score = 0.9 if expected_type == 'business' else 0.8
            self.chat_system.provide_feedback(i + 1, feedback_score, True)
            
            current_weights = self.chat_system.learning_system.weights.copy()
            change = sum(abs(current_weights[k] - initial_weights[k]) for k in current_weights.keys())
            weight_changes.append(change)
        
        adaptation_speed = np.mean(np.diff(weight_changes))
        self.validation_results['adaptation_speed'] = adaptation_speed
        return adaptation_speed
    
    def test_storage_selection_accuracy(self):
        test_cases = [
            ('SELECT revenue FROM quarterly_reports', 'enterprise_sql'),
            ('class MachineLearning: def train(self): pass', 'technical_nosql'),
            ('my private diary entry about family', 'personal_secure'),
            ('{"users": [{"name": "Alice"}]}', 'technical_nosql'),
            ('CREATE INDEX idx_customer ON customers(id)', 'enterprise_sql'),
            ('personal shopping list with private items', 'personal_secure')
        ]
        
        correct_predictions = 0
        for data, expected_storage in test_cases:
            result = self.chat_system.process_interaction(data, 'store this data')
            if result['storage_choice'] == expected_storage:
                correct_predictions += 1
        
        accuracy = correct_predictions / len(test_cases)
        self.validation_results['storage_accuracy'] = accuracy
        return accuracy
    
    def test_bias_weight_distribution(self):
        current_weights = self.chat_system.learning_system.weights
        
        weight_balance = 1.0 - np.std(list(current_weights.values()))
        weight_sum = sum(current_weights.values())
        normalization_check = abs(weight_sum - 1.0) < 0.01
        
        self.validation_results['weight_balance'] = weight_balance
        self.validation_results['weight_normalization'] = normalization_check
        return weight_balance, normalization_check
    
    def test_learning_convergence(self):
        convergence_data = []
        feedback_scores = []
        
        for iteration in range(20):
            test_data = f"business data iteration {iteration}"
            result = self.chat_system.process_interaction(test_data, "business analysis")
            
            expected_score = 0.9
            actual_score = result['storage_score']
            convergence_score = 1.0 - abs(expected_score - actual_score)
            convergence_data.append(convergence_score)
            
            self.chat_system.provide_feedback(iteration + 1, expected_score, True)
            feedback_scores.append(expected_score)
        
        convergence_rate = np.mean(convergence_data[-5:]) - np.mean(convergence_data[:5])
        self.validation_results['convergence_rate'] = convergence_rate
        return convergence_rate
    
    def test_intelligent_data_filtering(self):
        test_data = [
            ('x = 1', False),
            ('complex enterprise business intelligence dashboard with multiple data sources', True),
            ('hello', False),
            ('SELECT customers.id, orders.total, products.name FROM customers JOIN orders ON customers.id = orders.customer_id JOIN products ON orders.product_id = products.id WHERE orders.date > "2024-01-01" GROUP BY customers.id HAVING SUM(orders.total) > 10000', True)
        ]
        
        correct_filtering = 0
        for data, should_learn in test_data:
            features = self.chat_system.data_selector.extract_data_features(data, "process this")
            storage_choice, score = self.chat_system.data_selector.select_storage_option(features)
            will_learn = self.chat_system.data_selector.should_store_for_learning(features, score)
            
            if will_learn == should_learn:
                correct_filtering += 1
        
        filtering_accuracy = correct_filtering / len(test_data)
        self.validation_results['filtering_accuracy'] = filtering_accuracy
        return filtering_accuracy
    
    def test_performance_metrics(self):
        start_time = time.time()
        
        for i in range(100):
            data = f"performance test data {i}"
            self.chat_system.process_interaction(data, "test performance")
        
        processing_time = time.time() - start_time
        avg_processing_time = processing_time / 100
        
        self.validation_results['avg_processing_time'] = avg_processing_time
        self.validation_results['throughput'] = 100 / processing_time
        return avg_processing_time
    
    def run_comprehensive_validation(self):
        print("Comprehensive Learning System Validation")
        print("="*60)
        
        print("\n1. Testing Weight Adaptation Speed...")
        adaptation_speed = self.test_weight_adaptation_speed()
        print(f"Adaptation Speed: {adaptation_speed:.6f}")
        
        print("\n2. Testing Storage Selection Accuracy...")
        storage_accuracy = self.test_storage_selection_accuracy()
        print(f"Storage Accuracy: {storage_accuracy:.1%}")
        
        print("\n3. Testing Bias Weight Distribution...")
        weight_balance, normalization = self.test_bias_weight_distribution()
        print(f"Weight Balance: {weight_balance:.3f}")
        print(f"Weight Normalization: {'PASS' if normalization else 'FAIL'}")
        
        print("\n4. Testing Learning Convergence...")
        convergence_rate = self.test_learning_convergence()
        print(f"Convergence Rate: {convergence_rate:.3f}")
        
        print("\n5. Testing Intelligent Data Filtering...")
        filtering_accuracy = self.test_intelligent_data_filtering()
        print(f"Filtering Accuracy: {filtering_accuracy:.1%}")
        
        print("\n6. Testing Performance Metrics...")
        avg_processing_time = self.test_performance_metrics()
        print(f"Average Processing Time: {avg_processing_time:.6f}s")
        print(f"Throughput: {self.validation_results['throughput']:.1f} requests/second")
        
        self.calculate_overall_score()
    
    def calculate_overall_score(self):
        print(f"\nOverall System Validation:")
        print("-" * 40)
        
        scores = {
            'Storage Accuracy': self.validation_results['storage_accuracy'],
            'Filtering Accuracy': self.validation_results['filtering_accuracy'],
            'Weight Balance': self.validation_results['weight_balance'],
            'Convergence Rate': max(0, self.validation_results['convergence_rate']),
            'Performance': min(1.0, 0.001 / self.validation_results['avg_processing_time'])
        }
        
        for metric, score in scores.items():
            print(f"{metric}: {score:.1%}")
        
        overall_score = np.mean(list(scores.values()))
        print(f"\nOverall System Score: {overall_score:.1%}")
        
        if overall_score >= 0.8:
            print("✓ SYSTEM VALIDATION PASSED")
        elif overall_score >= 0.6:
            print("⚠ SYSTEM VALIDATION PARTIAL")
        else:
            print("✗ SYSTEM VALIDATION FAILED")
        
        print(f"\nFinal Learning Stats:")
        final_stats = self.chat_system.get_learning_stats()
        print(f"Total Interactions: {final_stats['feedback_count']}")
        print(f"Average Feedback: {final_stats['avg_feedback']:.3f}")
        print(f"Success Rate Weight: {final_stats['current_weights']['success_rate']:.3f}")

def run_validation():
    validator = ComprehensiveLearningValidator()
    validator.run_comprehensive_validation()

if __name__ == "__main__":
    run_validation()
