# Crissy Deutsch - Enhanced Regex Pattern Generator v2.0 - 2024, 2025
import re

def analyze_string_patterns(text):
    patterns = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?',
        'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        'date_mdy': r'\b(0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])[/-](\d{2,4})\b',
        'date_ymd': r'\b(\d{4})[/-](0?[1-9]|1[0-2])[/-](0?[1-9]|[12][0-9]|3[01])\b',
        'time_24h': r'\b([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?\b',
        'time_12h': r'\b(0?[1-9]|1[0-2]):[0-5][0-9](:[0-5][0-9])?(\s?[AaPp][Mm])\b',
        'social_security': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        'zip_code': r'\b\d{5}(-\d{4})?\b',
        'hex_color': r'#[0-9A-Fa-f]{6}\b',
        'mac_address': r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
        'uuid': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
        'hashtag': r'#\w+',
        'mention': r'@\w+',
        'html_tag': r'<[^>]+>',
        'markdown_link': r'\[([^\]]+)\]\(([^)]+)\)',
        'file_extension': r'\.\w{2,4}$',
        'version_number': r'\b\d+\.\d+(\.\d+)*\b',
        'currency': r'\$\d{1,3}(,\d{3})*(\.\d{2})?',
        'percentage': r'\d+(\.\d+)?%',
        'number_with_commas': r'\b\d{1,3}(,\d{3})+\b',
        'decimal_number': r'\b\d+\.\d+\b',
        'integer': r'\b\d+\b',
        'word': r'\b[A-Za-z]+\b',
        'alphanumeric': r'\b[A-Za-z0-9]+\b'
    }
    detected = []
    for pattern_name, pattern_regex in patterns.items():
        if re.search(pattern_regex, text, re.IGNORECASE):
            detected.append((pattern_name, pattern_regex))
    return detected

def create_flexible_pattern(text):
    escaped = re.escape(text)
    flexible = escaped.replace(r'\ ', r'\s+')
    flexible = re.sub(r'\\(\d)', r'\\d', flexible)
    flexible = re.sub(r'\\([A-Za-z])', r'[A-Za-z]', flexible)
    flexible = re.sub(r'\\\(', r'\\(', flexible)
    flexible = re.sub(r'\\\)', r'\\)', flexible)
    return flexible

def create_extraction_pattern(text):
    words = text.split()
    if len(words) == 1:
        return rf'\b{re.escape(text)}\b'
    pattern_parts = []
    for word in words:
        if word.isdigit():
            pattern_parts.append(r'\d+')
        elif word.isalpha():
            pattern_parts.append(r'[A-Za-z]+')
        elif any(c.isdigit() for c in word) and any(c.isalpha() for c in word):
            pattern_parts.append(r'[A-Za-z0-9]+')
        else:
            pattern_parts.append(re.escape(word))
    return r'\s+'.join(pattern_parts)

def create_replacement_pattern(text, replacement=''):
    return f"re.sub(r'{re.escape(text)}', '{replacement}', text, flags=re.IGNORECASE)"

def create_search_pattern(text):
    return f"re.search(r'{re.escape(text)}', text, re.IGNORECASE)"

def create_findall_pattern(text):
    flexible = create_flexible_pattern(text)
    return f"re.findall(r'{flexible}', text, re.IGNORECASE)"

def create_match_pattern(text):
    return f"re.match(r'^{re.escape(text)}', text, re.IGNORECASE)"

def create_split_pattern(text):
    return f"re.split(r'{re.escape(text)}', text)"

