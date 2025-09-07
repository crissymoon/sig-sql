#!/usr/bin/env python3

import requests
import os
import csv
import json
from urllib.parse import urlparse

def download_file(url, filename):
    """Download a file from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def create_dataset_file(filename, data):
    """Create a dataset file with given data"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, list):
                for item in data:
                    f.write(f"{item}\n")
            else:
                f.write(data)
        print(f"Created: {filename}")
        return True
    except Exception as e:
        print(f"Failed to create {filename}: {e}")
        return False

def download_datasets():
    """Download various datasets"""
    datasets_dir = "datasets"
    os.makedirs(datasets_dir, exist_ok=True)
    os.chdir(datasets_dir)
    
    # Programming languages data
    programming_languages = [
        "Python", "JavaScript", "Java", "C++", "C#", "TypeScript", "PHP", "Swift",
        "Kotlin", "Go", "Rust", "Ruby", "Scala", "Perl", "R", "MATLAB", "SQL",
        "HTML", "CSS", "Shell", "PowerShell", "Objective-C", "Dart", "Lua",
        "Haskell", "Clojure", "F#", "VB.NET", "Assembly", "COBOL", "Fortran",
        "Ada", "Pascal", "Delphi", "VHDL", "Verilog", "Prolog", "Lisp", "Scheme",
        "Erlang", "Elixir", "Crystal", "Nim", "Zig", "D", "OCaml", "Racket"
    ]
    create_dataset_file("programming_languages.txt", programming_languages)
    
    # Technology companies
    tech_companies = [
        "Apple", "Microsoft", "Google", "Amazon", "Meta", "Tesla", "Netflix",
        "Adobe", "Salesforce", "Oracle", "IBM", "Intel", "NVIDIA", "AMD",
        "Cisco", "VMware", "ServiceNow", "Workday", "Zoom", "Slack", "Spotify",
        "Uber", "Airbnb", "Twitter", "LinkedIn", "GitHub", "Stack Overflow",
        "Red Hat", "MongoDB", "Elastic", "Atlassian", "Shopify", "Square",
        "PayPal", "Stripe", "Dropbox", "Box", "Twilio", "SendGrid", "Mailchimp"
    ]
    create_dataset_file("tech_companies.txt", tech_companies)
    
    # Database systems
    databases = [
        "MySQL", "PostgreSQL", "SQLite", "Oracle", "SQL Server", "MongoDB",
        "Redis", "Elasticsearch", "Cassandra", "DynamoDB", "Firebase", "Neo4j",
        "InfluxDB", "CouchDB", "MariaDB", "H2", "Derby", "HSQLDB", "Firebird",
        "IBM DB2", "Teradata", "Vertica", "Snowflake", "BigQuery", "Redshift",
        "ClickHouse", "TimescaleDB", "ArangoDB", "OrientDB", "RavenDB", "Couchbase"
    ]
    create_dataset_file("database_systems.txt", databases)
    
    # Cloud platforms
    cloud_platforms = [
        "AWS", "Azure", "Google Cloud", "IBM Cloud", "Oracle Cloud", "Alibaba Cloud",
        "DigitalOcean", "Linode", "Vultr", "Heroku", "Vercel", "Netlify",
        "CloudFlare", "Fastly", "CDN77", "KeyCDN", "StackPath", "BunnyCDN",
        "Firebase", "Supabase", "PlanetScale", "Railway", "Render", "Fly.io"
    ]
    create_dataset_file("cloud_platforms.txt", cloud_platforms)
    
    # Machine learning frameworks
    ml_frameworks = [
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "LightGBM",
        "CatBoost", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
        "OpenCV", "NLTK", "spaCy", "Gensim", "Transformers", "JAX", "MLX",
        "Caffe", "Theano", "CNTK", "MXNet", "PaddlePaddle", "Chainer", "DL4J",
        "H2O", "Rapids", "Dask", "Ray", "MLflow", "Weights & Biases", "Neptune"
    ]
    create_dataset_file("ml_frameworks.txt", ml_frameworks)
    
    # Operating systems
    operating_systems = [
        "Windows", "macOS", "Linux", "Ubuntu", "Debian", "CentOS", "Red Hat",
        "SUSE", "Fedora", "Mint", "Arch", "Manjaro", "Elementary", "Zorin",
        "FreeBSD", "OpenBSD", "NetBSD", "Solaris", "AIX", "HP-UX", "Android",
        "iOS", "Chrome OS", "Tizen", "watchOS", "tvOS", "iPadOS", "HarmonyOS"
    ]
    create_dataset_file("operating_systems.txt", operating_systems)
    
    # Development tools
    dev_tools = [
        "Visual Studio Code", "IntelliJ IDEA", "Eclipse", "Sublime Text", "Atom",
        "Vim", "Emacs", "Nano", "WebStorm", "PyCharm", "Android Studio", "Xcode",
        "Git", "GitHub", "GitLab", "Bitbucket", "SVN", "Mercurial", "Perforce",
        "Docker", "Kubernetes", "Jenkins", "Travis CI", "CircleCI", "GitHub Actions",
        "Ansible", "Terraform", "Vagrant", "Chef", "Puppet", "Helm", "Istio"
    ]
    create_dataset_file("development_tools.txt", dev_tools)
    
    # Web frameworks
    web_frameworks = [
        "React", "Angular", "Vue.js", "Svelte", "Express.js", "Django", "Flask",
        "FastAPI", "Spring Boot", "ASP.NET", "Ruby on Rails", "Laravel", "Symfony",
        "CodeIgniter", "CakePHP", "Zend", "Yii", "Phalcon", "Slim", "Lumen",
        "Next.js", "Nuxt.js", "Gatsby", "Remix", "SvelteKit", "Astro", "Qwik",
        "Bootstrap", "Tailwind CSS", "Bulma", "Foundation", "Semantic UI", "Materialize"
    ]
    create_dataset_file("web_frameworks.txt", web_frameworks)
    
    # Cybersecurity terms
    cybersecurity_terms = [
        "Encryption", "Firewall", "Antivirus", "Malware", "Phishing", "Ransomware",
        "SQL Injection", "XSS", "CSRF", "DDoS", "Penetration Testing", "Vulnerability",
        "Zero Day", "SSL", "TLS", "VPN", "Two Factor Authentication", "Biometrics",
        "Public Key Infrastructure", "Digital Certificate", "Hash Function", "Salt",
        "Brute Force", "Social Engineering", "Spear Phishing", "APT", "Botnet",
        "Honeypot", "IDS", "IPS", "SIEM", "SOC", "Incident Response", "Forensics"
    ]
    create_dataset_file("cybersecurity_terms.txt", cybersecurity_terms)
    
    # Data science terms
    data_science_terms = [
        "Machine Learning", "Deep Learning", "Neural Network", "Algorithm", "Model",
        "Training", "Testing", "Validation", "Cross Validation", "Overfitting",
        "Underfitting", "Bias", "Variance", "Feature Engineering", "Data Mining",
        "Big Data", "Analytics", "Statistics", "Probability", "Regression",
        "Classification", "Clustering", "Dimensionality Reduction", "PCA", "t-SNE",
        "Random Forest", "Support Vector Machine", "K-Means", "DBSCAN", "Gradient Descent",
        "Backpropagation", "Convolutional Neural Network", "Recurrent Neural Network",
        "LSTM", "GRU", "Transformer", "Attention Mechanism", "Transfer Learning"
    ]
    create_dataset_file("data_science_terms.txt", data_science_terms)
    
    # Business roles
    business_roles = [
        "CEO", "CTO", "CFO", "COO", "CIO", "CISO", "VP", "Director", "Manager",
        "Senior Manager", "Team Lead", "Supervisor", "Coordinator", "Specialist",
        "Analyst", "Consultant", "Advisor", "Executive", "President", "Chairman",
        "Product Manager", "Project Manager", "Program Manager", "Scrum Master",
        "Business Analyst", "Data Analyst", "Financial Analyst", "Marketing Manager",
        "Sales Manager", "HR Manager", "Operations Manager", "Quality Assurance",
        "Developer", "Engineer", "Architect", "Designer", "Researcher", "Scientist"
    ]
    create_dataset_file("business_roles.txt", business_roles)
    
    # Industry sectors
    industry_sectors = [
        "Technology", "Healthcare", "Finance", "Education", "Manufacturing", "Retail",
        "Transportation", "Energy", "Telecommunications", "Media", "Entertainment",
        "Aerospace", "Automotive", "Construction", "Real Estate", "Agriculture",
        "Mining", "Oil and Gas", "Utilities", "Government", "Non-profit", "Consulting",
        "Insurance", "Banking", "Investment", "Hospitality", "Tourism", "Food Service",
        "Pharmaceutical", "Biotechnology", "Chemical", "Textile", "Fashion", "Sports",
        "Gaming", "Publishing", "Advertising", "Legal", "Accounting", "Architecture"
    ]
    create_dataset_file("industry_sectors.txt", industry_sectors)
    
    # Common English words (expanded)
    common_words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for",
        "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his",
        "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my",
        "one", "all", "would", "there", "their", "what", "so", "up", "out", "if",
        "about", "who", "get", "which", "go", "me", "when", "make", "can", "like",
        "time", "no", "just", "him", "know", "take", "people", "into", "year", "your",
        "good", "some", "could", "them", "see", "other", "than", "then", "now", "look",
        "only", "come", "its", "over", "think", "also", "back", "after", "use", "two",
        "how", "our", "work", "first", "well", "way", "even", "new", "want", "because",
        "any", "these", "give", "day", "most", "us", "is", "was", "are", "been", "has",
        "had", "were", "said", "each", "which", "their", "time", "will", "about", "if",
        "up", "out", "many", "then", "them", "these", "so", "some", "her", "would",
        "make", "like", "into", "him", "has", "two", "more", "very", "what", "know"
    ]
    create_dataset_file("expanded_common_words.txt", common_words)
    
    # Software design patterns
    design_patterns = [
        "Singleton", "Factory", "Abstract Factory", "Builder", "Prototype", "Adapter",
        "Bridge", "Composite", "Decorator", "Facade", "Flyweight", "Proxy", "Chain of Responsibility",
        "Command", "Interpreter", "Iterator", "Mediator", "Memento", "Observer", "State",
        "Strategy", "Template Method", "Visitor", "Model-View-Controller", "Model-View-Presenter",
        "Model-View-ViewModel", "Repository", "Unit of Work", "Dependency Injection", "Inversion of Control",
        "Publish-Subscribe", "Event Sourcing", "CQRS", "Saga", "Circuit Breaker", "Retry",
        "Bulkhead", "Timeout", "Cache-Aside", "Write-Through", "Write-Behind", "Refresh-Ahead"
    ]
    create_dataset_file("design_patterns.txt", design_patterns)
    
    # API types and protocols
    api_types = [
        "REST", "GraphQL", "SOAP", "gRPC", "WebSocket", "Server-Sent Events", "JSON-RPC",
        "XML-RPC", "OData", "JSON API", "HAL", "Siren", "Collection+JSON", "Ion",
        "OpenAPI", "Swagger", "RAML", "API Blueprint", "Postman", "Insomnia",
        "HTTP", "HTTPS", "TCP", "UDP", "WebRTC", "MQTT", "AMQP", "Kafka", "RabbitMQ",
        "Redis Pub/Sub", "Apache Pulsar", "NATS", "ZeroMQ", "Socket.IO", "SignalR"
    ]
    create_dataset_file("api_types.txt", api_types)
    
    # File formats
    file_formats = [
        "JSON", "XML", "CSV", "TSV", "YAML", "TOML", "INI", "Properties", "HCL",
        "Protobuf", "Avro", "Parquet", "ORC", "Arrow", "MessagePack", "CBOR", "BSON",
        "PDF", "DOC", "DOCX", "XLS", "XLSX", "PPT", "PPTX", "TXT", "RTF", "ODT",
        "JPG", "PNG", "GIF", "SVG", "BMP", "TIFF", "WebP", "HEIC", "ICO", "PSD",
        "MP3", "WAV", "FLAC", "AAC", "OGG", "M4A", "WMA", "MP4", "AVI", "MOV",
        "WMV", "FLV", "WebM", "MKV", "3GP", "ZIP", "RAR", "7Z", "TAR", "GZ", "BZ2"
    ]
    create_dataset_file("file_formats.txt", file_formats)
    
    print(f"\nDownloaded {len(os.listdir('.'))} dataset files to {datasets_dir}/")

if __name__ == "__main__":
    # Install requests if not available
    try:
        import requests
    except ImportError:
        print("Installing requests...")
        os.system("pip install requests")
        import requests
    
    download_datasets()
