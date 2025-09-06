import re
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    KEYWORD = "KEYWORD"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    CURRENCY = "CURRENCY"
    TIME_UNIT = "TIME_UNIT"
    DATE = "DATE"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    position: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        
        self.keywords = {
            'worked', 'hours', 'per', 'hour', 'week', 'month', 'year', 'day',
            'salary', 'wage', 'pay', 'paid', 'earned', 'overtime', 'rate',
            'employee', 'staff', 'worker', 'person', 'user', 'at', 'for',
            'total', 'amount', 'sum', 'calculate', 'add', 'store', 'save'
        }
        
        self.time_units = {
            'hour', 'hours', 'hr', 'hrs', 'day', 'days', 'week', 'weeks',
            'month', 'months', 'year', 'years', 'minute', 'minutes', 'min'
        }
        
        self.currency_symbols = {'$', '£', '€', '¥', 'usd', 'gbp', 'eur', 'dollar', 'dollars'}
        
    def advance(self):
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.position]
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_number(self):
        start_pos = self.position
        result = ''
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        
        return Token(TokenType.NUMBER, result, start_pos)
    
    def read_identifier(self):
        start_pos = self.position
        result = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char in '_@.-'):
            result += self.current_char
            self.advance()
        
        if self.is_email(result):
            return Token(TokenType.EMAIL, result, start_pos)
        elif self.is_phone(result):
            return Token(TokenType.PHONE, result, start_pos)
        elif self.is_date(result):
            return Token(TokenType.DATE, result, start_pos)
        elif result.lower() in self.keywords:
            return Token(TokenType.KEYWORD, result.lower(), start_pos)
        elif result.lower() in self.time_units:
            return Token(TokenType.TIME_UNIT, result.lower(), start_pos)
        elif result.lower() in self.currency_symbols:
            return Token(TokenType.CURRENCY, result.lower(), start_pos)
        else:
            return Token(TokenType.IDENTIFIER, result, start_pos)
    
    def read_string(self):
        start_pos = self.position
        quote_char = self.current_char
        result = ''
        self.advance()
        
        while self.current_char and self.current_char != quote_char:
            result += self.current_char
            self.advance()
        
        if self.current_char == quote_char:
            self.advance()
        
        return Token(TokenType.STRING, result, start_pos)
    
    def is_email(self, text):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, text) is not None
    
    def is_phone(self, text):
        pattern = r'^[\+]?[1-9]?[\-\s\(\)]?[\d\-\s\(\)]{7,15}$'
        return re.match(pattern, text) is not None
    
    def is_date(self, text):
        patterns = [
            r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$',
            r'^\d{4}[/-]\d{1,2}[/-]\d{1,2}$',
            r'^\d{1,2}[/-]\d{1,2}$'
        ]
        return any(re.match(pattern, text) for pattern in patterns)
    
    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.read_number()
            
            if self.current_char.isalpha() or self.current_char in '_@':
                return self.read_identifier()
            
            if self.current_char in '"\'':
                return self.read_string()
            
            if self.current_char == '$':
                pos = self.position
                self.advance()
                return Token(TokenType.CURRENCY, '$', pos)
            
            if self.current_char in '+-*/=<>!':
                pos = self.position
                char = self.current_char
                self.advance()
                return Token(TokenType.OPERATOR, char, pos)
            
            if self.current_char in '()[]{},.;:':
                pos = self.position
                char = self.current_char
                self.advance()
                return Token(TokenType.DELIMITER, char, pos)
            
            self.advance()
        
        return Token(TokenType.EOF, '', self.position)
    
    def tokenize(self):
        tokens = []
        token = self.get_next_token()
        
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        
        tokens.append(token)
        return tokens

