#!/usr/bin/env python3

import os
import json
import random
import string

def create_specialized_datasets():
    """Create more specialized datasets for ML training"""
    datasets_dir = "datasets"
    os.chdir(datasets_dir)
    
    # SQL commands and keywords
    sql_keywords = [
        "SELECT", "FROM", "WHERE", "JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN",
        "FULL JOIN", "GROUP BY", "ORDER BY", "HAVING", "DISTINCT", "COUNT", "SUM",
        "AVG", "MIN", "MAX", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP",
        "INDEX", "VIEW", "PROCEDURE", "FUNCTION", "TRIGGER", "CONSTRAINT", "PRIMARY KEY",
        "FOREIGN KEY", "UNIQUE", "NOT NULL", "DEFAULT", "CHECK", "UNION", "EXCEPT",
        "INTERSECT", "CASE", "WHEN", "THEN", "ELSE", "END", "EXISTS", "IN", "BETWEEN",
        "LIKE", "ILIKE", "REGEXP", "RLIKE", "IS NULL", "IS NOT NULL", "AND", "OR", "NOT"
    ]
    
    with open("sql_keywords.txt", "w") as f:
        for keyword in sql_keywords:
            f.write(f"{keyword}\n")
    
    # Programming concepts
    programming_concepts = [
        "Variable", "Function", "Class", "Object", "Method", "Property", "Constructor",
        "Inheritance", "Polymorphism", "Encapsulation", "Abstraction", "Interface",
        "Abstract Class", "Static Method", "Instance Method", "Getter", "Setter",
        "Array", "List", "Dictionary", "Hash Table", "Set", "Stack", "Queue", "Tree",
        "Binary Tree", "Graph", "Linked List", "Hash Map", "Heap", "Priority Queue",
        "Algorithm", "Data Structure", "Recursion", "Iteration", "Loop", "Conditional",
        "Exception", "Error Handling", "Try Catch", "Finally", "Memory Management",
        "Garbage Collection", "Pointer", "Reference", "Value Type", "Reference Type",
        "Scope", "Closure", "Lambda", "Anonymous Function", "Higher Order Function",
        "Callback", "Promise", "Async", "Await", "Thread", "Process", "Concurrency",
        "Parallelism", "Synchronization", "Mutex", "Semaphore", "Deadlock", "Race Condition"
    ]
    
    with open("programming_concepts.txt", "w") as f:
        for concept in programming_concepts:
            f.write(f"{concept}\n")
    
    # Network protocols and technologies
    network_tech = [
        "HTTP", "HTTPS", "FTP", "SFTP", "SSH", "Telnet", "SMTP", "POP3", "IMAP",
        "DNS", "DHCP", "TCP", "UDP", "IP", "IPv4", "IPv6", "ICMP", "ARP", "NAT",
        "VPN", "SSL", "TLS", "WPA", "WEP", "WPA2", "WPA3", "802.11", "Ethernet",
        "WiFi", "Bluetooth", "NFC", "LTE", "5G", "CDN", "Load Balancer", "Proxy",
        "Reverse Proxy", "API Gateway", "WebSocket", "REST", "GraphQL", "SOAP",
        "OAuth", "JWT", "Session", "Cookie", "CORS", "CSRF", "XSS", "SQL Injection"
    ]
    
    with open("network_technologies.txt", "w") as f:
        for tech in network_tech:
            f.write(f"{tech}\n")
    
    # Software testing terms
    testing_terms = [
        "Unit Test", "Integration Test", "End-to-End Test", "Smoke Test", "Regression Test",
        "Performance Test", "Load Test", "Stress Test", "Security Test", "Usability Test",
        "Acceptance Test", "Black Box Testing", "White Box Testing", "Gray Box Testing",
        "Manual Testing", "Automated Testing", "Test Case", "Test Suite", "Test Plan",
        "Test Coverage", "Code Coverage", "Branch Coverage", "Statement Coverage",
        "Mock", "Stub", "Fake", "Spy", "Test Double", "Test Framework", "Assertion",
        "Test Runner", "Continuous Integration", "Continuous Deployment", "DevOps",
        "Test Driven Development", "Behavior Driven Development", "Acceptance Criteria",
        "Bug", "Defect", "Issue", "Ticket", "Debug", "Troubleshoot", "Root Cause Analysis"
    ]
    
    with open("testing_terms.txt", "w") as f:
        for term in testing_terms:
            f.write(f"{term}\n")
    
    # Project management terms
    project_mgmt_terms = [
        "Agile", "Scrum", "Kanban", "Waterfall", "Sprint", "Backlog", "User Story",
        "Epic", "Feature", "Task", "Subtask", "Story Points", "Velocity", "Burndown",
        "Burnup", "Retrospective", "Daily Standup", "Sprint Planning", "Sprint Review",
        "Product Owner", "Scrum Master", "Development Team", "Stakeholder", "Customer",
        "Requirements", "Specification", "Acceptance Criteria", "Definition of Done",
        "Minimum Viable Product", "Release", "Deployment", "Go Live", "Rollback",
        "Hotfix", "Patch", "Version", "Milestone", "Deadline", "Timeline", "Roadmap",
        "Risk", "Issue", "Dependency", "Blocker", "Technical Debt", "Refactoring",
        "Code Review", "Pull Request", "Merge", "Branch", "Tag", "Release Notes"
    ]
    
    with open("project_management.txt", "w") as f:
        for term in project_mgmt_terms:
            f.write(f"{term}\n")
    
    # Error and status codes
    status_codes = [
        "200 OK", "201 Created", "204 No Content", "301 Moved Permanently",
        "302 Found", "304 Not Modified", "400 Bad Request", "401 Unauthorized",
        "403 Forbidden", "404 Not Found", "405 Method Not Allowed", "409 Conflict",
        "422 Unprocessable Entity", "429 Too Many Requests", "500 Internal Server Error",
        "502 Bad Gateway", "503 Service Unavailable", "504 Gateway Timeout",
        "NullPointerException", "IndexOutOfBoundsException", "IllegalArgumentException",
        "FileNotFoundException", "IOException", "SQLException", "TimeoutException",
        "ConnectionException", "AuthenticationException", "AuthorizationException",
        "ValidationException", "ParseException", "SerializationException", "RuntimeException",
        "OutOfMemoryError", "StackOverflowError", "ClassNotFoundException", "NoSuchMethodError"
    ]
    
    with open("error_status_codes.txt", "w") as f:
        for code in status_codes:
            f.write(f"{code}\n")
    
    # Data formats and serialization
    data_formats = [
        "JSON", "XML", "YAML", "TOML", "CSV", "TSV", "Parquet", "Avro", "Protocol Buffers",
        "MessagePack", "BSON", "CBOR", "Apache Arrow", "ORC", "HDF5", "NetCDF", "FITS",
        "Base64", "URL Encoding", "HTML Entities", "Unicode", "UTF-8", "UTF-16", "ASCII",
        "Binary", "Hexadecimal", "Octal", "Compression", "Gzip", "Deflate", "Brotli",
        "LZ4", "Snappy", "Encryption", "Hashing", "MD5", "SHA-1", "SHA-256", "SHA-512",
        "HMAC", "JWT", "XML Schema", "JSON Schema", "OpenAPI", "Swagger", "RAML"
    ]
    
    with open("data_formats.txt", "w") as f:
        for format_name in data_formats:
            f.write(f"{format_name}\n")
    
    # Generate sample business data
    business_data = []
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations", "Legal", "IT"]
    titles = ["Manager", "Director", "VP", "Senior", "Lead", "Principal", "Chief", "Head"]
    functions = ["Development", "Analysis", "Strategy", "Operations", "Support", "Research"]
    
    for i in range(100):
        dept = random.choice(departments)
        title = random.choice(titles)
        func = random.choice(functions)
        business_data.append(f"{title} {func} {dept}")
    
    with open("business_job_titles.txt", "w") as f:
        for title in business_data:
            f.write(f"{title}\n")
    
    # Generate sample technical queries
    technical_queries = [
        "How to implement authentication",
        "Database optimization techniques",
        "API rate limiting strategies",
        "Microservices architecture patterns",
        "Container orchestration best practices",
        "CI/CD pipeline configuration",
        "Load balancing algorithms",
        "Caching strategies for web applications",
        "Error handling in distributed systems",
        "Security best practices for APIs",
        "Performance monitoring and alerting",
        "Data backup and recovery procedures",
        "Code review guidelines",
        "Testing automation frameworks",
        "Infrastructure as code deployment",
        "Machine learning model deployment",
        "Real-time data processing pipelines",
        "Event-driven architecture design",
        "Database schema migration strategies",
        "API versioning approaches"
    ]
    
    with open("technical_queries.txt", "w") as f:
        for query in technical_queries:
            f.write(f"{query}\n")
    
    # Sample configuration and command patterns
    config_patterns = [
        "server.host=localhost",
        "server.port=8080",
        "database.url=jdbc:mysql://localhost:3306/mydb",
        "database.username=admin",
        "database.password=secret",
        "redis.host=localhost",
        "redis.port=6379",
        "logging.level=INFO",
        "cache.ttl=3600",
        "api.timeout=30000",
        "max.connections=100",
        "thread.pool.size=10",
        "security.enabled=true",
        "ssl.enabled=false",
        "cors.allowed.origins=*",
        "rate.limit.requests=1000",
        "rate.limit.window=3600",
        "monitoring.enabled=true",
        "metrics.export.interval=60",
        "backup.schedule=0 2 * * *"
    ]
    
    with open("configuration_patterns.txt", "w") as f:
        for pattern in config_patterns:
            f.write(f"{pattern}\n")
    
    print("Created specialized datasets:")
    new_files = [
        "sql_keywords.txt", "programming_concepts.txt", "network_technologies.txt",
        "testing_terms.txt", "project_management.txt", "error_status_codes.txt",
        "data_formats.txt", "business_job_titles.txt", "technical_queries.txt",
        "configuration_patterns.txt"
    ]
    for file in new_files:
        print(f"  - {file}")

if __name__ == "__main__":
    create_specialized_datasets()
