import time
import requests
from bs4 import BeautifulSoup

def scrape_google_patent(patent_id, retries=3):
    url = f"https://patents.google.com/patent/{patent_id}/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Successfully fetched the patent data
            break
        elif response.status_code == 503:
            # Retry with a smaller delay
            print(f"Attempt {attempt + 1} failed with 503. Retrying...")
            time.sleep(2)  # Fixed backoff, smaller delay
        else:
            # Handle other errors
            raise Exception(f"Patent {patent_id} not found or blocked. Status code: {response.status_code}")
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve patent {patent_id} after {retries} attempts.")
    
    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create a dictionary to store the data
    data = {
        "title": "",
        "abstract": "",
        "description": "",
        "claims": [],
        "priority_date": ""
    }

    # Extract data
    data["title"] = soup.find("span", itemprop="title").text.strip() if soup.find("span", itemprop="title") else "Title not available"
    data["abstract"] = soup.find("meta", {"name": "DC.description"}).get("content", "Abstract not available") if soup.find("meta", {"name": "DC.description"}) else "Abstract not available"
    data["description"] = soup.find("section", itemprop="description").get_text(strip=True) if soup.find("section", itemprop="description") else "Description not available"
    claims_section = soup.find("section", itemprop="claims")
    data["claims"] = [claim.get_text(strip=True) for claim in claims_section.find_all("div", class_="claim-text")] if claims_section else ["Claims not available"]
    data["priority_date"] = soup.find("time", itemprop="priorityDate").get_text(strip=True) if soup.find("time", itemprop="priorityDate") else "Priority date not available"

    # Add delay between requests
    time.sleep(2)

    return data