@dataclass
class ParsedData:
    data_type: str
    entities: Dict[str, Any]
    relationships: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else Token(TokenType.EOF, '', 0)
    
    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(TokenType.EOF, '', len(self.tokens))
    
    def peek(self, offset=1):
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return Token(TokenType.EOF, '', len(self.tokens))
    
    def consume(self, expected_type):
        if self.current_token.type == expected_type:
            token = self.current_token
            self.advance()
            return token
        return None
    
    def parse(self):
        if self.is_payroll_data():
            return self.parse_payroll()
        elif self.is_employee_data():
            return self.parse_employee()
        elif self.is_mathematical_expression():
            return self.parse_math()
        elif self.is_contact_data():
            return self.parse_contact()
        else:
            return self.parse_generic()
    
    def is_payroll_data(self):
        keywords = ['worked', 'hours', 'hour', 'pay', 'salary', 'wage', 'rate']
        token_values = [token.value.lower() for token in self.tokens]
        return any(keyword in token_values for keyword in keywords)
    
    def is_employee_data(self):
        keywords = ['employee', 'staff', 'worker', 'person']
        token_values = [token.value.lower() for token in self.tokens]
        return any(keyword in token_values for keyword in keywords)
    
    def is_mathematical_expression(self):
        has_numbers = any(token.type == TokenType.NUMBER for token in self.tokens)
        has_operators = any(token.type == TokenType.OPERATOR for token in self.tokens)
        return has_numbers and has_operators
    
    def is_contact_data(self):
        return any(token.type in [TokenType.EMAIL, TokenType.PHONE] for token in self.tokens)
    
    def parse_payroll(self):
        entities = {}
        relationships = []
        
        name = None
        hours = None
        rate = None
        currency = '$'
        period = 'week'
        
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            
            if token.type == TokenType.IDENTIFIER and not name:
                name = token.value
            
            elif token.type == TokenType.NUMBER:
                if i + 1 < len(self.tokens):
                    next_token = self.tokens[i + 1]
                    if next_token.type == TokenType.TIME_UNIT or next_token.value.lower() in ['hour', 'hours']:
                        hours = float(token.value)
                    elif (i > 0 and self.tokens[i - 1].type == TokenType.CURRENCY) or \
                         (i + 1 < len(self.tokens) and self.tokens[i + 1].value.lower() in ['dollar', 'dollars']):
                        rate = float(token.value)
            
            elif token.type == TokenType.CURRENCY:
                currency = token.value
            
            i += 1
        
        entities = {
            'employee_name': name,
            'hours_worked': hours,
            'hourly_rate': rate,
            'currency': currency,
            'pay_period': period
        }
        
        if hours and rate:
            total_pay = hours * rate
            entities['total_pay'] = total_pay
            relationships.append({
                'type': 'calculation',
                'formula': 'hours_worked * hourly_rate',
                'result': total_pay
            })
        
        return ParsedData(
            data_type='payroll',
            entities=entities,
            relationships=relationships,
            metadata={'confidence': 0.9, 'completeness': len([v for v in entities.values() if v is not None]) / len(entities)}
        )
    
    def parse_employee(self):
        entities = {}
        name = None
        role = None
        
        for token in self.tokens:
            if token.type == TokenType.IDENTIFIER and not name:
                name = token.value
            elif token.value.lower() in ['manager', 'developer', 'analyst', 'clerk']:
                role = token.value
        
        entities = {
            'name': name,
            'role': role
        }
        
        return ParsedData(
            data_type='employee',
            entities=entities,
            relationships=[],
            metadata={'confidence': 0.8}
        )
    
    def parse_math(self):
        expression = ' '.join(token.value for token in self.tokens if token.type != TokenType.EOF)
        
        return ParsedData(
            data_type='mathematical',
            entities={'expression': expression},
            relationships=[],
            metadata={'confidence': 0.95}
        )
    
    def parse_contact(self):
        entities = {}
        
        for token in self.tokens:
            if token.type == TokenType.EMAIL:
                entities['email'] = token.value
            elif token.type == TokenType.PHONE:
                entities['phone'] = token.value
            elif token.type == TokenType.IDENTIFIER:
                entities['name'] = token.value
        
        return ParsedData(
            data_type='contact',
            entities=entities,
            relationships=[],
            metadata={'confidence': 0.85}
        )
    
    def parse_generic(self):
        text_content = ' '.join(token.value for token in self.tokens if token.type not in [TokenType.EOF, TokenType.DELIMITER])
        
        return ParsedData(
            data_type='text',
            entities={'content': text_content},
            relationships=[],
            metadata={'confidence': 0.6}
        )

