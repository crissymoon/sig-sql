import os
import json
import csv
from datetime import datetime

def basic_file_operations():
    print("=== Basic File Read/Write Operations ===\n")
    
    # Writing to a text file
    filename = "sample_data.txt"
    
    # Write initial data
    with open(filename, 'w') as file:
        file.write("Hello, World!\n")
        file.write("This is a sample file.\n")
        file.write("Created on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    
    print(f"✓ Created and wrote to {filename}")
    
    # Read the entire file
    with open(filename, 'r') as file:
        content = file.read()
        print(f"File content:\n{content}")
    
    # Append to the file
    with open(filename, 'a') as file:
        file.write("This line was appended.\n")
        file.write("Python file I/O is powerful!\n")
    
    print("✓ Appended new content to file")
    
    # Read line by line
    print("Reading line by line:")
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            print(f"Line {line_number}: {line.strip()}")

def json_file_operations():
    print("\n=== JSON File Operations ===\n")
    
    # Sample data
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
        ],
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "1.0",
            "total_users": 3
        }
    }
    
    # Write JSON data
    json_filename = "users_data.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    
    print(f"✓ Created JSON file: {json_filename}")
    
    # Read JSON data
    with open(json_filename, 'r') as json_file:
        loaded_data = json.load(json_file)
    
    print("Loaded JSON data:")
    print(f"Total users: {loaded_data['metadata']['total_users']}")
    for user in loaded_data['users']:
        print(f"User: {user['name']} ({user['email']})")
    
    # Update JSON data
    loaded_data['users'].append({
        "id": 4, 
        "name": "Diana", 
        "email": "diana@example.com"
    })
    loaded_data['metadata']['total_users'] = len(loaded_data['users'])
    loaded_data['metadata']['updated'] = datetime.now().isoformat()
    
    # Write updated data back
    with open(json_filename, 'w') as json_file:
        json.dump(loaded_data, json_file, indent=2)
    
    print("✓ Updated JSON file with new user")

def csv_file_operations():
    print("\n=== CSV File Operations ===\n")
    
    # Sample CSV data
    csv_filename = "employee_data.csv"
    employees = [
        ['ID', 'Name', 'Department', 'Salary'],
        [1, 'John Doe', 'Engineering', 75000],
        [2, 'Jane Smith', 'Marketing', 65000],
        [3, 'Mike Johnson', 'Sales', 55000],
        [4, 'Sarah Wilson', 'HR', 60000]
    ]
    
    # Write CSV file
    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(employees)
    
    print(f"✓ Created CSV file: {csv_filename}")
    
    # Read CSV file
    print("Employee data from CSV:")
    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row_num, row in enumerate(reader):
            if row_num == 0:
                print(f"Headers: {', '.join(row)}")
            else:
                print(f"Employee {row[0]}: {row[1]} - {row[2]} (${row[3]})")
    
    # Read CSV as dictionary
    print("\nUsing DictReader:")
    with open(csv_filename, 'r') as csv_file:
        dict_reader = csv.DictReader(csv_file)
        for employee in dict_reader:
            print(f"{employee['Name']} works in {employee['Department']}")

def binary_file_operations():
    print("\n=== Binary File Operations ===\n")
    
    # Create some binary data
    binary_data = b"This is binary data: \x00\x01\x02\x03\xFF"
    binary_filename = "binary_data.bin"
    
    # Write binary data
    with open(binary_filename, 'wb') as binary_file:
        binary_file.write(binary_data)
    
    print(f"✓ Created binary file: {binary_filename}")
    
    # Read binary data
    with open(binary_filename, 'rb') as binary_file:
        read_data = binary_file.read()
    
    print(f"Binary data read: {read_data}")
    print(f"Data matches: {binary_data == read_data}")

def advanced_file_operations():
    print("\n=== Advanced File Operations ===\n")
    
    # File existence and metadata
    files_to_check = ["sample_data.txt", "users_data.json", "employee_data.csv"]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            stat = os.stat(filename)
            print(f"✓ {filename}:")
            print(f"  Size: {stat.st_size} bytes")
            print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        else:
            print(f"✗ {filename} does not exist")
    
    # Create a directory and file
    directory = "data_backup"
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✓ Created directory: {directory}")
    
    # Copy file to backup directory
    backup_file = os.path.join(directory, "backup_sample.txt")
    with open("sample_data.txt", 'r') as source:
        with open(backup_file, 'w') as dest:
            dest.write(source.read())
    
    print(f"✓ Backed up file to: {backup_file}")

def error_handling_example():
    print("\n=== File Error Handling ===\n")
    
    # Handle file not found
    try:
        with open("nonexistent_file.txt", 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print("✗ File not found - handled gracefully")
    
    # Handle permission errors
    try:
        import tempfile
        restricted_path = "/invalid/path/restricted_file.txt"
        with open(restricted_path, 'w') as file:
            file.write("This won't work")
    except (PermissionError, FileNotFoundError, OSError):
        print("✗ Permission/path error - handled gracefully")
    
    # Safe file operations with context manager
    filename = "safe_operations.txt"
    try:
        with open(filename, 'w') as file:
            file.write("Safe file operations\n")
            file.write("Using context managers\n")
        print(f"✓ Safely wrote to {filename}")
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            print(f"Read {len(lines)} lines safely")
            
    except Exception as e:
        print(f"✗ Error: {e}")

def cleanup_files():
    print("\n=== Cleanup ===\n")
    
    files_to_remove = [
        "sample_data.txt", "users_data.json", "employee_data.csv", 
        "binary_data.bin", "safe_operations.txt"
    ]
    
    for filename in files_to_remove:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"✓ Removed {filename}")
        except Exception as e:
            print(f"✗ Could not remove {filename}: {e}")
    
    # Remove backup directory
    import shutil
    if os.path.exists("data_backup"):
        shutil.rmtree("data_backup")
        print("✓ Removed backup directory")

if __name__ == "__main__":
    print("Python File I/O Operations Example")
    print("=" * 50)
    
    basic_file_operations()
    json_file_operations()
    csv_file_operations()
    binary_file_operations()
    advanced_file_operations()
    error_handling_example()
    
    # Uncomment the next line to cleanup files after running
    # cleanup_files()
    
    print("\n" + "=" * 50)
    print("File I/O operations completed successfully!")
