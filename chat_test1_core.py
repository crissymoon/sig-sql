#!/usr/bin/env python3

import time
import json
import random
import uuid
import hashlib
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import os

@dataclass
class ChatResponse:
    response_text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    processing_time: float = 0.0
    success: bool = True
    uniqueness_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

@dataclass
class RequestAnalysis:
    intent: str
    domain: str
    complexity: str
    confidence: float
    approach: str
    primary_dataset: str = ""
    required_datasets: List[str] = field(default_factory=list)

class SessionLogger:
    def __init__(self):
        self.responses: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.unique_responses: Set[str] = set()

    def log_response(self, response: ChatResponse, user_input: str, request_analysis: RequestAnalysis):
        response_hash = hashlib.md5(response.response_text.encode()).hexdigest()
        is_unique = response_hash not in self.unique_responses
        if is_unique:
            self.unique_responses.add(response_hash)

        self.responses.append({
            "timestamp": response.timestamp,
            "user_input": user_input,
            "response": response.response_text,
            "processing_time": response.processing_time,
            "success": response.success,
            "uniqueness_id": response.uniqueness_id,
            "is_unique": is_unique,
            "intent": request_analysis.intent,
            "domain": request_analysis.domain,
            "complexity": request_analysis.complexity,
            "confidence": request_analysis.confidence,
            "approach": request_analysis.approach,
            "primary_dataset": request_analysis.primary_dataset,
            "required_datasets": request_analysis.required_datasets
        })

    def log_error(self, error_message: str, context: Dict[str, Any]):
        self.errors.append({
            "timestamp": time.time(),
            "error": error_message,
            "context": context
        })

    def calculate_metrics(self) -> Dict[str, float]:
        if not self.responses:
            return {"success_rate": 0.0, "uniqueness_rate": 0.0, "avg_processing_time": 0.0, 
                   "conversational_rate": 0.0, "analytical_rate": 0.0}

        successful = sum(1 for r in self.responses if r["success"])
        unique_count = len(self.unique_responses)
        conversational = sum(1 for r in self.responses if "conversational" in r["approach"])
        analytical = sum(1 for r in self.responses if "analytical" in r["approach"])
        
        total_responses = len(self.responses)
        avg_time = sum(r["processing_time"] for r in self.responses) / total_responses
        
        return {
            "success_rate": (successful / total_responses) * 100,
            "uniqueness_rate": (unique_count / total_responses) * 100,
            "avg_processing_time": avg_time,
            "conversational_rate": (conversational / total_responses) * 100,
            "analytical_rate": (analytical / total_responses) * 100,
            "total_responses": total_responses,
            "session_duration": time.time() - self.start_time
        }

class DatasetManager:
    def __init__(self):
        self.datasets: Dict[str, List[str]] = {}
        self.dataset_metadata: Dict[str, Dict[str, Any]] = {}
        self.dataset_patterns: Dict[str, List[str]] = {}
        self.load_datasets()

    def load_datasets(self):
        datasets_dir = "/Users/mac/Desktop/sig-sql/datasets"
        
        if not os.path.exists(datasets_dir):
            return

        for filename in os.listdir(datasets_dir):
            if filename.endswith(('.txt', '.py', '.js', '.sql', '.csv')):
                file_path = os.path.join(datasets_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    dataset_name = filename.replace('.', '_')
                    lines = content.split('\n')
                    self.datasets[dataset_name] = [line.strip() for line in lines if line.strip()]
                    
                    self.dataset_metadata[dataset_name] = {
                        "filename": filename,
                        "size": len(lines),
                        "file_type": filename.split('.')[-1],
                        "last_loaded": time.time()
                    }
                    
                    self._extract_patterns(dataset_name, content)
                    
                except Exception as e:
                    continue

    def _extract_patterns(self, dataset_name: str, content: str):
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['def ', 'function', 'class ', 'for ', 'if ', 'while ']):
                context_start = max(0, i-2)
                context_end = min(len(lines), i+3)
                pattern = '\n'.join(lines[context_start:context_end])
                patterns.append(pattern)
        
        self.dataset_patterns[dataset_name] = patterns

    def get_relevant_datasets(self, user_input: str) -> List[str]:
        user_lower = user_input.lower()
        relevant = []
        
        for dataset_name in self.datasets.keys():
            if any(keyword in dataset_name for keyword in ['programming', 'code', 'algorithm', 'example']):
                if any(lang in user_lower for lang in ['python', 'javascript', 'c#', 'csharp']):
                    relevant.append(dataset_name)
        
        return relevant[:5]

    def analyze_request_requirements(self, user_input: str) -> List[str]:
        tokens = user_input.lower().split()
        requirements = []
        
        technical_keywords = ['code', 'programming', 'function', 'algorithm', 'example', 'tutorial']
        language_keywords = ['python', 'javascript', 'c#', 'csharp', 'java', 'sql']
        
        for keyword in technical_keywords:
            if keyword in tokens:
                requirements.append(f"technical_{keyword}")
        
        for keyword in language_keywords:
            if keyword in tokens:
                requirements.append(f"language_{keyword}")
        
        return requirements

