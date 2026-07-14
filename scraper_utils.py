
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
    """Hits the business website to scrape contact emails, social media presence, and contact forms."""
    if not url or url == "not website" or url == "":
        return "", False, False
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    email = ""
    social_media_available = False
    contact_form_found = False

    try:
        response = requests.get(url, headers=headers, timeout=6, verify=False)
        if response.status_code != 200:
            return "", False, False
            
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for social media
        social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']
        for a in soup.find_all('a', href=True):
            if any(domain in a['href'].lower() for domain in social_domains):
                social_media_available = True
                break

        # Check for contact forms
        forms = soup.find_all('form')
        for form in forms:
            form_text = form.text.lower()
            if any(keyword in form_text for keyword in ['contact', 'message', 'name', 'email']):
                contact_form_found = True
                break
            # Also check input names
            for input_tag in form.find_all('input'):
                name_attr = input_tag.get('name', '').lower()
                if any(keyword in name_attr for keyword in ['email', 'contact', 'message']):
                    contact_form_found = True
                    break
            if contact_form_found:
                break
        
        # 1. Search for mailto links on homepage
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('mailto:'):
                potential_email = a['href'].split('mailto:')[1].split('?')[0].strip()
                if EMAIL_REGEX.match(potential_email):
                    email = potential_email
                    break
                    
        # 2. Search for raw email patterns in text
        if not email:
            valid_emails = extract_valid_emails(response.text)
            if valid_emails:
                email = valid_emails[0]
            
        # 3. If no email found, check for Contact, About, Imprint pages
        if not email:
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
                try:
                    response_contact = requests.get(contact_url, headers=headers, timeout=6, verify=False)
                    if response_contact.status_code == 200:
                        soup_contact = BeautifulSoup(response_contact.text, 'html.parser')
                        
                        # Also check contact forms on contact page
                        if not contact_form_found:
                            forms = soup_contact.find_all('form')
                            for form in forms:
                                form_text = form.text.lower()
                                if any(keyword in form_text for keyword in ['contact', 'message', 'name', 'email']):
                                    contact_form_found = True
                                    break
                                for input_tag in form.find_all('input'):
                                    name_attr = input_tag.get('name', '').lower()
                                    if any(keyword in name_attr for keyword in ['email', 'contact', 'message']):
                                        contact_form_found = True
                                        break
                                if contact_form_found:
                                    break
                        
                        for a in soup_contact.find_all('a', href=True):
                            if a['href'].startswith('mailto:'):
                                potential_email = a['href'].split('mailto:')[1].split('?')[0].strip()
                                if EMAIL_REGEX.match(potential_email):
                                    email = potential_email
                                    break
                        if not email:
                            valid_contact_emails = extract_valid_emails(response_contact.text)
                            if valid_contact_emails:
                                email = valid_contact_emails[0]
                except:
                    pass
                    
    except Exception as e:
        print(f"Error scraping email from {url}: {e}")
        
    return email, social_media_available, contact_form_found
