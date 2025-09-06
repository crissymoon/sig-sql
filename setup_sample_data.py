#!/usr/bin/env python3

from smart_cli import SmartCLI
import json
import os
import sqlite3

def populate_sample_data():
    """Add comprehensive sample data to test the retrieval functionality"""
    cli = SmartCLI()
    
    # Enhanced sample data covering multiple domains
    sample_data = [
        # Business/Employee data
        "store employee Crissy Deutsch salary 75000 department engineering skills python javascript database",
        "store employee John Smith worked 40 hours at 25 dollars per hour position developer",
        "store employee Sarah Wilson manager marketing salary 85000 experience 8 years",
        "store payroll March 2024 total 450000 employees 15 overtime 120 hours",
        
        # Customer/Commercial data
        "store customer Jane Wilson order 12345 total 299.99 status shipped",
        "store customer Mike Johnson subscription premium 99 dollars monthly active since 2023",
        "store order 67890 customer David Brown items laptop mouse keyboard total 1299.50",
        
        # Educational data
        "store student Alice Johnson grade A+ course Python Programming semester spring 2024",
        "store student Robert Lee grade B course Database Design project completed",
        "store course Advanced Algorithms instructor Dr Smith students 25 duration 16 weeks",
        
        # Medical data
        "store patient Robert Brown diagnosed with diabetes treatment insulin dosage 20 units",
        "store patient Mary Davis checkup routine blood pressure 120/80 weight 65kg",
        "store appointment patient John Doe doctor Smith date 2024-09-15 type consultation",
        
        # Technology/Project data
        "store project Smart Database CLI status completed developer Crissy language python",
        "store project Mobile App development team 4 deadline 2024-12-01 budget 50000",
        "store server database01 status running cpu 45% memory 8GB storage 500GB",
        
        # Financial data
        "store transaction 2024-09-01 amount 1500 type deposit account savings customer Wilson",
        "store invoice INV-2024-001 client TechCorp amount 25000 status paid date 2024-08-30",
        "store budget Q4-2024 marketing 75000 development 150000 operations 50000"
    ]
    
    print("Populating comprehensive sample data for testing...")
    print("=" * 60)
    
    for i, data in enumerate(sample_data, 1):
        print(f"\nAdding record {i}/{len(sample_data)}: {data}")
        try:
            cli.handle_store(data.replace("store ", ""))
        except Exception as e:
            print(f"Error storing record {i}: {e}")
            continue
    
    print("\nSample data population complete!")
    print("\nAvailable test commands:")
    print("  Data Retrieval:")
    print("    - pull any information about crissy")
    print("    - list employee data")
    print("    - show patient records")
    print("    - get project information")
    print("    - find financial transactions")
    print("    - search customer orders")
    print("  ")
    print("  Programming Examples:")
    print("    - make a python example that sorts a linked list")
    print("    - create a javascript function with math operations")
    print("    - show C terminal animation example")
    print("  ")
    print("  Storage Operations:")
    print("    - store new employee data")
    print("    - analyze data patterns")
    
    # Display current database statistics
    display_database_stats()

def display_database_stats():
    """Display statistics about the stored data"""
    try:
        conn = sqlite3.connect('smart_cli.db')
        cursor = conn.cursor()
        
        # Get total records
        cursor.execute('SELECT COUNT(*) FROM data_store')
        total_records = cursor.fetchone()[0]
        
        # Get records by backend
        cursor.execute('SELECT backend, COUNT(*) FROM data_store GROUP BY backend')
        backend_stats = cursor.fetchall()
        
        print(f"\nDatabase Statistics:")
        print(f"  Total Records: {total_records}")
        print(f"  Storage Distribution:")
        for backend, count in backend_stats:
            print(f"    {backend}: {count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"Could not retrieve database statistics: {e}")

def clear_existing_data():
    """Clear existing data for fresh testing"""
    try:
        if os.path.exists('smart_cli.db'):
            conn = sqlite3.connect('smart_cli.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM data_store')
            conn.commit()
            conn.close()
            print("Cleared existing database records.")
        else:
            print("No existing database found.")
    except Exception as e:
        print(f"Error clearing database: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--clear":
        clear_existing_data()
    
    populate_sample_data()
