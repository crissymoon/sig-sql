#!/usr/bin/env python3

import os
import json
import requests
from urllib.parse import urlparse

def create_english_grammar_datasets():
    """Create comprehensive English grammar datasets"""
    
    # Parts of speech with examples
    parts_of_speech = {
        "nouns": {
            "common": ["dog", "house", "book", "tree", "computer", "happiness", "freedom", "knowledge"],
            "proper": ["John", "London", "Microsoft", "Amazon", "Shakespeare", "Einstein"],
            "abstract": ["love", "courage", "wisdom", "beauty", "justice", "democracy"],
            "collective": ["team", "family", "crowd", "audience", "committee", "flock"],
            "compound": ["notebook", "sunshine", "basketball", "keyboard", "smartphone"]
        },
        "verbs": {
            "action": ["run", "jump", "write", "sing", "dance", "cook", "drive", "study"],
            "linking": ["is", "are", "was", "were", "become", "seem", "appear", "feel"],
            "helping": ["will", "would", "can", "could", "may", "might", "must", "should"],
            "irregular": ["go/went/gone", "see/saw/seen", "eat/ate/eaten", "think/thought/thought"]
        },
        "adjectives": {
            "descriptive": ["beautiful", "large", "red", "intelligent", "happy", "difficult"],
            "comparative": ["bigger", "smaller", "faster", "more beautiful", "less expensive"],
            "superlative": ["biggest", "smallest", "fastest", "most beautiful", "least expensive"],
            "demonstrative": ["this", "that", "these", "those"]
        },
        "adverbs": {
            "manner": ["quickly", "carefully", "loudly", "beautifully", "efficiently"],
            "time": ["now", "then", "yesterday", "tomorrow", "always", "never", "often"],
            "place": ["here", "there", "everywhere", "nowhere", "upstairs", "outside"],
            "degree": ["very", "quite", "extremely", "somewhat", "rather", "too"]
        }
    }
    
    with open("parts_of_speech.json", "w") as f:
        json.dump(parts_of_speech, f, indent=2)
    
    # Sentence structures and patterns
    sentence_patterns = [
        "Subject + Verb (S + V): The dog barks.",
        "Subject + Verb + Object (S + V + O): She reads books.",
        "Subject + Verb + Complement (S + V + C): He is tall.",
        "Subject + Verb + Indirect Object + Direct Object (S + V + IO + DO): I gave him a gift.",
        "Subject + Verb + Object + Complement (S + V + O + C): They elected her president.",
        "Compound: I like coffee, but she prefers tea.",
        "Complex: When it rains, we stay inside.",
        "Compound-Complex: Although it was late, we went to the store, and we bought groceries."
    ]
    
    with open("sentence_patterns.txt", "w") as f:
        for pattern in sentence_patterns:
            f.write(f"{pattern}\n")
    
    # Verb tenses with examples
    verb_tenses = {
        "present": {
            "simple": "I work every day.",
            "continuous": "I am working right now.",
            "perfect": "I have worked here for five years.",
            "perfect_continuous": "I have been working since morning."
        },
        "past": {
            "simple": "I worked yesterday.",
            "continuous": "I was working when you called.",
            "perfect": "I had worked before you arrived.",
            "perfect_continuous": "I had been working for hours."
        },
        "future": {
            "simple": "I will work tomorrow.",
            "continuous": "I will be working at 3 PM.",
            "perfect": "I will have worked by then.",
            "perfect_continuous": "I will have been working for 10 hours."
        }
    }
    
    with open("verb_tenses.json", "w") as f:
        json.dump(verb_tenses, f, indent=2)

