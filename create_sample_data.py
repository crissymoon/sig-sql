#!/usr/bin/env python3

import json
import csv
import random
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample structured data files"""
    
    # Sample user data
    users = []
    first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Chris", "Emma", "Ryan", "Jessica"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com", "example.org"]
    
    for i in range(100):
        first = random.choice(first_names)
        last = random.choice(last_names)
        users.append({
            "id": i + 1,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}@{random.choice(domains)}",
            "age": random.randint(18, 65),
            "department": random.choice(["Engineering", "Sales", "Marketing", "HR", "Finance"]),
            "salary": random.randint(40000, 150000),
            "join_date": (datetime.now() - timedelta(days=random.randint(30, 1095))).strftime("%Y-%m-%d"),
            "active": random.choice([True, False])
        })
    
    with open("sample_users.json", "w") as f:
        json.dump(users, f, indent=2)
    
    # Sample sales data
    products = ["Software License", "Cloud Service", "Consulting", "Training", "Support"]
    regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
    
    sales_data = []
    for i in range(200):
        sales_data.append({
            "sale_id": f"S{1000 + i}",
            "product": random.choice(products),
            "amount": round(random.uniform(1000, 50000), 2),
            "region": random.choice(regions),
            "salesperson": random.choice([f"{u['first_name']} {u['last_name']}" for u in users[:20]]),
            "date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "quarter": f"Q{random.randint(1, 4)} 2024"
        })
    
    with open("sample_sales.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=sales_data[0].keys())
        writer.writeheader()
        writer.writerows(sales_data)
    
    # Sample log data
    log_levels = ["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]
    services = ["api-gateway", "user-service", "payment-service", "notification-service", "auth-service"]
    
    log_entries = []
    for i in range(500):
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 10080))  # Last week
        log_entries.append({
            "timestamp": timestamp.isoformat(),
            "level": random.choice(log_levels),
            "service": random.choice(services),
            "message": f"Sample log message {i}",
            "request_id": f"req-{random.randint(100000, 999999)}",
            "user_id": random.randint(1, 100),
            "duration_ms": random.randint(10, 5000)
        })
    
    with open("sample_logs.json", "w") as f:
        json.dump(log_entries, f, indent=2)
    
    # Sample API responses
    api_responses = [
        {
            "status": "success",
            "data": {"users": users[:5]},
            "message": "Users retrieved successfully",
            "timestamp": datetime.now().isoformat()
        },
        {
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input parameters",
                "details": ["Email field is required", "Age must be greater than 0"]
            },
            "timestamp": datetime.now().isoformat()
        },
        {
            "status": "success",
            "data": {"total_sales": 125000.00, "count": 50},
            "pagination": {"page": 1, "limit": 10, "total_pages": 5},
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    with open("sample_api_responses.json", "w") as f:
        json.dump(api_responses, f, indent=2)
    
    # Sample configuration
    config_data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "app_db",
            "username": "app_user",
            "password": "secure_password",
            "pool_size": 10,
            "timeout": 30
        },
        "redis": {
            "host": "localhost",
            "port": 6379,
            "password": None,
            "ttl": 3600
        },
        "api": {
            "port": 8080,
            "host": "0.0.0.0",
            "cors_origins": ["*"],
            "rate_limit": {
                "requests": 1000,
                "window": 3600
            }
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "/var/log/app.log"
        }
    }
    
    with open("sample_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    
    print("Created sample data files:")
    files = [
        "sample_users.json",
        "sample_sales.csv", 
        "sample_logs.json",
        "sample_api_responses.json",
        "sample_config.json"
    ]
    for file in files:
        print(f"  - {file}")

if __name__ == "__main__":
    import os
    os.chdir("datasets")
    create_sample_data()
