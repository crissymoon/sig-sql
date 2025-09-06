#!/usr/bin/env python3
"""
Neural Network Moon Scripting Test
Demonstrates complex goto-based neural pathways
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import required modules directly
from language_processor import LanguageProcessor
from nosql_manager import NoSQLManager
import re

class TestNeuralAnalyzer:
    """Simplified neural analyzer for testing without external dependencies"""
    
    def __init__(self):
        self.neural_pathways = {
            'input_layer': ['data_ingestion', 'pattern_detection', 'complexity_assessment'],
            'hidden_layer_1': ['semantic_analysis', 'structural_analysis', 'context_evaluation'],
            'hidden_layer_2': ['business_classification', 'technical_classification', 'personal_classification'],
            'output_layer': ['storage_recommendation', 'confidence_calculation', 'explanation_generation']
        }
    
    def extract_neural_features(self, data, user_input):
        """Extract features that simulate neural network inputs"""
        
        features = {}
        
        # Data complexity (input layer feature)
        features['data_complexity'] = int(len(data) / 10) + len(re.findall(r'[^\w\s]', data))
        
        # Semantic analysis score
        semantic_indicators = ['define', 'explain', 'what is', 'meaning', 'description']
        features['semantic_score'] = sum(10 for indicator in semantic_indicators if indicator in user_input.lower())
        
        # Context analysis score
        context_indicators = ['store', 'save', 'analyze', 'process', 'understand']
        features['context_score'] = sum(8 for indicator in context_indicators if indicator in user_input.lower())
        
        # Business classification weights
        business_terms = ['employee', 'customer', 'revenue', 'salary', 'payroll', 'business', 'company']
        features['business_score'] = sum(15 for term in business_terms if term in data.lower() or term in user_input.lower())
        
        # Technical classification weights
        technical_terms = ['code', 'function', 'algorithm', 'database', 'api', 'system', 'programming']
        features['technical_score'] = sum(12 for term in technical_terms if term in data.lower() or term in user_input.lower())
        
        # Personal classification weights
        personal_terms = ['personal', 'private', 'my', 'purchase', 'expense', 'diary', 'note']
        features['personal_score'] = sum(10 for term in personal_terms if term in data.lower() or term in user_input.lower())
        
        return features
    
    def simulate_neural_pathways(self, features):
        """Simulate neural network pathway traversal"""
        
        pathways = ["INPUT LAYER: Data Ingestion"]
        recommendation = "Smart Storage"
        confidence = 60
        
        # Input layer processing
        if features['data_complexity'] > 50:
            pathways.append("INPUT LAYER: Deep Pattern Detection")
            pathways.append("HIDDEN LAYER 1A: Advanced Semantic Analysis")
        elif features['data_complexity'] > 20:
            pathways.append("INPUT LAYER: Medium Pattern Detection") 
            pathways.append("HIDDEN LAYER 1B: Standard Analysis")
        else:
            pathways.append("INPUT LAYER: Light Pattern Detection")
            pathways.append("HIDDEN LAYER 1C: Lightweight Analysis")
        
        # Hidden layer 2 classification
        if features['business_score'] > 30:
            pathways.append("HIDDEN LAYER 2: Business Classification")
            if features['data_complexity'] > 70:
                pathways.append("OUTPUT LAYER: Secure Enterprise Storage")
                recommendation = "Enterprise Secure Storage"
                confidence = 95
            else:
                pathways.append("OUTPUT LAYER: Business SQL Storage")
                recommendation = "Business SQL Storage"
                confidence = 85
        elif features['technical_score'] > 25:
            pathways.append("HIDDEN LAYER 2: Technical Classification")
            pathways.append("OUTPUT LAYER: Technical NoSQL Storage")
            recommendation = "Technical NoSQL Storage"
            confidence = 90
        elif features['personal_score'] > 20:
            pathways.append("HIDDEN LAYER 2: Personal Classification")
            pathways.append("OUTPUT LAYER: Personal Secure Storage")
            recommendation = "Personal Secure Storage"
            confidence = 80
        else:
            pathways.append("HIDDEN LAYER 2: Mixed Classification")
            pathways.append("OUTPUT LAYER: Balanced Storage")
            recommendation = "Balanced Storage"
            confidence = 70
        
        return {
            'pathways_traversed': pathways,
            'recommendation': recommendation,
            'confidence_score': confidence,
            'layers_activated': 4
        }
    
    def generate_moon_neural_snippet(self, features):
        """Generate a snippet of Moon neural script"""
        
        return f''':::
Neural Network Moon Script - Multi-Layer Data Processing
Input Features: {len(features)} detected
Processing Layers: 4 (Input -> Hidden1 -> Hidden2 -> Output)
:::

# Neural network state variables
input_strength = {features['data_complexity']}
semantic_weight = {features['semantic_score']}
business_weight = {features['business_score']}
technical_weight = {features['technical_score']}
personal_weight = {features['personal_score']}

p("=== Neural Network Data Processing ===")

# INPUT LAYER - Data ingestion and feature extraction
start input_layer
    p("INPUT LAYER: Processing raw data...")
    
    if input_strength > 50 then
        p("  High complexity detected -> deep processing pathway")
        goto hidden_layer_1_advanced
    else
        if input_strength > 20 then
            goto hidden_layer_1_standard
        else
            goto hidden_layer_1_simple
        end_
    end_

# HIDDEN LAYER 1 - Multiple pathways based on complexity
start hidden_layer_1_advanced
    p("HIDDEN LAYER 1A: Advanced pathway activated")
    
    if business_weight > technical_weight then
        if business_weight > personal_weight then
            goto hidden_layer_2_business
        else
            goto hidden_layer_2_personal
        end_
    else
        goto hidden_layer_2_technical
    end_

start hidden_layer_1_standard
    p("HIDDEN LAYER 1B: Standard pathway activated")
    goto hidden_layer_2_mixed

start hidden_layer_1_simple
    p("HIDDEN LAYER 1C: Simple pathway activated")
    goto output_layer_simple

# HIDDEN LAYER 2 - Classification pathways
start hidden_layer_2_business
    p("HIDDEN LAYER 2: Business classification")
    
    if input_strength > 70 then
        goto output_secure_enterprise
    else
        goto output_business_sql
    end_

start hidden_layer_2_technical
    p("HIDDEN LAYER 2: Technical classification")
    goto output_technical_nosql

start hidden_layer_2_personal
    p("HIDDEN LAYER 2: Personal classification")
    goto output_personal_secure

start hidden_layer_2_mixed
    p("HIDDEN LAYER 2: Mixed classification")
    goto output_balanced

# OUTPUT LAYER - Final recommendations
start output_secure_enterprise
    p("OUTPUT: Enterprise Secure Storage Recommended")
    confidence = 95
    goto neural_complete

start output_business_sql
    p("OUTPUT: Business SQL Storage Recommended")
    confidence = 85
    goto neural_complete

start output_technical_nosql
    p("OUTPUT: Technical NoSQL Storage Recommended")
    confidence = 90
    goto neural_complete

start output_personal_secure
    p("OUTPUT: Personal Secure Storage Recommended")
    confidence = 80
    goto neural_complete

start output_balanced
    p("OUTPUT: Balanced Storage Recommended")
    confidence = 70
    goto neural_complete

start output_layer_simple
    p("OUTPUT: Simple Storage Recommended")
    confidence = 60
    goto neural_complete

start neural_complete
    p("=== Neural Processing Complete ===")
    p("Confidence:")
    p(confidence)
    end_
'''

def test_neural_network_analysis():
    """Test the neural network-style Moon scripting"""
    
    print("Testing Neural Network Moon Scripting")
    print("=" * 50)
    
    analyzer = EnhancedMoonAnalyzer()
    
    # Test cases with different complexity levels
    test_cases = [
        {
            'name': 'Enterprise Business Data',
            'data': 'Employee ID: 12345, Salary: $85000, Department: Engineering, Revenue: $2.5M, Customer Count: 15000',
            'input': 'Store this business data securely'
        },
        {
            'name': 'Technical Programming Data', 
            'data': 'function calculateComplexity() { return algorithms.sort().filter(x => x.performance > 0.8); } API endpoints: /users, /data',
            'input': 'Analyze this code and store it'
        },
        {
            'name': 'Personal Expense Data',
            'data': 'My groceries: $150, personal note: bought organic vegetables, private expense tracking',
            'input': 'Save my personal expenses'
        },
        {
            'name': 'Mixed Complex Data',
            'data': 'Business revenue $50K, technical API system v2.3, personal reminder: call mom, employee@company.com',
            'input': 'Process this mixed data intelligently'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test_case['name']}")
        print("-" * 30)
        
        # Run neural assessment
        result = analyzer.intelligent_data_assessment(test_case['data'], test_case['input'])
        
        print(f"Neural Recommendation: {result['neural_recommendation']}")
        print(f"Confidence Score: {result['confidence_score']}%")
        print(f"Layers Activated: {result['neural_layers_activated']}/4")
        
        if result['pathways_traversed']:
            print("Neural Pathways:")
            for pathway in result['pathways_traversed']:
                print(f"  → {pathway}")
        
        if result['features_extracted']:
            features = result['features_extracted']
            print("Feature Extraction:")
            print(f"  Data Complexity: {features.get('data_complexity', 0)}")
            print(f"  Business Score: {features.get('business_score', 0)}")
            print(f"  Technical Score: {features.get('technical_score', 0)}")
            print(f"  Personal Score: {features.get('personal_score', 0)}")
        
        print()

def demonstrate_moon_neural_script():
    """Show the actual Moon script generated for neural processing"""
    
    print("\nGenerated Neural Moon Script Sample")
    print("=" * 50)
    
    analyzer = EnhancedMoonAnalyzer()
    sample_data = "Employee data: John Smith, salary $75000, department: IT, customer revenue tracking"
    sample_input = "Store this business data with high security"
    
    # Generate the neural script
    moon_script = analyzer.generate_neural_moon_script(sample_data, sample_input)
    
    # Show first 30 lines to demonstrate structure
    lines = moon_script.split('\n')
    print("Generated Moon Script (first 30 lines):")
    print("-" * 40)
    for i, line in enumerate(lines[:30], 1):
        print(f"{i:2d}: {line}")
    
    print(f"\nTotal script lines: {len(lines)}")
    print("Features: Multi-layer neural pathways, goto-based flow control")
    print("Layers: Input → Hidden1 → Hidden2 → Output")

if __name__ == "__main__":
    test_neural_network_analysis()
    demonstrate_moon_neural_script()
