import requests
from bs4 import BeautifulSoup
import time

def scrape_google_patent(patent_id, retries=5):
    url = f"https://patents.google.com/patent/{patent_id}/en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for attempt in range(retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            # Successfully fetched the patent data
            break
        elif response.status_code == 503:
            # Server is temporarily unavailable, retry after exponential backoff
            print(f"Attempt {attempt + 1} failed with 503. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff (2, 4, 8, 16 seconds)
        else:
            # Other status codes (e.g., 404, 500), log and raise the exception
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

    # Get title
    title_tag = soup.find("span", itemprop="title")
    data["title"] = title_tag.text.strip() if title_tag else "Title not available"

    # Get abstract
    abstract_tag = soup.find("meta", {"name": "DC.description"})
    data["abstract"] = abstract_tag.get("content", "Abstract not available") if abstract_tag else "Abstract not available"

    # Get description
    desc_tag = soup.find("section", itemprop="description")
    data["description"] = desc_tag.get_text(strip=True) if desc_tag else "Description not available"

    # Get claims
    claims_section = soup.find("section", itemprop="claims")
    if claims_section:
        data["claims"] = [claim.get_text(strip=True) for claim in claims_section.find_all("div", class_="claim-text")]
    else:
        data["claims"] = ["Claims not available"]

    # Get priority date
    priority_date_tag = soup.find("time", itemprop="priorityDate")
    data["priority_date"] = priority_date_tag.get_text(strip=True) if priority_date_tag else "Priority date not available"

    # Add a delay between requests to avoid being blocked by Google Patents
    time.sleep(2)  # sleep for 2 seconds (adjust based on your scraping volume)

    return data

# Example usage
try:
    patent_data = scrape_google_patent("US11134316B1")
    print(patent_data)
except Exception as e:
    print("Error scraping patent:", e)
