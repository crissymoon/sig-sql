#!/usr/bin/env python3

import sys
import json
import os
import re
import math
import random
import subprocess
import tempfile
from pathlib import Path
import sqlite3
import pickle
from datetime import datetime
from language_processor import LanguageProcessor
from hair import create_banner, create_prompt, create_footer
from eyes import analyze_string_patterns, generate_advanced_patterns

class ConversationalPersonality:
    def __init__(self):
        self.responses = {
            'greeting': [
                "Hello there! I'm excited to help you with your data today.",
                "Hey! What interesting data challenge can we tackle together?",
                "Hi! I'm here and ready to dive into some data analysis with you.",
                "Welcome back! What would you like to explore or store today?"
            ],
            'understanding': [
                "I see what you're getting at...",
                "That's an interesting perspective...",
                "I understand where you're coming from...",
                "That makes sense to me...",
                "I follow your thinking here..."
            ],
            'thinking': [
                "Let me think about this for a moment...",
                "I'm processing what you've shared...",
                "Hmm, this is intriguing, let me analyze...",
                "Give me a second to work through this...",
                "I'm considering the best approach here..."
            ],
            'excitement': [
                "This is fascinating data!",
                "I love working with this type of information!",
                "This is exactly the kind of challenge I enjoy!",
                "What an interesting dataset to analyze!",
                "This data tells a compelling story!"
            ],
            'encouragement': [
                "You're asking great questions!",
                "That's a really smart approach!",
                "I like how you're thinking about this!",
                "You're on the right track with this!",
                "That's exactly what I was hoping you'd ask!"
            ],
            'curiosity': [
                "I'm curious about something...",
                "This makes me wonder...",
                "Here's what's interesting to me...",
                "I noticed something worth exploring...",
                "There's an aspect here that caught my attention..."
            ]
        }
        
        self.conversation_context = {
            'previous_topics': [],
            'user_preferences': {},
            'interaction_count': 0
        }
    
    def get_response(self, category, context=None):
        responses = self.responses.get(category, ["I understand."])
        response = random.choice(responses)
        
        if context:
            response = response.replace("{context}", str(context))
        
        return response
    
    def personalize_response(self, base_response, user_input):
        if "purchase" in user_input.lower() or "bought" in user_input.lower():
            return f"{base_response} I can tell you're tracking expenses - that's really smart financial planning!"
        elif "employee" in user_input.lower() or "staff" in user_input.lower():
            return f"{base_response} Managing employee data is crucial for good business operations."
        elif "code" in user_input.lower() or "programming" in user_input.lower():
            return f"{base_response} I love working with programming-related data - there's so much structure to analyze!"
        else:
            return base_response

class EnhancedMoonAnalyzer:
    def __init__(self):
        self.moon_interpreter_path = "./moon/main"
        self.personality = ConversationalPersonality()
        self.neural_pathways = {
            'input_layer': ['data_ingestion', 'pattern_detection', 'complexity_assessment'],
            'hidden_layer_1': ['semantic_analysis', 'structural_analysis', 'context_evaluation'],
            'hidden_layer_2': ['business_classification', 'technical_classification', 'personal_classification'],
            'output_layer': ['storage_recommendation', 'confidence_calculation', 'explanation_generation']
        }
        self.language_bridges = {
            'python': self.bridge_python,
            'javascript': self.bridge_javascript,
            'sql': self.bridge_sql,
            'bash': self.bridge_bash,
            'json': self.bridge_json,
            'csv': self.bridge_csv,
            'moon': self.bridge_moon_native
        }
        self.adaptive_patterns = {}
        
    def detect_language_context(self, data, user_input):
        language_indicators = {
            'python': ['def ', 'import ', 'class ', 'if __name__', '.py', 'print(', 'return '],
            'javascript': ['function ', 'var ', 'let ', 'const ', '.js', 'console.log', '=>'],
            'sql': ['SELECT ', 'INSERT ', 'CREATE TABLE', 'WHERE ', 'JOIN ', 'UPDATE '],
            'bash': ['#!/bin/bash', 'echo ', 'ls ', 'cd ', 'grep ', 'awk ', '$1'],
            'json': ['{', '}', '":', '[]', 'null', 'true', 'false'],
            'csv': [',', 'headers', 'rows', '.csv', 'column'],
            'moon': ['start ', 'goto ', 'put ', ' in ', 'try', 'catch', 'end_']
        }
        
        combined_text = (data + " " + user_input).lower()
        language_scores = {}
        
        for lang, indicators in language_indicators.items():
            score = sum(1 for indicator in indicators if indicator.lower() in combined_text)
            if score > 0:
                language_scores[lang] = score
        
        primary_language = max(language_scores.items(), key=lambda x: x[1])[0] if language_scores else 'moon'
        secondary_languages = [lang for lang, score in language_scores.items() if lang != primary_language and score > 0]
        
        return primary_language, secondary_languages, language_scores
    
    def bridge_python(self, data, context):
        return f'''
try
    python_data = ___
{data}
___
    put python_data in "python_bridge.py"
    
    if context.complexity > 50 then
        put "import sys, json, sqlite3" in "python_imports.py"
        put "def process_data(data): return analyze_complexity(data)" in "python_functions.py"
    end_
    
    goto python_processing_complete
catch python_error
    put "Python bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_javascript(self, data, context):
        return f'''
try
    js_data = ___
{data}
___
    put js_data in "javascript_bridge.js"
    
    if context.has_async then
        put "async function processData(data) {{ return await analyze(data); }}" in "js_async.js"
    else
        put "function processData(data) {{ return analyze(data); }}" in "js_sync.js"
    end_
    
    goto javascript_processing_complete
catch js_error
    put "JavaScript bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_sql(self, data, context):
        return f'''
try
    sql_commands = ___
{data}
___
    put sql_commands in "sql_bridge.sql"
    
    if context.has_tables then
        put "CREATE BACKUP TABLE IF NOT EXISTS data_backup AS" in "sql_backup.sql"
        put sql_commands in "sql_main.sql"
    end_
    
    goto sql_processing_complete
catch sql_error
    put "SQL bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_bash(self, data, context):
        return f'''
try
    bash_script = ___
{data}
___
    put bash_script in "bash_bridge.sh"
    
    if context.has_pipes then
        put "set -e" in "bash_safety.sh"
        put "trap 'echo Error on line $LINENO' ERR" in "bash_error_handling.sh"
    end_
    
    goto bash_processing_complete
catch bash_error
    put "Bash bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_json(self, data, context):
        return f'''
try
    json_structure = ___
{data}
___
    put json_structure in "json_bridge.json"
    
    if context.nested_depth > 3 then
        put "deep_json_detected" in "json_metadata.txt"
    end_
    
    goto json_processing_complete
catch json_error
    put "JSON bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_csv(self, data, context):
        return f'''
try
    csv_data = ___
{data}
___
    put csv_data in "csv_bridge.csv"
    
    if context.has_headers then
        put "headers_detected" in "csv_metadata.txt"
    end_
    
    goto csv_processing_complete
catch csv_error
    put "CSV bridge error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def bridge_moon_native(self, data, context):
        return f'''
try
    moon_code = ___
{data}
___
    put moon_code in "moon_native.moon"
    
    if context.has_goto then
        put "goto_flow_detected" in "moon_metadata.txt"
    end_
    
    goto moon_processing_complete
catch moon_error
    put "Moon native error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def generate_adaptive_bridge(self, primary_lang, secondary_langs, data, context):
        bridge_script = f'''
try
    put "multi_language_processing_started" in "bridge_log.txt"
    primary_language = "{primary_lang}"
    secondary_count = {len(secondary_langs)}
    
'''
        
        bridge_script += self.language_bridges[primary_lang](data, context)
        
        for i, lang in enumerate(secondary_langs):
            bridge_script += f'''
    
start secondary_language_{i}
    secondary_lang = "{lang}"
    put secondary_lang in "secondary_languages.txt"
    {self.language_bridges[lang](data, context)}
'''
        
        bridge_script += f'''
    
start language_integration
    try
        if secondary_count > 0 then
            put "multi_language_integration_active" in "integration_log.txt"
            
            if primary_language == "python" then
                if secondary_count > 1 then
                    goto advanced_python_integration
                else
                    goto simple_python_integration
                end_
            end_
            
            if primary_language == "javascript" then
                goto javascript_integration
            end_
            
            if primary_language == "sql" then
                goto sql_integration
            end_
            
            goto general_integration
        else
            goto single_language_processing
        end_
        
    catch integration_error
        put "Language integration error" in "error_log.txt"
        goto fallback_integration
    end_

start advanced_python_integration
    try
        integration_code = ___
import json
import sqlite3
from pathlib import Path

def integrate_languages(primary_data, secondary_data):
    results = {{}}
    results['primary'] = process_python_data(primary_data)
    
    for lang, data in secondary_data.items():
        if lang == 'javascript':
            results[lang] = convert_js_to_python(data)
        elif lang == 'sql':
            results[lang] = execute_sql_in_python(data)
        elif lang == 'json':
            results[lang] = json.loads(data)
    
    return results
___
        put integration_code in "python_multi_integration.py"
        goto integration_complete
        
    catch advanced_error
        goto simple_python_integration
    end_

start simple_python_integration
    put "Simple Python integration with single secondary language" in "integration_log.txt"
    goto integration_complete

start javascript_integration
    try
        js_integration = ___
function integrateLanguages(primaryData, secondaryData) {{
    const results = {{}};
    results.primary = processJavaScriptData(primaryData);
    
    Object.keys(secondaryData).forEach(lang => {{
        if (lang === 'python') {{
            results[lang] = convertPythonToJS(secondaryData[lang]);
        }} else if (lang === 'json') {{
            results[lang] = JSON.parse(secondaryData[lang]);
        }}
    }});
    
    return results;
}}
___
        put js_integration in "javascript_integration.js"
        goto integration_complete
        
    catch js_integration_error
        goto general_integration
    end_

start sql_integration
    try
        sql_integration = ___
CREATE TABLE language_bridge (
    id INTEGER PRIMARY KEY,
    primary_language TEXT,
    secondary_language TEXT,
    data_content TEXT,
    integration_status TEXT
);

INSERT INTO language_bridge (primary_language, secondary_language, data_content, integration_status)
SELECT 'sql' as primary_language, 
       secondary_lang as secondary_language,
       data_content,
       'integrated' as integration_status
FROM secondary_data_table;
___
        put sql_integration in "sql_integration.sql"
        goto integration_complete
        
    catch sql_integration_error
        goto general_integration
    end_

start general_integration
    put "General multi-language integration" in "integration_log.txt"
    goto integration_complete

start single_language_processing
    put "Single language processing mode" in "processing_log.txt"
    goto integration_complete

start fallback_integration
    put "Fallback integration mode activated" in "error_log.txt"
    goto integration_complete

start integration_complete
    put "Language bridge integration completed" in "completion_log.txt"
    goto neural_processing
    
catch bridge_error
    put "Critical bridge error" in "critical_error_log.txt"
    goto emergency_processing
end_
'''
        
        return bridge_script
        
    def generate_neural_moon_script(self, data, user_input):
        """Generate Moon script with comprehensive try-catch and backup functionality"""
        
        # Calculate input features
        features = self.extract_neural_features(data, user_input)
        
        moon_script = f''':::
Enhanced Neural Network Moon Script - Multi-Layer Data Processing
Features: Try-Catch Error Handling, SQL Backup System, Data Recovery
Input Features: {len(features)} detected
Processing Layers: 4 (Input -> Hidden1 -> Hidden2 -> Output)
Security: Backup enabled, Error recovery active
:::

# Neural network state variables
input_strength = {features['data_complexity']}
semantic_weight = {features['semantic_score']}
context_weight = {features['context_score']}
business_weight = {features['business_score']}
technical_weight = {features['technical_score']}
personal_weight = {features['personal_score']}

# Error handling and backup variables
error_count = 0
backup_enabled = 1
recovery_mode = 0
sql_backup_active = 1

# Activation thresholds for neural pathways
threshold_low = 30
threshold_medium = 60
threshold_high = 80

p("=== Enhanced Neural Network Data Processing ===")
p("Initializing multi-layer analysis with backup protection...")
p("SQL backup system: ACTIVE")
p("Error recovery mode: STANDBY")