def create_grammar_rules_dataset():
    """Create comprehensive grammar rules dataset"""
    
    # Grammar rules and explanations
    grammar_rules = [
        "Subject-Verb Agreement: Singular subjects take singular verbs, plural subjects take plural verbs.",
        "Article Usage: Use 'a' before consonant sounds, 'an' before vowel sounds, 'the' for specific items.",
        "Comma Usage: Use commas to separate items in a series, before coordinating conjunctions in compound sentences.",
        "Apostrophe Rules: Use apostrophes for contractions (don't, can't) and possessives (John's book).",
        "Capitalization: Capitalize proper nouns, first words of sentences, and important words in titles.",
        "Pronoun-Antecedent Agreement: Pronouns must agree with their antecedents in number and gender.",
        "Dangling Modifiers: Place modifiers close to the words they modify to avoid confusion.",
        "Parallel Structure: Use the same grammatical form for items in a series or comparison.",
        "Run-on Sentences: Avoid joining independent clauses without proper punctuation or conjunctions.",
        "Sentence Fragments: Ensure every sentence has a subject and predicate."
    ]
    
    with open("grammar_rules.txt", "w") as f:
        for rule in grammar_rules:
            f.write(f"{rule}\n")
    
    # Common grammar mistakes
    grammar_mistakes = [
        "Its vs It's: 'Its' is possessive, 'it's' is a contraction for 'it is'.",
        "Your vs You're: 'Your' is possessive, 'you're' is a contraction for 'you are'.",
        "There vs Their vs They're: Location, possession, and contraction respectively.",
        "Affect vs Effect: 'Affect' is usually a verb, 'effect' is usually a noun.",
        "Who vs Whom: 'Who' is subjective, 'whom' is objective.",
        "Less vs Fewer: 'Less' for uncountable nouns, 'fewer' for countable nouns.",
        "Me vs I: Use 'I' as subject, 'me' as object.",
        "Lie vs Lay: 'Lie' is intransitive, 'lay' is transitive and requires an object.",
        "Than vs Then: 'Than' for comparisons, 'then' for time or sequence.",
        "Accept vs Except: 'Accept' means to receive, 'except' means to exclude."
    ]
    
    with open("common_grammar_mistakes.txt", "w") as f:
        for mistake in grammar_mistakes:
            f.write(f"{mistake}\n")

def create_linguistic_patterns():
    """Create datasets for linguistic patterns and structures"""
    
    # Phonetic patterns and sounds
    phonetic_patterns = [
        "Consonant Clusters: bl, br, cl, cr, dr, fl, fr, gl, gr, pl, pr, sc, sk, sl, sm, sn, sp, st, sw, tr, tw",
        "Vowel Sounds: /æ/ cat, /e/ bed, /ɪ/ sit, /ɒ/ hot, /ʌ/ cup, /ʊ/ put, /i:/ see, /ɑ:/ car, /ɔ:/ saw, /u:/ too",
        "Diphthongs: /aɪ/ my, /eɪ/ day, /ɔɪ/ boy, /aʊ/ now, /əʊ/ go, /ɪə/ here, /eə/ there, /ʊə/ sure",
        "Silent Letters: know, lamb, castle, listen, honest, island, psychology, knee, write, thumb",
        "Stress Patterns: PREsent (noun) vs preSENT (verb), REcord (noun) vs reCORD (verb)"
    ]
    
    with open("phonetic_patterns.txt", "w") as f:
        for pattern in phonetic_patterns:
            f.write(f"{pattern}\n")
    
    # Morphological patterns
    morphological_patterns = [
        "Prefixes: un- (unhappy), re- (redo), pre- (preview), dis- (disagree), mis- (mistake)",
        "Suffixes: -ing (running), -ed (walked), -er (teacher), -est (fastest), -ly (quickly)",
        "Root Words: act (action, actor, active), port (transport, import, export)",
        "Compound Words: sunshine, basketball, notebook, keyboard, smartphone",
        "Inflection: walk/walks/walking/walked, good/better/best, I/me/my/mine"
    ]
    
    with open("morphological_patterns.txt", "w") as f:
        for pattern in morphological_patterns:
            f.write(f"{pattern}\n")

