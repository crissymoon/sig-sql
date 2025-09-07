#!/usr/bin/env python3

import json
import time
import random
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

class SimpleChatHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/chat' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Simple Chat Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-area { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 10px; margin: 20px 0; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; margin-left: 50px; }
        .bot { background: #f3e5f5; margin-right: 50px; }
        .input-area { display: flex; gap: 10px; margin: 20px 0; }
        input[type="text"] { flex: 1; padding: 10px; }
        button { padding: 10px 20px; background: #2196f3; color: white; border: none; cursor: pointer; }
        button:hover { background: #1976d2; }
        .data-input { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
    </style>
</head>
<body>
    <h1>Simple Chat Test</h1>
    <div class="chat-area" id="chatArea">
        <div class="message bot">
            <strong>AI:</strong> Hello! Send me a message and some data to analyze.
        </div>
    </div>
    
    <div>
        <input type="text" id="userInput" placeholder="Enter your message..." />
        <button onclick="sendMessage()">Send</button>
    </div>
    
    <div>
        <textarea id="dataInput" class="data-input" placeholder="Enter data to analyze (code, text, etc.)..."></textarea>
    </div>

    <script>
        function sendMessage() {
            const userInput = document.getElementById('userInput').value.trim();
            const dataInput = document.getElementById('dataInput').value.trim();
            
            if (!userInput) {
                alert('Please enter a message');
                return;
            }
            
            // Add user message to chat
            addMessage('user', userInput);
            
            // Send request to server
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_input: userInput,
                    data_content: dataInput || 'No data provided'
                })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('bot', data.response);
                addMessage('bot', `Analysis: ${data.analysis}`);
            })
            .catch(error => {
                addMessage('bot', 'Error: ' + error.message);
            });
            
            document.getElementById('userInput').value = '';
        }
        
        function addMessage(sender, message) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI'}:</strong> ${message}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        document.getElementById('userInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>'''
            self.wfile.write(html_content.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                user_input = data.get('user_input', '')
                data_content = data.get('data_content', '')
                
                # Simple response generation
                response = self.generate_response(user_input, data_content)
                analysis = self.analyze_data(data_content)
                
                result = {
                    'response': response,
                    'analysis': analysis,
                    'timestamp': time.time()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def generate_response(self, user_input, data_content):
        """Generate a dynamic response based on input"""
        responses = []
        
        # Analyze user input for keywords
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            responses.append("Hello! I'm here to help analyze your data.")
        
        if any(word in user_lower for word in ['help', 'what', 'how']):
            responses.append("I can analyze various types of data including code, text, and structured data.")
        
        if any(word in user_lower for word in ['code', 'program', 'function', 'class']):
            responses.append("I see you're working with code. Let me analyze the programming patterns.")
        
        if any(word in user_lower for word in ['data', 'information', 'analyze']):
            responses.append("I'll analyze the data structure and content for you.")
        
        if any(word in user_lower for word in ['business', 'enterprise', 'company']):
            responses.append("This looks like business-related content. I'll focus on enterprise analysis.")
        
        if any(word in user_lower for word in ['personal', 'private', 'confidential']):
            responses.append("I understand this is sensitive data. I'll handle it with appropriate care.")
        
        # Analyze data content
        if data_content and len(data_content) > 10:
            data_lower = data_content.lower()
            
            if any(word in data_lower for word in ['def ', 'function', 'class ', 'import ', 'return']):
                responses.append("I detected programming code in your data.")
            
            if any(word in data_lower for word in ['select', 'insert', 'update', 'create table']):
                responses.append("This appears to be SQL database content.")
            
            if any(word in data_lower for word in ['{', '}', '":', 'null', 'true', 'false']):
                responses.append("I found JSON-like structured data.")
        
        if not responses:
            responses = [
                "Thank you for your input. I'm processing the information you provided.",
                "I've received your request and I'm analyzing the content.",
                "Based on your input, I'm generating an appropriate response.",
                "Let me examine the data and provide you with insights."
            ]
            return random.choice(responses)
        
        return " ".join(responses)
    
    def analyze_data(self, data_content):
        """Analyze the provided data content"""
        if not data_content or data_content == 'No data provided':
            return "No data to analyze"
        
        analysis_parts = []
        
        # Basic metrics
        char_count = len(data_content)
        word_count = len(data_content.split())
        line_count = data_content.count('\\n') + 1
        
        analysis_parts.append(f"Data contains {char_count} characters, {word_count} words, {line_count} lines")
        
        # Content type detection
        data_lower = data_content.lower()
        
        if any(word in data_lower for word in ['def ', 'function', 'class ', 'import ', 'return']):
            analysis_parts.append("Detected: Programming code (likely Python)")
        
        if any(word in data_lower for word in ['select', 'insert', 'update', 'create', 'from ', 'where ']):
            analysis_parts.append("Detected: SQL database queries")
        
        if any(word in data_lower for word in ['{', '}', '":', 'null']):
            analysis_parts.append("Detected: JSON/structured data")
        
        if any(word in data_lower for word in ['<html', '<div', '<script', '</html>']):
            analysis_parts.append("Detected: HTML/web content")
        
        # Complexity analysis
        if char_count > 1000:
            analysis_parts.append("Large dataset detected")
        elif char_count > 100:
            analysis_parts.append("Medium-sized content")
        else:
            analysis_parts.append("Small content sample")
        
        return ". ".join(analysis_parts)

def run_server(port=8005):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleChatHandler)
    print(f"Simple chat server running on http://localhost:{port}/chat")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