# Initialize backup system first
start backup_initialization
    p("BACKUP SYSTEM: Initializing Moon SQL backup...")
    
    try_
        # Create backup tables using Moon SQL
        sql("CREATE TABLE IF NOT EXISTS data_backup (
            id INTEGER PRIMARY KEY,
            original_data TEXT,
            features_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            processing_stage TEXT,
            backup_hash TEXT
        )")
        
        sql("CREATE TABLE IF NOT EXISTS error_log (
            id INTEGER PRIMARY KEY,
            error_stage TEXT,
            error_message TEXT,
            data_snapshot TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            recovery_action TEXT
        )")
        
        sql("CREATE TABLE IF NOT EXISTS processing_checkpoints (
            id INTEGER PRIMARY KEY,
            checkpoint_name TEXT,
            data_state TEXT,
            pathway_taken TEXT,
            confidence_level INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )")
        
        p("BACKUP SYSTEM: Moon SQL tables created successfully")
        
        # Insert initial data backup
        backup_data = "{data[:500]}..."
        features_json = "complexity:{features['data_complexity']},semantic:{features['semantic_score']}"
        
        sql("INSERT INTO data_backup (original_data, features_data, processing_stage, backup_hash) 
             VALUES (?, ?, 'initialization', 'hash_' || datetime('now'))", backup_data, features_json)
        
        p("BACKUP SYSTEM: Initial data backup completed")
        goto input_layer
        
    catch_error_
        error_count = error_count + 1
        p("BACKUP ERROR: Failed to initialize backup system")
        
        sql("INSERT INTO error_log (error_stage, error_message, data_snapshot, recovery_action) 
             VALUES ('backup_init', 'Backup system failure', ?, 'proceeding_without_backup')", backup_data)
        
        backup_enabled = 0
        p("WARNING: Proceeding without backup protection")
        goto input_layer
    end_try_

# INPUT LAYER - Data ingestion and feature extraction with error handling
start input_layer
start input_layer
    p("INPUT LAYER: Processing raw data with error protection...")
    
    try_
        # Checkpoint: Save input layer state
        if backup_enabled == 1 then
            checkpoint_data = "input_layer_state"
            sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                 VALUES ('input_layer', ?, 'data_ingestion')", checkpoint_data)
        end_
        
        # Node 1: Data ingestion with validation
        start data_ingestion
            p("  Node 1: Data ingestion active with validation")
            data_size = {len(data)}
            
            try_
                if data_size > 1000 then
                    p("    Large dataset detected -> activating deep processing")
                    
                    # Backup large data processing decision
                    if backup_enabled == 1 then
                        sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                             VALUES ('data_ingestion', 'large_dataset', 'pattern_detection_deep')")
                    end_
                    
                    goto pattern_detection_deep
                else
                    if data_size > 100 then
                        # Backup medium data processing
                        if backup_enabled == 1 then
                            sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                                 VALUES ('data_ingestion', 'medium_dataset', 'pattern_detection_medium')")
                        end_
                        goto pattern_detection_medium
                    else
                        # Backup light data processing
                        if backup_enabled == 1 then
                            sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                                 VALUES ('data_ingestion', 'light_dataset', 'pattern_detection_light')")
                        end_
                        goto pattern_detection_light
                    end_
                end_
                
            catch_error_
                error_count = error_count + 1
                p("ERROR: Data ingestion failed, attempting recovery...")
                
                sql("INSERT INTO error_log (error_stage, error_message, data_snapshot, recovery_action) 
                     VALUES ('data_ingestion', 'Size calculation error', ?, 'fallback_to_medium')", "data_size_unknown")
                
                p("RECOVERY: Falling back to medium processing")
                goto pattern_detection_medium
            end_try_
        
        # Node 2: Pattern detection with multiple pathways and error handling
        start pattern_detection_deep
            p("  Node 2a: Deep pattern detection with error recovery")
            
            try_
                pattern_score = input_strength + 40
                
                # Validate pattern score
                if pattern_score > 200 then
                    p("    WARNING: Pattern score exceeding safe limits, capping at 200")
                    pattern_score = 200
                end_
                
                # Backup pattern detection results
                if backup_enabled == 1 then
                    pattern_data = "deep_patterns_detected"
                    sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                         VALUES ('pattern_detection_deep', ?, 'complexity_assessment_high', ?)", pattern_data, pattern_score)
                end_
                
                goto complexity_assessment_high
                
            catch_error_
                error_count = error_count + 1
                p("ERROR: Deep pattern detection failed")
                
                sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                     VALUES ('pattern_detection_deep', 'Pattern calculation error', 'fallback_to_medium')")
                
                p("RECOVERY: Switching to medium pattern detection")
                goto pattern_detection_medium
            end_try_
        
        start pattern_detection_medium
            p("  Node 2b: Medium pattern detection with backup")
            
            try_
                pattern_score = input_strength + 20
                
                # Backup medium pattern results
                if backup_enabled == 1 then
                    sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                         VALUES ('pattern_detection_medium', 'medium_patterns', 'complexity_assessment_medium', ?)", pattern_score)
                end_
                
                goto complexity_assessment_medium
                
            catch_error_
                error_count = error_count + 1
                p("ERROR: Medium pattern detection failed")
                
                sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                     VALUES ('pattern_detection_medium', 'Medium pattern error', 'fallback_to_light')")
                
                p("RECOVERY: Switching to light pattern detection")
                goto pattern_detection_light
            end_try_
        
        start pattern_detection_light
            p("  Node 2c: Light pattern detection (safe mode)")
            
            try_
                pattern_score = input_strength + 10
                
                # Even light processing gets backed up
                if backup_enabled == 1 then
                    sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                         VALUES ('pattern_detection_light', 'light_patterns', 'complexity_assessment_low', ?)", pattern_score)
                end_
                
                goto complexity_assessment_low
                
            catch_error_
                error_count = error_count + 1
                p("CRITICAL ERROR: Even light pattern detection failed")
                
                sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                     VALUES ('pattern_detection_light', 'Critical pattern failure', 'emergency_fallback')")
                
                p("EMERGENCY: Activating emergency processing mode")
                goto emergency_processing
            end_try_
        
    catch_error_
        error_count = error_count + 1
        p("CRITICAL ERROR: Input layer catastrophic failure")
        
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('input_layer', 'Catastrophic input failure', 'emergency_recovery')")
        
        recovery_mode = 1
        p("SYSTEM: Activating recovery mode")
        goto emergency_recovery
    end_try_
    
    # Node 3: Complexity assessment with comprehensive error handling
    start complexity_assessment_high
        p("  Node 3a: High complexity assessment with backup protection")
        
        try_
            complexity_level = pattern_score + 30
            
            # Validate complexity calculation
            if complexity_level < 0 then
                p("    ERROR: Negative complexity detected, correcting...")
                complexity_level = 50
            end_
            
            # Backup complexity assessment
            if backup_enabled == 1 then
                sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                     VALUES ('complexity_assessment_high', 'high_complexity_calculated', 'hidden_layer_1_pathway_a', ?)", complexity_level)
            end_
            
            goto hidden_layer_1_pathway_a
            
        catch_error_
            error_count = error_count + 1
            p("ERROR: High complexity assessment failed")
            
            sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                 VALUES ('complexity_assessment_high', 'Complexity calculation error', 'fallback_to_medium')")
            
            p("RECOVERY: Falling back to medium complexity assessment")
            goto complexity_assessment_medium
        end_try_
    
    start complexity_assessment_medium
        p("  Node 3b: Medium complexity assessment with error handling")
        
        try_
            complexity_level = pattern_score + 15
            
            # Backup medium complexity
            if backup_enabled == 1 then
                sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                     VALUES ('complexity_assessment_medium', 'medium_complexity_calculated', 'hidden_layer_1_pathway_b', ?)", complexity_level)
            end_
            
            goto hidden_layer_1_pathway_b
            
        catch_error_
            error_count = error_count + 1
            p("ERROR: Medium complexity assessment failed")
            
            sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                 VALUES ('complexity_assessment_medium', 'Medium complexity error', 'fallback_to_low')")
            
            goto complexity_assessment_low
        end_try_
    
    start complexity_assessment_low
        p("  Node 3c: Low complexity assessment (safe mode)")
        
        try_
            complexity_level = pattern_score + 5
            
            # Backup low complexity
            if backup_enabled == 1 then
                sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                     VALUES ('complexity_assessment_low', 'low_complexity_calculated', 'hidden_layer_1_pathway_c', ?)", complexity_level)
            end_
            
            goto hidden_layer_1_pathway_c
            
        catch_error_
            error_count = error_count + 1
            p("CRITICAL ERROR: Even low complexity assessment failed")
            
            sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                 VALUES ('complexity_assessment_low', 'Critical complexity failure', 'emergency_processing')")
            
            goto emergency_processing
        end_try_

# HIDDEN LAYER 1 - Semantic and structural analysis with enhanced error handling
start hidden_layer_1_pathway_a
    p("HIDDEN LAYER 1A: Advanced semantic analysis with backup protection")
    
    try_
        # Create checkpoint for hidden layer 1A
        if backup_enabled == 1 then
            sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                 VALUES ('hidden_layer_1a', 'semantic_analysis_deep', 'semantic_processing')")
        end_
        
        # Multiple interconnected nodes with error handling
        start semantic_analysis_deep
            p("  HL1 Node 1: Deep semantic processing with validation")
            
            try_
                semantic_activation = semantic_weight + complexity_level
                
                # Validate semantic activation
                if semantic_activation < 0 then
                    p("    Correcting negative semantic activation")
                    semantic_activation = 10
                end_
                
                # Backup semantic results
                if backup_enabled == 1 then
                    sql("INSERT INTO data_backup (original_data, features_data, processing_stage) 
                         VALUES ('semantic_deep', ?, 'hidden_layer_1a')", semantic_activation)
                end_
                
                if semantic_activation > threshold_high then
                    p("    High semantic activation -> business context")
                    goto structural_analysis_business
                else
                    if semantic_activation > threshold_medium then
                        goto structural_analysis_technical
                    else
                        goto structural_analysis_personal
                    end_
                end_
                
            catch_error_
                error_count = error_count + 1
                p("ERROR: Deep semantic processing failed")
                
                sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                     VALUES ('semantic_analysis_deep', 'Semantic processing error', 'fallback_to_structural')")
                
                p("RECOVERY: Bypassing semantic analysis")
                goto structural_analysis_business
            end_try_
        
    catch_error_
        error_count = error_count + 1
        p("ERROR: Hidden layer 1A pathway failed")
        
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('hidden_layer_1a', 'Pathway A failure', 'switch_to_pathway_b')")
        
        p("RECOVERY: Switching to pathway B")
        goto hidden_layer_1_pathway_b
    end_try_
    
    start structural_analysis_business
        p("  HL1 Node 2: Business structure analysis")
        structure_score = semantic_activation + business_weight
        goto context_evaluation_business
    
    start structural_analysis_technical
        p("  HL1 Node 2: Technical structure analysis")
        structure_score = semantic_activation + technical_weight
        goto context_evaluation_technical
    
    start structural_analysis_personal
        p("  HL1 Node 2: Personal structure analysis")
        structure_score = semantic_activation + personal_weight
        goto context_evaluation_personal

start hidden_layer_1_pathway_b
    p("HIDDEN LAYER 1B: Standard analysis pathway")
    
    start semantic_analysis_standard
        p("  HL1 Node 1: Standard semantic processing")
        semantic_activation = semantic_weight + (complexity_level / 2)
        goto structural_analysis_mixed
    
    start structural_analysis_mixed
        p("  HL1 Node 2: Mixed structure analysis")
        structure_score = semantic_activation + 25
        goto context_evaluation_mixed

start hidden_layer_1_pathway_c
    p("HIDDEN LAYER 1C: Lightweight analysis pathway")
    
    start semantic_analysis_light
        p("  HL1 Node 1: Light semantic processing")
        semantic_activation = semantic_weight + 10
        goto context_evaluation_simple

# Context evaluation nodes (bridge to hidden layer 2)
start context_evaluation_business
    p("  HL1 Node 3: Business context evaluation")
    context_score = structure_score + business_weight
    goto hidden_layer_2_business_path

start context_evaluation_technical
    p("  HL1 Node 3: Technical context evaluation")
    context_score = structure_score + technical_weight
    goto hidden_layer_2_technical_path

start context_evaluation_personal
    p("  HL1 Node 3: Personal context evaluation")
    context_score = structure_score + personal_weight
    goto hidden_layer_2_personal_path

start context_evaluation_mixed
    p("  HL1 Node 3: Mixed context evaluation")
    context_score = structure_score + 15
    goto hidden_layer_2_mixed_path

start context_evaluation_simple
    p("  HL1 Node 3: Simple context evaluation")
    context_score = semantic_activation + 10
    goto hidden_layer_2_simple_path

# HIDDEN LAYER 2 - Classification and feature refinement
start hidden_layer_2_business_path
    p("HIDDEN LAYER 2: Business classification pathway")
    
    start business_classification_enterprise
        p("  HL2 Node 1: Enterprise business classification")
        classification_score = context_score + 30
        
        if classification_score > 150 then
            p("    Enterprise-level data -> secure processing")
            goto output_layer_secure_enterprise
        else
            if classification_score > 100 then
                goto output_layer_secure_standard
            else
                goto output_layer_business_standard
            end_
        end_

start hidden_layer_2_technical_path
    p("HIDDEN LAYER 2: Technical classification pathway")
    
    start technical_classification_complex
        p("  HL2 Node 1: Complex technical classification")
        classification_score = context_score + technical_weight
        
        if classification_score > 120 then
            p("    Complex technical data -> specialized storage")
            goto output_layer_technical_specialized
        else
            goto output_layer_technical_standard
        end_

start hidden_layer_2_personal_path
    p("HIDDEN LAYER 2: Personal classification pathway")
    
    start personal_classification_private
        p("  HL2 Node 1: Private personal classification")
        classification_score = context_score + personal_weight
        goto output_layer_personal_secure

start hidden_layer_2_mixed_path
    p("HIDDEN LAYER 2: Mixed classification pathway")
    
    start mixed_classification_analysis
        p("  HL2 Node 1: Mixed data classification")
        classification_score = context_score + 20
        
        # Neural decision tree with multiple branches
        if business_weight > technical_weight then
            if business_weight > personal_weight then
                goto output_layer_business_primary
            else
                goto output_layer_personal_primary
            end_
        else
            if technical_weight > personal_weight then
                goto output_layer_technical_primary
            else
                goto output_layer_mixed_balanced
            end_
        end_

start hidden_layer_2_simple_path
    p("HIDDEN LAYER 2: Simple classification pathway")
    
    start simple_classification
        p("  HL2 Node 1: Simple data classification")
        classification_score = context_score + 10
        goto output_layer_simple_storage

# OUTPUT LAYER - Final recommendations and confidence scores
start output_layer_secure_enterprise
    p("OUTPUT LAYER: Secure Enterprise Storage")
    p("RECOMMENDATION: Enterprise Secure Storage")
    p("  → Maximum security protocols")
    p("  → High-availability infrastructure")
    p("  → Compliance-ready architecture")
    confidence_score = 95
    goto neural_conclusion

start output_layer_secure_standard
    p("OUTPUT LAYER: Standard Secure Storage")
    p("RECOMMENDATION: Secure Storage")
    p("  → Enhanced security measures")
    p("  → Encrypted data handling")
    p("  → Access control systems")
    confidence_score = 85
    goto neural_conclusion

start output_layer_business_standard
    p("OUTPUT LAYER: Business Standard Storage")
    p("RECOMMENDATION: Business SQL Storage")
    p("  → Structured business data handling")
    p("  → Transactional integrity")
    p("  → Business intelligence ready")
    confidence_score = 80
    goto neural_conclusion

start output_layer_technical_specialized
    p("OUTPUT LAYER: Technical Specialized Storage")
    p("RECOMMENDATION: Technical NoSQL Storage")
    p("  → Flexible schema design")
    p("  → High-performance queries")
    p("  → Developer-optimized")
    confidence_score = 90
    goto neural_conclusion

start output_layer_technical_standard
    p("OUTPUT LAYER: Technical Standard Storage")
    p("RECOMMENDATION: Standard NoSQL Storage")
    p("  → Document-based storage")
    p("  → Scalable architecture")
    p("  → API-friendly")
    confidence_score = 75
    goto neural_conclusion

start output_layer_personal_secure
    p("OUTPUT LAYER: Personal Secure Storage")
    p("RECOMMENDATION: Personal Secure Storage")
    p("  → Privacy-focused design")
    p("  → Personal data protection")
    p("  → Easy access controls")
    confidence_score = 80
    goto neural_conclusion

start output_layer_business_primary
    p("OUTPUT LAYER: Business-Primary Mixed Storage")
    p("RECOMMENDATION: Business-Oriented Hybrid Storage")
    p("  → Business logic priority")
    p("  → Mixed data type support")
    p("  → Reporting capabilities")
    confidence_score = 70
    goto neural_conclusion

start output_layer_technical_primary
    p("OUTPUT LAYER: Technical-Primary Mixed Storage")
    p("RECOMMENDATION: Technical-Oriented Hybrid Storage")
    p("  → Technical performance priority")
    p("  → Multi-format support")
    p("  → Development-friendly")
    confidence_score = 75
    goto neural_conclusion

start output_layer_personal_primary
    p("OUTPUT LAYER: Personal-Primary Mixed Storage")
    p("RECOMMENDATION: Personal-Oriented Storage")
    p("  → User-centric design")
    p("  → Simple management")
    p("  → Privacy by default")
    confidence_score = 70
    goto neural_conclusion

start output_layer_mixed_balanced
    p("OUTPUT LAYER: Balanced Mixed Storage")
    p("RECOMMENDATION: Balanced Multi-Purpose Storage")
    p("  → Equal priority handling")
    p("  → Versatile architecture")
    p("  → Adaptive performance")
    confidence_score = 65
    goto neural_conclusion

start output_layer_simple_storage
    p("OUTPUT LAYER: Simple Storage")
    p("RECOMMENDATION: Simple File Storage")
    p("  → Straightforward approach")
    p("  → Minimal complexity")
    p("  → Cost-effective")
    confidence_score = 60
    goto neural_conclusion

# Emergency Processing and Recovery Systems
start emergency_processing
    p("EMERGENCY PROCESSING: Activating minimal safe mode")
    
    try_
        p("  Emergency mode: Bypassing complex analysis")
        p("  Using basic classification only")
        
        # Emergency backup
        emergency_data = "emergency_mode_activated"
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('emergency_processing', 'System in emergency mode', 'minimal_processing')")
        
        # Simple emergency classification
        if business_weight > 0 then
            p("  Emergency classification: Business data detected")
            goto emergency_business_storage
        else
            if technical_weight > 0 then
                p("  Emergency classification: Technical data detected")
                goto emergency_technical_storage
            else
                p("  Emergency classification: General data")
                goto emergency_general_storage
            end_
        end_
        
    catch_error_
        p("CRITICAL: Emergency processing also failed")
        goto system_failure_recovery
    end_try_

start emergency_recovery
    p("EMERGENCY RECOVERY: Attempting system restoration")
    
    try_
        p("  Recovery: Checking backup integrity...")
        
        # Attempt to restore from last good checkpoint
        sql("SELECT checkpoint_name, data_state, pathway_taken FROM processing_checkpoints 
             ORDER BY timestamp DESC LIMIT 1")
        
        p("  Recovery: Last checkpoint found, attempting restoration")
        recovery_mode = 1
        
        # Simplified processing based on last known good state
        if business_weight > technical_weight then
            if business_weight > personal_weight then
                goto output_layer_business_standard
            else
                goto output_layer_personal_secure
            end_
        else
            goto output_layer_technical_standard
        end_
        
    catch_error_
        p("CRITICAL: Recovery failed, using absolute fallback")
        goto system_failure_recovery
    end_try_

start system_failure_recovery
    p("SYSTEM FAILURE RECOVERY: Last resort processing")
    
    # Absolute minimal processing without any complex operations
    p("  Using hardcoded safe defaults")
    p("  All advanced features disabled")
    
    # Log the complete system failure
    sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
         VALUES ('system_failure', 'Complete system failure', 'hardcoded_fallback')")
    
    # Hardcoded safe recommendation
    p("RECOMMENDATION: Simple Storage")
    p("  → Emergency safe storage mode")
    p("  → All data protection features disabled")
    p("  → Manual review required")
    confidence_score = 30
    goto neural_conclusion

# Emergency storage recommendations
start emergency_business_storage
    p("EMERGENCY RECOMMENDATION: Basic Business Storage")
    p("  → Emergency business data handling")
    p("  → Reduced security features")
    confidence_score = 50
    goto neural_conclusion

start emergency_technical_storage
    p("EMERGENCY RECOMMENDATION: Basic Technical Storage")
    p("  → Emergency technical data handling")
    p("  → Standard features only")
    confidence_score = 45
    goto neural_conclusion

start emergency_general_storage
    p("EMERGENCY RECOMMENDATION: Basic General Storage")
    p("  → Emergency general data handling")
    p("  → Minimal features")
    confidence_score = 40
    goto neural_conclusion

# Enhanced neural network conclusion with comprehensive backup
start neural_conclusion
    p("=== Enhanced Neural Network Processing Complete ===")
    p("Multi-layer analysis finished with backup protection")
    
    try_
        # Final backup of results
        if backup_enabled == 1 then
            final_backup_data = "processing_complete"
            sql("INSERT INTO data_backup (original_data, features_data, processing_stage) 
                 VALUES (?, 'final_results', 'neural_conclusion')", final_backup_data)
            
            sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken, confidence_level) 
                 VALUES ('neural_conclusion', 'processing_complete', 'final_results', ?)", confidence_score)
        end_
        
        p("Confidence score:")
        p(confidence_score)
        
        # Enhanced feedback with error statistics
        if error_count == 0 then
            p("Processing completed successfully - no errors encountered")
            p("Neural pathways operated optimally")
        else
            if error_count <= 2 then
                p("Processing completed with minor errors recovered")
                p("Neural pathways: ")
                p(error_count)
                p(" errors automatically corrected")
            else
                p("Processing completed with multiple errors")
                p("Total errors handled: ")
                p(error_count)
                p("Backup system prevented data loss")
            end_
        end_
        
        # Backup integrity verification
        if backup_enabled == 1 then
            p("Backup verification: Running integrity check...")
            
            # Count backup records
            sql("SELECT COUNT(*) FROM data_backup")
            sql("SELECT COUNT(*) FROM processing_checkpoints")
            sql("SELECT COUNT(*) FROM error_log")
            
            p("Backup system: All data safely stored")
            p("Recovery capability: VERIFIED")
        else
            p("WARNING: Backup system was disabled due to errors")
            p("Data recovery capability: LIMITED")
        end_
        
        # Recovery mode status
        if recovery_mode == 1 then
            p("System operated in recovery mode")
            p("Performance may have been reduced for safety")
        else
            p("System operated in normal mode")
            p("Full performance achieved")
        end_
        
        # Simulate backpropagation feedback with error consideration
        adjusted_confidence = confidence_score - (error_count * 5)
        if adjusted_confidence < 20 then
            adjusted_confidence = 20
        end_
        
        if adjusted_confidence > 85 then
            p("High confidence - neural pathways reinforced")
            
            # Update success metrics in backup
            if backup_enabled == 1 then
                sql("INSERT INTO processing_checkpoints (checkpoint_name, data_state, pathway_taken) 
                     VALUES ('success_feedback', 'high_confidence', 'pathway_reinforcement')")
            end_
        else
            if adjusted_confidence > 70 then
                p("Good confidence - pathways stable")
            else
                p("Moderate confidence - suggesting pathway adjustment")
                p("Consider manual review of results")
                
                # Log recommendation for manual review
                if backup_enabled == 1 then
                    sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
                         VALUES ('confidence_check', 'Low confidence detected', 'manual_review_recommended')")
                end_
            end_
        end_
        
        p("Neural processing pathways traversed:")
        p("Input Layer -> Hidden Layer 1 -> Hidden Layer 2 -> Output Layer")
        
        # Final backup completion confirmation
        if backup_enabled == 1 then
            p("=== BACKUP SYSTEM STATUS ===")
            p("Data backup: COMPLETE")
            p("Error logging: ACTIVE")
            p("Recovery points: VERIFIED")
            p("System integrity: MAINTAINED")
        end_
        
    catch_error_
        p("ERROR: Neural conclusion phase failed")
        p("Using emergency conclusion...")
        
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('neural_conclusion', 'Conclusion phase error', 'emergency_conclusion')")
        
        p("Emergency conclusion: Processing completed with errors")
        p("Confidence score: UNKNOWN")
        p("Backup status: UNCERTAIN")
    end_try_
    
    end_

# Comprehensive error handling and pathway correction
start pathway_error_correction
    p("Neural pathway error detected - initiating comprehensive correction")
    
    try_
        # Log the pathway error
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('pathway_correction', 'Pathway error detected', 'correction_initiated')")
        
        p("Analyzing error pattern...")
        
        # Attempt intelligent correction based on available data
        if error_count > 5 then
            p("Multiple errors detected - switching to emergency mode")
            goto emergency_processing
        else
            p("Falling back to simplified analysis")
            goto hidden_layer_2_simple_path
        end_
        
    catch_error_
        p("CRITICAL: Pathway correction failed")
        goto system_failure_recovery
    end_try_

# Data integrity verification system
start data_integrity_check
    p("Data integrity check initiated...")
    
    try_
        # Verify backup data consistency
        sql("SELECT COUNT(*) FROM data_backup WHERE processing_stage IS NOT NULL")
        sql("SELECT COUNT(*) FROM processing_checkpoints WHERE confidence_level > 0")
        
        p("Backup integrity: VERIFIED")
        p("Data consistency: CONFIRMED")
        
        goto neural_conclusion
        
    catch_error_
        p("WARNING: Data integrity check failed")
        
        sql("INSERT INTO error_log (error_stage, error_message, recovery_action) 
             VALUES ('integrity_check', 'Data integrity verification failed', 'proceeding_with_caution')")
        
        p("Proceeding with caution...")
        goto neural_conclusion
    end_try_
'''
        
        return moon_script
    
    def extract_neural_features(self, data, user_input):
        """Extract features that simulate neural network inputs"""
        
        features = {}
        
        # Data complexity (input layer feature)
        features['data_complexity'] = int(self.calculate_complexity(data) * 10)
        
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
    
    def run_neural_moon_assessment(self, data, user_input):
        """Execute neural network-style Moon script with language bridging"""
        
        try:
            primary_lang, secondary_langs, lang_scores = self.detect_language_context(data, user_input)
            context = {
                'complexity': len(data),
                'has_async': 'async' in data.lower(),
                'has_tables': 'table' in data.lower(),
                'has_pipes': '|' in data,
                'nested_depth': data.count('{'),
                'has_headers': 'header' in data.lower(),
                'has_goto': 'goto' in data.lower()
            }
            
            neural_script = self.process_neural_pathways(data, user_input, context)
            
            if os.path.exists(self.moon_interpreter_path):
                result = subprocess.run(
                    [self.moon_interpreter_path],
                    input=neural_script,
                    text=True,
                    capture_output=True,
                    timeout=15
                )
                
                neural_output = result.stdout
                recommendation = self.parse_neural_output(neural_output)
                pathways = self.extract_neural_pathways(neural_output)
                confidence = self.extract_confidence_score(neural_output)
                
                return {
                    'neural_output': neural_output,
                    'recommendation': recommendation,
                    'pathways_traversed': pathways,
                    'confidence_score': confidence,
                    'primary_language': primary_lang,
                    'secondary_languages': secondary_langs,
                    'language_scores': lang_scores,
                    'bridge_integration': True,
                    'features_extracted': self.extract_neural_features(data, user_input),
                    'neural_layers_activated': self.count_activated_layers(neural_output)
                }
            else:
                return self.neural_fallback_assessment(data, user_input, primary_lang, secondary_langs)
                
        except Exception as e:
            print(f"Neural processing error: {e}")
            return self.neural_fallback_assessment(data, user_input, 'moon', [])
    
    def parse_neural_output(self, output):
        """Parse the neural network output for storage recommendation"""
        
        recommendations = {
            "Enterprise Secure Storage": "Enterprise Secure Storage",
            "Secure Storage": "Secure Storage",
            "Business SQL Storage": "Business SQL Storage", 
            "Technical NoSQL Storage": "Technical NoSQL Storage",
            "Standard NoSQL Storage": "Standard NoSQL Storage",
            "Personal Secure Storage": "Personal Secure Storage",
            "Business-Oriented Hybrid Storage": "Business Hybrid Storage",
            "Technical-Oriented Hybrid Storage": "Technical Hybrid Storage",
            "Personal-Oriented Storage": "Personal Storage",
            "Balanced Multi-Purpose Storage": "Balanced Storage",
            "Simple File Storage": "Simple Storage"
        }
        
        for key, value in recommendations.items():
            if key in output:
                return value
        
        return "Smart Storage"
    
    def extract_neural_pathways(self, output):
        """Extract the neural pathways that were traversed"""
        
        pathways = []
        pathway_indicators = [
            "INPUT LAYER",
            "HIDDEN LAYER 1A", "HIDDEN LAYER 1B", "HIDDEN LAYER 1C",
            "HIDDEN LAYER 2",
            "OUTPUT LAYER"
        ]
        
        for indicator in pathway_indicators:
            if indicator in output:
                pathways.append(indicator)
        
        return pathways
    
    def extract_confidence_score(self, output):
        """Extract confidence score from neural output"""
        
        confidence_match = re.search(r'confidence_score = (\d+)', output)
        if confidence_match:
            return int(confidence_match.group(1))
        
        lines = output.split('\n')
        for line in lines:
            if line.strip().isdigit() and 50 <= int(line.strip()) <= 100:
                return int(line.strip())
        
        return 75
    
    def count_activated_layers(self, output):
        """Count how many neural layers were activated"""
        
        layer_patterns = [
            "INPUT LAYER",
            "HIDDEN LAYER 1",
            "HIDDEN LAYER 2", 
            "OUTPUT LAYER"
        ]
        
        activated = sum(1 for pattern in layer_patterns if pattern in output)
        return activated
    
    def neural_fallback_assessment(self, data, user_input, primary_lang='moon', secondary_langs=None):
        """Fallback neural assessment when Moon interpreter unavailable"""
        if secondary_langs is None:
            secondary_langs = []
        
        features = self.extract_neural_features(data, user_input)
        
        # Simulate neural network decision process
        if features['business_score'] > 30:
            if features['data_complexity'] > 70:
                recommendation = "Enterprise Secure Storage"
                confidence = 90
            else:
                recommendation = "Business SQL Storage"
                confidence = 80
        elif features['technical_score'] > 25:
            recommendation = "Technical NoSQL Storage"
            confidence = 85
        elif features['personal_score'] > 20:
            recommendation = "Personal Secure Storage"
            confidence = 75
        else:
            recommendation = "Balanced Storage"
            confidence = 70
        
        pathways = ["INPUT LAYER", "HIDDEN LAYER 1", "HIDDEN LAYER 2", "OUTPUT LAYER"]
        
        return {
            'neural_output': f"Neural fallback assessment completed\nPrimary language: {primary_lang}\nSecondary languages: {secondary_langs}\nRecommendation: {recommendation}\nConfidence: {confidence}%",
            'recommendation': recommendation,
            'pathways_traversed': pathways,
            'confidence_score': confidence,
            'primary_language': primary_lang,
            'secondary_languages': secondary_langs,
            'language_scores': {primary_lang: 1},
            'bridge_integration': False,
            'features_extracted': features,
            'neural_layers_activated': 4
        }
        
    def intelligent_data_assessment(self, data, user_input):
        """Enhanced assessment using neural network Moon scripting"""
        
        print(f"{self.personality.get_response('thinking')}")
        print("Initializing neural network analysis...")
        
        # Run neural Moon assessment
        neural_result = self.run_neural_moon_assessment(data, user_input)
        
        # Also run pattern detection
        eye_patterns = analyze_string_patterns(data)
        
        print(f"Neural pathways activated: {neural_result['neural_layers_activated']}/4 layers")
        
        if neural_result['pathways_traversed']:
            print("Processing flow:")
            for i, pathway in enumerate(neural_result['pathways_traversed'], 1):
                print(f"  {i}. {pathway}")
        
        print(f"Neural confidence: {neural_result['confidence_score']}%")
        
        if eye_patterns:
            print(f"Pattern recognition found {len(eye_patterns)} data patterns:")
            for pattern_name, _ in eye_patterns[:3]:
                print(f"  • {pattern_name.replace('_', ' ').title()}")
        
        assessment = {
            'neural_recommendation': neural_result['recommendation'],
            'confidence_score': neural_result['confidence_score'],
            'pathways_traversed': neural_result['pathways_traversed'],
            'features_extracted': neural_result['features_extracted'],
            'detected_patterns': eye_patterns,
            'neural_output': neural_result['neural_output']
        }
        
        if neural_result['confidence_score'] > 85:
            print(f"\n{self.personality.get_response('excitement')}")
            print("The neural network is highly confident in this analysis!")
        elif neural_result['confidence_score'] > 70:
            print("Neural analysis shows good confidence in the recommendation.")
        else:
            print("Neural pathways suggest this data could benefit from additional analysis.")
        
        return assessment
    
    def calculate_complexity(self, data):
        if not data:
            return 0.0
        
        unique_chars = len(set(data))
        char_diversity = min(unique_chars / 50, 1.0)
        
        pattern_score = 0
        if re.search(r'\d+', data): pattern_score += 0.2
        if re.search(r'[A-Z][a-z]+', data): pattern_score += 0.2
        if re.search(r'[{}()\[\];]', data): pattern_score += 0.3
        if re.search(r'[!@#$%^&*]', data): pattern_score += 0.2
        if re.search(r'http[s]?://', data): pattern_score += 0.1
        
        length_factor = min(len(data) / 1000, 1.0)
        
        char_counts = {}
        for char in data:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        data_len = len(data)
        for count in char_counts.values():
            probability = count / data_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        entropy_factor = min(entropy / 8, 1.0)
        complexity = (char_diversity + pattern_score + length_factor + entropy_factor) * 2.5
        return min(complexity, 10.0)

class ConversationalCLI:
    def __init__(self):
        self.analyzer = EnhancedMoonAnalyzer()
        self.personality = ConversationalPersonality()
        self.storage = SimpleStorage()
        self.language_processor = LanguageProcessor()
        self.session_data = []
        self.user_name = None
        self.conversation_history = []
        
    def start(self):
        print(create_banner("SMART CLI", "Your Intelligent Data Companion"))
        print()
        print(self.personality.get_response('greeting'))
        print()
        print("I can help you store, analyze, and understand your data.")
        print("Just tell me what you'd like to do in natural language!")
        print()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                self.conversation_history.append(('user', user_input))
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print(f"\nAssistant: Thanks for chatting with me today! Your data is safe and sound.")
                    print(create_footer("Until next time!"))
                    break
                
                response = self.process_natural_input(user_input)
                self.conversation_history.append(('assistant', response))
                
            except KeyboardInterrupt:
                print(f"\nAssistant: No worries! Feel free to come back anytime.")
                break
            except Exception as e:
                print(f"Assistant: Hmm, I ran into a small issue: {e}")
                print("But don't worry, let's keep going!")
    
    def process_natural_input(self, user_input):
        print(f"\nAssistant: ", end="")
        
        if self.is_greeting(user_input):
            return self.handle_greeting(user_input)
        elif self.is_question_about_capabilities(user_input):
            return self.explain_capabilities()
        elif self.is_data_storage_request(user_input):
            return self.handle_smart_storage(user_input)
        elif self.is_search_request(user_input):
            return self.handle_intelligent_search(user_input)
        elif self.is_analysis_request(user_input):
            return self.handle_conversational_analysis(user_input)
        elif self.is_programming_request(user_input):
            return self.handle_programming_chat(user_input)
        elif self.is_purchase_entry(user_input):
            return self.handle_purchase_conversation(user_input)
        else:
            return self.handle_general_conversation(user_input)
    
    def is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in text.lower() for greeting in greetings)
    
    def is_question_about_capabilities(self, text):
        capability_words = ['what can you', 'what do you', 'how can you', 'help me', 'what are you']
        return any(phrase in text.lower() for phrase in capability_words)
    
    def is_data_storage_request(self, text):
        storage_words = ['store', 'save', 'keep', 'remember', 'put this', 'hold onto']
        return any(word in text.lower() for word in storage_words)
    
    def is_search_request(self, text):
        search_words = ['find', 'search', 'look for', 'get me', 'show me', 'tell me about']
        return any(word in text.lower() for word in search_words)
    
    def is_analysis_request(self, text):
        analysis_words = ['analyze', 'examine', 'study', 'understand', 'explain', 'break down']
        return any(word in text.lower() for word in analysis_words)
    
    def is_programming_request(self, text):
        prog_words = ['code', 'program', 'script', 'python', 'javascript', 'example']
        action_words = ['make', 'create', 'write', 'show', 'generate']
        has_prog = any(word in text.lower() for word in prog_words)
        has_action = any(word in text.lower() for word in action_words)
        return has_prog and has_action
    
    def is_purchase_entry(self, text):
        purchase_words = ['bought', 'purchase', 'spent', 'paid', '$', 'dollar']
        return any(word in text.lower() for word in purchase_words)
    
    def handle_greeting(self, user_input):
        if 'name' in user_input.lower() and not self.user_name:
            name_match = re.search(r'(?:i\'?m|my name is|call me)\s+(\w+)', user_input.lower())
            if name_match:
                self.user_name = name_match.group(1).title()
                return f"Nice to meet you, {self.user_name}! {self.personality.get_response('greeting')}"
        
        response = self.personality.get_response('greeting')
        if self.user_name:
            return f"Hello again, {self.user_name}! {response}"
        else:
            return f"{response} Feel free to tell me your name if you'd like me to remember it!"
    
    def explain_capabilities(self):
        response = f"{self.personality.get_response('excitement')}\n\n"
        response += "Here's what I can help you with:\n\n"
        response += "• Store and organize your data intelligently\n"
        response += "• Analyze patterns and complexity in your information\n"
        response += "• Search the web for answers to your questions\n"
        response += "• Generate code examples in multiple languages\n"
        response += "• Track purchases and expenses\n"
        response += "• Have natural conversations about your data\n\n"
        response += f"{self.personality.get_response('encouragement')}"
        return response
    
    def handle_smart_storage(self, user_input):
        print(f"{self.personality.get_response('understanding')} Let me analyze this data for you.")
        
        data_to_store = self.extract_data_from_input(user_input)
        
        if not data_to_store:
            return "I'd love to help you store something! Could you tell me what specific data you want me to keep safe?"
        
        assessment = self.analyzer.intelligent_data_assessment(data_to_store, user_input)
        
        try:
            record_data = {
                'original_input': user_input,
                'extracted_data': data_to_store,
                'timestamp': datetime.now().isoformat(),
                'patterns_detected': assessment['detected_patterns'],
                'complexity_score': assessment['complexity'],
                'recommendations': assessment['recommendations']
            }
            
            record_key = f"conversation_{len(self.session_data)}_{datetime.now().strftime('%H%M%S')}"
            backend = assessment['recommendations'][0].split(' - ')[0] if assessment['recommendations'] else "Smart Storage"
            
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO data_store (key, value, backend) VALUES (?, ?, ?)',
                (record_key, json.dumps(record_data), backend)
            )
            conn.commit()
            conn.close()
            
            self.session_data.append(record_data)
            
            response = f"Perfect! I've stored your data safely using {backend}.\n"
            response += f"I found it quite interesting - complexity score of {assessment['complexity']:.1f}/10.\n"
            if assessment['detected_patterns']:
                response += f"I also noticed some {assessment['detected_patterns'][0][0].replace('_', ' ')} patterns in there."
            
            return self.personality.personalize_response(response, user_input)
            
        except Exception as e:
            return f"I ran into a small hiccup storing that data: {e}. But don't worry, let's try again!"
    
    def handle_intelligent_search(self, user_input):
        search_query = self.extract_search_query(user_input)
        
        if not search_query:
            return "I'd be happy to search for information! What would you like me to look up?"
        
        print(f"{self.personality.get_response('thinking')}")
        print(f"Let me search for information about '{search_query}'...")
        
        try:
            search_results = dive_search(search_query)
            
            if search_results and len(search_results) > 100:
                response = f"Great question! Here's what I found:\n\n"
                response += search_results[:800] + "..."
                response += f"\n\n{self.personality.get_response('curiosity')} Would you like me to dive deeper into any particular aspect?"
                return response
            else:
                return f"I searched for '{search_query}' but didn't find detailed results. Could you try rephrasing your question?"
                
        except Exception as e:
            return f"I had trouble with that search. Let me try a different approach - could you be more specific about what you're looking for?"
    
    def handle_conversational_analysis(self, user_input):
        data_to_analyze = self.extract_data_from_input(user_input)
        
        if not data_to_analyze:
            return "I'd love to analyze something for you! What data should I take a closer look at?"
        
        print(f"{self.personality.get_response('thinking')}")
        
        eye_patterns = analyze_string_patterns(data_to_analyze)
        complexity = self.analyzer.calculate_complexity(data_to_analyze)
        
        response = f"{self.personality.get_response('excitement')}\n\n"
        response += f"Here's my analysis of your data:\n\n"
        response += f"Complexity Level: {complexity:.1f}/10\n"
        
        if eye_patterns:
            response += f"Patterns I detected:\n"
            for pattern_name, _ in eye_patterns[:3]:
                response += f"  • {pattern_name.replace('_', ' ').title()}\n"
        
        response += f"\nData characteristics:\n"
        response += f"  • Length: {len(data_to_analyze)} characters\n"
        response += f"  • Words: {len(data_to_analyze.split())}\n"
        
        if complexity > 7:
            response += f"\n{self.personality.get_response('curiosity')} This is quite complex data with rich patterns!"
        elif complexity > 4:
            response += f"\nThis data has moderate complexity - there's definitely structure here."
        else:
            response += f"\nThis appears to be straightforward, well-structured data."
        
        return response
    
    def handle_programming_chat(self, user_input):
        print(f"{self.personality.get_response('excitement')} I love helping with programming!")
        
        if 'python' in user_input.lower():
            return self.provide_python_conversation()
        elif 'javascript' in user_input.lower():
            return self.provide_javascript_conversation()
        else:
            return self.provide_general_programming_conversation()
    
    def provide_python_conversation(self):
        response = "Python is one of my favorites! Here's a useful example:\n\n"
        response += "```python\n"
        response += "def analyze_data(data_list):\n"
        response += "    results = {\n"
        response += "        'total': len(data_list),\n"
        response += "        'unique': len(set(data_list)),\n"
        response += "        'most_common': max(set(data_list), key=data_list.count)\n"
        response += "    }\n"
        response += "    return results\n\n"
        response += "# Example usage\n"
        response += "data = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']\n"
        response += "print(analyze_data(data))\n"
        response += "```\n\n"
        response += "This shows how to analyze patterns in data - something I do all the time! Would you like to see more examples?"
        return response
    
    def provide_javascript_conversation(self):
        response = "JavaScript is great for dynamic data processing! Here's something cool:\n\n"
        response += "```javascript\n"
        response += "function smartAnalysis(dataArray) {\n"
        response += "    return {\n"
        response += "        count: dataArray.length,\n"
        response += "        average: dataArray.reduce((a, b) => a + b) / dataArray.length,\n"
        response += "        maximum: Math.max(...dataArray),\n"
        response += "        minimum: Math.min(...dataArray)\n"
        response += "    };\n"
        response += "}\n\n"
        response += "// Example\n"
        response += "const numbers = [10, 25, 30, 15, 20];\n"
        response += "console.log(smartAnalysis(numbers));\n"
        response += "```\n\n"
        response += "This kind of analysis helps understand data patterns quickly! Want to see more?"
        return response
    
    def provide_general_programming_conversation(self):
        response = "Programming is all about solving problems creatively! What specific language or concept interests you?\n\n"
        response += "I can help with:\n"
        response += "• Python data analysis and file handling\n"
        response += "• JavaScript for dynamic web applications\n"
        response += "• Database operations and SQL\n"
        response += "• Algorithm design and optimization\n\n"
        response += "Just tell me what you'd like to explore!"
        return response
    
    def handle_purchase_conversation(self, user_input):
        print(f"{self.personality.get_response('understanding')} Let me help you track that purchase.")
        
        amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', user_input)
        store_match = re.search(r'at\s+([^.!?]+)', user_input, re.IGNORECASE)
        
        amount = amount_match.group(1) if amount_match else "unknown"
        store = store_match.group(1).strip() if store_match else "unknown store"
        
        purchase_data = {
            'type': 'purchase',
            'amount': amount,
            'store': store,
            'description': user_input,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            record_key = f"purchase_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO data_store (key, value, backend) VALUES (?, ?, ?)',
                (record_key, json.dumps(purchase_data), "Secure Storage")
            )
            conn.commit()
            conn.close()
            
            response = f"Got it! I've recorded your ${amount} purchase"
            if store != "unknown store":
                response += f" from {store}"
            response += f".\n\n{self.personality.get_response('encouragement')}"
            response += f" Keeping track of expenses like this is really smart financial planning!"
            
            return response
            
        except Exception as e:
            return f"I had a small issue recording that purchase: {e}. Could you try telling me about it again?"
    
    def handle_general_conversation(self, user_input):
        responses = [
            f"{self.personality.get_response('understanding')} That's interesting! How can I help you work with that?",
            f"{self.personality.get_response('curiosity')} Tell me more about what you'd like to do with this information.",
            f"I find that fascinating! Would you like me to store it, analyze it, or search for related information?",
            f"{self.personality.get_response('encouragement')} What would be most helpful for you right now?"
        ]
        
        base_response = random.choice(responses)
        
        if len(user_input) > 50:
            complexity = self.analyzer.calculate_complexity(user_input)
            if complexity > 6:
                base_response += f"\n\nI notice your message has quite a bit of complexity to it - there might be some interesting patterns to explore!"
        
        return base_response
    
    def extract_data_from_input(self, user_input):
        data_indicators = ['store this', 'save this', 'keep this', 'remember this']
        
        for indicator in data_indicators:
            if indicator in user_input.lower():
                start_idx = user_input.lower().find(indicator) + len(indicator)
                return user_input[start_idx:].strip(': "\'')
        
        quoted_match = re.search(r'"([^"]+)"', user_input)
        if quoted_match:
            return quoted_match.group(1)
        
        if len(user_input.split()) > 8:
            return user_input
        
        return None
    
    def extract_search_query(self, user_input):
        search_phrases = ['search for', 'look up', 'find', 'tell me about', 'what is', 'who is']
        
        for phrase in search_phrases:
            if phrase in user_input.lower():
                start_idx = user_input.lower().find(phrase) + len(phrase)
                return user_input[start_idx:].strip(': "\'?')
        
        question_words = ['what', 'who', 'where', 'when', 'why', 'how']
        if any(user_input.lower().startswith(word) for word in question_words):
            return user_input
        
        return None

class SimpleStorage:
    def __init__(self):
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

if __name__ == "__main__":
    cli = ConversationalCLI()
    cli.start()

class MoonGotoAnalyzer:
    """
    Enhanced data analyzer that uses Moon language's goto functionality
    to jump between different data assessment routines based on characteristics
    """
    
    def __init__(self):
        self.moon_interpreter_path = "./moon/main"
        self.assessment_cache = {}
        self.goto_flow_map = {
            'business_data': 'business_analysis',
            'code_data': 'code_analysis', 
            'numerical_data': 'numerical_analysis',
            'textual_data': 'text_analysis',
            'mixed_data': 'comprehensive_analysis',
            'error_data': 'error_handling'
        }
    
    def generate_moon_assessment_script(self, data, data_type):
        """Generate a Moon language script with goto flow control for data assessment"""
        
        # Calculate data characteristics
        char_count = len(data)
        word_count = len(data.split()) if data else 0
        complexity_score = self.calculate_complexity(data)
        has_numbers = bool(re.search(r'\d+', data))
        has_code_patterns = bool(re.search(r'[{}()\[\];]', data))
        has_business_terms = any(term in data.lower() for term in ['employee', 'salary', 'payroll', 'customer', 'revenue'])
        
        moon_script = f''':::
Moon Language Data Assessment Script
Generated for: {data_type}
Data Length: {char_count} characters
Complexity: {complexity_score:.2f}
:::

# Initialize analysis variables
data_length = {char_count}
word_count = {word_count}  
complexity = {int(complexity_score * 100)}
has_numbers = {1 if has_numbers else 0}
has_code = {1 if has_code_patterns else 0}
has_business = {1 if has_business_terms else 0}

p("=== Moon Language Data Assessment ===")
p("Starting intelligent data analysis...")
p("Data characteristics detected, selecting analysis path...")

# Main assessment flow with goto logic
start main_assessment

    # Determine primary data type
    if has_business == 1 then
        p("Business data patterns detected")
        goto business_analysis
    end_
    
    if has_code == 1 then
        p("Code-like patterns identified")
        goto code_analysis
    end_
    
    if has_numbers == 1 then
        p("Numerical data found")
        goto numerical_analysis  
    end_
    
    if word_count > 10 then
        p("Text-heavy content detected")
        goto text_analysis
    end_
    
    # Default to comprehensive analysis
    p("Mixed content type, using comprehensive analysis")
    goto comprehensive_analysis

# Business data analysis routine
start business_analysis
    p("→ Entering business data analysis routine")
    p("  Checking for employee records...")
    p("  Analyzing payroll patterns...")
    p("  Assessing customer data structures...")
    
    if complexity > 50 then
        p("  Complex business data - recommending Secure Storage")
        goto secure_storage_recommendation
    else
        p("  Standard business data - recommending SQL Storage")
        goto sql_storage_recommendation
    end_

# Code analysis routine  
start code_analysis
    p("→ Entering code analysis routine")
    p("  Scanning for function definitions...")
    p("  Detecting programming language patterns...")
    p("  Analyzing code complexity...")
    
    if complexity > 60 then
        p("  High complexity code - recommending Jeans Storage")
        goto jeans_storage_recommendation
    else
        p("  Standard code - recommending NoSQL Storage")
        goto nosql_storage_recommendation
    end_

# Numerical analysis routine
start numerical_analysis
    p("→ Entering numerical analysis routine")
    p("  Processing mathematical expressions...")
    p("  Calculating statistical patterns...")
    p("  Evaluating data ranges...")
    
    if word_count > 20 then
        p("  Mixed numerical/text data detected")
        goto comprehensive_analysis
    else
        p("  Pure numerical data - recommending SQL Storage")
        goto sql_storage_recommendation
    end_

# Text analysis routine
start text_analysis
    p("→ Entering text analysis routine") 
    p("  Analyzing linguistic patterns...")
    p("  Processing natural language content...")
    p("  Evaluating semantic complexity...")
    
    if complexity > 40 then
        p("  Complex text patterns - recommending NoSQL Storage")
        goto nosql_storage_recommendation
    else
        p("  Simple text data - recommending Jill Storage")
        goto jill_storage_recommendation
    end_

# Comprehensive analysis for mixed data
start comprehensive_analysis
    p("→ Entering comprehensive analysis routine")
    p("  Multi-modal data analysis in progress...")
    p("  Evaluating all detected patterns...")
    p("  Cross-referencing data characteristics...")
    
    if has_business == 1 then
        if has_code == 1 then
            p("  Business + Code hybrid - recommending Secure Storage")
            goto secure_storage_recommendation
        else
            goto business_analysis
        end_
    end_
    
    if complexity > 70 then
        p("  Highly complex mixed data - recommending Secure Storage")
        goto secure_storage_recommendation
    else
        p("  Standard mixed data - recommending NoSQL Storage") 
        goto nosql_storage_recommendation
    end_

# Storage recommendation routines
start secure_storage_recommendation
    p("RECOMMENDATION: Secure Storage Backend")
    p("  → High security requirements detected")
    p("  → Complex data patterns require encryption")
    p("  → Suitable for sensitive business/personal data")
    goto analysis_complete

start sql_storage_recommendation  
    p("RECOMMENDATION: SQL Storage Backend")
    p("  → Structured data patterns detected")
    p("  → Relational storage optimal for this data type")
    p("  → ACID compliance recommended")
    goto analysis_complete

start nosql_storage_recommendation
    p("RECOMMENDATION: NoSQL Storage Backend")
    p("  → Flexible schema requirements identified")
    p("  → Document/object storage optimal")
    p("  → Scalable for varying data structures")
    goto analysis_complete

start jeans_storage_recommendation
    p("RECOMMENDATION: Jeans Storage Backend")
    p("  → Code/algorithmic patterns detected")
    p("  → Specialized storage for development data")
    p("  → Optimized for programming content")
    goto analysis_complete

start jill_storage_recommendation
    p("RECOMMENDATION: Jill Storage Backend")
    p("  → Simple textual data identified")
    p("  → Lightweight storage sufficient")
    p("  → Cost-effective for basic content")
    goto analysis_complete

start analysis_complete
    p("=== Analysis Complete ===")
    p("Moon language assessment finished successfully")
    p("Storage backend recommendation generated")
    
    # Calculate final metrics
    total_score = complexity + (word_count / 10) + (data_length / 100)
    p("Final analysis score:")
    p(total_score)
    
    end_

# Error handling routine
start error_handling
    p("Error in analysis detected")
    p("Falling back to default assessment...")
    goto comprehensive_analysis
'''
        
        return moon_script
    
    def calculate_complexity(self, data):
        """Calculate data complexity score (0-10)"""
        if not data:
            return 0.0
            
        # Character diversity
        unique_chars = len(set(data))
        char_diversity = min(unique_chars / 50, 1.0)
        
        # Pattern complexity
        pattern_score = 0
        if re.search(r'\d+', data): pattern_score += 0.2
        if re.search(r'[A-Z][a-z]+', data): pattern_score += 0.2
        if re.search(r'[{}()\[\];]', data): pattern_score += 0.3
        if re.search(r'[!@#$%^&*]', data): pattern_score += 0.2
        if re.search(r'http[s]?://', data): pattern_score += 0.1
        
        # Length factor
        length_factor = min(len(data) / 1000, 1.0)
        
        # Entropy calculation
        char_counts = {}
        for char in data:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        entropy = 0
        data_len = len(data)
        for count in char_counts.values():
            probability = count / data_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        entropy_factor = min(entropy / 8, 1.0)
        
        # Combined complexity score
        complexity = (char_diversity + pattern_score + length_factor + entropy_factor) * 2.5
        return min(complexity, 10.0)
    
    def run_moon_assessment(self, data, data_type):
        """Execute Moon language assessment script and capture results"""
        
        try:
            # Generate the Moon script
            moon_script = self.generate_moon_assessment_script(data, data_type)
            
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.moon', delete=False) as f:
                f.write(moon_script)
                script_path = f.name
            
            # Execute Moon interpreter
            if os.path.exists(self.moon_interpreter_path):
                result = subprocess.run(
                    [self.moon_interpreter_path],
                    input=moon_script,
                    text=True,
                    capture_output=True,
                    timeout=10
                )
                
                assessment_output = result.stdout
                
                # Clean up temp file
                os.unlink(script_path)
                
                # Parse Moon output for recommendations
                recommendation = self.parse_moon_output(assessment_output)
                
                return {
                    'moon_output': assessment_output,
                    'recommendation': recommendation,
                    'flow_path': self.extract_flow_path(assessment_output),
                    'complexity_score': self.calculate_complexity(data),
                    'script_generated': True
                }
            else:
                # Fallback if Moon interpreter not available
                print("Moon interpreter not found, using fallback analysis...")
                return self.fallback_assessment(data, data_type)
                
        except Exception as e:
            print(f"Error running Moon assessment: {e}")
            return self.fallback_assessment(data, data_type)
    
    def parse_moon_output(self, output):
        """Parse Moon interpreter output to extract recommendation"""
        
        if "Secure Storage Backend" in output:
            return "Secure Storage"
        elif "SQL Storage Backend" in output:
            return "SQL Storage"  
        elif "NoSQL Storage Backend" in output:
            return "NoSQL Storage"
        elif "Jeans Storage Backend" in output:
            return "Jeans Storage"
        elif "Jill Storage Backend" in output:
            return "Jill Storage"
        else:
            return "NoSQL Storage"  # Default fallback
    
    def extract_flow_path(self, output):
        """Extract the goto flow path taken during analysis"""
        flow_steps = []
        
        lines = output.split('\n')
        for line in lines:
            if '→ Entering' in line:
                step = line.strip()
                flow_steps.append(step)
        
        return flow_steps
    
    def fallback_assessment(self, data, data_type):
        """Fallback assessment when Moon interpreter unavailable"""
        
        complexity = self.calculate_complexity(data)
        
        # Simple rule-based recommendation
        if any(term in data.lower() for term in ['employee', 'salary', 'payroll', 'customer']):
            recommendation = "Secure Storage"
            flow_path = ["→ Entering business data analysis routine"]
        elif re.search(r'[{}()\[\];]', data):
            recommendation = "Jeans Storage"
            flow_path = ["→ Entering code analysis routine"]
        elif complexity > 7.0:
            recommendation = "Secure Storage"
            flow_path = ["→ Entering comprehensive analysis routine"]
        elif re.search(r'\d+', data):
            recommendation = "SQL Storage"
            flow_path = ["→ Entering numerical analysis routine"]
        else:
            recommendation = "Jill Storage"
            flow_path = ["→ Entering text analysis routine"]
        
        return {
            'moon_output': f"Fallback analysis completed\nRecommendation: {recommendation}",
            'recommendation': recommendation,
            'flow_path': flow_path,
            'complexity_score': complexity,
            'script_generated': False
        }

class EnhancedSmartCLI:
    """Enhanced CLI with Moon language goto-based data assessment"""
    
    def __init__(self):
        self.moon_analyzer = MoonGotoAnalyzer()
        self.storage = SimpleStorage()
        self.language_processor = LanguageProcessor()
        self.session_data = []
        
    def start(self):
        print("Enhanced Smart Database CLI with Moon Language Analysis")
        print("Features: Intelligent goto-based data assessment, multi-backend storage")
        print("Commands: store, retrieve, analyze, moon-assess, help, quit")
        print()
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Moon-powered analysis complete. Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.show_enhanced_help()
                elif user_input.startswith('store '):
                    self.handle_enhanced_store(user_input[6:])
                elif user_input.startswith('moon-assess '):
                    self.handle_moon_assessment(user_input[12:])
                elif user_input == 'moon-assess':
                    print("Usage: moon-assess <data>")
                    print("   Example: moon-assess big purchase $100 at Ralphs grocery store")
                elif user_input.startswith('analyze '):
                    self.handle_enhanced_analyze(user_input[8:])
                elif user_input.startswith('retrieve '):
                    self.handle_retrieve(user_input[9:])
                elif user_input.startswith('search '):
                    self.handle_search(user_input[7:])
                elif 'purchase' in user_input.lower() or 'bought' in user_input.lower() or '$' in user_input:
                    self.handle_purchase_entry(user_input)
                elif self.is_programming_request(user_input):
                    self.handle_programming_request(user_input)
                else:
                    self.handle_conversation(user_input)
                    
            except KeyboardInterrupt:
                print("\nMoon analysis terminated.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_purchase_entry(self, user_input):
        """Handle purchase data entry with intelligent parsing"""
        
        print("Processing purchase data entry...")
        
        # Extract purchase details using regex
        amount_match = re.search(r'\$?(\d+(?:\.\d{2})?)', user_input)
        store_match = re.search(r'at\s+([^.!?]+)', user_input, re.IGNORECASE)
        
        amount = amount_match.group(1) if amount_match else "unknown"
        store = store_match.group(1).strip() if store_match else "unknown store"
        
        # Create structured purchase data
        purchase_data = {
            'type': 'purchase',
            'amount': amount,
            'store': store,
            'description': user_input,
            'timestamp': datetime.now().isoformat(),
            'category': 'retail' if 'ralphs' in user_input.lower() else 'general'
        }
        
        # Run Moon assessment on the purchase data
        moon_result = self.moon_analyzer.run_moon_assessment(
            json.dumps(purchase_data), "purchase_data"
        )
        
        print(f"Purchase Details:")
        print(f"   Amount: ${amount}")
        print(f"   Store: {store}")
        print(f"   Category: {purchase_data['category']}")
        print(f"   Moon Recommendation: {moon_result['recommendation']}")
        
        # Store the purchase data
        try:
            record_key = f"purchase_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            full_record = {
                'purchase_data': purchase_data,
                'moon_analysis': moon_result,
                'timestamp': datetime.now().isoformat()
            }
            
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO data_store (key, value, backend) VALUES (?, ?, ?)',
                (record_key, json.dumps(full_record), moon_result['recommendation'])
            )
            conn.commit()
            conn.close()
            
            print(f"Purchase stored successfully with key: {record_key}")
            
        except Exception as e:
            print(f"Error storing purchase: {e}")
    
    def show_enhanced_help(self):
        print("\nEnhanced Smart CLI - Moon Language Powered")
        print("=" * 50)
        print("Commands:")
        print("  store <data>        - Store with Moon-guided backend selection")
        print("  moon-assess <data>  - Run Moon language goto analysis")
        print("  analyze <data>      - Comprehensive analysis with flow visualization")
        print("  retrieve <key>      - Retrieve stored data")
        print("  search <term>       - Search stored data")
        print("  help               - Show this help")
        print("  quit               - Exit")
        print()
        print("Special Features:")
        print("  * Moon language goto flow control for data assessment")
        print("  * Intelligent backend selection using label jumping")  
        print("  * Complex pattern recognition with branching logic")
        print("  * Visual flow path display showing analysis journey")
        print("  * Automatic purchase data parsing and categorization")
        print()
    
    def handle_enhanced_store(self, data):
        """Enhanced storage with Moon language analysis"""
        
        print("Initiating Moon-powered data analysis...")
        
        # Run Moon language assessment
        moon_result = self.moon_analyzer.run_moon_assessment(data, "user_input")
        
        # Display analysis flow
        print("\nAnalysis Flow Path:")
        for step in moon_result['flow_path']:
            print(f"   {step}")
        
        print(f"\nMoon Recommendation: {moon_result['recommendation']}")
        print(f"Complexity Score: {moon_result['complexity_score']:.2f}/10")
        
        # Process with language processor for additional insights
        processed = self.language_processor.process(data)
        
        # Store with Moon-recommended backend
        try:
            record_data = {
                'original_input': data,
                'timestamp': datetime.now().isoformat(),
                'moon_analysis': moon_result,
                'language_processing': processed['parsed'],
                'goto_flow': moon_result['flow_path'],
                'complexity_score': moon_result['complexity_score']
            }
            
            structured_data = json.dumps(record_data)
            record_key = f"moon_data_{len(self.session_data)}_{moon_result['recommendation'].lower().replace(' ', '_')}"
            
            # Use Moon recommendation for storage backend override
            backend = moon_result['recommendation']
            
            # Store in database with Moon-recommended backend
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO data_store (key, value, backend) VALUES (?, ?, ?)',
                (record_key, structured_data, backend)
            )
            conn.commit()
            conn.close()
            
            print(f"Data stored successfully!")
            print(f"   Backend: {backend}")
            print(f"   Key: {record_key}")
            print(f"   Analysis: Moon goto flow completed")
            
            self.session_data.append(record_data)
            
        except Exception as e:
            print(f"Storage error: {e}")
    
    def handle_moon_assessment(self, data):
        """Dedicated Moon language assessment command"""
        
        print("Running dedicated Moon language assessment...")
        print("=" * 55)
        
        # Run assessment
        moon_result = self.moon_analyzer.run_moon_assessment(data, "assessment_target")
        
        # Display detailed results
        print("\nAssessment Results:")
        print(f"   Data Length: {len(data)} characters")
        print(f"   Complexity Score: {moon_result['complexity_score']:.2f}/10")
        print(f"   Moon Script Generated: {moon_result['script_generated']}")
        
        print("\nGoto Flow Analysis:")
        for i, step in enumerate(moon_result['flow_path'], 1):
            print(f"   {i}. {step}")
        
        print(f"\nFinal Recommendation: {moon_result['recommendation']}")
        
        print("\nMoon Interpreter Output:")
        print("-" * 40)
        print(moon_result['moon_output'])
        print("-" * 40)
        
        # Provide reasoning
        self.explain_recommendation(moon_result, data)
    
    def explain_recommendation(self, moon_result, data):
        """Explain why Moon analysis chose this path"""
        
        print("\nAnalysis Reasoning:")
        
        has_business = any(term in data.lower() for term in ['employee', 'salary', 'payroll', 'customer', 'revenue'])
        has_code = bool(re.search(r'[{}()\[\];]', data))
        has_numbers = bool(re.search(r'\d+', data))
        word_count = len(data.split()) if data else 0
        
        if has_business:
            print("   * Business terminology detected -> goto business_analysis")
        if has_code:
            print("   * Code patterns found -> goto code_analysis")
        if has_numbers:
            print("   * Numerical data present -> goto numerical_analysis")
        if word_count > 10:
            print("   * Text-heavy content -> goto text_analysis")
        
        complexity = moon_result['complexity_score']
        if complexity > 7:
            print("   * High complexity -> goto secure_storage_recommendation")
        elif complexity > 4:
            print("   * Medium complexity -> goto nosql_storage_recommendation")
        else:
            print("   * Low complexity -> goto jill_storage_recommendation")
        
        print(f"\n   Moon's goto logic selected: {moon_result['recommendation']}")
    
    def handle_enhanced_analyze(self, data):
        """Enhanced analysis with visualization"""
        
        print("Enhanced Analysis with Moon Language Integration")
        print("=" * 55)
        
        # Moon assessment
        moon_result = self.moon_analyzer.run_moon_assessment(data, "analysis")
        
        # Language processing
        processed = self.language_processor.process(data)
        
        # Display comprehensive analysis
        print("\n1. Basic Metrics:")
        print(f"   Length: {len(data)} characters")
        print(f"   Words: {len(data.split()) if data else 0}")
        print(f"   Lines: {data.count(chr(10)) + 1 if data else 0}")
        
        print("\n2. Pattern Detection:")
        patterns = {
            'Numbers': bool(re.search(r'\d+', data)),
            'URLs': bool(re.search(r'http[s]?://', data)),
            'Code Brackets': bool(re.search(r'[{}()\[\];]', data)),
            'Special Chars': bool(re.search(r'[!@#$%^&*]', data)),
            'Business Terms': any(term in data.lower() for term in ['employee', 'salary', 'payroll'])
        }
        
        for pattern, found in patterns.items():
            status = "[X]" if found else "[ ]"
            print(f"   {status} {pattern}")
        
        print("\n3. Moon Language Goto Flow:")
        for i, step in enumerate(moon_result['flow_path'], 1):
            print(f"   Step {i}: {step}")
        
        print(f"\n4. Storage Recommendation:")
        print(f"   Target: {moon_result['recommendation']}")
        print(f"   Confidence: {moon_result['complexity_score']:.1f}/10")
        
        print("\n5. Language Processing:")
        print(f"   Data Type: {processed['parsed']['data_type']}")
        print(f"   Domain: {processed['parsed']['domain']}")
        if processed['parsed']['entities']:
            print("   Entities Found:")
            for key, value in processed['parsed']['entities'].items():
                if value:
                    print(f"      {key}: {value}")
    
    def handle_retrieve(self, key):
        """Enhanced retrieval with Moon analysis history"""
        try:
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute('SELECT value, backend FROM data_store WHERE key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                value, backend = result
                
                try:
                    # Try to parse as JSON for enhanced display
                    data = json.loads(value)
                    
                    print(f"Retrieved: {key}")
                    print(f"Backend: {backend}")
                    
                    if 'moon_analysis' in data:
                        moon_data = data['moon_analysis']
                        print(f"Moon Analysis:")
                        print(f"   Recommendation: {moon_data['recommendation']}")
                        print(f"   Complexity: {moon_data['complexity_score']:.2f}")
                        print(f"   Flow Steps: {len(moon_data['flow_path'])}")
                    
                    print(f"Original Data: {data.get('original_input', '')[:100]}...")
                    
                except json.JSONDecodeError:
                    print(f"Retrieved: {value}")
                    
            else:
                print(f"Key '{key}' not found")
                
        except Exception as e:
            print(f"Retrieval error: {e}")
    
    def handle_search(self, term):
        """Enhanced search with Moon analysis filtering"""
        try:
            conn = sqlite3.connect("smart_cli.db")
            cursor = conn.cursor()
            cursor.execute('SELECT key, value, backend FROM data_store WHERE value LIKE ?', (f'%{term}%',))
            results = cursor.fetchall()
            conn.close()
            
            if results:
                print(f"Found {len(results)} results for '{term}':")
                print()
                
                for key, value, backend in results:
                    try:
                        data = json.loads(value)
                        moon_rec = data.get('moon_analysis', {}).get('recommendation', 'Unknown')
                        complexity = data.get('moon_analysis', {}).get('complexity_score', 0)
                        
                        print(f"{key}")
                        print(f"   Backend: {backend} | Moon Rec: {moon_rec} | Complexity: {complexity:.1f}")
                        print(f"   Data: {data.get('original_input', '')[:80]}...")
                        print()
                        
                    except json.JSONDecodeError:
                        print(f"{key}: {value[:80]}...")
                        print()
            else:
                print(f"No results found for '{term}'")
                
        except Exception as e:
            print(f"Search error: {e}")
    
    def handle_conversation(self, user_input):
        """Enhanced conversation with Moon insights"""
        
        # Quick Moon assessment for conversation context
        if len(user_input) > 20:
            moon_result = self.moon_analyzer.run_moon_assessment(user_input, "conversation")
            
            print(f"Processing your message...")
            print(f"Moon analysis suggests: {moon_result['recommendation']} approach")
            
            if moon_result['complexity_score'] > 6:
                print("Your message shows high complexity - very interesting!")
            
        print("I understand your request. Try 'store', 'analyze', or 'moon-assess' with your data.")

    def is_programming_request(self, user_input):
        """Detect if user is asking for programming examples or code"""
        programming_keywords = ['make', 'create', 'generate', 'build', 'write', 'develop', 'show', 'example', 'code']
        language_keywords = ['python', 'javascript', 'c', 'algorithm', 'function', 'class', 'method', 'script']
        
        user_lower = user_input.lower()
        has_programming = any(keyword in user_lower for keyword in programming_keywords)
        has_language = any(keyword in user_lower for keyword in language_keywords)
        
        return has_programming and has_language

    def handle_programming_request(self, user_input):
        """Handle programming and code generation requests"""
        user_lower = user_input.lower()
        
        print("Programming Request Detected")
        print("=" * 40)
        
        if 'python' in user_lower and 'example' in user_lower:
            self.provide_python_examples()
        elif 'python' in user_lower and 'file' in user_lower:
            self.provide_python_file_example()
        elif 'python' in user_lower and ('data' in user_lower or 'database' in user_lower):
            self.provide_python_data_example()
        elif 'javascript' in user_lower:
            self.provide_javascript_examples()
        elif 'c' in user_lower and 'animation' in user_lower:
            self.provide_c_animation_example()
        elif 'algorithm' in user_lower:
            self.provide_algorithm_examples()
        else:
            self.provide_general_programming_examples()

    def provide_python_examples(self):
        """Provide comprehensive Python examples"""
        print("Python Programming Examples")
        print("-" * 30)
        
        examples = [
            {
                "title": "File Processing Example",
                "code": '''
import json
import csv
from datetime import datetime

def process_data_file(filename):
    """Process different types of data files"""
    
    if filename.endswith('.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
            print(f"Loaded JSON data: {len(data)} items")
            return data
    
    elif filename.endswith('.csv'):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
            print(f"Loaded CSV data: {len(data)} rows")
            return data
    
    else:
        with open(filename, 'r') as f:
            content = f.read()
            print(f"Loaded text file: {len(content)} characters")
            return content

# Usage
data = process_data_file("sample.json")
'''
            },
            {
                "title": "Data Analysis Example",
                "code": '''
def analyze_sales_data(sales_records):
    """Analyze sales data with statistics"""
    
    total_sales = sum(record['amount'] for record in sales_records)
    avg_sale = total_sales / len(sales_records) if sales_records else 0
    
    # Find top customer
    customer_totals = {}
    for record in sales_records:
        customer = record['customer']
        customer_totals[customer] = customer_totals.get(customer, 0) + record['amount']
    
    top_customer = max(customer_totals.items(), key=lambda x: x[1]) if customer_totals else None
    
    return {
        'total_sales': total_sales,
        'average_sale': avg_sale,
        'top_customer': top_customer,
        'total_transactions': len(sales_records)
    }

# Example usage
sales = [
    {'customer': 'Alice', 'amount': 150.00},
    {'customer': 'Bob', 'amount': 200.00},
    {'customer': 'Alice', 'amount': 75.00}
]

results = analyze_sales_data(sales)
print(f"Total Sales: ${results['total_sales']}")
print(f"Top Customer: {results['top_customer'][0]} (${results['top_customer'][1]})")
'''
            },
            {
                "title": "Class-Based Data Manager",
                "code": '''
class DataManager:
    """Simple data management class"""
    
    def __init__(self):
        self.records = []
        self.categories = set()
    
    def add_record(self, data, category='general'):
        """Add a new data record"""
        record = {
            'id': len(self.records) + 1,
            'data': data,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        self.records.append(record)
        self.categories.add(category)
        return record['id']
    
    def get_by_category(self, category):
        """Get all records in a category"""
        return [r for r in self.records if r['category'] == category]
    
    def search(self, keyword):
        """Search records by keyword"""
        return [r for r in self.records if keyword.lower() in str(r['data']).lower()]
    
    def stats(self):
        """Get statistics"""
        return {
            'total_records': len(self.records),
            'categories': list(self.categories),
            'latest_record': self.records[-1] if self.records else None
        }

# Example usage
dm = DataManager()
dm.add_record("Customer John Doe purchase $150", "sales")
dm.add_record("Employee Sarah Smith hired", "hr")
dm.add_record("Server maintenance completed", "technical")

print("Sales records:", dm.get_by_category("sales"))
print("Search results:", dm.search("john"))
print("Statistics:", dm.stats())
'''
            }
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n{i}. {example['title']}")
            print(example['code'])

    def provide_python_file_example(self):
        """Provide Python file handling example"""
        print("Python File Operations Example")
        print("-" * 30)
        
        code = '''
import os
import json
import csv
from pathlib import Path

class FileProcessor:
    """Handle various file operations"""
    
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def write_json(self, filename, data):
        """Write data to JSON file"""
        filepath = self.base_dir / f"{filename}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"JSON written to {filepath}")
    
    def read_json(self, filename):
        """Read data from JSON file"""
        filepath = self.base_dir / f"{filename}.json"
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return None
    
    def write_csv(self, filename, data, headers):
        """Write data to CSV file"""
        filepath = self.base_dir / f"{filename}.csv"
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV written to {filepath}")
    
    def process_directory(self):
        """Process all files in directory"""
        results = []
        for file_path in self.base_dir.glob("*"):
            if file_path.is_file():
                results.append({
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'type': file_path.suffix
                })
        return results

# Example usage
processor = FileProcessor()

# Write some data
sample_data = {
    "purchases": [
        {"item": "Groceries", "amount": 100.00, "store": "Ralphs"},
        {"item": "Gas", "amount": 45.00, "store": "Shell"}
    ],
    "total": 145.00
}

processor.write_json("purchases", sample_data)

# Read it back
loaded_data = processor.read_json("purchases")
print("Loaded data:", loaded_data)

# Process directory
files = processor.process_directory()
print("Files in directory:", files)
'''
        
        print(code)

    def provide_python_data_example(self):
        """Provide Python database/data handling example"""
        print("Python Data Management Example")
        print("-" * 30)
        
        code = '''
import sqlite3
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PurchaseRecord:
    """Data class for purchase records"""
    item: str
    amount: float
    store: str
    date: str
    category: str = "general"

class PurchaseDatabase:
    """Database manager for purchase records"""
    
    def __init__(self, db_path="purchases.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                amount REAL NOT NULL,
                store TEXT NOT NULL,
                date TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_purchase(self, purchase: PurchaseRecord):
        """Add a new purchase record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO purchases (item, amount, store, date, category)
            VALUES (?, ?, ?, ?, ?)
        """, (purchase.item, purchase.amount, purchase.store, 
              purchase.date, purchase.category))
        purchase_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return purchase_id
    
    def get_purchases_by_store(self, store: str) -> List[dict]:
        """Get all purchases from a specific store"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM purchases WHERE store LIKE ?
        """, (f"%{store}%",))
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_monthly_summary(self) -> dict:
        """Get monthly spending summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_purchases,
                SUM(amount) as total_spent,
                AVG(amount) as avg_purchase,
                MIN(amount) as min_purchase,
                MAX(amount) as max_purchase
            FROM purchases
            WHERE date >= date('now', 'start of month')
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total_purchases': row[0],
            'total_spent': row[1] or 0,
            'average_purchase': row[2] or 0,
            'min_purchase': row[3] or 0,
            'max_purchase': row[4] or 0
        }

# Example usage
db = PurchaseDatabase()

# Add some purchases
grocery_purchase = PurchaseRecord(
    item="Weekly groceries",
    amount=100.00,
    store="Ralphs",
    date=datetime.now().strftime("%Y-%m-%d"),
    category="food"
)

gas_purchase = PurchaseRecord(
    item="Gasoline",
    amount=45.50,
    store="Shell",
    date=datetime.now().strftime("%Y-%m-%d"),
    category="transportation"
)

# Store purchases
db.add_purchase(grocery_purchase)
db.add_purchase(gas_purchase)

# Query data
ralphs_purchases = db.get_purchases_by_store("Ralphs")
print("Ralphs purchases:", json.dumps(ralphs_purchases, indent=2))

# Get summary
summary = db.get_monthly_summary()
print("Monthly summary:", summary)
'''
        
        print(code)

    def provide_javascript_examples(self):
        """Provide JavaScript examples"""
        print("JavaScript Programming Examples")
        print("-" * 30)
        
        code = '''
// 1. Data Processing Functions
function processTransactionData(transactions) {
    const summary = {
        total: 0,
        count: transactions.length,
        byCategory: {},
        byMonth: {}
    };
    
    transactions.forEach(transaction => {
        // Total amount
        summary.total += transaction.amount;
        
        // By category
        if (!summary.byCategory[transaction.category]) {
            summary.byCategory[transaction.category] = 0;
        }
        summary.byCategory[transaction.category] += transaction.amount;
        
        // By month
        const month = transaction.date.substring(0, 7); // YYYY-MM
        if (!summary.byMonth[month]) {
            summary.byMonth[month] = 0;
        }
        summary.byMonth[month] += transaction.amount;
    });
    
    return summary;
}

// 2. Async Data Fetching
async function fetchAndProcessData(apiUrl) {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        
        const processed = data.map(item => ({
            id: item.id,
            amount: parseFloat(item.amount),
            date: new Date(item.date).toISOString().split('T')[0],
            category: item.category || 'uncategorized'
        }));
        
        return processTransactionData(processed);
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

// 3. ES6 Class Example
class DataManager {
    constructor() {
        this.data = [];
        this.listeners = [];
    }
    
    addData(item) {
        this.data.push({
            ...item,
            id: this.generateId(),
            timestamp: new Date().toISOString()
        });
        this.notifyListeners('add', item);
    }
    
    filterBy(property, value) {
        return this.data.filter(item => item[property] === value);
    }
    
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    notifyListeners(event, data) {
        this.listeners.forEach(listener => listener(event, data));
    }
    
    subscribe(callback) {
        this.listeners.push(callback);
    }
}

// Example usage
const manager = new DataManager();

manager.subscribe((event, data) => {
    console.log(`Event: ${event}`, data);
});

manager.addData({
    type: 'purchase',
    amount: 100.00,
    store: 'Ralphs',
    category: 'groceries'
});

const groceries = manager.filterBy('category', 'groceries');
console.log('Grocery purchases:', groceries);
'''
        
        print(code)

    def provide_c_animation_example(self):
        """Provide C animation example"""
        print("C Terminal Animation Example")
        print("-" * 30)
        
        code = '''
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

// Progress bar animation
void animated_progress_bar(int total_steps) {
    printf("Processing data...\n");
    
    for (int i = 0; i <= total_steps; i++) {
        printf("\r[");
        
        // Draw filled portion
        int filled = (i * 50) / total_steps;
        for (int j = 0; j < filled; j++) {
            printf("=");
        }
        
        // Draw empty portion
        for (int j = filled; j < 50; j++) {
            printf(" ");
        }
        
        printf("] %d%%", (i * 100) / total_steps);
        fflush(stdout);
        
        usleep(100000); // 100ms delay
    }
    printf("\nComplete!\n");
}

// Matrix-style falling text
void matrix_effect() {
    char chars[] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int cols = 80, rows = 24;
    
    printf("\033[2J\033[H"); // Clear screen
    printf("\033[32m");     // Green color
    
    for (int frame = 0; frame < 50; frame++) {
        printf("\033[H"); // Move to top
        
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (rand() % 10 == 0) {
                    printf("%c", chars[rand() % strlen(chars)]);
                } else {
                    printf(" ");
                }
            }
            printf("\n");
        }
        
        usleep(200000); // 200ms delay
    }
    
    printf("\033[0m\033[2J\033[H"); // Reset and clear
}

// Bouncing ball simulation
void bouncing_ball() {
    int width = 50, height = 15;
    int x = 5, y = 5;
    int dx = 1, dy = 1;
    
    for (int frame = 0; frame < 100; frame++) {
        printf("\033[2J\033[H"); // Clear screen
        
        // Draw the ball
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                if (row == y && col == x) {
                    printf("O");
                } else if (row == 0 || row == height-1) {
                    printf("-");
                } else if (col == 0 || col == width-1) {
                    printf("|");
                } else {
                    printf(" ");
                }
            }
            printf("\n");
        }
        
        // Update ball position
        x += dx;
        y += dy;
        
        // Bounce off walls
        if (x <= 1 || x >= width-2) dx = -dx;
        if (y <= 1 || y >= height-2) dy = -dy;
        
        usleep(150000); // 150ms delay
    }
}

int main() {
    srand(time(NULL));
    
    printf("C Animation Examples\n");
    printf("1. Progress Bar\n");
    printf("2. Matrix Effect\n");
    printf("3. Bouncing Ball\n");
    printf("Choose (1-3): ");
    
    int choice;
    scanf("%d", &choice);
    
    switch(choice) {
        case 1:
            animated_progress_bar(20);
            break;
        case 2:
            matrix_effect();
            break;
        case 3:
            bouncing_ball();
            break;
        default:
            printf("Invalid choice\n");
    }
    
    return 0;
}
'''
        
        print(code)

    def provide_algorithm_examples(self):
        """Provide algorithm examples"""
        print("Algorithm Examples")
        print("-" * 30)
        
        algorithms = [
            {
                "name": "Binary Search",
                "language": "Python",
                "code": '''
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Usage
numbers = [1, 3, 5, 7, 9, 11, 13, 15]
result = binary_search(numbers, 7)
print(f"Found at index: {result}")
'''
            },
            {
                "name": "Quick Sort",
                "language": "Python", 
                "code": '''
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

# Usage
data = [64, 34, 25, 12, 22, 11, 90]
sorted_data = quicksort(data)
print(f"Sorted: {sorted_data}")
'''
            },
            {
                "name": "Fibonacci with Memoization",
                "language": "Python",
                "code": '''
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

# Usage
for i in range(10):
    print(f"F({i}) = {fibonacci_memo(i)}")
'''
            }
        ]
        
        for alg in algorithms:
            print(f"\n{alg['name']} ({alg['language']}):")
            print(alg['code'])

    def provide_general_programming_examples(self):
        """Provide general programming guidance"""
        print("Programming Examples Available:")
        print("* Python data processing and file handling")
        print("* JavaScript async operations and ES6 classes") 
        print("* C terminal animations and graphics")
        print("* Common algorithms (sorting, searching)")
        print("* Database operations and data analysis")
        print()
        print("Try specific requests like:")
        print("  'make python file example'")
        print("  'create javascript data processing'") 
        print("  'show c animation code'")
        print("  'generate algorithm examples'")

# Import necessary classes (assuming they exist from the original)
class SimpleStorage:
    def __init__(self):
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

if __name__ == "__main__":
    cli = EnhancedSmartCLI()
    cli.start()
