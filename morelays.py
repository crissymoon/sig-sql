
import sqlite3
import re
import sys
import countries
import math
from typing import List, Dict, Any, Optional

DB_NAME = "cis261_db.db"
PATTERNS = {k: re.compile(v) for k, v in {
    'phone': r'^\+?1?[-.\s]?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'date': r'^\d{4}-\d{2}-\d{2}$|^\d{2}/\d{2}/\d{4}$',
    'boolean': r'^(true|false|yes|no|1|0)$',
    'country': r'^[A-Z]{2}$'
}.items()}
PATTERNS['boolean'] = re.compile(PATTERNS['boolean'].pattern, re.IGNORECASE)
_country_cache = {}

def sigmoid(x: float) -> float:
    try:
        clamped_x = max(-500, min(500, x))
        return 1 / (1 + math.exp(-clamped_x))
    except (OverflowError, ValueError, ZeroDivisionError):
        return 0.0 if x < 0 else 1.0

def multi_layer_sigmoid(x: float, layers: List[Dict[str, float]]) -> float:
    current_value = x
    for layer in layers:
        weight = layer.get('weight', 1.0)
        bias = layer.get('bias', 0.0)
        current_value = sigmoid(current_value * weight + bias)
    return current_value

def deep_confidence_analysis(the_input: Any, use_deep_layers: bool = True) -> Dict[str, float]:
    if not isinstance(the_input, str):
        return {"primary": 1.0}
    
    input_str = str(the_input).strip()
    confidence_scores = {}
    
    if use_deep_layers:
        email_layers = [
            {'weight': 2.0, 'bias': 0.5},
            {'weight': 1.5, 'bias': -0.2},
            {'weight': 1.2, 'bias': 0.1}
        ]
        phone_layers = [
            {'weight': 1.8, 'bias': 0.3},
            {'weight': 1.4, 'bias': -0.1},
            {'weight': 1.1, 'bias': 0.2}
        ]
        country_layers = [
            {'weight': 2.2, 'bias': 0.4},
            {'weight': 1.3, 'bias': 0.0}
        ]
        boolean_layers = [
            {'weight': 3.0, 'bias': 0.2},
            {'weight': 1.6, 'bias': -0.3}
        ]
    else:
        email_layers = [{'weight': 1.0, 'bias': 0.0}]
        phone_layers = [{'weight': 1.0, 'bias': 0.0}]
        country_layers = [{'weight': 1.0, 'bias': 0.0}]
        boolean_layers = [{'weight': 1.0, 'bias': 0.0}]
    
    if PATTERNS['boolean'].match(input_str):
        confidence_scores['boolean'] = multi_layer_sigmoid(5.0, boolean_layers)
    
    if normalize_country_code(input_str):
        confidence_scores['country'] = multi_layer_sigmoid(4.0, country_layers)
    
    phone_formatted = format_phone_number(input_str)
    if phone_formatted:
        confidence_scores['phone'] = multi_layer_sigmoid(4.5, phone_layers)
    
    if PATTERNS['email'].match(input_str):
        confidence_scores['email'] = multi_layer_sigmoid(4.5, email_layers)
    
    if PATTERNS['date'].match(input_str):
        confidence_scores['date'] = multi_layer_sigmoid(3.0, [{'weight': 1.5, 'bias': 0.1}])
    
    if not confidence_scores:
        confidence_scores['text'] = multi_layer_sigmoid(1.0, [{'weight': 0.8, 'bias': 0.0}])
    
    return confidence_scores

def format_phone_number(phone_str: str) -> Optional[str]:
    if not isinstance(phone_str, str):
        return None
    
    match = PATTERNS['phone'].match(phone_str.strip())
    if match:
        area, exchange, number = match.groups()
        formatted = f"({area}) {exchange}-{number}"
        confidence = sigmoid(4.0)
        return formatted if confidence > 0.8 else None
    return None

def calculate_type_confidence(the_input: Any) -> Dict[str, float]:
    return deep_confidence_analysis(the_input, use_deep_layers=True)

