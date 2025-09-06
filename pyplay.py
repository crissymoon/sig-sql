import datetime
from secure_storage import storage

data = storage.get_data()

data_template = {
    "id": "",
    "name": "",
    "description": "",
    "created_at": "",
    "updated_at": "",
    "data": []
} # Python dictionary template for data records

# Define control characters for delimiters
DELIMITER_RECORD_SEPARATOR = chr(30)
DELIMITER_GROUP_SEPARATOR = chr(29) 
DELIMITER_FILE_SEPARATOR = chr(28)
DELIMITER_UNIT_SEPARATOR = chr(31)
DELIMITER_LINE_SEPARATOR = '\u2028'
DELIMITER_PARAGRAPH_SEPARATOR = '\u2029'

def generate_unique_id(string):
    if string is None: string = "None"
    elif string is True: string = "True"  
    else: string = str(string)
    build = ""
    for x in string:
        # Pad ASCII values to 3 digits (000-255)
        build = build + str(ord(x)).zfill(3) + DELIMITER_UNIT_SEPARATOR
    return build

def convert_to_string(string):
    split_str = string.split(DELIMITER_UNIT_SEPARATOR)
    new_str = ''.join(chr(int(x)) for x in split_str if x.isdigit())
    if new_str == "None": return None
    elif new_str == "True": return True
    return new_str

def sort_any_data(the_list): # Sort mixed data types by ASCII values
    build_new_list = []
    for x in the_list:
        build_new_list.append(generate_unique_id(x))
    build_new_list.sort()
    return [convert_to_string(x) for x in build_new_list]


def sort_list_by_alpha(the_list):
    pairs = []
    for x in the_list:
        lowercase_encoded = generate_unique_id(str(x).lower())
        pairs.append((lowercase_encoded, x))
    sorted_pairs = sorted(pairs, key=lambda item: item[0])
    return [pair[1] for pair in sorted_pairs]


def add_record_with_unique_id(name, description, items=None):
    unique_id = generate_unique_id(name + str(len(data)))
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_record = {
        "id": unique_id,
        "name": str(name),
        "description": str(description),
        "created_at": current_time,
        "updated_at": current_time,    # Timestamp
        "data": items if items else []
    }
    data.append(new_record)
    storage.set_data(data)
    return new_record

def update_record_by_id(record_id, name=None, description=None, items=None):
    try:
        for record in data:
            if record["id"] == record_id:
                if name is not None:
                    record["name"] = str(name)
                if description is not None:
                    record["description"] = str(description)
                if items is not None:
                    record["data"] = items
                
                record["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                storage.set_data(data)
                return record
        
        print(f"Record with ID '{record_id}' not found")
        return None
    except Exception as e:
        print(f"Error updating record: {e}")
        return None

def delete_record_by_id(record_id):
    try:
        for i, record in enumerate(data):
            if record["id"] == record_id:
                deleted_record = data.pop(i)
                storage.set_data(data)
                print(f"Deleted record: {deleted_record['name']}")
                return deleted_record
        
        print(f"Record with ID '{record_id}' not found")
        return None
    except Exception as e:
        print(f"Error deleting record: {e}")
        return None

def find_record_by_id(record_id):
    try:
        for record in data:
            if record["id"] == record_id:
                return record
        return None
    except Exception as e:
        print(f"Error finding record: {e}")
        return None

def find_all_records():
    try:
        return data.copy()
    except Exception as e:
        print(f"Error getting all records: {e}")
        return []

if __name__ == "__main__": # For moudle testing
    mixed_datatypes_list = [1, 2.5, "hello", True, None]
    sorted_list = sort_any_data(mixed_datatypes_list)
    print("Original:", mixed_datatypes_list)
    print("Sorted:", sorted_list)

    test_list = ["Hello", "apple", "hello", "Banana", "apple", 1, 2.0, False, True]
    result = sort_list_by_alpha(test_list)
    print(result)  # ['apple', 'apple', 'Banana', 'Hello', 'hello']

    test_str = "Hello"
    print("Original String: " + test_str)
    print("Unique ID: " + generate_unique_id(test_str))
    print("Converted back to String: " + convert_to_string(generate_unique_id(test_str)))

    print("Testing add_record_with_unique_id:")
    add_record_with_unique_id("Alice", "Test user", ["item1", 42, True])
    add_record_with_unique_id("Bob", "Another user", ["item2", "hello"])

    if data:
        record_id = data[0]["id"]
        found_record = find_record_by_id(record_id)
        if found_record:
            print(f"Found record: {found_record['name']}")
        
        all_records = find_all_records()
        print(f"Total records: {len(all_records)}")
        
        update_record_by_id(record_id, name="Updated Name")
        delete_record_by_id(record_id)


