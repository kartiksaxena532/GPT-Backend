import requests
from bs4 import BeautifulSoup
import time

def scrape_google_patent(patent_id):
    url = f"https://patents.google.com/patent/{patent_id}/en"
    headers = {"User-Agent": "Mozilla/5.0"}

    # Make the request with a delay to prevent being blocked
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Patent {patent_id} not found or blocked. Status code: {response.status_code}")

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
