#!/usr/bin/env python3

import json
import os
import re
import sqlite3
import subprocess
from eyes import analyze_string_patterns

class MoonLanguageBridge:
    def __init__(self):
        self.moon_interpreter_path = "./moon/main"
        self.language_bridges = {
            'python': self.bridge_python,
            'javascript': self.bridge_javascript,
            'sql': self.bridge_sql,
            'bash': self.bridge_bash,
            'json': self.bridge_json,
            'csv': self.bridge_csv,
            'moon': self.bridge_moon_native
        }
        
    def detect_language_context(self, data, user_input):
        language_indicators = {
            'python': ['def ', 'import ', 'class ', 'if __name__', '.py', 'print(', 'return ', 'elif ', 'lambda ', 'with ', 'as ', 'for ', 'while ', 'break ', 'continue '],
            'javascript': ['function ', 'var ', 'let ', 'const ', '.js', 'console.log', '=>', 'async ', 'await ', 'promise', 'callback', 'typeof ', 'instanceof '],
            'sql': ['SELECT ', 'INSERT ', 'CREATE TABLE', 'WHERE ', 'JOIN ', 'UPDATE ', 'DELETE ', 'ALTER ', 'DROP ', 'INDEX ', 'UNION ', 'GROUP BY', 'ORDER BY', 'HAVING '],
            'bash': ['#!/bin/bash', 'echo ', 'ls ', 'cd ', 'grep ', 'awk ', '$1', 'chmod ', 'mkdir ', 'rm ', 'mv ', 'cp ', 'find ', 'sed ', 'sort ', 'uniq '],
            'json': ['{', '}', '":', '[]', 'null', 'true', 'false', '"type":', '"value":', '"data":'],
            'csv': [',', 'headers', 'rows', '.csv', 'column', 'delimiter', 'separator'],
            'moon': ['start ', 'goto ', 'put ', ' in ', 'try', 'catch', 'end_', 'm ', 'p(', 'get(', 'read ', 'fish ', 'all ', 'hint ', 'export ', 'http ', 'stop', '___', '__', ':::', '<-', '# ']
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
    <- Moon native processing with full feature support
    moon_code = ___
{data}
___
    put moon_code in "moon_native.moon"
    
    if context.has_goto then
        put "goto_flow_detected" in "moon_metadata.txt"
    end_
    
    <- Check for advanced Moon features
    if moon_code contains "m " then
        put "function_definitions_detected" in "moon_functions.txt"
    end_
    
    if moon_code contains "fish " then
        put "selective_imports_detected" in "moon_imports.txt"
    end_
    
    if moon_code contains "http " then
        put "http_operations_detected" in "moon_http.txt"
    end_
    
    if moon_code contains "hint " then
        put "type_checking_detected" in "moon_types.txt"
    end_
    
    if moon_code contains "___" then
        put "multiline_strings_detected" in "moon_strings.txt"
    end_
    
    <- Process different comment styles
    if moon_code contains "#" then
        put "hash_comments_found" in "moon_comments.txt"
    end_
    
    if moon_code contains "<-" then
        put "arrow_comments_found" in "moon_comments.txt"
    end_
    
    if moon_code contains "__" then
        put "section_comments_found" in "moon_comments.txt"
    end_
    
    if moon_code contains ":::" then
        put "multiline_comments_found" in "moon_comments.txt"
    end_
    
    goto moon_processing_complete
catch moon_error
    put "Moon native error" in "error_log.txt"
    goto fallback_processing
end_
'''
    
    def generate_bridge_script(self, primary_lang, secondary_langs, data, context):
        bridge_script = f'''
start language_bridge_processing
    try
        put "Language bridge processing started" in "bridge_log.txt"
        primary_language = "{primary_lang}"
        secondary_count = {len(secondary_langs)}
        
        {self.language_bridges[primary_lang](data, context)}
        
'''
        
        for i, lang in enumerate(secondary_langs):
            bridge_script += f'''
start secondary_language_{i}
    secondary_lang = "{lang}"
    put secondary_lang in "secondary_languages.txt"
    {self.language_bridges[lang](data, context)}
'''
        
        bridge_script += f'''

start bridge_integration
    try
        final_results = {{
            "primary_language": "{primary_lang}",
            "secondary_languages": {secondary_langs},
            "bridge_status": "successful",
            "processing_complete": true
        }}
        
        put final_results in "bridge_results.txt"
        put "Language bridge integration completed successfully" in "completion_log.txt"
        goto processing_complete
        
    catch integration_error
        put "Bridge integration error" in "error_log.txt"
        goto emergency_processing
    end_

start emergency_processing
    put "Emergency processing mode activated" in "emergency_log.txt"
    goto processing_complete

start processing_complete
    put "All language bridges completed" in "final_completion_log.txt"
    
catch bridge_error
    put "Critical bridge error" in "critical_error_log.txt"
    goto emergency_processing
end_
'''
        
        return bridge_script
    
    def process_with_language_bridge(self, data, user_input):
        """Process data with language bridging capabilities"""
        
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
        
        bridge_script = self.generate_bridge_script(primary_lang, secondary_langs, data, context)
        
        try:
            if os.path.exists(self.moon_interpreter_path):
                result = subprocess.run(
                    [self.moon_interpreter_path],
                    input=bridge_script,
                    text=True,
                    capture_output=True,
                    timeout=10
                )
                
                moon_output = result.stdout
                bridge_success = "successful" in moon_output
                
                return {
                    'moon_output': moon_output,
                    'primary_language': primary_lang,
                    'secondary_languages': secondary_langs,
                    'language_scores': lang_scores,
                    'bridge_integration': bridge_success,
                    'context_analysis': context,
                    'recommendation': self.get_storage_recommendation(primary_lang, secondary_langs, context)
                }
            else:
                return self.fallback_bridge_assessment(primary_lang, secondary_langs, lang_scores, context)
                
        except Exception as e:
            print(f"Bridge processing error: {e}")
            return self.fallback_bridge_assessment(primary_lang, secondary_langs, lang_scores, context)
    
    def get_storage_recommendation(self, primary_lang, secondary_langs, context):
        """Generate storage recommendation based on language analysis"""
        
        if primary_lang == 'sql' or 'sql' in secondary_langs:
            return "SQL Database Storage"
        elif primary_lang == 'json' or 'json' in secondary_langs:
            return "NoSQL Document Storage"
        elif primary_lang == 'python' and context['complexity'] > 100:
            return "Python-Optimized Storage"
        elif primary_lang == 'javascript' and context['has_async']:
            return "Async-Compatible Storage"
        elif len(secondary_langs) > 2:
            return "Multi-Language Hybrid Storage"
        else:
            return "Adaptive Smart Storage"
    
    def fallback_bridge_assessment(self, primary_lang, secondary_langs, lang_scores, context):
        """Fallback when Moon interpreter is not available"""
        
        return {
            'moon_output': f"Fallback bridge assessment completed\nPrimary: {primary_lang}\nSecondary: {secondary_langs}",
            'primary_language': primary_lang,
            'secondary_languages': secondary_langs,
            'language_scores': lang_scores,
            'bridge_integration': False,
            'context_analysis': context,
            'recommendation': self.get_storage_recommendation(primary_lang, secondary_langs, context)
        }

def test_language_bridge():
    """Test the language bridge with various code samples"""
    
    bridge = MoonLanguageBridge()
    
    test_cases = [
        {
            'name': 'Advanced Moon Code',
            'data': '''
:::
Advanced Moon Language Demo
Multiple features and syntax variations
:::

__MAIN_SECTION__
<- Function definitions with Moon syntax
m calculate_sum(a, b) {
    result = a + b
    put result in "calculation_log.txt"
    return result
}

# Variable assignments and conditionals
user_age = get("Enter age: ")
hint user_age as number

if user_age >= 18 then
    p("Adult user")
    status = "adult"
else
    p("Minor user")  
    status = "minor"
end_

# File operations and error handling
try
    data = read("user_preferences.txt")
    if data != "" then
        p("Preferences loaded")
    else
        put "default_preferences" in "user_preferences.txt"
    end_
catch file_error
    p("File operation failed")
    goto error_handling
end_

# Advanced imports
fish calculate_sum, user_validation in "utilities.moon"
fish all in "constants.moon"

# HTTP operations (if supported)
http get "https://api.example.com/data" -> response_data
put response_data in "api_cache.txt"

# Multiline string processing
description = ___
This is a multiline description
that spans multiple lines
and preserves formatting
___

start error_handling
    p("Handling errors gracefully")
    stop

__END_SECTION__
''',
            'query': 'process advanced moon language features'
        },
        {
            'name': 'Python Function',
            'data': '''
def process_data(data):
    import json
    return json.loads(data)
''',
            'query': 'analyze this python function'
        },
        {
            'name': 'JavaScript with Async',
            'data': '''
async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}
''',
            'query': 'handle async javascript code'
        },
        {
            'name': 'SQL Query',
            'data': '''
