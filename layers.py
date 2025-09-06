import re
import math
from typing import Dict, Any, List
from sigmoid import sigmoid, multi_layer_sigmoid

PATTERNS = {k: re.compile(v) for k, v in {
    'phone': r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'date': r'^\d{4}-\d{2}-\d{2}$|^\d{2}/\d{2}/\d{4}$',
    'boolean': r'^(true|false|yes|no|1|0)$',
    'country': r'^[A-Z]{2}$',
    'url': r'^https?://[^\s/$.?#].[^\s]*$',
    'ipv4': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    'credit_card': r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3[0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$',
    'ssn': r'^\d{3}-\d{2}-\d{4}$',
    'zipcode': r'^\d{5}(-\d{4})?$',
    'currency': r'^\$?[\d,]+\.?\d{0,2}$',
    'percentage': r'^\d+(\.\d+)?%$',
    'time': r'^([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$',
    'hex_color': r'^#[0-9a-fA-F]{6}$'
}.items()}
PATTERNS['boolean'] = re.compile(PATTERNS['boolean'].pattern, re.IGNORECASE)

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
        
    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    length = len(text)
    entropy = 0.0
    for count in char_counts.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy

def analyze_character_patterns(text: str) -> Dict[str, float]:
    if not text:
        return {}
    
    length = len(text)
    patterns = {
        'digit_ratio': sum(1 for c in text if c.isdigit()) / length,
        'alpha_ratio': sum(1 for c in text if c.isalpha()) / length,
        'upper_ratio': sum(1 for c in text if c.isupper()) / length,
        'lower_ratio': sum(1 for c in text if c.islower()) / length,
        'special_ratio': sum(1 for c in text if not c.isalnum()) / length,
        'space_ratio': sum(1 for c in text if c.isspace()) / length,
        'entropy': calculate_entropy(text),
        'length_factor': min(length / 50.0, 1.0),
        'consecutive_digits': max([len(s) for s in re.findall(r'\d+', text)] + [0]) / length,
        'consecutive_alpha': max([len(s) for s in re.findall(r'[a-zA-Z]+', text)] + [0]) / length
    }
    
    return patterns

def get_context_bias(text: str, field_name: str = "") -> Dict[str, float]:
    context_bias = {}
    text_lower = text.lower()
    field_lower = field_name.lower()
    
    sensitive_keywords = ['password', 'pass', 'pwd', 'secret', 'token', 'key', 'auth']
    personal_keywords = ['name', 'fname', 'lname', 'firstname', 'lastname', 'full']
    contact_keywords = ['email', 'mail', 'phone', 'tel', 'mobile', 'contact']
    address_keywords = ['address', 'street', 'city', 'state', 'zip', 'postal']
    financial_keywords = ['price', 'cost', 'amount', 'salary', 'income', 'balance']
    
    context_bias['sensitive'] = 1.0 if any(kw in field_lower for kw in sensitive_keywords) else 0.0
    context_bias['personal'] = 1.0 if any(kw in field_lower for kw in personal_keywords) else 0.0
    context_bias['contact'] = 1.0 if any(kw in field_lower for kw in contact_keywords) else 0.0
    context_bias['address'] = 1.0 if any(kw in field_lower for kw in address_keywords) else 0.0
    context_bias['financial'] = 1.0 if any(kw in field_lower for kw in financial_keywords) else 0.0
    
    if '@' in text and '.' in text:
        context_bias['email_structure'] = 1.0
    else:
        context_bias['email_structure'] = 0.0
    
    if any(char.isdigit() for char in text) and len(text) >= 7:
        context_bias['phone_structure'] = 1.0
    else:
        context_bias['phone_structure'] = 0.0
    
    return context_bias

def deep_confidence_analysis(the_input: Any, use_deep_layers: bool = True, field_name: str = "") -> Dict[str, float]:
    if not isinstance(the_input, str):
        return {"primary": 1.0}
    
    input_str = str(the_input).strip()
    confidence_scores = {}
    
    char_patterns = analyze_character_patterns(input_str)
    context_bias = get_context_bias(input_str, field_name)
    
    if use_deep_layers:
        email_layers = [
            {'weight': 2.2, 'bias': 0.6 + context_bias.get('email_structure', 0) * 0.4},
            {'weight': 1.7, 'bias': -0.1 + context_bias.get('contact', 0) * 0.3},
            {'weight': 1.3, 'bias': 0.15 + char_patterns.get('special_ratio', 0) * 0.2}
        ]
        phone_layers = [
            {'weight': 2.0, 'bias': 0.4 + context_bias.get('phone_structure', 0) * 0.5},
            {'weight': 1.6, 'bias': 0.0 + char_patterns.get('digit_ratio', 0) * 0.3},
            {'weight': 1.2, 'bias': 0.25 + context_bias.get('contact', 0) * 0.2}
        ]
        country_layers = [
            {'weight': 2.5, 'bias': 0.5 + char_patterns.get('upper_ratio', 0) * 0.3},
            {'weight': 1.4, 'bias': 0.1 + char_patterns.get('length_factor', 0) * 0.2}
        ]
        boolean_layers = [
            {'weight': 3.2, 'bias': 0.3},
            {'weight': 1.8, 'bias': -0.2 + char_patterns.get('alpha_ratio', 0) * 0.4}
        ]
        url_layers = [
            {'weight': 2.8, 'bias': 0.4},
            {'weight': 1.5, 'bias': 0.2}
        ]
        ipv4_layers = [
            {'weight': 3.0, 'bias': 0.5 + char_patterns.get('digit_ratio', 0) * 0.3},
            {'weight': 1.6, 'bias': 0.1}
        ]
        uuid_layers = [
            {'weight': 3.5, 'bias': 0.6},
            {'weight': 1.9, 'bias': 0.0}
        ]
        credit_card_layers = [
            {'weight': 3.8, 'bias': 0.7 + context_bias.get('financial', 0) * 0.3},
            {'weight': 2.0, 'bias': 0.2 + char_patterns.get('digit_ratio', 0) * 0.4}
        ]
        currency_layers = [
            {'weight': 2.6, 'bias': 0.4 + context_bias.get('financial', 0) * 0.4},
            {'weight': 1.4, 'bias': 0.1}
        ]
        time_layers = [
            {'weight': 2.3, 'bias': 0.3},
            {'weight': 1.3, 'bias': 0.1}
        ]
        date_layers = [
            {'weight': 2.1, 'bias': 0.2},
            {'weight': 1.4, 'bias': 0.1}
        ]
        personal_layers = [
            {'weight': 1.8, 'bias': 0.2 + context_bias.get('personal', 0) * 0.5},
            {'weight': 1.2, 'bias': 0.0 + char_patterns.get('alpha_ratio', 0) * 0.3}
        ]
    else:
        email_layers = [{'weight': 1.0, 'bias': 0.0}]
        phone_layers = [{'weight': 1.0, 'bias': 0.0}]
        country_layers = [{'weight': 1.0, 'bias': 0.0}]
        boolean_layers = [{'weight': 1.0, 'bias': 0.0}]
        url_layers = [{'weight': 1.0, 'bias': 0.0}]
        ipv4_layers = [{'weight': 1.0, 'bias': 0.0}]
        uuid_layers = [{'weight': 1.0, 'bias': 0.0}]
        credit_card_layers = [{'weight': 1.0, 'bias': 0.0}]
        currency_layers = [{'weight': 1.0, 'bias': 0.0}]
        time_layers = [{'weight': 1.0, 'bias': 0.0}]
        date_layers = [{'weight': 1.0, 'bias': 0.0}]
        personal_layers = [{'weight': 1.0, 'bias': 0.0}]
    
    if PATTERNS['boolean'].match(input_str):
        confidence_scores['boolean'] = multi_layer_sigmoid(5.0, boolean_layers)
    
    if PATTERNS['email'].match(input_str):
        base_score = 4.8 + char_patterns.get('special_ratio', 0) * 2.0
        confidence_scores['email'] = multi_layer_sigmoid(base_score, email_layers)
    
    if PATTERNS['phone'].match(input_str):
        base_score = 4.7 + char_patterns.get('digit_ratio', 0) * 1.5
        confidence_scores['phone'] = multi_layer_sigmoid(base_score, phone_layers)
    
    if PATTERNS['country'].match(input_str):
        base_score = 4.2 + char_patterns.get('upper_ratio', 0) * 1.0
        confidence_scores['country'] = multi_layer_sigmoid(base_score, country_layers)
    
    if PATTERNS['url'].match(input_str):
        confidence_scores['url'] = multi_layer_sigmoid(4.5, url_layers)
    
    if PATTERNS['ipv4'].match(input_str):
        base_score = 4.9 + char_patterns.get('digit_ratio', 0) * 1.0
        confidence_scores['ipv4'] = multi_layer_sigmoid(base_score, ipv4_layers)
    
    if PATTERNS['uuid'].match(input_str.lower()):
        confidence_scores['uuid'] = multi_layer_sigmoid(5.2, uuid_layers)
    
    if PATTERNS['credit_card'].match(input_str.replace(' ', '').replace('-', '')):
        base_score = 5.0 + context_bias.get('financial', 0) * 1.5
        confidence_scores['credit_card'] = multi_layer_sigmoid(base_score, credit_card_layers)
    
    if PATTERNS['ssn'].match(input_str):
        base_score = 4.8 + context_bias.get('personal', 0) * 1.0
        confidence_scores['ssn'] = multi_layer_sigmoid(base_score, personal_layers)
    
    if PATTERNS['zipcode'].match(input_str):
        base_score = 4.0 + context_bias.get('address', 0) * 1.2
        confidence_scores['zipcode'] = multi_layer_sigmoid(base_score, personal_layers)
    
    if PATTERNS['currency'].match(input_str):
        base_score = 4.3 + context_bias.get('financial', 0) * 1.5
        confidence_scores['currency'] = multi_layer_sigmoid(base_score, currency_layers)
    
    if PATTERNS['percentage'].match(input_str):
        confidence_scores['percentage'] = multi_layer_sigmoid(4.1, currency_layers)
    
    if PATTERNS['time'].match(input_str):
        confidence_scores['time'] = multi_layer_sigmoid(4.2, time_layers)
    
    if PATTERNS['date'].match(input_str):
        confidence_scores['date'] = multi_layer_sigmoid(4.0, date_layers)
    
    if PATTERNS['hex_color'].match(input_str):
        confidence_scores['hex_color'] = multi_layer_sigmoid(4.4, uuid_layers)
    
    entropy_factor = char_patterns.get('entropy', 0)
    if entropy_factor > 3.5:
        base_score = 2.5 + (entropy_factor - 3.5) * 0.5
        confidence_scores['encoded'] = multi_layer_sigmoid(base_score, uuid_layers)
    
    if char_patterns.get('alpha_ratio', 0) > 0.8 and len(input_str) > 2:
        base_score = 2.0 + char_patterns.get('alpha_ratio', 0) * 1.5 + context_bias.get('personal', 0) * 2.0
        confidence_scores['name'] = multi_layer_sigmoid(base_score, personal_layers)
    
    if not confidence_scores:
        base_score = 1.2 + char_patterns.get('alpha_ratio', 0) * 0.8
        confidence_scores['text'] = multi_layer_sigmoid(base_score, [{'weight': 0.9, 'bias': 0.0}])
    
    return confidence_scores