class DataStructurer:
    def __init__(self):
        self.schema_templates = {
            'payroll': {
                'table_name': 'payroll_records',
                'fields': {
                    'employee_name': 'VARCHAR(100)',
                    'hours_worked': 'DECIMAL(5,2)',
                    'hourly_rate': 'DECIMAL(8,2)',
                    'total_pay': 'DECIMAL(10,2)',
                    'currency': 'VARCHAR(10)',
                    'pay_period': 'VARCHAR(20)',
                    'created_at': 'TIMESTAMP'
                }
            },
            'employee': {
                'table_name': 'employees',
                'fields': {
                    'name': 'VARCHAR(100)',
                    'role': 'VARCHAR(50)',
                    'created_at': 'TIMESTAMP'
                }
            },
            'contact': {
                'table_name': 'contacts',
                'fields': {
                    'name': 'VARCHAR(100)',
                    'email': 'VARCHAR(255)',
                    'phone': 'VARCHAR(20)',
                    'created_at': 'TIMESTAMP'
                }
            }
        }
    
    def structure_data(self, parsed_data: ParsedData):
        if parsed_data.data_type in self.schema_templates:
            schema = self.schema_templates[parsed_data.data_type]
            structured = {
                'schema': schema,
                'data': parsed_data.entities,
                'storage_recommendation': self.recommend_storage(parsed_data),
                'indexing_strategy': self.recommend_indexing(parsed_data)
            }
            return structured
        else:
            return {
                'schema': {'table_name': 'generic_data', 'fields': {'content': 'TEXT'}},
                'data': parsed_data.entities,
                'storage_recommendation': 'document_store',
                'indexing_strategy': 'full_text'
            }
    
    def recommend_storage(self, parsed_data: ParsedData):
        if parsed_data.data_type in ['payroll', 'employee', 'contact']:
            return 'relational_database'
        elif parsed_data.data_type == 'mathematical':
            return 'computational_store'
        else:
            return 'document_store'
    
    def recommend_indexing(self, parsed_data: ParsedData):
        if 'employee_name' in parsed_data.entities or 'name' in parsed_data.entities:
            return ['name_index', 'timestamp_index']
        elif parsed_data.data_type == 'mathematical':
            return ['expression_hash']
        else:
            return ['full_text_index']

class LanguageProcessor:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.structurer = DataStructurer()
    
    def process(self, input_text: str):
        self.lexer = Lexer(input_text)
        tokens = self.lexer.tokenize()
        
        self.parser = Parser(tokens)
        parsed_data = self.parser.parse()
        
        # Enhanced domain classification
        domain = self.classify_data_domain(tokens, parsed_data)
        parsed_data.metadata['domain'] = domain
        
        structured_data = self.structurer.structure_data(parsed_data)
        
        return {
            'tokens': [{'type': t.type.value, 'value': t.value, 'position': t.position} for t in tokens[:-1]],
            'parsed': {
                'data_type': parsed_data.data_type,
                'entities': parsed_data.entities,
                'relationships': parsed_data.relationships,
                'metadata': parsed_data.metadata,
                'domain': domain
            },
            'structured': structured_data
        }
    
    def classify_data_domain(self, tokens, parsed_data):
        """Classify data domain using expanded vocabulary knowledge"""
        token_values = [t.value.lower() for t in tokens if t.type != TokenType.EOF]
        
        business_indicators = {
            'employee', 'staff', 'worker', 'personnel', 'payroll', 'salary', 'wage', 'hourly',
            'overtime', 'benefits', 'compensation', 'department', 'manager', 'supervisor',
            'customer', 'client', 'revenue', 'profit', 'invoice', 'payment', 'order', 'business',
            'commercial', 'corporate', 'company', 'organization'
        }
        
        tech_indicators = {
            'database', 'query', 'sql', 'api', 'framework', 'library', 'algorithm', 'code',
            'programming', 'development', 'software', 'application', 'system', 'technology',
            'function', 'class', 'method', 'variable', 'array', 'object', 'technical'
        }
        
        education_indicators = {
            'student', 'teacher', 'course', 'class', 'grade', 'exam', 'education', 'school',
            'university', 'college', 'learning', 'curriculum', 'degree', 'certificate',
            'academic', 'educational', 'instructor', 'professor'
        }
        
        medical_indicators = {
            'patient', 'doctor', 'medical', 'health', 'hospital', 'treatment', 'diagnosis',
            'medicine', 'healthcare', 'clinical', 'therapy', 'symptom', 'physician'
        }
        
        financial_indicators = {
            'money', 'dollar', 'cost', 'price', 'budget', 'expense', 'income', 'tax',
            'financial', 'accounting', 'banking', 'investment', 'credit', 'debit',
            'transaction', 'economic', 'fiscal', 'monetary'
        }
        
        # Calculate domain scores
        business_score = len(set(token_values) & business_indicators)
        tech_score = len(set(token_values) & tech_indicators)
        education_score = len(set(token_values) & education_indicators)
        medical_score = len(set(token_values) & medical_indicators)
        financial_score = len(set(token_values) & financial_indicators)
        
        # Determine primary domain
        scores = {
            'business': business_score,
            'technology': tech_score,
            'education': education_score,
            'medical': medical_score,
            'financial': financial_score
        }
        
        max_score = max(scores.values())
        if max_score > 0:
            return max(scores, key=scores.get)
        
        return 'general'