def create_multilingual_datasets():
    """Create datasets for multiple languages"""
    
    # Basic greetings in multiple languages
    multilingual_greetings = {
        "english": ["hello", "good morning", "good afternoon", "good evening", "goodbye"],
        "spanish": ["hola", "buenos días", "buenas tardes", "buenas noches", "adiós"],
        "french": ["bonjour", "bon matin", "bon après-midi", "bonsoir", "au revoir"],
        "german": ["hallo", "guten Morgen", "guten Tag", "guten Abend", "auf Wiedersehen"],
        "italian": ["ciao", "buongiorno", "buon pomeriggio", "buonasera", "arrivederci"],
        "portuguese": ["olá", "bom dia", "boa tarde", "boa noite", "tchau"],
        "japanese": ["こんにちは", "おはよう", "こんにちは", "こんばんは", "さようなら"],
        "korean": ["안녕하세요", "좋은 아침", "좋은 오후", "좋은 저녁", "안녕히 가세요"],
        "chinese": ["你好", "早上好", "下午好", "晚上好", "再见"],
        "russian": ["привет", "доброе утро", "добрый день", "добрый вечер", "до свидания"]
    }
    
    with open("multilingual_greetings.json", "w") as f:
        json.dump(multilingual_greetings, f, indent=2, ensure_ascii=False)
    
    # Language families and characteristics
    language_families = {
        "indo_european": {
            "germanic": ["English", "German", "Dutch", "Swedish", "Norwegian"],
            "romance": ["Spanish", "French", "Italian", "Portuguese", "Romanian"],
            "slavic": ["Russian", "Polish", "Czech", "Ukrainian", "Bulgarian"],
            "celtic": ["Irish", "Welsh", "Scottish Gaelic", "Breton"],
            "indo_iranian": ["Hindi", "Persian", "Kurdish", "Bengali"]
        },
        "sino_tibetan": {
            "chinese": ["Mandarin", "Cantonese", "Wu", "Min"],
            "tibetan": ["Tibetan", "Dzongkha", "Ladakhi"]
        },
        "afroasiatic": {
            "semitic": ["Arabic", "Hebrew", "Amharic", "Tigrinya"],
            "berber": ["Tamazight", "Kabyle", "Tuareg"]
        },
        "niger_congo": {
            "bantu": ["Swahili", "Zulu", "Yoruba", "Igbo"]
        }
    }
    
    with open("language_families.json", "w") as f:
        json.dump(language_families, f, indent=2)

def create_discourse_patterns():
    """Create datasets for discourse and conversation patterns"""
    
    # Conversation starters and patterns
    conversation_patterns = [
        "Greetings: How are you? / I'm fine, thank you.",
        "Introductions: Nice to meet you. / The pleasure is mine.",
        "Small talk: How's the weather? / It's quite nice today.",
        "Asking for help: Could you help me with this? / Of course, I'd be happy to.",
        "Making requests: Would you mind if...? / Not at all, go ahead.",
        "Expressing opinions: I think that... / That's an interesting point.",
        "Agreeing: I completely agree. / You're absolutely right.",
        "Disagreeing: I'm afraid I disagree. / I see it differently.",
        "Apologizing: I'm sorry about that. / No worries, it happens.",
        "Thanking: Thank you so much. / You're very welcome."
    ]
    
    with open("conversation_patterns.txt", "w") as f:
        for pattern in conversation_patterns:
            f.write(f"{pattern}\n")
    
    # Discourse markers and connectors
    discourse_markers = {
        "addition": ["furthermore", "moreover", "in addition", "also", "besides"],
        "contrast": ["however", "nevertheless", "on the other hand", "in contrast", "although"],
        "cause_effect": ["therefore", "consequently", "as a result", "because", "since"],
        "sequence": ["first", "then", "next", "finally", "meanwhile"],
        "emphasis": ["indeed", "certainly", "obviously", "clearly", "definitely"],
        "example": ["for example", "for instance", "such as", "namely", "specifically"],
        "summary": ["in conclusion", "to sum up", "overall", "in summary", "briefly"]
    }
    
    with open("discourse_markers.json", "w") as f:
        json.dump(discourse_markers, f, indent=2)

