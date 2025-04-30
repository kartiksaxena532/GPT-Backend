import requests
from bs4 import BeautifulSoup

def scrape_google_patent(patent_id):
    url = f"https://patents.google.com/patent/{patent_id}/en"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Patent not found or blocked")

    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        "title": soup.find("span", itemprop="title").text.strip() if soup.find("span", itemprop="title") else "",
        "abstract": soup.find("meta", {"name": "DC.description"}).get("content", ""),
        "description": "",
        "claims": [],
        "priority_date": ""
    }

    # Get description section
    desc_tag = soup.find("section", itemprop="description")
    if desc_tag:
        data["description"] = desc_tag.text.strip()

    # Get claims section
    claims_section = soup.find("section", itemprop="claims")
    if claims_section:
        data["claims"] = [c.text.strip() for c in claims_section.find_all("div", class_="claim-text")]

    # Get priority date
    priority_date_tag = soup.find("time", itemprop="priorityDate")
    if priority_date_tag:
        data["priority_date"] = priority_date_tag.text.strip()

    return data