def normalize_country_code(country_input: str) -> Optional[str]:
    if not country_input or not isinstance(country_input, str):
        return None
    country_clean = country_input.strip()
    if country_clean in _country_cache:
        return _country_cache[country_clean]
    
    country_lower = country_clean.lower()
    
    for attempt in [
        lambda: countries.get(country_clean) if len(country_clean) == 2 and country_clean.isupper() else None,
        lambda: countries.get(country_lower.upper()) if len(country_lower) == 2 else None,
        lambda: countries.get(name=country_clean.title()),
        lambda: next((c for c in countries if country_lower in [c.name.lower(), c.alpha2.lower(), c.alpha3.lower()] or 
                     (hasattr(c, 'common_name') and c.common_name and country_lower == c.common_name.lower())), None)
    ]:
        try:
            country_obj = attempt()
            if country_obj:
                _country_cache[country_clean] = country_obj.alpha2
                return country_obj.alpha2
        except Exception:
            continue
    
    _country_cache[country_clean] = None
    return None

def detect_type(the_input: Any) -> str:
    if isinstance(the_input, (bool, int, float)):
        return {bool: "BOOLEAN", int: "INTEGER", float: "REAL"}[type(the_input)]
    
    if isinstance(the_input, str):
        confidence_scores = calculate_type_confidence(the_input)
        
        if 'boolean' in confidence_scores and confidence_scores['boolean'] > 0.8:
            return "BOOLEAN"
        if 'country' in confidence_scores and confidence_scores['country'] > 0.8:
            return "TEXT"
        
        type_mappings = {
            'phone': "TEXT NOT NULL",
            'email': "TEXT UNIQUE", 
            'date': "DATE",
            'country': "TEXT"
        }
        
        for pattern_type, sql_type in type_mappings.items():
            if pattern_type in confidence_scores and confidence_scores[pattern_type] > 0.7:
                return sql_type
    
    return "TEXT"

def suggest_improvements(the_input: str) -> Optional[str]:
    confidence_scores = calculate_type_confidence(the_input)
    max_confidence = max(confidence_scores.values()) if confidence_scores else 0
    
    if max_confidence < 0.5:
        suggestions = []
        if '@' in the_input and 'email' not in confidence_scores:
            suggestions.append("email format")
        if any(c.isdigit() for c in the_input) and len(the_input) >= 10:
            formatted_phone = format_phone_number(the_input)
            if formatted_phone:
                suggestions.append(f"phone format: {formatted_phone}")
            else:
                suggestions.append("phone number format")
        
        if suggestions:
            return f"Consider formatting as: {', '.join(suggestions)}"
    
    return None

def validate_name(name: str) -> bool:
    return bool(name and isinstance(name, str) and name.replace('_', '').isalnum() and not name[0].isdigit() and len(name) <= 64)

def execute_db(query: str, params: tuple = (), fetch: str = None) -> Any:
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = {"one": cursor.fetchone, "all": cursor.fetchall, "count": lambda: cursor.rowcount}.get(fetch, lambda: True)()
            conn.commit()
            return result
    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return [] if fetch else False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return [] if fetch else False

def table_exists(table_name: str) -> bool:
    return validate_name(table_name) and bool(execute_db("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,), "one"))

def list_tables() -> List[str]:
    result = execute_db("SELECT name FROM sqlite_master WHERE type='table'", fetch="all")
    return [row[0] for row in result] if result else []

def get_table_schema(table_name: str) -> List[tuple]:
    return execute_db(f"PRAGMA table_info({table_name})", fetch="all") if validate_name(table_name) else []

def create_table_dynamic(table_name: str, columns: Dict[str, Any]) -> bool:
    if not validate_name(table_name) or table_exists(table_name):
        print(f"{'Invalid name' if not validate_name(table_name) else 'Table already exists'}: {table_name}")
        return False
    
    col_defs = []
    for col, val in columns.items():
        if validate_name(col):
            normalized = normalize_country_code(str(val)) if isinstance(val, str) else None
            if normalized:
                columns[col] = normalized
            col_defs.append(f"{col} {detect_type(val)}")
    
    if 'id' not in columns:
        col_defs.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
    
    result = execute_db(f"CREATE TABLE {table_name} ({', '.join(col_defs)})")
    if result:
        print(f"Table '{table_name}' created successfully")
    return result

def insert_record(table_name: str, data: Dict[str, Any]) -> bool:
    if not validate_name(table_name) or not table_exists(table_name):
        print(f"Table '{table_name}' doesn't exist")
        return False
    
    processed_data = {}
    for k, v in data.items():
        if validate_name(k):
            if isinstance(v, str):
                formatted_phone = format_phone_number(v)
                if formatted_phone:
                    processed_data[k] = formatted_phone
                else:
                    normalized_country = normalize_country_code(v)
                    processed_data[k] = normalized_country or v
            else:
                processed_data[k] = v
    
    if not processed_data:
        print("No valid data to insert")
        return False
    
    cols, vals = list(processed_data.keys()), list(processed_data.values())
    return execute_db(f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['?'] * len(vals))})", tuple(vals))

