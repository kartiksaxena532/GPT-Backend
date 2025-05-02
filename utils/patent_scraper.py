import time
import requests
import random
from bs4 import BeautifulSoup

# Google Patents base URL
GOOGLE_PATENT_URL = "https://patents.google.com/patent/{patent_id}/en"

# Optional: List of proxies (strings in format 'http://user:pass@ip:port' or 'http://ip:port')
proxies = [
    # 'http://123.456.78.90:8080',
    # Add more proxies if needed
]

# Rotate user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0"
]

def scrape_google_patent(patent_id, retries=3):
    url = GOOGLE_PATENT_URL.format(patent_id=patent_id)

    for attempt in range(retries):
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
        }
        proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None

        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)

            if response.status_code == 200:
                print(f"Successfully fetched Google Patents page for {patent_id}")
                soup = BeautifulSoup(response.text, "html.parser")

                # Title
                title_tag = soup.find("span", attrs={"itemprop": "title"})
                title = title_tag.get_text(strip=True) if title_tag else "Title not found"

                # Abstract
                abstract_tag = soup.find("meta", attrs={"name": "DC.description"})
                abstract = abstract_tag["content"].strip() if abstract_tag else "Abstract not found"

                # Claims
                claims_tag = soup.find("section", attrs={"itemprop": "claims"})
                claims = claims_tag.get_text(strip=True) if claims_tag else "Claims not found"

                # Description
                desc_tag = soup.find("section", attrs={"itemprop": "description"})
                description = desc_tag.get_text(strip=True) if desc_tag else "Description not found"

                # Priority Date
                priority_tag = soup.find("dd", attrs={"itemprop": "priorityDate"})
                priority_date = priority_tag.get_text(strip=True) if priority_tag else "Priority date not found"

                time.sleep(random.uniform(2, 5))  # Delay to avoid getting blocked

                return {
                    "title": title,
                    "abstract": abstract,
                    "claims": claims,
                    "description": description,
                    "priority_date": priority_date,
                }

            elif response.status_code == 429:
                print(f"Rate limited (429). Waiting before retrying...")
                time.sleep(10)
            else:
                print(f"Attempt {attempt+1} failed with status {response.status_code}. Retrying...")
                time.sleep(2 ** attempt)

        except requests.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(2 ** attempt)

    raise Exception(f"Failed to fetch patent {patent_id} after {retries} attempts.")

# Example usage
if __name__ == "__main__":
    patent_id = "US11134316B1"
    try:
        data = scrape_google_patent(patent_id)
        print(data)
    except Exception as e:
        print(f"Error: {e}")
