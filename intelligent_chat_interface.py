#!/usr/bin/env python3

import json
import time
from learning_test_system import AdaptiveChatSystem

class IntelligentChatInterface:
    def __init__(self):
        self.chat_system = AdaptiveChatSystem()
        self.session_interactions = []
        self.user_satisfaction_threshold = 0.7
        
    def process_user_input(self, data, user_input):
        start_time = time.time()
        
        result = self.chat_system.process_interaction(data, user_input)
        
        processing_time = time.time() - start_time
        
        response = {
            'storage_recommendation': result['storage_choice'],
            'confidence_score': result['storage_score'],
            'should_learn': result['should_learn'],
            'features_analyzed': result['features'],
            'processing_time': processing_time,
            'weights_used': result['weights_snapshot']
        }
        
        self.session_interactions.append({
            'input': user_input,
            'data_length': len(data),
            'response': response,
            'timestamp': time.time()
        })
        
        return response
    
    def get_smart_recommendation(self, response):
        storage_choice = response['storage_recommendation']
        confidence = response['confidence_score']
        
        recommendations = {
            'enterprise_sql': {
                'description': 'Enterprise SQL Database',
                'best_for': 'Business data, structured queries, reporting',
                'features': ['ACID compliance', 'Complex joins', 'Business intelligence']
            },
            'technical_nosql': {
                'description': 'Technical NoSQL Storage',
                'best_for': 'Code, JSON data, flexible schemas',
                'features': ['Document storage', 'Scalability', 'Developer tools']
            },
            'personal_secure': {
                'description': 'Personal Secure Storage',
                'best_for': 'Private data, personal notes, sensitive info',
                'features': ['Encryption', 'Access control', 'Privacy protection']
            },
            'hybrid_intelligent': {
                'description': 'Hybrid Intelligent Storage',
                'best_for': 'Mixed data types, complex workflows',
                'features': ['Multi-format support', 'AI optimization', 'Adaptive indexing']
            }
        }
        
        rec = recommendations.get(storage_choice, recommendations['hybrid_intelligent'])
        
        return {
            'storage_type': rec['description'],
            'confidence': f"{confidence:.1%}",
            'recommended_for': rec['best_for'],
            'key_features': rec['features'],
            'learning_status': 'Will learn from this interaction' if response['should_learn'] else 'Standard processing'
        }
    
    def provide_user_feedback(self, interaction_index, satisfaction_rating):
        if 0 <= interaction_index < len(self.session_interactions):
            feedback_score = satisfaction_rating / 10.0
            success = feedback_score >= self.user_satisfaction_threshold
            
            self.chat_system.provide_feedback(interaction_index + 1, feedback_score, success)
            
            self.session_interactions[interaction_index]['user_feedback'] = {
                'rating': satisfaction_rating,
                'feedback_score': feedback_score,
                'success': success
            }
            
            return True
        return False
    
    def get_learning_insights(self):
        stats = self.chat_system.get_learning_stats()
        
        return {
            'current_weights': stats['current_weights'],
            'total_feedback': stats['feedback_count'],
            'average_satisfaction': stats['avg_feedback'],
            'session_interactions': len(self.session_interactions),
            'learning_efficiency': self.calculate_learning_efficiency()
        }
    
    def calculate_learning_efficiency(self):
        if len(self.session_interactions) < 2:
            return 0.0
        
        recent_interactions = self.session_interactions[-5:]
        efficiency_scores = []
        
        for interaction in recent_interactions:
            if 'user_feedback' in interaction:
                response_confidence = interaction['response']['confidence_score']
                user_satisfaction = interaction['user_feedback']['feedback_score']
                efficiency = min(1.0, response_confidence * user_satisfaction)
                efficiency_scores.append(efficiency)
        
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0.0

def run_interactive_chat():
    interface = IntelligentChatInterface()
    
    test_scenarios = [
        {
            'data': 'CREATE TABLE sales (id INT, customer_id INT, amount DECIMAL(10,2), date DATE)',
            'input': 'store this sales table structure for business reporting'
        },
        {
            'data': 'def neural_network_training(data, epochs=100): model = create_model(); return model.fit(data, epochs)',
            'input': 'save this machine learning code for later use'
        },
        {
            'data': 'personal reminder: call mom on Sunday, buy groceries, schedule dentist appointment',
            'input': 'keep this private reminder list secure'
        },
        {
            'data': '{"config": {"database": {"host": "localhost", "port": 5432}, "api": {"key": "secret", "endpoint": "https://api.example.com"}}}',
            'input': 'store this application configuration'
        }
    ]
    
    print("Intelligent Chat Interface Test")
    print("="*50)
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\nScenario {i+1}:")
        print(f"User Input: {scenario['input']}")
        print(f"Data: {scenario['data'][:80]}...")
        
        response = interface.process_user_input(scenario['data'], scenario['input'])
        recommendation = interface.get_smart_recommendation(response)
        
        print(f"Recommendation: {recommendation['storage_type']}")
        print(f"Confidence: {recommendation['confidence']}")
        print(f"Best For: {recommendation['recommended_for']}")
        print(f"Features: {', '.join(recommendation['key_features'])}")
        print(f"Learning: {recommendation['learning_status']}")
        print(f"Processing Time: {response['processing_time']:.3f}s")
        
        satisfaction = [9, 8, 9, 8][i]
        interface.provide_user_feedback(i, satisfaction)
        print(f"User Satisfaction: {satisfaction}/10")
    
    print(f"\nSession Learning Insights:")
    insights = interface.get_learning_insights()
    for key, value in insights.items():
        if key == 'current_weights':
            print(f"{key}:")
            for weight_name, weight_value in value.items():
                print(f"  {weight_name}: {weight_value:.4f}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    run_interactive_chat()
