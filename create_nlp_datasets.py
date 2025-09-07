#!/usr/bin/env python3

import os
import random
import json

def create_nlp_datasets():
    """Create NLP and conversational datasets"""
    datasets_dir = "datasets"
    os.chdir(datasets_dir)
    
    # Common English phrases and expressions
    common_phrases = [
        "How are you", "Thank you", "You're welcome", "Excuse me", "I'm sorry",
        "Nice to meet you", "See you later", "Have a good day", "What's your name",
        "Where are you from", "How old are you", "What do you do", "I don't understand",
        "Can you help me", "I need help", "What time is it", "Where is the bathroom",
        "How much does it cost", "I would like", "Please give me", "Can I have",
        "I'm looking for", "Do you have", "Is there a", "How do I get to",
        "What's the weather like", "I'm hungry", "I'm tired", "I'm excited",
        "I'm confused", "I'm interested", "I agree", "I disagree", "That's correct",
        "That's wrong", "I think so", "I don't think so", "Maybe", "Probably",
        "Definitely", "Absolutely", "Of course", "No problem", "Don't worry",
        "Take your time", "Hurry up", "Slow down", "Be careful", "Good luck"
    ]
    
    with open("common_phrases.txt", "w") as f:
        for phrase in common_phrases:
            f.write(f"{phrase}\n")
    
    # Question starters and patterns
    question_patterns = [
        "What is", "What are", "What was", "What were", "What will", "What would",
        "How is", "How are", "How was", "How were", "How will", "How would",
        "How do", "How does", "How did", "How can", "How could", "How should",
        "When is", "When are", "When was", "When were", "When will", "When would",
        "Where is", "Where are", "Where was", "Where were", "Where will", "Where would",
        "Who is", "Who are", "Who was", "Who were", "Who will", "Who would",
        "Why is", "Why are", "Why was", "Why were", "Why will", "Why would",
        "Which is", "Which are", "Which was", "Which were", "Which will", "Which would",
        "Can you", "Could you", "Will you", "Would you", "Should you", "Do you",
        "Did you", "Have you", "Had you", "Are you", "Were you", "Is there",
        "Are there", "Was there", "Were there", "Will there", "Would there"
    ]
    
    with open("question_patterns.txt", "w") as f:
        for pattern in question_patterns:
            f.write(f"{pattern}\n")
    
    # Sentiment and emotion words
    positive_words = [
        "amazing", "awesome", "brilliant", "excellent", "fantastic", "great", "incredible",
        "magnificent", "marvelous", "outstanding", "perfect", "spectacular", "superb",
        "wonderful", "good", "nice", "pleasant", "lovely", "beautiful", "attractive",
        "charming", "delightful", "enjoyable", "satisfying", "impressive", "remarkable",
        "exceptional", "extraordinary", "phenomenal", "terrific", "fabulous", "gorgeous",
        "stunning", "breathtaking", "magnificent", "splendid", "divine", "heavenly"
    ]
    
    negative_words = [
        "awful", "terrible", "horrible", "dreadful", "disgusting", "revolting", "appalling",
        "atrocious", "abysmal", "deplorable", "despicable", "detestable", "loathsome",
        "repugnant", "repulsive", "vile", "bad", "poor", "inferior", "substandard",
        "mediocre", "unsatisfactory", "disappointing", "frustrating", "annoying",
        "irritating", "unpleasant", "disagreeable", "offensive", "objectionable",
        "inadequate", "insufficient", "deficient", "lacking", "faulty", "flawed"
    ]
    
    with open("positive_words.txt", "w") as f:
        for word in positive_words:
            f.write(f"{word}\n")
    
    with open("negative_words.txt", "w") as f:
        for word in negative_words:
            f.write(f"{word}\n")
    
    # Intent classifications for chatbots
    intent_examples = {
        "greeting": [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
            "howdy", "what's up", "how's it going", "nice to see you"
        ],
        "goodbye": [
            "goodbye", "bye", "see you later", "farewell", "take care", "until next time",
            "have a good day", "catch you later", "so long", "adios"
        ],
        "help": [
            "help me", "I need help", "can you help", "assist me", "support",
            "I'm stuck", "I don't know how", "guide me", "show me", "explain"
        ],
        "information": [
            "tell me about", "what is", "how does", "explain", "describe",
            "I want to know", "information about", "details on", "facts about"
        ],
        "complaint": [
            "I'm not happy", "this is wrong", "there's a problem", "I'm frustrated",
            "this doesn't work", "I'm disappointed", "this is broken", "error"
        ],
        "compliment": [
            "great job", "well done", "excellent work", "amazing", "fantastic",
            "I love this", "this is perfect", "outstanding", "brilliant"
        ]
    }
    
    with open("intent_examples.json", "w") as f:
        json.dump(intent_examples, f, indent=2)
    
    # Conversation templates
    conversation_templates = [
        "User asks about {topic}, Assistant explains {concept}",
        "User requests help with {task}, Assistant provides {solution}",
        "User expresses {emotion}, Assistant responds with {support}",
        "User mentions {problem}, Assistant suggests {fix}",
        "User wants to {action}, Assistant guides through {steps}",
        "User is confused about {subject}, Assistant clarifies {details}",
        "User complains about {issue}, Assistant offers {resolution}",
        "User compliments {feature}, Assistant acknowledges {feedback}",
        "User asks for {information}, Assistant provides {data}",
        "User needs {assistance}, Assistant offers {help}"
    ]
    
    with open("conversation_templates.txt", "w") as f:
        for template in conversation_templates:
            f.write(f"{template}\n")
    
    # Sample conversation flows
    sample_conversations = [
        {
            "user": "I need help with my database connection",
            "assistant": "I'd be happy to help you with your database connection. What specific issue are you experiencing?",
            "user": "I'm getting a timeout error",
            "assistant": "Timeout errors often occur due to network issues or incorrect connection parameters. Can you check your connection string and network connectivity?"
        },
        {
            "user": "How do I implement authentication in my API?",
            "assistant": "There are several ways to implement API authentication. The most common approaches are JWT tokens, API keys, and OAuth. Which method would you prefer?",
            "user": "JWT tokens sound good",
            "assistant": "Great choice! JWT tokens are secure and stateless. You'll need to generate a token on login and validate it on each request."
        },
        {
            "user": "My application is running slowly",
            "assistant": "Performance issues can have various causes. Let me help you troubleshoot. What type of application is it and where do you notice the slowness?",
            "user": "It's a web application and the database queries are slow",
            "assistant": "Slow database queries are common performance bottlenecks. Have you checked if your queries are properly indexed?"
        }
    ]
    
    with open("sample_conversations.json", "w") as f:
        json.dump(sample_conversations, f, indent=2)
    
    # Technical explanation templates
    explanation_templates = [
        "A {concept} is a {definition} that {purpose}",
        "To {action}, you need to {steps} because {reason}",
        "The difference between {item1} and {item2} is that {explanation}",
        "When {condition}, the system {behavior} which {result}",
        "You can {achieve_goal} by {method} and {additional_step}",
        "{Technology} works by {mechanism} to {outcome}",
        "The main advantage of {approach} is {benefit}",
        "Common problems with {system} include {issues}",
        "Best practices for {domain} involve {practices}",
        "To troubleshoot {problem}, first {step1}, then {step2}"
    ]
    
    with open("explanation_templates.txt", "w") as f:
        for template in explanation_templates:
            f.write(f"{template}\n")
    
    # Action words and verbs
    action_words = [
        "analyze", "assess", "build", "calculate", "check", "compare", "compile",
        "configure", "connect", "create", "debug", "deploy", "design", "develop",
        "download", "execute", "export", "extract", "generate", "implement",
        "import", "install", "integrate", "load", "modify", "monitor", "optimize",
        "parse", "process", "query", "refactor", "remove", "run", "save", "search",
        "setup", "test", "transform", "update", "upload", "validate", "verify"
    ]
    
    with open("action_words.txt", "w") as f:
        for word in action_words:
            f.write(f"{word}\n")
    
    print("Created NLP datasets:")
    nlp_files = [
        "common_phrases.txt", "question_patterns.txt", "positive_words.txt",
        "negative_words.txt", "intent_examples.json", "conversation_templates.txt",
        "sample_conversations.json", "explanation_templates.txt", "action_words.txt"
    ]
    for file in nlp_files:
        print(f"  - {file}")

if __name__ == "__main__":
    create_nlp_datasets()
