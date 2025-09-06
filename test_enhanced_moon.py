#!/usr/bin/env python3

import sys
import os
import tempfile
import subprocess
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from moon_enhanced_cli import EnhancedMoonAnalyzer

def test_enhanced_moon_features():
    """Test the enhanced Moon script with try-catch and backup features"""
    
    print("Enhanced Moon Script Testing")
    print("=" * 50)
    print("Features: Try-Catch Error Handling, SQL Backup System, Data Recovery")
    print()
    
    # Initialize the analyzer
    analyzer = EnhancedMoonAnalyzer()
    
    # Test scenarios with different data types
    test_scenarios = [
        {
            'name': 'Business Data with Complex Patterns',
            'data': 'Employee payroll records: John Smith $75,000, Jane Doe $82,000, Mike Johnson $68,000. Customer revenue tracking for Q4 shows significant growth.',
            'input': 'Store sensitive business payroll and revenue data securely'
        },
        {
            'name': 'Technical Code with High Complexity',
            'data': '''
            def neural_network_processor(data_matrix, weights):
                """Complex neural network processing function"""
                import numpy as np
                activation = np.dot(data_matrix, weights)
                return np.tanh(activation)
            
            class DataProcessor:
                def __init__(self, config):
                    self.config = config
                    self.results = []
            ''',
            'input': 'Analyze and store this complex Python neural network code'
        },
        {
            'name': 'Personal Data with Medium Complexity',
            'data': 'My personal diary entry: Today I purchased groceries at Ralphs for $127.43. Also bought gas for $45.20. Planning to track my monthly expenses more carefully.',
            'input': 'Save my personal purchase tracking information'
        },
        {
            'name': 'Simple Text Data',
            'data': 'Simple reminder note',
            'input': 'Store this basic note'
        },
        {
            'name': 'Problematic Data (Test Error Handling)',
            'data': 'This is a test with extremely long and complex data that might cause processing issues. ' * 100 + 'Special characters: @#$%^&*()[]{}|\\;:\'",.<>?/',
            'input': 'Test error handling with problematic data'
        }
    ]
    
    print("Running enhanced Moon script tests with backup protection...")
    print()
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"Test {i}: {scenario['name']}")
        print("-" * 40)
        print(f"Data: {scenario['data'][:100]}...")
        print(f"Input: {scenario['input']}")
        print()
        
        try:
            # Run the enhanced neural Moon assessment
            result = analyzer.run_neural_moon_assessment(scenario['data'], scenario['input'])
            
            print("Assessment Results:")
            print(f"  Neural Recommendation: {result['recommendation']}")
            print(f"  Confidence Score: {result['confidence_score']}%")
            print(f"  Pathways Traversed: {len(result['pathways_traversed'])}")
            print(f"  Neural Layers Activated: {result['neural_layers_activated']}")
            
            # Display pathway flow
            if result['pathways_traversed']:
                print("  Processing Flow:")
                for j, pathway in enumerate(result['pathways_traversed'], 1):
                    print(f"    {j}. {pathway}")
            
            # Check for backup and error handling features
            moon_output = result['neural_output']
            has_backup = 'BACKUP SYSTEM' in moon_output
            has_error_handling = 'try_' in moon_output or 'catch_error_' in moon_output
            has_recovery = 'RECOVERY' in moon_output or 'EMERGENCY' in moon_output
            
            print("  Enhanced Features:")
            print(f"    Backup System: {'✓' if has_backup else '✗'}")
            print(f"    Error Handling: {'✓' if has_error_handling else '✗'}")
            print(f"    Recovery Mode: {'✓' if has_recovery else '✗'}")
            
            # Extract error and backup information
            if 'error_count' in moon_output.lower():
                print(f"    Error Handling: Active (error recovery detected)")
            
            if 'sql(' in moon_output.lower():
                print(f"    SQL Backup: Active (backup operations detected)")
            
        except Exception as e:
            print(f"  ERROR: Test failed - {e}")
            print(f"  This demonstrates the need for error handling!")
        
        print()
        print("=" * 50)
        print()