def select_records(table_name: str, where_clause: str = "", params: tuple = ()) -> List[tuple]:
    if not validate_name(table_name) or not table_exists(table_name):
        return []
    query = f"SELECT * FROM {table_name}" + (f" WHERE {where_clause}" if where_clause else "")
    return execute_db(query, params, "all") or []

def update_records(table_name: str, set_clause: str, where_clause: str, params: tuple) -> int:
    return execute_db(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}", params, "count") if validate_name(table_name) and table_exists(table_name) else 0

def delete_records(table_name: str, where_clause: str, params: tuple) -> int:
    return execute_db(f"DELETE FROM {table_name} WHERE {where_clause}", params, "count") if validate_name(table_name) and table_exists(table_name) else 0

def drop_table(table_name: str) -> bool:
    if not validate_name(table_name):
        print(f"Invalid table name: {table_name}")
        return False
    result = execute_db(f"DROP TABLE IF EXISTS {table_name}")
    if result:
        print(f"Dropped table '{table_name}'")
    return result

def print_table_contents(table_name: str) -> None:
    if not validate_name(table_name) or not table_exists(table_name):
        print(f"Invalid or non-existent table: {table_name}")
        return
    
    rows = execute_db(f"SELECT * FROM {table_name}", fetch="all")
    cols = [col[1] for col in get_table_schema(table_name)]
    
    print(f"\nTable: {table_name}\n" + "-" * 60)
    if cols:
        print(" | ".join(cols) + "\n" + "-" * 60)
    
    if rows:
        for row in rows:
            print(" | ".join(str(cell) for cell in row))
    else:
        print("No data found")

def get_input(prompt: str, validator=None) -> str:
    while True:
        value = input(prompt).strip()
        if not validator or validator(value):
            return value
        print("That's not gonna work, try again")

def interactive_table_creator():
    available_tables = list_tables()
    if available_tables:
        print(f"Existing tables: {', '.join(available_tables)}")
    
    table_name = get_input("What's the table name? ", validate_name)
    columns = {}
    print("Define your columns (type 'done' when you're finished):")
    
    while True:
        col_name = input("Column name: ").strip()
        if col_name.lower() == 'done':
            break
        if not validate_name(col_name):
            print("Invalid column name, keep it simple")
            continue
        
        sample_value = input(f"Sample value for {col_name}: ").strip()
        
        suggestion = suggest_improvements(sample_value)
        if suggestion:
            print(f"Suggestion: {suggestion}")
        
        formatted_phone = format_phone_number(sample_value)
        if formatted_phone:
            sample_value = formatted_phone
            print(f"Formatted phone to: {formatted_phone}")
        else:
            normalized = normalize_country_code(sample_value)
            if normalized:
                sample_value = normalized
                print(f"Normalized country to: {normalized}")
            else:
                try:
                    sample_value = int(sample_value) if sample_value.isdigit() else float(sample_value) if sample_value.replace('.', '').replace('-', '').isdigit() else sample_value
                except ValueError:
                    pass
        
        confidence_scores = calculate_type_confidence(sample_value)
        if confidence_scores:
            max_type = max(confidence_scores.items(), key=lambda x: x[1])
            print(f"Detected type confidence: {max_type[0]} ({max_type[1]:.2f})")
        
        columns[col_name] = sample_value
    
    if columns:
        create_table_dynamic(table_name, columns)
    else:
        print("No columns defined, nothing to create")

def interactive_record_insert():
    tables = list_tables()
    if not tables:
        print("No tables exist yet, create one first")
        return
    
    print(f"Available tables: {', '.join(tables)}")
    table_name = get_input("Which table? ")
    
    if not table_exists(table_name):
        print(f"Table '{table_name}' doesn't exist")
        return
    
    data = {}
    for col_info in get_table_schema(table_name):
        col_name = col_info[1]
        if col_name == 'id' and 'AUTOINCREMENT' in str(col_info):
            continue
        
        value = input(f"Value for {col_name}: ").strip()
        if value:
            suggestion = suggest_improvements(value)
            if suggestion:
                print(f"Suggestion: {suggestion}")
            
            formatted_phone = format_phone_number(value)
            if formatted_phone:
                print(f"Formatted phone to: {formatted_phone}")
                data[col_name] = formatted_phone
            else:
                normalized = normalize_country_code(value)
                if normalized:
                    print(f"Normalized country to: {normalized}")
                    data[col_name] = normalized
                else:
                    data[col_name] = value
    
    if data and insert_record(table_name, data):
        print("Record inserted successfully")
    elif not data:
        print("No data provided")