def create_semantic_datasets():
    """Create datasets for semantic relationships and meaning"""
    
    # Semantic relationships
    semantic_relationships = {
        "synonyms": [
            "happy - joyful - cheerful - glad - content",
            "big - large - huge - enormous - massive",
            "small - tiny - little - minute - miniature",
            "fast - quick - rapid - swift - speedy",
            "beautiful - gorgeous - stunning - lovely - attractive"
        ],
        "antonyms": [
            "hot - cold", "big - small", "happy - sad", "fast - slow", "light - dark",
            "good - bad", "old - young", "rich - poor", "strong - weak", "easy - difficult"
        ],
        "hypernyms_hyponyms": [
            "animal > mammal > dog > poodle",
            "vehicle > car > sedan > Toyota Camry",
            "furniture > chair > armchair > recliner",
            "food > fruit > citrus > orange",
            "building > house > mansion > palace"
        ],
        "meronyms": [
            "car: engine, wheels, doors, windows",
            "house: roof, walls, foundation, rooms",
            "computer: processor, memory, keyboard, screen",
            "tree: roots, trunk, branches, leaves",
            "book: cover, pages, chapters, index"
        ]
    }
    
    with open("semantic_relationships.json", "w") as f:
        json.dump(semantic_relationships, f, indent=2)
    
    # Collocations and word combinations
    collocations = [
        "make a decision", "take a break", "do homework", "have breakfast",
        "strong coffee", "heavy rain", "bright light", "deep sleep",
        "catch a cold", "break the rules", "keep a secret", "tell the truth",
        "fast food", "high speed", "low price", "hard work",
        "pay attention", "save time", "waste money", "spend time"
    ]
    
    with open("collocations.txt", "w") as f:
        for collocation in collocations:
            f.write(f"{collocation}\n")

def create_pragmatic_datasets():
    """Create datasets for pragmatics and language use in context"""
    
    # Speech acts and their functions
    speech_acts = {
        "assertives": [
            "I believe that climate change is real.",
            "The meeting is scheduled for tomorrow.",
            "This book is very interesting.",
            "He graduated from Harvard University."
        ],
        "directives": [
            "Please close the door.",
            "Could you help me with this?",
            "Turn left at the next corner.",
            "Don't forget to call me."
        ],
        "commissives": [
            "I promise to be there on time.",
            "I will help you with your project.",
            "We guarantee your satisfaction.",
            "I swear to tell the truth."
        ],
        "expressives": [
            "Thank you for your help.",
            "I'm sorry for being late.",
            "Congratulations on your promotion!",
            "I apologize for the inconvenience."
        ],
        "declarations": [
            "I now pronounce you husband and wife.",
            "The meeting is adjourned.",
            "You're hired!",
            "I declare this exhibition open."
        ]
    }
    
    with open("speech_acts.json", "w") as f:
        json.dump(speech_acts, f, indent=2)
    
    # Politeness strategies
    politeness_strategies = [
        "Direct: Give me that book.",
        "Conventionally indirect: Could you give me that book?",
        "Unconventionally indirect: I wonder if you might have a book I could borrow.",
        "Positive politeness: You're so good at finding books, could you help me?",
        "Negative politeness: I hate to bother you, but could I possibly borrow that book?",
        "Off-record: It's getting quite dark in here (implying: turn on the light)."
    ]
    
    with open("politeness_strategies.txt", "w") as f:
        for strategy in politeness_strategies:
            f.write(f"{strategy}\n")

def main():
    """Main function to create all grammar and language datasets"""
    os.chdir("datasets")
    
    print("Creating English grammar datasets...")
    create_english_grammar_datasets()
    
    print("Creating grammar rules datasets...")
    create_grammar_rules_dataset()
    
    print("Creating linguistic patterns datasets...")
    create_linguistic_patterns()
    
    print("Creating multilingual datasets...")
    create_multilingual_datasets()
    
    print("Creating discourse patterns datasets...")
    create_discourse_patterns()
    
    print("Creating semantic datasets...")
    create_semantic_datasets()
    
    print("Creating pragmatic datasets...")
    create_pragmatic_datasets()
    
    print("\nCreated comprehensive grammar and language datasets:")
    
    # List all created files
    grammar_files = [
        "parts_of_speech.json", "sentence_patterns.txt", "verb_tenses.json",
        "grammar_rules.txt", "common_grammar_mistakes.txt", "phonetic_patterns.txt",
        "morphological_patterns.txt", "multilingual_greetings.json", "language_families.json",
        "conversation_patterns.txt", "discourse_markers.json", "semantic_relationships.json",
        "collocations.txt", "speech_acts.json", "politeness_strategies.txt"
    ]
    
    for file in grammar_files:
        print(f"  - {file}")
    
    print(f"\nTotal grammar and language files created: {len(grammar_files)}")

if __name__ == "__main__":
    main()