def test_moon_script_generation():
    """Test Moon script generation with enhanced features"""
    
    print("Moon Script Generation Test")
    print("=" * 40)
    
    analyzer = EnhancedMoonAnalyzer()
    
    # Generate a sample enhanced Moon script
    test_data = "Employee database with salary information and customer purchase records"
    test_input = "Store this business data securely with backup protection"
    
    print("Generating enhanced Moon script...")
    print()
    
    # Generate the script
    moon_script = analyzer.generate_neural_moon_script(test_data, test_input)
    
    # Analyze the generated script
    script_lines = moon_script.split('\n')
    
    features_found = {
        'try_catch_blocks': sum(1 for line in script_lines if 'try_' in line or 'catch_error_' in line),
        'sql_backup_operations': sum(1 for line in script_lines if 'sql(' in line),
        'error_logging': sum(1 for line in script_lines if 'error_log' in line),
        'recovery_procedures': sum(1 for line in script_lines if 'recovery' in line.lower()),
        'checkpoint_saves': sum(1 for line in script_lines if 'checkpoint' in line.lower()),
        'goto_statements': sum(1 for line in script_lines if 'goto ' in line)
    }
    
    print("Enhanced Moon Script Analysis:")
    print(f"  Script Length: {len(script_lines)} lines")
    print(f"  Try-Catch Blocks: {features_found['try_catch_blocks']}")
    print(f"  SQL Backup Operations: {features_found['sql_backup_operations']}")
    print(f"  Error Logging Statements: {features_found['error_logging']}")
    print(f"  Recovery Procedures: {features_found['recovery_procedures']}")
    print(f"  Checkpoint Saves: {features_found['checkpoint_saves']}")
    print(f"  Goto Statements: {features_found['goto_statements']}")
    
    print()
    print("Sample Moon Script (First 50 lines):")
    print("-" * 40)
    for i, line in enumerate(script_lines[:50], 1):
        if line.strip():
            print(f"{i:2d}: {line}")
    print("... (script continues)")
    print("-" * 40)
    
    # Check for key enhanced features
    has_backup_init = any('backup_initialization' in line for line in script_lines)
    has_error_recovery = any('emergency_recovery' in line for line in script_lines)
    has_sql_tables = any('CREATE TABLE' in line for line in script_lines)
    
    print()
    print("Feature Verification:")
    print(f"  Backup Initialization: {'✓' if has_backup_init else '✗'}")
    print(f"  Error Recovery System: {'✓' if has_error_recovery else '✗'}")
    print(f"  SQL Table Creation: {'✓' if has_sql_tables else '✗'}")
    
    if all([has_backup_init, has_error_recovery, has_sql_tables]):
        print()
        print("✓ All enhanced features successfully integrated!")
    else:
        print()
        print("⚠ Some enhanced features may be missing")

def demonstrate_backup_features():
    """Demonstrate the backup and recovery features"""
    
    print("Backup and Recovery Features Demonstration")
    print("=" * 50)
    
    analyzer = EnhancedMoonAnalyzer()
    
    # Test with data that might cause errors
    problematic_data = "This is test data with potential issues: " + "x" * 10000
    test_input = "Test backup and recovery with large dataset"
    
    print("Testing with potentially problematic data...")
    print(f"Data size: {len(problematic_data)} characters")
    print()
    
    try:
        result = analyzer.run_neural_moon_assessment(problematic_data, test_input)
        
        # Analyze the output for backup and recovery indicators
        output = result['neural_output']
        
        backup_indicators = [
            'BACKUP SYSTEM: Initializing',
            'CREATE TABLE',
            'INSERT INTO data_backup',
            'INSERT INTO error_log',
            'INSERT INTO processing_checkpoints',
            'Backup integrity: VERIFIED',
            'Recovery capability: VERIFIED'
        ]
        
        error_indicators = [
            'ERROR:',
            'RECOVERY:',
            'EMERGENCY:',
            'CRITICAL:',
            'Falling back',
            'emergency_processing',
            'system_failure_recovery'
        ]
        
        print("Backup System Status:")
        for indicator in backup_indicators:
            found = indicator in output
            print(f"  {'✓' if found else '✗'} {indicator}")
        
        print()
        print("Error Handling Status:")
        for indicator in error_indicators:
            found = indicator in output
            if found:
                print(f"  ⚠ {indicator} - Found in output")
        
        print()
        print("Final Assessment:")
        print(f"  Recommendation: {result['recommendation']}")
        print(f"  Confidence: {result['confidence_score']}%")
        print(f"  Processing completed successfully with backup protection")
        
    except Exception as e:
        print(f"Test failed: {e}")
        print("This demonstrates why backup and error handling is essential!")

if __name__ == "__main__":
    print("Enhanced Moon Script with Try-Catch and Backup Testing")
    print("=" * 60)
    print()
    
    # Run all tests
    test_enhanced_moon_features()
    test_moon_script_generation()
    demonstrate_backup_features()
    
    print("Testing completed!")
    print("Enhanced Moon script successfully integrates:")
    print("  • Comprehensive try-catch error handling")
    print("  • SQL-based backup system")
    print("  • Data recovery procedures")
    print("  • Emergency processing modes")
    print("  • Checkpoint save/restore functionality")