def generate_advanced_patterns(text, var_name="text"):
    patterns = {}
    
    # Auto-detect known patterns
    detected = analyze_string_patterns(text)
    if detected:
        patterns['detected_patterns'] = detected
    
    # Basic patterns
    patterns['exact_match'] = f"{var_name}_match = re.search(r'{re.escape(text)}', {var_name}, re.IGNORECASE)"
    patterns['flexible_match'] = f"{var_name}_flexible = re.search(r'{create_flexible_pattern(text)}', {var_name}, re.IGNORECASE)"
    patterns['word_boundary'] = f"{var_name}_word = re.search(r'\\b{re.escape(text)}\\b', {var_name}, re.IGNORECASE)"
    
    # Extraction patterns
    patterns['extract_similar'] = f"{var_name}_extract = re.findall(r'{create_extraction_pattern(text)}', {var_name}, re.IGNORECASE)"
    
    # Replacement patterns
    patterns['remove_text'] = f"{var_name}_clean = re.sub(r'{re.escape(text)}', '', {var_name}, flags=re.IGNORECASE)"
    patterns['replace_with'] = f"{var_name}_replaced = re.sub(r'{re.escape(text)}', 'REPLACEMENT', {var_name}, flags=re.IGNORECASE)"
    
    # Advanced patterns
    patterns['case_insensitive'] = f"{var_name}_ci = re.search(r'(?i){re.escape(text)}', {var_name})"
    patterns['multiline'] = f"{var_name}_ml = re.search(r'^{re.escape(text)}$', {var_name}, re.MULTILINE)"
    patterns['dotall'] = f"{var_name}_dot = re.search(r'{re.escape(text)}', {var_name}, re.DOTALL)"
    
    # Split patterns
    patterns['split_by'] = f"{var_name}_split = re.split(r'{re.escape(text)}', {var_name})"
    
    # Validation patterns
    patterns['starts_with'] = f"{var_name}_starts = re.match(r'^{re.escape(text)}', {var_name}, re.IGNORECASE)"
    patterns['ends_with'] = f"{var_name}_ends = re.search(r'{re.escape(text)}$', {var_name}, re.IGNORECASE)"
    patterns['contains_only'] = f"{var_name}_only = re.match(r'^{re.escape(text)}+$', {var_name}, re.IGNORECASE)"
    
    return patterns

def interactive_pattern_builder():
    print("Enhanced Regex Pattern Generator v2.0")
    print("=" * 50)
    print("Features:")
    print("• Auto-detects common patterns (email, phone, URL, etc.)")
    print("• Generates multiple pattern variations")
    print("• Creates search, replace, extract, and validation patterns")
    print("• Supports custom variable names")
    print("\nUsage: text|variable_name (or just text)")
    print("Commands: 'help', 'examples', 'q' to quit\n")
    
    while True:
        try:
            user_input = input("Enter pattern: ").strip()
            
            if user_input.lower() == 'q':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("\nHelp:")
                print("• 'hello world' - generates patterns for exact text")
                print("• 'user@email.com|email_var' - custom variable name")
                print("• 'examples' - see sample patterns")
                print("• Auto-detects: emails, phones, URLs, dates, etc.\n")
                continue
            elif user_input.lower() == 'examples':
                print("\nExamples:")
                examples = [
                    "john@example.com",
                    "123-45-6789",
                    "(555) 123-4567", 
                    "https://github.com",
                    "2024-01-15",
                    "#python",
                    "@username",
                    "$1,234.56"
                ]
                for ex in examples:
                    detected = analyze_string_patterns(ex)
                    if detected:
                        print(f"  '{ex}' → {', '.join([d[0] for d in detected])}")
                print()
                continue
            
            if '|' in user_input:
                text, var_name = user_input.split('|', 1)
                text, var_name = text.strip(), var_name.strip()
            else:
                text = user_input
                var_name = "text"
            
            if not text:
                print("Please enter some text\n")
                continue
                
            print(f"\nAnalyzing: '{text}'")
            print("=" * 60)
            
            patterns = generate_advanced_patterns(text, var_name)
            
            # Show detected patterns first
            if 'detected_patterns' in patterns:
                print("AUTO-DETECTED PATTERNS:")
                for pattern_name, pattern_regex in patterns['detected_patterns']:
                    print(f"  {pattern_name.upper()}: {pattern_regex}")
                print()
            
            print("GENERATED PATTERNS:")
            pattern_categories = {
                'Basic Matching': ['exact_match', 'flexible_match', 'word_boundary'],
                'Extraction': ['extract_similar'],
                'Replacement': ['remove_text', 'replace_with'],
                'Validation': ['starts_with', 'ends_with', 'contains_only'],
                'Advanced': ['case_insensitive', 'multiline', 'dotall', 'split_by']
            }
            
            for category, pattern_keys in pattern_categories.items():
                print(f"\n  {category}:")
                for key in pattern_keys:
                    if key in patterns:
                        print(f"    • {patterns[key]}")
            
            print("\n" + "=" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

def main():
    interactive_pattern_builder()

if __name__ == "__main__": main()
