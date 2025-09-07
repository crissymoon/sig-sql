#!/usr/bin/env python3

import os
import json

def create_advanced_linguistics_datasets():
    """Create advanced linguistics and language learning datasets"""
    
    # Word frequency lists
    high_frequency_words = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us"
    ]
    
    with open("high_frequency_words.txt", "w") as f:
        for word in high_frequency_words:
            f.write(f"{word}\n")
    
    # Academic vocabulary
    academic_vocabulary = [
        "analyze", "approach", "area", "assess", "assume", "authority", "available",
        "benefit", "concept", "conclude", "conduct", "consistent", "constitute", "context",
        "contract", "create", "data", "define", "derive", "distribute", "economy",
        "environment", "establish", "estimate", "evaluate", "evidence", "export",
        "factor", "finance", "formula", "function", "identify", "income", "indicate",
        "individual", "interpret", "involve", "issue", "labor", "legal", "legislate",
        "major", "method", "occur", "percent", "period", "policy", "principle",
        "procedure", "process", "require", "research", "respond", "role", "section",
        "sector", "significant", "similar", "source", "specific", "structure",
        "theory", "transfer", "variable"
    ]
    
    with open("academic_vocabulary.txt", "w") as f:
        for word in academic_vocabulary:
            f.write(f"{word}\n")
    
    # Idioms and phrasal verbs
    idioms_phrasal_verbs = [
        "break down - to stop working or to analyze",
        "bring up - to mention or to raise a child",
        "call off - to cancel",
        "come across - to find by chance",
        "cut down - to reduce or to fell a tree",
        "figure out - to solve or understand",
        "give up - to quit or surrender",
        "look after - to take care of",
        "pick up - to collect or to learn quickly",
        "put off - to postpone",
        "run into - to meet by chance",
        "turn down - to reject or to lower volume",
        "break the ice - to start a conversation",
        "piece of cake - something very easy",
        "spill the beans - to reveal a secret",
        "hit the nail on the head - to be exactly right",
        "burn the midnight oil - to work late into the night",
        "bite the bullet - to face a difficult situation",
        "the ball is in your court - it's your turn to act",
        "don't judge a book by its cover - don't judge by appearance"
    ]
    
    with open("idioms_phrasal_verbs.txt", "w") as f:
        for item in idioms_phrasal_verbs:
            f.write(f"{item}\n")

def create_sociolinguistics_datasets():
    """Create sociolinguistics and dialectology datasets"""
    
    # Regional dialects and variations
    dialectal_variations = {
        "british_vs_american": {
            "vocabulary": [
                "lift (UK) - elevator (US)",
                "biscuit (UK) - cookie (US)",
                "lorry (UK) - truck (US)",
                "petrol (UK) - gas/gasoline (US)",
                "rubber (UK) - eraser (US)",
                "queue (UK) - line (US)",
                "jumper (UK) - sweater (US)",
                "autumn (UK) - fall (US)"
            ],
            "spelling": [
                "colour (UK) - color (US)",
                "realise (UK) - realize (US)",
                "centre (UK) - center (US)",
                "defence (UK) - defense (US)",
                "travelling (UK) - traveling (US)"
            ]
        },
        "register_variations": {
            "formal": "I would like to request your assistance.",
            "neutral": "Could you help me?",
            "informal": "Can you give me a hand?",
            "very_informal": "Help me out?"
        }
    }
    
    with open("dialectal_variations.json", "w") as f:
        json.dump(dialectal_variations, f, indent=2)
    
    # Social contexts and language use
    social_contexts = [
        "Academic writing: formal register, third person, passive voice",
        "Business communication: professional, clear, concise",
        "Casual conversation: informal, contractions, slang",
        "Public speaking: clear articulation, varied intonation",
        "Text messaging: abbreviations, emojis, informal grammar",
        "Legal documents: precise terminology, complex sentences",
        "Medical communication: technical vocabulary, clear instructions",
        "Social media: informal, hashtags, trending language"
    ]
    
    with open("social_contexts.txt", "w") as f:
        for context in social_contexts:
            f.write(f"{context}\n")

def create_language_learning_datasets():
    """Create language learning and pedagogy datasets"""
    
    # Common language learning errors
    common_errors = {
        "article_errors": [
            "Incorrect: I want to be doctor. | Correct: I want to be a doctor.",
            "Incorrect: She is playing piano. | Correct: She is playing the piano.",
            "Incorrect: I like a music. | Correct: I like music."
        ],
        "preposition_errors": [
            "Incorrect: I am good in English. | Correct: I am good at English.",
            "Incorrect: She depends from her parents. | Correct: She depends on her parents.",
            "Incorrect: He is afraid from spiders. | Correct: He is afraid of spiders."
        ],
        "word_order_errors": [
            "Incorrect: I like very much coffee. | Correct: I like coffee very much.",
            "Incorrect: Always she is late. | Correct: She is always late.",
            "Incorrect: I know not the answer. | Correct: I don't know the answer."
        ],
        "false_friends": [
            "Spanish 'embarazada' ≠ English 'embarrassed' (means pregnant)",
            "French 'preservatif' ≠ English 'preservative' (means condom)",
            "German 'Gift' ≠ English 'gift' (means poison)"
        ]
    }
    
    with open("common_language_errors.json", "w") as f:
        json.dump(common_errors, f, indent=2)
    
    # Language learning strategies
    learning_strategies = [
        "Immersion: Surround yourself with the target language",
        "Spaced repetition: Review vocabulary at increasing intervals",
        "Language exchange: Practice with native speakers",
        "Media consumption: Watch movies, listen to music in target language",
        "Mnemonics: Use memory techniques for vocabulary retention",
        "Grammar pattern drills: Practice sentence structures repeatedly",
        "Reading graded materials: Start with simple texts, progress gradually",
        "Shadowing: Repeat after audio recordings to improve pronunciation",
        "Error analysis: Identify and correct common mistakes",
        "Cultural immersion: Learn about culture alongside language"
    ]
    
    with open("language_learning_strategies.txt", "w") as f:
        for strategy in learning_strategies:
            f.write(f"{strategy}\n")