SELECT users.name, orders.total 
FROM users 
JOIN orders ON users.id = orders.user_id 
WHERE orders.date > '2024-01-01'
''',
            'query': 'store this sql query'
        },
        {
            'name': 'Mixed Languages',
            'data': '''
#!/bin/bash
echo "Processing data..."
cat data.json | grep "user" | python3 -c "import json; print(json.load())"
''',
            'query': 'handle mixed bash python json'
        },
        {
            'name': 'JSON Data',
            'data': '''
{
    "users": [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ],
    "metadata": {
        "version": "1.0",
        "created": "2024-01-01"
    }
}
''',
            'query': 'process json structure'
        }
    ]
    
    print("Moon Language Bridge Testing")
    print("="*50)
    
    for test in test_cases:
        print(f"\nTest Case: {test['name']}")
        print("-" * 30)
        
        result = bridge.process_with_language_bridge(test['data'], test['query'])
        
        print(f"Primary Language: {result['primary_language']}")
        print(f"Secondary Languages: {result['secondary_languages']}")
        print(f"Language Scores: {result['language_scores']}")
        print(f"Bridge Integration: {result['bridge_integration']}")
        print(f"Context Analysis: {result['context_analysis']}")
        print(f"Storage Recommendation: {result['recommendation']}")
        
        if result['moon_output']:
            print(f"Moon Output Preview: {result['moon_output'][:100]}...")

if __name__ == "__main__":
    test_language_bridge()