def interactive_record_query():
    tables = list_tables()
    if not tables:
        print("No tables exist yet")
        return
    
    print(f"Available tables: {', '.join(tables)}")
    table_name = get_input("Which table? ")
    
    if not table_exists(table_name):
        print(f"Table '{table_name}' doesn't exist")
        return
    
    where_clause = input("WHERE clause (optional): ").strip()
    params = ()
    
    if where_clause:
        params_input = input("Parameters (comma-separated, optional): ").strip()
        if params_input:
            raw_params = [p.strip() for p in params_input.split(',')]
            processed_params = []
            for p in raw_params:
                formatted_phone = format_phone_number(p)
                if formatted_phone:
                    processed_params.append(formatted_phone)
                else:
                    normalized = normalize_country_code(p)
                    processed_params.append(normalized or p)
            params = tuple(processed_params)
    
    records = select_records(table_name, where_clause, params)
    
    if records:
        cols = [col[1] for col in get_table_schema(table_name)]
        print(" | ".join(cols) + "\n" + "-" * 60)
        for record in records:
            print(" | ".join(str(cell) for cell in record))
    else:
        print("No records found")

def sigmoid_demo():
    print("\n-+-+-+- MULTI-LAYER SIGMOID CONFIDENCE DEMO -+-+-+-")
    
    test_inputs = [
        "x123sjnjd@example.com",
        "555-123-4567", 
        "(555) 123-4567",
        "5551234567",
        "US",
        "2025-12-25",
        "true",
        "random text",
        "maybe_email@",
        "1234567890123"
    ] # Messing it up some for testing 9-5-2025
    
    print("Comparing single-layer vs multi-layer sigmoid analysis:")
    
    for test_input in test_inputs:
        single_layer_scores = deep_confidence_analysis(test_input, use_deep_layers=False)
        multi_layer_scores = deep_confidence_analysis(test_input, use_deep_layers=True)
        
        print(f"\nInput: '{test_input}'")
        
        formatted_phone = format_phone_number(test_input)
        if formatted_phone:
            print(f"  Formatted phone: {formatted_phone}")
        
        print("  Single-layer sigmoid:")
        for data_type, confidence in single_layer_scores.items():
            print(f"    {data_type}: {confidence:.3f} ({confidence*100:.1f}%)")
        
        print("  Multi-layer sigmoid:")
        for data_type, confidence in multi_layer_scores.items():
            print(f"    {data_type}: {confidence:.3f} ({confidence*100:.1f}%)")
        
        suggestion = suggest_improvements(test_input)
        if suggestion:
            print(f"  Suggestion: {suggestion}")
    
    print("\n-+-+-+- MULTI-LAYER SIGMOID DEMO COMPLETE -+-+-+-")

def main():
    actions = {
        '1': interactive_table_creator,
        '2': lambda: print(f"Tables: {', '.join(list_tables()) or 'None found'}"),
        '3': lambda: print_table_contents(get_input("Table name: ")),
        '4': interactive_record_insert,
        '5': interactive_record_query,
        '6': lambda: drop_table(get_input("Table to drop: ")),
        '7': sigmoid_demo,
        '8': lambda: (print("Later!"), sys.exit())
    }
    
    menu_items = ["Create table", "List tables", "Show table contents", "Insert record", "Query records", "Drop table", "Multi-layer sigmoid demo", "Exit"]
    
    while True:
        print("\n-+-+-+- UNIVERSAL DB MANAGER/Grand Finale CIS261 -+-+-+-")
        for i, desc in enumerate(menu_items, 1):
            print(f"{i}. {desc}")
        
        choice = input("\nPick an option: ").strip()
        
        try:
            actions.get(choice, lambda: print("Invalid choice, try again"))()
        except KeyboardInterrupt:
            print("\nCaught interrupt, exiting...")
            break
        except Exception as e:
            print(f"Something went wrong: {e}")
            continue

if __name__ == "__main__":
    main()