def create_computational_linguistics_datasets():
    """Create computational linguistics and NLP datasets"""
    
    # NLP tasks and techniques
    nlp_tasks = {
        "text_preprocessing": [
            "Tokenization: splitting text into words or subwords",
            "Normalization: converting to lowercase, removing punctuation",
            "Stopword removal: filtering out common words like 'the', 'and'",
            "Stemming: reducing words to their root form",
            "Lemmatization: reducing words to their dictionary form"
        ],
        "syntactic_analysis": [
            "Part-of-speech tagging: identifying grammatical categories",
            "Named entity recognition: identifying persons, places, organizations",
            "Dependency parsing: identifying grammatical relationships",
            "Constituency parsing: identifying phrase structure",
            "Chunking: identifying noun phrases, verb phrases"
        ],
        "semantic_analysis": [
            "Word sense disambiguation: determining word meaning in context",
            "Semantic role labeling: identifying who did what to whom",
            "Sentiment analysis: determining emotional tone",
            "Topic modeling: identifying themes in text collections",
            "Machine translation: converting between languages"
        ]
    }
    
    with open("nlp_tasks.json", "w") as f:
        json.dump(nlp_tasks, f, indent=2)
    
    # Regular expressions for linguistic patterns
    regex_patterns = [
        "Email: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
        "Phone: \\+?1?-?\\(?\\d{3}\\)?-?\\d{3}-?\\d{4}",
        "URL: https?://[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
        "Date (MM/DD/YYYY): \\d{1,2}/\\d{1,2}/\\d{4}",
        "Time (HH:MM): \\d{1,2}:\\d{2}",
        "Currency: \\$\\d+\\.\\d{2}",
        "Hashtag: #[a-zA-Z0-9_]+",
        "Mention: @[a-zA-Z0-9_]+",
        "Word boundaries: \\b\\w+\\b",
        "Capitalized words: [A-Z][a-z]+"
    ]
    
    with open("regex_patterns.txt", "w") as f:
        for pattern in regex_patterns:
            f.write(f"{pattern}\n")

def create_historical_linguistics_datasets():
    """Create historical linguistics and etymology datasets"""
    
    # Language evolution examples
    language_evolution = {
        "old_english_to_modern": [
            "Old English 'hlāf' → Modern English 'loaf'",
            "Old English 'hlāfweard' → Modern English 'lord' (loaf-ward)",
            "Old English 'hlǣfdige' → Modern English 'lady' (loaf-kneader)",
            "Old English 'cyning' → Modern English 'king'",
            "Old English 'cū' → Modern English 'cow'"
        ],
        "latin_borrowings": [
            "Latin 'computare' → English 'compute'",
            "Latin 'universitas' → English 'university'",
            "Latin 'communicare' → English 'communicate'",
            "Latin 'informare' → English 'inform'",
            "Latin 'demonstrare' → English 'demonstrate'"
        ],
        "sound_changes": [
            "Great Vowel Shift: Middle English /iː/ → Modern English /aɪ/ (like 'time')",
            "Grimm's Law: Proto-Indo-European *p → Germanic *f (pater → father)",
            "Rhotacism: Latin 'honor' → 'honoris' (n becomes r between vowels)"
        ]
    }
    
    with open("language_evolution.json", "w") as f:
        json.dump(language_evolution, f, indent=2)
    
    # Etymology examples
    etymology_examples = [
        "Sandwich: Named after the Earl of Sandwich who ate meat between bread while gambling",
        "Boycott: From Charles Boycott, an Irish land agent who was ostracized",
        "Serendipity: Coined by Horace Walpole from the Persian fairy tale 'The Three Princes of Serendip'",
        "Silly: Originally meant 'blessed' in Old English, evolved through 'innocent' to 'foolish'",
        "Nice: From Latin 'nescius' meaning 'ignorant', evolved through 'foolish' to 'pleasant'",
        "Awful: Originally meant 'inspiring awe', now means 'terrible'",
        "Computer: Originally referred to a person who computed, now refers to the machine",
        "Mouse: Computer device named for its resemblance to the animal"
    ]
    
    with open("etymology_examples.txt", "w") as f:
        for example in etymology_examples:
            f.write(f"{example}\n")

def main():
    """Main function to create all advanced grammar and language datasets"""
    os.chdir("datasets")
    
    print("Creating advanced linguistics datasets...")
    create_advanced_linguistics_datasets()
    
    print("Creating sociolinguistics datasets...")
    create_sociolinguistics_datasets()
    
    print("Creating language learning datasets...")
    create_language_learning_datasets()
    
    print("Creating computational linguistics datasets...")
    create_computational_linguistics_datasets()
    
    print("Creating historical linguistics datasets...")
    create_historical_linguistics_datasets()
    
    print("\nCreated advanced grammar and language datasets:")
    
    # List all created files
    advanced_files = [
        "high_frequency_words.txt", "academic_vocabulary.txt", "idioms_phrasal_verbs.txt",
        "dialectal_variations.json", "social_contexts.txt", "common_language_errors.json",
        "language_learning_strategies.txt", "nlp_tasks.json", "regex_patterns.txt",
        "language_evolution.json", "etymology_examples.txt"
    ]
    
    for file in advanced_files:
        print(f"  - {file}")
    
    print(f"\nTotal advanced language files created: {len(advanced_files)}")

if __name__ == "__main__":
    main()
