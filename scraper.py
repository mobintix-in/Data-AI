import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs

def get_driver():
    """Configures and returns a headless Selenium Chrome WebDriver."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1200,800')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_element(driver, strategies, attribute=None):
    """Helper to try multiple locator strategies to extract text or attribute."""
    for by, value in strategies:
        try:
            el = driver.find_element(by, value)
            if attribute:
                return el.get_attribute(attribute).strip()
            return el.text.strip()
        except:
            continue
    return ""

def scrape_google_maps(niche, city, country):
    driver = None
    scraped_leads = []
    
    try:
        driver = get_driver()
        search_query = f"{niche} in {city}, {country}"
        driver.get(f"https://www.google.com/maps/search/{search_query}?hl=en")
        time.sleep(1.5)
        
        try:
            consent_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Accept all') or contains(., 'Accept') or contains(., 'Agree')]")
            if consent_buttons:
                consent_buttons[0].click()
                time.sleep(1)
        except:
            pass
            
        business_urls = []
        if "/maps/place/" in driver.current_url:
            business_urls.append(driver.current_url)
        else:
            try:
                WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
                )
                feed = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                for _ in range(2):
                    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", feed)
                    time.sleep(1)
            except Exception as e:
                print("Sidebar feed not found or failed to scroll:", e)
                
            links_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
            for link in links_elements:
                href = link.get_attribute('href')
                if href and href not in business_urls:
                    business_urls.append(href)
                    
        business_urls = business_urls[:8]
        print(f"Found {len(business_urls)} business detail URLs. Commencing details scrape...")
        
        for url in business_urls:
            try:
                driver.get(url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1')))
                time.sleep(0.5)
                
                name = extract_element(driver, [(By.CSS_SELECTOR, 'h1')])
                
                address_strategies = [
                    (By.CSS_SELECTOR, '[data-item-id="address"]'),
                ]
                address = extract_element(driver, address_strategies)
                if not address:
                    address = extract_element(driver, [(By.XPATH, "//*[contains(@aria-label, 'Address:')]")], attribute='aria-label')
                    address = address.replace('Address:', '').strip()
                
                website_strategies = [(By.CSS_SELECTOR, '[data-item-id="authority"]')]
                website = extract_element(driver, website_strategies, attribute='href')
                if not website:
                    # fallback to tag lookup
                    try:
                        wel = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]')
                        if wel.tag_name != 'a':
                            link_child = wel.find_element(By.TAG_NAME, 'a')
                            website = link_child.get_attribute('href')
                    except:
                        website = extract_element(driver, [(By.XPATH, "//*[contains(@aria-label, 'Website:')]")], attribute='href')
                
                if website and "google.com/url" in website:
                    parsed = urlparse(website)
                    website = parse_qs(parsed.query).get('q', [website])[0]
                    
                phone = extract_element(driver, [(By.XPATH, "//*[contains(@aria-label, 'Phone:')]")], attribute='aria-label')
                phone = phone.replace('Phone:', '').strip()
                if not phone:
                    try:
                        phone_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-item-id^="phone:tel:"]')
                        if phone_buttons:
                            phone = phone_buttons[0].get_attribute("data-item-id").replace("phone:tel:", "").strip()
                    except:
                        pass
                
                rating = ""
                reviews = ""
                try:
                    rating_el = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'stars')]")
                    aria_label = rating_el.get_attribute('aria-label')
                    match = re.search(r'([\d\.]+)\s+stars?.*?([\d,]+)\s+Reviews?', aria_label, re.IGNORECASE)
                    if match:
                        rating = match.group(1)
                        reviews = match.group(2)
                    elif "stars" in aria_label:
                        rating = aria_label.split("stars")[0].strip()
                except:
                    pass
                    
                price_range = ""
                try:
                    price_el = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Price:')]")
                    price_range = price_el.get_attribute('aria-label').replace('Price:', '').strip()
                except:
                    try:
                        header_spans = driver.find_elements(By.CSS_SELECTOR, 'span')
                        for span in header_spans:
                            if span.text in ['$', '$$', '$$$', '$$$$']:
                                price_range = span.text
                                break
                    except:
                        pass
                        
                niche_size = ""
                try:
                    if reviews:
                        num_reviews = int(reviews.replace(',', ''))
                        if num_reviews < 50:
                            niche_size = "Small"
                        elif num_reviews < 500:
                            niche_size = "Medium"
                        else:
                            niche_size = "Large"
                except:
                    pass
                    
                google_maps_verified = True
                try:
                    claim_elements = driver.find_elements(By.XPATH, "//*[contains(@aria-label, 'Claim this business') or contains(text(), 'Claim this business') or contains(@href, 'business.google.com/add')]")
                    if claim_elements:
                        google_maps_verified = False
                except:
                    pass

                business_active = True
                page_text = driver.page_source.lower()
                if "permanently closed" in page_text or "temporarily closed" in page_text:
                    business_active = False

                scraped_leads.append({
                    "name": name,
                    "rating": rating,
                    "reviews": reviews,
                    "price_range": price_range,
                    "niche_size": niche_size,
                    "address": address,
                    "phone": phone,
                    "website": website,
                    "google_maps_verified": google_maps_verified,
                    "business_active": business_active
                })
            except Exception as ex:
                print(f"Error extracting business profile details at {url}: {ex}")
                
    finally:
        if driver:
            driver.quit()
            
    return scraped_leads
