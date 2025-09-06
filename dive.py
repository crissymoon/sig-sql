# Crissy Deutsch - Dive Search Module - Super Scraper 2025
from selenium import webdriver; from selenium.webdriver.chrome.service import Service; from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By; from selenium.webdriver.chrome.options import Options; import time; import re
from selenium.webdriver.support.ui import WebDriverWait; from selenium.webdriver.support import expected_conditions as EC
import requests; import urllib.parse; import random; import json
from bs4 import BeautifulSoup
# This is more-the-less a bunch of header options, urls, and regex patterns to help with scraping

def extract_meaningful_content(url, query_words, max_sentences=3):
    """Extract actual informative content from a webpage, not just titles"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'button']):
                tag.decompose()
            
            # Try to find the main content
            content_selectors = [
                'main', 'article', '.content', '#content', '.post-content', 
                '.entry-content', '.article-body', '.post-body', '.text-content'
            ]
            main_content = None
            
            for selector in content_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # Get all meaningful text elements
                text_elements = main_content.find_all(['p', 'div', 'li', 'span'], string=True)
                informative_content = []
                
                for element in text_elements:
                    # Get direct text and nearby text
                    text = element.get_text().strip()
                    
                    # Filter for informative content
                    if (len(text) > 50 and len(text) < 400 and 
                        not any(skip in text.lower() for skip in [
                            'cookie', 'subscribe', 'newsletter', 'advertisement', 
                            'click here', 'read more', 'learn more', 'sign up',
                            'follow us', 'share this', 'comment', 'login'
                        ])):
                        
                        # Check if text is relevant to query
                        text_lower = text.lower()
                        query_match_count = sum(1 for word in query_words if word.lower() in text_lower)
                        
                        if query_match_count >= 1 or any(
                            word in text_lower for word in ['definition', 'explained', 'means', 'refers to', 'is a', 'are a']
                        ):
                            # Clean up the text
                            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
                            text = re.sub(r'[^\w\s.,!?()-]', '', text)  # Remove special chars
                            if text not in [existing['text'] for existing in informative_content]:
                                informative_content.append({
                                    'text': text,
                                    'relevance': query_match_count
                                })
                
                # Sort by relevance and return top results
                informative_content.sort(key=lambda x: x['relevance'], reverse=True)
                return [item['text'] for item in informative_content[:max_sentences]]
                
    except Exception as e:
        print(f"Content extraction error for {url}: {e}", flush=True)
    return []

def get_wikipedia_summary(query):
    """Get informative content from Wikipedia"""
    try:
        # Clean the query for Wikipedia search
        wiki_query = query.replace('what is ', '').replace('define ', '').strip()
        
        # Try Wikipedia API
        wiki_search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SearchBot/1.0)'
        }
        
        response = requests.get(wiki_search_url, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if 'extract' in data and len(data['extract']) > 50:
                return [data['extract']]
        
        # Fallback: Try Wikipedia search
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(wiki_query)}&format=json&srlimit=1"
        
        response = requests.get(search_url, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if 'query' in data and 'search' in data['query'] and data['query']['search']:
                page_title = data['query']['search'][0]['title']
                
                # Get the page summary
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(page_title)}"
                response = requests.get(summary_url, headers=headers, timeout=8)
                if response.status_code == 200:
                    data = response.json()
                    if 'extract' in data and len(data['extract']) > 50:
                        return [data['extract']]
                        
    except Exception as e:
        print(f"Wikipedia search error: {e}", flush=True)
    return []

def get_contextual_search_results(query):
    """Get search results based on query type - not just definitions"""
    results = []
    
    # Determine query type and search accordingly
    query_lower = query.lower()
    
    if any(term in query_lower for term in ['what is', 'define', 'meaning of', 'definition']):
        # Definition queries - use Wikipedia
        wiki_results = get_wikipedia_summary(query)
        if wiki_results:
            results.extend(wiki_results)
    
    elif any(term in query_lower for term in ['how to', 'tutorial', 'guide', 'steps', 'instructions']):
        # How-to queries - search for instructional content
        results.extend(search_instructional_content(query))
    
    elif any(term in query_lower for term in ['best', 'top', 'compare', 'vs', 'versus', 'better']):
        # Comparison/recommendation queries
        results.extend(search_comparison_content(query))
    
    elif any(term in query_lower for term in ['why', 'reason', 'because', 'cause']):
        # Explanation queries
        results.extend(search_explanation_content(query))
    
    elif any(term in query_lower for term in ['when', 'history', 'timeline', 'invented', 'created']):
        # Historical/timeline queries
        results.extend(search_historical_content(query))
    
    else:
        # General information queries - try multiple approaches
        wiki_results = get_wikipedia_summary(query)
        if wiki_results:
            results.extend(wiki_results)
        else:
            results.extend(search_general_content(query))
    
    # Try DuckDuckGo as backup for any query type
    if len(results) < 2:
        try:
            ddg_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1&skip_disambig=1"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; SearchBot/1.0)'}
            
            response = requests.get(ddg_url, headers=headers, timeout=8)
            if response.status_code == 200:
                data = response.json()
                
                if 'Abstract' in data and len(data['Abstract']) > 50:
                    results.append(data['Abstract'])
                
                if 'Definition' in data and len(data['Definition']) > 30:
                    results.append(data['Definition'])
                    
        except Exception as e:
            print(f"DuckDuckGo search error: {e}", flush=True)
    
    return results[:3]

def search_instructional_content(query):
    """Search for how-to and instructional content"""
    try:
        # Remove question words and search for instructional content
        clean_query = query.replace('how to ', '').replace('how do i ', '').strip()
        
        # Try to get step-by-step information
        search_terms = f"{clean_query} tutorial steps guide"
        wiki_results = get_wikipedia_summary(search_terms)
        
        if wiki_results:
            return [f"Instructions for {clean_query}: {wiki_results[0]}"]
        else:
            return [f"This appears to be a how-to query about {clean_query}. Try searching for specific tutorials or guides."]
    except:
        return []

def search_comparison_content(query):
    """Search for comparison and recommendation content"""
    try:
        # Extract comparison terms
        if ' vs ' in query.lower():
            items = query.lower().split(' vs ')
        elif ' versus ' in query.lower():
            items = query.lower().split(' versus ')
        else:
            items = [query.replace('best ', '').replace('top ', '').strip()]
        
        if len(items) >= 2:
            item1, item2 = items[0].strip(), items[1].strip()
            wiki1 = get_wikipedia_summary(item1)
            wiki2 = get_wikipedia_summary(item2)
            
            results = []
            if wiki1:
                results.append(f"About {item1}: {wiki1[0]}")
            if wiki2:
                results.append(f"About {item2}: {wiki2[0]}")
            return results
        else:
            return [f"This is a comparison/recommendation query about {items[0]}."]
    except:
        return []

def search_explanation_content(query):
    """Search for explanatory content answering 'why' questions"""
    try:
        # Clean up why queries
        clean_query = query.replace('why ', '').replace('why is ', '').replace('why do ', '').strip()
        
        wiki_results = get_wikipedia_summary(clean_query)
        if wiki_results:
            return [f"Explanation: {wiki_results[0]}"]
        else:
            return [f"This is an explanation query about why {clean_query}."]
    except:
        return []

def search_historical_content(query):
    """Search for historical and timeline content"""
    try:
        # Focus on historical aspects
        clean_query = query.replace('when ', '').replace('history of ', '').strip()
        
        wiki_results = get_wikipedia_summary(f"{clean_query} history")
        if wiki_results:
            return [f"Historical information: {wiki_results[0]}"]
        else:
            return [f"This is a historical query about {clean_query}."]
    except:
        return []

def search_general_content(query):
    """Search for general information content"""
    try:
        # Try a direct search approach
        wiki_results = get_wikipedia_summary(query)
        if wiki_results:
            return wiki_results
        else:
            return [f"General information query about {query}. Try rephrasing for more specific results."]
    except:
        return []

def google_enhanced_search(query):
    """Enhanced Google search that gets both titles and content"""
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
        
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us&num=10"
        print(f"Enhanced search for: {query}", flush=True)
        
        response = session.get(search_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []
            
            # Find search result containers
            result_containers = soup.find_all('div', class_='g')
            
            for container in result_containers[:3]:  # Process top 3 results
                try:
                    # Get title
                    title_element = container.find('h3')
                    if not title_element:
                        continue
                    title = title_element.get_text().strip()
                    
                    # Get URL
                    link_element = container.find('a', href=True)
                    if not link_element:
                        continue
                    url = link_element['href']
                    
                    # Clean up Google redirect URLs
                    if url.startswith('/url?q='):
                        url = urllib.parse.unquote(url.split('&')[0][7:])
                    
                    # Get snippet from Google
                    snippet_element = container.find('span', class_='aCOpRe') or container.find('div', class_='VwiC3b')
                    google_snippet = snippet_element.get_text().strip() if snippet_element else ""
                    
                    # Try to get additional content from the actual page
                    query_words = query.split()
                    page_content = extract_meaningful_content(url, query_words)
                    
                    result = {
                        'title': title,
                        'url': url,
                        'google_snippet': google_snippet,
                        'page_content': page_content
                    }
                    results.append(result)
                    
                except Exception as e:
                    print(f"Error processing result: {e}", flush=True)
                    continue
            
            return results
    except Exception as e:
        print(f"Enhanced search error: {e}", flush=True)
    return []

# This is more-the-less a bunch of header options, urls, and regex patterns to help with scraping
def google_http_search(query):
    try: # Currently not being detected by Google, but this may change
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        print("Establishing Google session...", flush=True)
        session.get('https://www.google.com', headers=headers, timeout=10)
        time.sleep(random.uniform(1, 3))
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&hl=en&gl=us&num=10"
        print(f"HTTP request to: {search_url[:50]}...", flush=True)
        headers['Referer'] = 'https://www.google.com/'
        response = session.get(search_url, headers=headers, timeout=15)
        print(f"Response status: {response.status_code}, length: {len(response.text)}", flush=True)
        if response.status_code == 200 and len(response.text) > 5000:
            html_content = response.text
            title_patterns = [
                r'<h3[^>]*>(.*?)</h3>',
                r'class="LC20lb[^"]*"[^>]*>(.*?)</[^>]*>',
                r'class="DKV0Md[^"]*"[^>]*>(.*?)</[^>]*>',
                r'role="heading"[^>]*>(.*?)</[^>]*>'
            ]
            found_results = []
            for pattern in title_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
                found_results.extend(matches)
            print(f"HTTP parsing found {len(found_results)} potential results", flush=True)
            for match in found_results[:10]:
                clean_text = re.sub(r'<[^>]+>', '', match).strip()
                if clean_text and 5 < len(clean_text) < 100:
                    print(f"  HTTP result: '{clean_text[:50]}...'", flush=True)
                    yield clean_text
        return None
    except Exception as e:
        print(f"HTTP request error: {e}", flush=True)
        return None

def google_selenium_search(query):
    driver = None
    try:
        print("Attempting advanced stealth Selenium...", flush=True)
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--disable-javascript")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        options.add_argument(f"--user-agent={random.choice(user_agents)}")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.media_stream": 2,
        })
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        stealth_scripts = [
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",
            "window.chrome = {runtime: {}}",
            "Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})"
        ]
        for script in stealth_scripts:
            try:
                driver.execute_script(script)
            except:
                pass
        search_params = {
            'q': query,
            'hl': 'en',
            'gl': 'us',
            'safe': 'off',
            'num': '10',
            'start': '0'
        }
        search_url = 'https://www.google.com/search?' + urllib.parse.urlencode(search_params)
        print(f"Advanced Selenium URL: {search_url[:50]}...", flush=True)
        driver.get(search_url)
        time.sleep(random.uniform(3, 6))
        page_title = driver.title.lower()
        page_source_snippet = driver.page_source[:500].lower()
        if 'captcha' in page_title or 'captcha' in page_source_snippet:
            print("CAPTCHA detected, trying workaround...", flush=True)
            driver.refresh()
            time.sleep(random.uniform(5, 8))
        search_selectors = [
            'h3',
            '.LC20lb.MBeuO.DKV0Md',
            '.yuRUbf h3',
            '.g .yuRUbf a h3',
            '.tF2Cxc .yuRUbf a h3',
            'div[role="heading"]',
            '.DKV0Md',
            'h3.LC20lb',
            '[data-attrid="title"]'
        ]
        results = []
        for selector in search_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"Advanced selector '{selector}': {len(elements)} results", flush=True)
                for element in elements[:8]:
                    try:
                        text = element.text.strip()
                        if text and 5 < len(text) < 100:
                            print(f"  Advanced result: '{text[:40]}...'", flush=True)
                            results.append(text)
                    except:
                        continue
            except:
                continue
        driver.quit()
        return results  # Return list instead of generator
    except Exception as e:
        print(f"Advanced Selenium error: {e}", flush=True)
        if driver:
            try:
                driver.quit()
            except:
                pass
        return []

def google_api_simulation(query):
    try:
        print("Trying Google API simulation...", flush=True)
        session = requests.Session()
        api_headers = {
            'User-Agent': 'GoogleBot/2.1 (+http://www.google.com/bot.html)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        mobile_search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}&ie=UTF-8&tbm="
        print(f"API simulation request...", flush=True)
        response = session.get(mobile_search_url, headers=api_headers, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            text_patterns = [
                r'>(.*?' + re.escape(query.split()[0].lower()) + r'.*?)<'
            ]
            for pattern in text_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE | re.DOTALL)
                for match in matches[:5]:
                    text_clean = re.sub(r'<[^>]+>', '', match).strip()
                    if text_clean and 10 < len(text_clean) < 80:
                        print(f"  API simulation found: '{text_clean[:50]}...'", flush=True)
                        yield text_clean
        return None
    except Exception as e:
        print(f"API simulation error: {e}", flush=True)
        return None

def bing_search(query):
    try:
        options = Options()
        options.add_argument("--headless"); options.add_argument("--no-sandbox"); options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
        print(f"Fallback Bing search...", flush=True)
        driver.get(search_url); time.sleep(3)
        elements = driver.find_elements(By.CSS_SELECTOR, "h2 a")
        for element in elements[:5]:
            try:
                text = element.text.strip()
                if text and 5 < len(text) < 80:
                    yield text
            except: continue
        driver.quit()
    except: 
        driver.quit() if 'driver' in locals() else None
        return None

def imdb_direct_search(query):
    try:
        options = Options()
        options.add_argument("--headless"); options.add_argument("--no-sandbox"); options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        imdb_url = f"https://www.imdb.com/find?q={query.replace(' ', '+')}&s=tt&ttype=ft"
        print(f"Trying IMDB direct search...", flush=True)
        driver.get(imdb_url); time.sleep(3)
        imdb_selectors = [".findResult .result_text a", ".ipc-metadata-list-summary-item__t", "h3.ipc-title__text", ".titleColumn a"]
        for selector in imdb_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"IMDB selector '{selector}': {len(elements)} results", flush=True)
                for element in elements[:5]:
                    try:
                        text = element.text.strip()
                        if text and len(text) > 3:
                            print(f"  IMDB result: '{text}'", flush=True)
                            yield text
                    except: continue
            except: continue
        driver.quit()
    except Exception as e:
        print(f"IMDB error: {e}", flush=True)
        driver.quit() if 'driver' in locals() else None

def clean_title(title):
    if not title: return title
    clean = title.strip()
    suffixes = [" - IMDb", " - Wikipedia", " (film)", " (movie)", " movie", " film", " - Trailer"]
    for suffix in suffixes:
        if clean.endswith(suffix): clean = clean[:-len(suffix)]
    clean = re.sub(r'\s*\(\d{4}\)\s*$', '', clean)
    return clean.strip()

def is_match(text, query, match_terms=None):
    text_lower = text.lower(); query_lower = query.lower()
    if len(text) < 3 or len(text) > 100: return False
    skip_terms = ["watch online", "download", "streaming", "torrent", "subtitle", "buy", "rent", "reviews"]
    if any(term in text_lower for term in skip_terms): return False
    if match_terms:
        has_indicator = any(ind in text_lower for ind in match_terms)
    else:
        has_indicator = True
    query_words = [w for w in query_lower.split() if len(w) > 2]
    matches = sum(1 for qw in query_words if qw in text_lower)
    overlap = matches / len(query_words) if query_words else 0
    return has_indicator or overlap >= 0.7

def dive_search(query, search_type="general", match_terms=None):
    # Try to get contextual search results based on query type
    direct_answers = get_contextual_search_results(query)
    
    if direct_answers:
        # Create comprehensive summary with actual informative content
        summary = f"Search Results for: '{query}'\n"
        summary += "=" * 60 + "\n\n"
        
        summary += "INFORMATIVE CONTENT:\n"
        summary += "-" * 30 + "\n\n"
        
        for i, answer in enumerate(direct_answers, 1):
            # Clean and format the answer
            clean_answer = answer.strip()
            if len(clean_answer) > 20:
                summary += f"Answer {i}:\n{clean_answer}\n\n"
        
        # Add query analysis
        if any(term in query.lower() for term in ['what is', 'define', 'meaning']):
            summary += "Query Type: Definition/Explanation\n"
        elif any(term in query.lower() for term in ['how to', 'tutorial', 'guide']):
            summary += "Query Type: How-to/Tutorial\n"
        elif any(term in query.lower() for term in ['best', 'top', 'compare']):
            summary += "Query Type: Comparison/Recommendation\n"
        elif any(term in query.lower() for term in ['why', 'reason']):
            summary += "Query Type: Explanation\n"
        elif any(term in query.lower() for term in ['when', 'history']):
            summary += "Query Type: Historical/Timeline\n"
        else:
            summary += "Query Type: General Information\n"
            
        return summary
    
    # Fallback to enhanced search if direct answers fail
    enhanced_results = google_enhanced_search(query)
    
    if enhanced_results:
        # Create comprehensive summary with actual content
        summary = f"Search Results for: '{query}'\n"
        summary += "=" * 60 + "\n\n"
        
        for i, result in enumerate(enhanced_results, 1):
            summary += f"Result {i}: {result['title']}\n"
            summary += f"Source: {result['url'][:60]}{'...' if len(result['url']) > 60 else ''}\n"
            
            # Add Google snippet if available
            if result['google_snippet']:
                summary += f"Summary: {result['google_snippet']}\n"
            
            # Add extracted page content if available
            if result['page_content']:
                summary += f"Key Points:\n"
                for j, point in enumerate(result['page_content'], 1):
                    # Limit each point to reasonable length
                    point = point[:200] + "..." if len(point) > 200 else point
                    summary += f"   {j}. {point}\n"
            
            summary += "\n" + "-" * 40 + "\n\n"
        
        # Add query analysis
        if any(term in query.lower() for term in ['what is', 'define', 'meaning']):
            summary += "Query Type: Definition/Explanation\n"
        elif any(term in query.lower() for term in ['how to', 'tutorial', 'guide']):
            summary += "Query Type: How-to/Tutorial\n"
        elif any(term in query.lower() for term in ['best', 'top', 'compare']):
            summary += "Query Type: Comparison/Recommendation\n"
        else:
            summary += "Query Type: General Information\n"
            
        return summary
    
    # Final fallback to original search methods
    search_methods = [
        google_http_search,
        google_selenium_search,
        google_api_simulation,
        bing_search
    ]
    if search_type == "movie":
        search_methods.append(imdb_direct_search)
    
    all_results = []
    for method in search_methods:
        try:
            results = method(query)
            if results:
                for result in results:
                    if is_match(result, query, match_terms):
                        cleaned_result = clean_title(result)
                        if cleaned_result not in all_results and len(cleaned_result) > 10:
                            all_results.append(cleaned_result)
                            if len(all_results) >= 5:  # Collect up to 5 good results
                                break
            if len(all_results) >= 5:
                break
        except: 
            continue
    
    if all_results:
        # Create a basic summary as fallback
        summary = f"Basic Results for: '{query}'\n"
        summary += "=" * 50 + "\n\n"
        summary += f"Top Result: {all_results[0]}\n\n"
        if len(all_results) > 1:
            summary += "Additional Results:\n"
            for i, result in enumerate(all_results[1:4], 2):  # Show up to 3 more
                summary += f"   {i}. {result}\n"
        
        # Add query context
        if any(term in query.lower() for term in ['what is', 'define', 'meaning']):
            summary += f"\nThis appears to be a definition query about '{query}'."
        elif any(term in query.lower() for term in ['how to', 'tutorial', 'guide']):
            summary += f"\nThis appears to be a tutorial query about '{query}'."
        elif search_type == "movie" or any(term in query.lower() for term in ['movie', 'film', 'actor']):
            summary += f"\nThis appears to be an entertainment query about '{query}'."
        else:
            summary += f"\nGeneral information query about '{query}'"
            
        return summary
    
    return f"No detailed results found for '{query}'. Try rephrasing your search query."
