import time
import requests
import random
from bs4 import BeautifulSoup

# USPTO API URL (example to get patent details by patent number)
USPTO_API_URL = "https://api.uspto.gov/patent/v1/patent/{patent_id}"

def scrape_google_patent(patent_id, retries=3):
    # Format the URL with the patent ID
    url = USPTO_API_URL.format(patent_id=patent_id)

    # List of User-Agents to rotate (optional for further optimization)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    ]
    headers = {"User-Agent": random.choice(user_agents)}  # Randomize User-Agent

    # Retry logic with exponential backoff
    for attempt in range(retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Successfully fetched the patent data
            print(f"Successfully fetched patent {patent_id}")
            break
        elif response.status_code == 503:
            # Server unavailable, retry with backoff
            print(f"Attempt {attempt + 1} failed with 503. Retrying in {2 ** attempt} seconds...")
            time.sleep(2 ** attempt)  # Exponential backoff (2, 4, 8 seconds, etc.)
        else:
            # Handle other errors (e.g., 404, 500)
            raise Exception(f"Patent {patent_id} not found or blocked. Status code: {response.status_code}")
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve patent {patent_id} after {retries} attempts.")

    # Extract data from the response
    data = response.json()

    # Create a dictionary to store the extracted patent data
    patent_data = {
        "title": data.get("title", "Title not available"),
        "abstract": data.get("abstract", "Abstract not available"),
        "description": data.get("description", "Description not available"),
        "claims": data.get("claims", "Claims not available"),
        "priority_date": data.get("priority_date", "Priority date not available"),
    }

    # Add a delay between requests to avoid being blocked (adjust as needed)
    time.sleep(2)

    return patent_data

# Example usage
try:
    patent_id = "US11134316B1"  # Example patent ID
    patent_data = scrape_google_patent(patent_id)
    print(patent_data)
except Exception as e:
    print(f"Error fetching patent data: {e}")
