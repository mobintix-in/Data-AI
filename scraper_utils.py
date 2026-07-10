
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_valid_emails(text):
    emails = EMAIL_REGEX.findall(text)
    return [
        e for e in emails 
        if not any(e.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.tiff'])
    ]

def scrape_email_from_website(url):
    """Hits the business website to scrape contact emails from mailto tags and text regex."""
    if not url or url == "not website" or url == "":
        return ""
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=6, verify=False)
        if response.status_code != 200:
            return ""
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Search for mailto links on homepage
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('mailto:'):
                email = a['href'].split('mailto:')[1].split('?')[0].strip()
                if EMAIL_REGEX.match(email):
                    return email
                    
        # 2. Search for raw email patterns in text
        valid_emails = extract_valid_emails(response.text)
        if valid_emails:
            return valid_emails[0]
            
        # 3. If no email found, check for Contact, About, Imprint pages
        contact_url = None
        for a in soup.find_all('a', href=True):
            link_text = a.text.lower()
            href = a['href'].lower()
            if any(term in link_text or term in href for term in ['contact', 'about', 'imprint', 'support', 'info']):
                target_href = a['href']
                if target_href.startswith('/'):
                    contact_url = urljoin(url, target_href)
                elif target_href.startswith('http'):
                    contact_url = target_href
                break
                
        if contact_url:
            response_contact = requests.get(contact_url, headers=headers, timeout=6, verify=False)
            if response_contact.status_code == 200:
                soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                for a in soup_contact.find_all('a', href=True):
                    if a['href'].startswith('mailto:'):
                        email = a['href'].split('mailto:')[1].split('?')[0].strip()
                        if EMAIL_REGEX.match(email):
                            return email
                            
                valid_contact_emails = extract_valid_emails(response_contact.text)
                if valid_contact_emails:
                    return valid_contact_emails[0]
                    
    except Exception as e:
        print(f"Error scraping email from {url}: {e}")
        
    return ""