class RequestProcessor:
    def __init__(self):
        self.intent_patterns = {
            "programming_request": ["code", "program", "function", "algorithm", "example", "script", "loop", "class"],
            "question": ["what", "how", "why", "when", "where", "explain", "tell"],
            "request_creation": ["create", "make", "build", "generate", "develop", "write"],
            "technical_help": ["help", "fix", "debug", "error", "problem", "issue"],
            "conversational": ["hello", "hi", "thanks", "please", "opinion", "think"]
        }
        
        self.domain_patterns = {
            "technical": ["programming", "code", "software", "development", "algorithm", "function"],
            "business": ["business", "company", "strategy", "management", "corporate"],
            "academic": ["research", "study", "analysis", "theory", "academic"],
            "personal": ["feel", "think", "believe", "personal", "opinion"]
        }

    def analyze_user_request(self, user_input: str) -> RequestAnalysis:
        tokens = user_input.lower().split()
        
        intent = self._classify_intent(tokens, user_input)
        domain = self._classify_domain(tokens)
        complexity = self._assess_complexity(user_input, tokens)
        confidence = self._calculate_confidence(tokens, intent, domain)
        approach = self._determine_approach(intent, domain, complexity)
        
        return RequestAnalysis(
            intent=intent,
            domain=domain,
            complexity=complexity,
            confidence=confidence,
            approach=approach
        )

    def _classify_intent(self, tokens: List[str], full_input: str) -> str:
        intent_scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for token in tokens if token in keywords)
            intent_scores[intent] = score
        
        if not any(intent_scores.values()):
            return "general_inquiry"
        
        return max(intent_scores, key=intent_scores.get)

    def _classify_domain(self, tokens: List[str]) -> str:
        domain_scores = {}
        
        for domain, keywords in self.domain_patterns.items():
            score = sum(1 for token in tokens if token in keywords)
            domain_scores[domain] = score
        
        if not any(domain_scores.values()):
            return "general"
        
        return max(domain_scores, key=domain_scores.get)

    def _assess_complexity(self, full_input: str, tokens: List[str]) -> str:
        complexity_indicators = {
            "high": ["complex", "advanced", "sophisticated", "comprehensive", "detailed"],
            "medium": ["explain", "how to", "example", "demonstrate", "show"],
            "low": ["simple", "basic", "quick", "easy", "brief"]
        }
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in full_input.lower() for indicator in indicators):
                return complexity
        
        if len(tokens) > 10:
            return "medium"
        elif len(tokens) > 5:
            return "low"
        else:
            return "minimal"

    def _calculate_confidence(self, tokens: List[str], intent: str, domain: str) -> float:
        base_confidence = 0.3
        
        if intent != "general_inquiry":
            base_confidence += 0.3
        
        if domain != "general":
            base_confidence += 0.2
        
        token_factor = min(0.2, len(tokens) * 0.02)
        base_confidence += token_factor
        
        return min(0.95, base_confidence)

    def _determine_approach(self, intent: str, domain: str, complexity: str) -> str:
        if intent == "programming_request" and domain == "technical":
            return "structured_response"
        elif intent == "conversational":
            return "adaptive_conversation"
        elif complexity == "high":
            return "analytical_approach"
        else:
            return "balanced_response"

    def validate_input(self, user_input: str) -> Tuple[bool, str]:
        if not user_input or not isinstance(user_input, str):
            return False, "Invalid input: empty or non-string"
        
        if len(user_input.strip()) == 0:
            return False, "Invalid input: empty string"
        
        if len(user_input) > 10000:
            return False, "Invalid input: too long (max 10000 characters)"
        
        dangerous_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
        if any(pattern in user_input.lower() for pattern in dangerous_patterns):
            return False, "Invalid input: contains potentially dangerous content"
        
        return True, "Valid input"
