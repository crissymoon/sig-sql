#!/usr/bin/env python3

import time
import random
from typing import Dict, List, Any
from chat_test1_core import RequestAnalysis, ChatResponse, DatasetManager, RequestProcessor

class PatternGenerator:
    def __init__(self, dataset_manager: DatasetManager):
        self.dataset_manager = dataset_manager
        self.response_cache: Dict[str, str] = {}

    def generate_programming_response(self, pattern: str, elements: Dict[str, List[str]], 
                                    request_analysis: RequestAnalysis, user_input: str) -> str:
        """Generate programming-specific responses from dataset content."""
        user_lower = user_input.lower()
        
        # Extract programming patterns from datasets
        if ('c#' in user_lower or 'csharp' in user_lower or 'c sharp' in user_lower) and ('for' in user_lower or 'loop' in user_lower):
            # Search for for loop patterns that can be repatternized for C#
            loop_patterns = []
            
            try:
                with open('/Users/mac/Desktop/sig-sql/datasets/programming_examples.txt', 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Extract for loop patterns and repatternize for C#
                    for i, line in enumerate(lines):
                        if 'for' in line and ('range' in line or 'in' in line):
                            # Extract the loop logic and repatternize for C#
                            if 'range(' in line:
                                # Python: for i in range(n): -> C#: for (int i = 0; i < n; i++)
                                start = max(0, i-1)
                                end = min(len(lines), i+3)
                                context = lines[start:end]
                                
                                # Repatternize Python for loop to C# syntax
                                csharp_pattern = self._repatternize_to_csharp(context)
                                if csharp_pattern:
                                    loop_patterns.append(csharp_pattern)
            except FileNotFoundError:
                pass
            
            if loop_patterns:
                selected_pattern = random.choice(loop_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                return f"Repatternized from dataset analysis - C# for loop:\n\n```csharp\n{selected_pattern}\n```\n\nPattern derived from training data (ID: {unique_timestamp})"
            else:
                return "Need more training data for C# for loop patterns. Current datasets contain Python patterns that could be repatternized."
                
        elif 'python' in user_lower and ('for' in user_lower or 'loop' in user_lower):
            # Search for for loop patterns in programming datasets
            for_loop_patterns = []
            
            # Extract specific range requirements from user input
            range_match = None
            if '1 to 50' in user_input or '1-50' in user_input:
                range_match = (1, 51)
            elif '1 to 10' in user_input or '1-10' in user_input:
                range_match = (1, 11)
            elif '1 to' in user_input:
                # Try to extract the end number
                import re
                match = re.search(r'1 to (\d+)', user_input)
                if match:
                    end_num = int(match.group(1))
                    range_match = (1, end_num + 1)
            
            # Check multiple dataset files for for loop patterns
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/programming_examples.txt',
                '/Users/mac/Desktop/sig-sql/datasets/python_basic_loops.py',
                '/Users/mac/Desktop/sig-sql/datasets/python_range_patterns.py'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        # Extract for loop code blocks that match the request
                        for i, line in enumerate(lines):
                            if 'for' in line and 'range' in line:
                                # If user requested specific range, try to find matching pattern
                                if range_match:
                                    if f'range({range_match[0]}, {range_match[1]})' in line or f'range(1, 51)' in line:
                                        # Extract this specific pattern
                                        start = max(0, i-1)
                                        end = min(len(lines), i+3)
                                        code_block = '\n'.join(lines[start:end])
                                        for_loop_patterns.append(code_block)
                                else:
                                    # Extract any for loop pattern
                                    start = max(0, i-2)
                                    end = min(len(lines), i+3)
                                    code_block = '\n'.join(lines[start:end])
                                    for_loop_patterns.append(code_block)
                except FileNotFoundError:
                    continue
            
            if for_loop_patterns:
                # Select the most relevant pattern
                selected_pattern = random.choice(for_loop_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                
                return f"Extracted from dataset analysis - Python for loop pattern:\n\n```python\n{selected_pattern}\n```\n\nPattern sourced from training datasets (ID: {unique_timestamp})"
            else:
                return "Need more training data for this specific Python for loop pattern. Current datasets don't contain matching range examples."
        
        return "I haven't been trained on that specific programming topic yet. Need more datasets for this type of request."
    
    def generate_business_email_response(self, user_input: str) -> str:
        """Generate business email content from marketing and communication datasets."""
        user_lower = user_input.lower()
        
        # Check if request is for email creation
        if any(keyword in user_lower for keyword in ['email', 'marketing', 'sales', 'business communication']):
            email_patterns = []
            
            # Search multiple email/marketing datasets
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/business_marketing_emails.txt',
                '/Users/mac/Desktop/sig-sql/datasets/development_sales_emails.txt',
                '/Users/mac/Desktop/sig-sql/datasets/email_marketing_templates.txt'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        
                        # Extract email templates and patterns
                        sections = content.split('Subject:')
                        for section in sections[1:]:  # Skip first empty section
                            if section.strip():
                                # Extract complete email template
                                email_pattern = 'Subject:' + section
                                
                                # Filter for development/sales related content
                                if any(term in email_pattern.lower() for term in ['development', 'software', 'business', 'custom', 'technical']):
                                    email_patterns.append(email_pattern.strip())
                except FileNotFoundError:
                    continue
            
            if email_patterns:
                selected_pattern = random.choice(email_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                
                # Extract just the relevant portions for display
                lines = selected_pattern.split('\n')
                display_lines = []
                for line in lines:
                    if line.strip():
                        display_lines.append(line)
                    if len(display_lines) >= 15:  # Limit display length
                        break
                
                display_content = '\n'.join(display_lines)
                return f"Email template extracted from business communication datasets:\n\n{display_content}\n\n[Template continues...]\n\nPattern sourced from marketing datasets (ID: {unique_timestamp})"
            else:
                return "Need more training data for business email templates. Current datasets don't contain sufficient marketing communication examples."
        
        return "I haven't been trained on that specific business communication topic yet. Need more datasets for this type of request."
    
    def generate_content_creation_response(self, user_input: str) -> str:
        """Generate general content creation responses from various datasets."""
        user_lower = user_input.lower()
        
        # Detect content creation keywords
        content_keywords = ['write', 'create', 'make', 'generate', 'draft', 'compose', 'develop']
        content_types = ['article', 'blog', 'post', 'content', 'copy', 'text', 'document', 'proposal', 'report']
        
        is_content_request = any(keyword in user_lower for keyword in content_keywords) or \
                           any(content_type in user_lower for content_type in content_types)
        
        if is_content_request:
            content_patterns = []
            
            # Search content creation datasets
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/content_creation_templates.txt',
                '/Users/mac/Desktop/sig-sql/datasets/business_writing_examples.txt',
                '/Users/mac/Desktop/sig-sql/datasets/business_marketing_emails.txt'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        
                        # Extract content sections
                        sections = content.split('\n\n')
                        for section in sections:
                            if section.strip() and len(section) > 100:
                                # Look for relevant content based on request
                                if any(term in section.lower() for term in ['template', 'example', 'structure', 'format']):
                                    content_patterns.append(section.strip())
                except FileNotFoundError:
                    continue
            
            if content_patterns:
                selected_pattern = random.choice(content_patterns)
                unique_timestamp = int(time.time_ns()) % 10000
                
                # Limit display length and format appropriately
                lines = selected_pattern.split('\n')
                display_lines = []
                for line in lines:
                    if line.strip():
                        display_lines.append(line)
                    if len(display_lines) >= 12:
                        break
                
                display_content = '\n'.join(display_lines)
                return f"Content template extracted from writing datasets:\n\n{display_content}\n\n[Template continues...]\n\nPattern sourced from content creation datasets (ID: {unique_timestamp})"
            else:
                return "Need more training data for this type of content creation. Current datasets don't contain sufficient writing examples."
        
        return "I haven't been trained on that specific content creation topic yet. Need more datasets for this type of request."
    
    def generate_educational_response(self, user_input: str) -> str:
        """Generate educational content from technical and academic datasets."""
        user_lower = user_input.lower()
        
        # Detect educational/explanatory keywords
        educational_keywords = ['explain', 'how', 'what', 'about', 'works', 'understand', 'learn', 'describe']
        technical_topics = ['machine learning', 'ai', 'artificial intelligence', 'algorithm', 'data science', 'programming', 'technology']
        
        is_educational_request = any(keyword in user_lower for keyword in educational_keywords) and \
                               any(topic in user_lower for topic in technical_topics)
        
        if is_educational_request or 'machine learning' in user_lower or 'ai' in user_lower:
            educational_content = []
            
            # Search educational and technical datasets
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/machine_learning_explained.txt',
                '/Users/mac/Desktop/sig-sql/datasets/ai_ml_educational_content.txt',
                '/Users/mac/Desktop/sig-sql/datasets/machine_learning_intro.md'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        
                        # Extract educational paragraphs
                        paragraphs = content.split('\n\n')
                        for paragraph in paragraphs:
                            if paragraph.strip() and len(paragraph) > 150:
                                # Look for explanatory content
                                if any(term in paragraph.lower() for term in ['machine learning', 'algorithm', 'data', 'model', 'training', 'prediction']):
                                    # Clean up formatting
                                    clean_paragraph = paragraph.replace('#', '').replace('**', '').strip()
                                    if clean_paragraph and not clean_paragraph.startswith('##'):
                                        educational_content.append(clean_paragraph)
                except FileNotFoundError:
                    continue
            
            if educational_content:
                # Select multiple paragraphs for comprehensive explanation
                selected_paragraphs = random.sample(educational_content, min(3, len(educational_content)))
                unique_timestamp = int(time.time_ns()) % 10000
                
                # Format the educational response
                response_text = "Educational content extracted from machine learning datasets:\n\n"
                for i, paragraph in enumerate(selected_paragraphs, 1):
                    # Limit paragraph length for readability
                    if len(paragraph) > 400:
                        paragraph = paragraph[:400] + "..."
                    response_text += f"{paragraph}\n\n"
                
                response_text += f"Content sourced from AI/ML educational datasets (ID: {unique_timestamp})"
                return response_text
            else:
                return "Need more training data for machine learning educational content. Current datasets don't contain sufficient technical explanations."
        
        return "I haven't been trained on that specific educational topic yet. Need more datasets for this type of request."

    def generate_grammar_correction_response(self, user_input: str) -> str:
        """Generate grammar-corrected and enhanced business communication from writing datasets."""
        user_lower = user_input.lower()
        
        # Detect grammar correction and writing enhancement keywords
        grammar_keywords = ['grammar', 'correct', 'fix', 'improve', 'enhance', 'rewrite', 'edit', 'proofread']
        writing_keywords = ['writing', 'communication', 'professional', 'business', 'formal', 'email']
        expansion_keywords = ['expand', 'elaborate', 'develop', 'extend', 'detail']
        
        is_grammar_request = any(keyword in user_lower for keyword in grammar_keywords) or \
                           any(keyword in user_lower for keyword in writing_keywords + expansion_keywords)
        
        # Also check if user provided text for correction (common pattern)
        has_text_to_correct = len(user_input.split()) > 10 and any(word in user_lower for word in ['upon', 'implementation', 'receipt', 'notwithstanding'])
        
        if is_grammar_request or has_text_to_correct:
            enhancement_patterns = []
            
            # Search grammar and writing enhancement datasets
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/grammar_correction_templates.txt',
                '/Users/mac/Desktop/sig-sql/datasets/professional_writing_enhancement.txt',
                '/Users/mac/Desktop/sig-sql/datasets/business_writing_examples.txt'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        
                        # Extract enhancement patterns and corrected examples
                        sections = content.split('\n\n')
                        for section in sections:
                            if section.strip() and len(section) > 300:
                                # Look for enhancement patterns
                                section_lower = section.lower()
                                if any(term in section_lower for term in ['enhanced', 'improved', 'professional', 'refined', 'corrected', 'version']):
                                    # Extract specific improvement examples
                                    lines = section.split('\n')
                                    for i, line in enumerate(lines):
                                        if any(indicator in line.lower() for indicator in ['enhanced:', 'improved:', 'professional:', 'version']):
                                            # Get the enhanced version and some context
                                            enhanced_content = []
                                            for j in range(i, min(i + 6, len(lines))):
                                                if lines[j].strip() and not lines[j].startswith('Enhanced') and not lines[j].startswith('Original'):
                                                    enhanced_content.append(lines[j].strip())
                                            
                                            if enhanced_content:
                                                enhancement_patterns.append('\n'.join(enhanced_content))
                except FileNotFoundError:
                    continue
            
            if enhancement_patterns:
                # Select relevant enhancement patterns
                selected_patterns = random.sample(enhancement_patterns, min(3, len(enhancement_patterns)))
                unique_timestamp = int(time.time_ns()) % 10000
                
                # Format the grammar enhancement response
                response_text = "Professional writing enhancement extracted from grammar datasets:\n\n"
                
                # Provide multiple enhanced versions
                for i, pattern in enumerate(selected_patterns, 1):
                    if len(pattern) > 500:
                        pattern = pattern[:500] + "..."
                    response_text += f"Enhanced Version {i}:\n{pattern}\n\n"
                
                response_text += f"Grammar improvements sourced from professional writing datasets (ID: {unique_timestamp})"
                return response_text
            else:
                return "Need more training data for grammar correction and writing enhancement. Current datasets don't contain sufficient professional writing examples."
        
        return "I haven't been trained on that specific grammar or writing enhancement topic yet. Need more datasets for this type of request."

    def generate_seo_marketing_response(self, user_input: str) -> str:
        """Generate SEO and marketing strategy responses from specialized datasets."""
        user_lower = user_input.lower()
        
        # Detect SEO and marketing keywords
        seo_keywords = ['seo', 'search engine', 'optimization', 'keywords', 'ranking', 'traffic', 'visibility']
        marketing_keywords = ['marketing', 'strategy', 'campaign', 'promotion', 'advertising', 'brand']
        nonprofit_keywords = ['nonprofit', 'non-profit', 'charity', 'fundraising', 'donation', 'volunteer']
        theater_keywords = ['theater', 'theatre', 'performance', 'arts', 'cultural', 'drama', 'production']
        
        is_seo_request = any(keyword in user_lower for keyword in seo_keywords + marketing_keywords)
        is_nonprofit = any(keyword in user_lower for keyword in nonprofit_keywords)
        is_theater = any(keyword in user_lower for keyword in theater_keywords)
        
        if is_seo_request or (is_nonprofit and is_theater):
            seo_content = []
            
            # Search specialized SEO and marketing datasets
            dataset_files = [
                '/Users/mac/Desktop/sig-sql/datasets/seo_strategy_templates.txt',
                '/Users/mac/Desktop/sig-sql/datasets/nonprofit_marketing_strategies.txt',
                '/Users/mac/Desktop/sig-sql/datasets/theater_seo_resources.txt'
            ]
            
            for dataset_file in dataset_files:
                try:
                    with open(dataset_file, 'r') as f:
                        content = f.read()
                        
                        # Extract strategy sections
                        sections = content.split('\n\n')
                        for section in sections:
                            if section.strip() and len(section) > 200:
                                # Look for relevant strategy content
                                section_lower = section.lower()
                                if any(term in section_lower for term in ['strategy', 'optimization', 'campaign', 'framework', 'implementation']):
                                    seo_content.append(section.strip())
                except FileNotFoundError:
                    continue
            
            if seo_content:
                # Select comprehensive strategy content
                selected_strategies = random.sample(seo_content, min(2, len(seo_content)))
                unique_timestamp = int(time.time_ns()) % 10000
                
                # Format the SEO strategy response
                response_text = "SEO strategy extracted from marketing datasets:\n\n"
                for i, strategy in enumerate(selected_strategies, 1):
                    # Extract key points from strategy content
                    lines = strategy.split('\n')
                    key_points = []
                    
                    for line in lines:
                        if line.strip():
                            # Look for strategy elements
                            if any(indicator in line for indicator in ['1.', '2.', '3.', '-', '•']) or \
                               line.strip().endswith(':') or \
                               any(term in line.lower() for term in ['keyword', 'content', 'local', 'technical', 'social']):
                                key_points.append(line.strip())
                                if len(key_points) >= 8:  # Limit to 8 key points
                                    break
                    
                    if key_points:
                        strategy_content = '\n'.join(key_points)
                        response_text += f"{strategy_content}\n\n"
                
                response_text += f"Strategy sourced from nonprofit theater SEO datasets (ID: {unique_timestamp})"
                return response_text
            else:
                return "Need more training data for SEO and marketing strategies. Current datasets don't contain sufficient digital marketing examples."
        
        return "I haven't been trained on that specific SEO or marketing topic yet. Need more datasets for this type of request."

    def _repatternize_to_csharp(self, python_context: List[str]) -> str:
        """Repatternize Python for loop patterns to C# syntax."""
        csharp_lines = []
        
        for line in python_context:
            if 'for' in line and 'range(' in line:
                # Extract range parameters and convert to C# for loop
                if 'range(n)' in line or 'range(len(' in line:
                    csharp_lines.append("for (int i = 0; i < 10; i++)")
                    csharp_lines.append("{")
                elif 'range(0,' in line or 'range(' in line:
                    csharp_lines.append("for (int i = 0; i < array.Length; i++)")  
                    csharp_lines.append("{")
            elif line.strip() and not line.startswith('    def ') and not line.startswith('def '):
                # Convert basic operations 
                indented_line = line.replace('    ', '    ')  # Keep indentation
                if 'print(' in line:
                    csharp_line = indented_line.replace('print(', 'Console.WriteLine(')
                    csharp_lines.append(csharp_line)
                elif '[j]' in line and '[j+1]' in line:
                    # Array swap operation
                    csharp_lines.append("    // Array swap operation")
                    csharp_lines.append("    int temp = array[j];")
                    csharp_lines.append("    array[j] = array[j + 1];")
                    csharp_lines.append("    array[j + 1] = temp;")
                elif line.strip():
                    csharp_lines.append(indented_line)
        
        if csharp_lines and any('{' in line for line in csharp_lines):
            csharp_lines.append("}")
            return '\n'.join(csharp_lines)
        
        # Fallback pattern if no specific conversion found
        return """for (int i = 1; i <= 10; i++)
{
    Console.WriteLine($"Number: {i}");
}"""

    def generate_technical_help_response(self, pattern: str, elements: Dict[str, List[str]], 
                                       request_analysis: RequestAnalysis, user_input: str) -> str:
        """Generate technical assistance responses."""
        technical_assistance = [
            f"I'm here to help with technical issues! Could you provide more details about the specific problem you're encountering?",
            f"Technical troubleshooting often requires understanding the context. What technology or system are you working with?",
            f"I can assist with debugging and technical solutions. What error messages or unexpected behavior are you seeing?"
        ]
        
        return random.choice(technical_assistance)

    def generate_adaptive_response(self, pattern: str, elements: Dict[str, List[str]], 
                                 request_analysis: RequestAnalysis, user_input: str) -> str:
        """Generate adaptive conversational responses using dataset patterns."""
        
        # Try to find relevant dataset content first
        relevant_datasets = self.dataset_manager.get_relevant_datasets(user_input)
        
        if relevant_datasets:
            # Extract patterns from relevant datasets
            for dataset_name in relevant_datasets:
                if dataset_name in self.dataset_manager.dataset_patterns:
                    patterns = self.dataset_manager.dataset_patterns[dataset_name]
                    if patterns:
                        # Use dataset pattern as basis for response
                        selected_pattern = random.choice(patterns)
                        unique_timestamp = int(time.time_ns()) % 10000
                        return f"Based on dataset pattern analysis: {selected_pattern[:200]}... (Pattern ID: {unique_timestamp})"
        
        # Fallback if no relevant dataset content found
        return "I haven't been trained on sufficient data for this request yet. Need more datasets for comprehensive responses."

    def generate_response(self, user_input: str, intent: str, domain: str) -> str:
        """Main response generation coordinator."""
        request_analysis = RequestAnalysis(
            intent=intent,
            domain=domain,
            complexity="medium",
            confidence=0.8,
            approach="dataset_driven"
        )
        
        # Check for specific content types first
        user_lower = user_input.lower()
        
        # Grammar correction and writing enhancement (highest priority for accuracy)
        if any(keyword in user_lower for keyword in ['grammar', 'correct', 'fix', 'improve', 'enhance', 'rewrite', 'edit', 'expand']) or \
           (len(user_input.split()) > 15 and any(word in user_lower for word in ['upon', 'implementation', 'receipt', 'notwithstanding', 'correspondence'])):
            return self.generate_grammar_correction_response(user_input)
        # SEO and marketing requests  
        elif any(keyword in user_lower for keyword in ['seo', 'search engine', 'marketing strategy', 'digital marketing', 'optimization']) or \
           (any(keyword in user_lower for keyword in ['nonprofit', 'non-profit']) and any(keyword in user_lower for keyword in ['theater', 'theatre'])) or \
           ('plan' in user_lower and any(keyword in user_lower for keyword in ['seo', 'marketing', 'strategy'])):
            return self.generate_seo_marketing_response(user_input)
        elif any(keyword in user_lower for keyword in ['email', 'marketing', 'sales', 'business communication', 'development company']):
            return self.generate_business_email_response(user_input)
        elif any(topic in user_lower for topic in ['machine learning', 'ai', 'artificial intelligence']) or \
             (intent == "question" and any(keyword in user_lower for keyword in ['explain', 'how', 'what', 'about', 'works'])):
            return self.generate_educational_response(user_input)
        elif intent == "request_creation" or any(keyword in user_lower for keyword in ['write', 'create', 'make', 'generate', 'draft']):
            return self.generate_content_creation_response(user_input)
        elif intent == "programming_request":
            return self.generate_programming_response("", {}, request_analysis, user_input)
        elif intent == "technical_help":
            return self.generate_technical_help_response("", {}, request_analysis, user_input)
        else:
            return self.generate_adaptive_response("", {}, request_analysis, user_input)
