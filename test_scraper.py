from utils.patent_scraper import scrape_google_patent
import tiktoken

# Helper to count tokens
def count_tokens(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example patent number
patent_id = "US10893571B2"

try:
    data = scrape_google_patent(patent_id)

    # Basic info
    print("\n🧾 Title:", data["title"])
    print("\n📄 Abstract:\n", data["abstract"] or "No abstract found.")

    # Description
    description = data["description"]
    print("\n📘 Full Description:\n", description or "No description found.")

    # Claims
    claims = data["claims"]
    print(f"\n📝 Number of Claims: {len(claims)}")
    if claims:
        print("\n🔹 First Claim:\n", claims[0])
    else:
        print("No claims found.")

    # Stats
    desc_chars = len(description)
    claims_chars = sum(len(c) for c in claims)
    total_text = data["title"] + data["abstract"] + description + ''.join(claims)
    total_bytes = len(total_text.encode('utf-8'))

    # Token counts
    desc_tokens = count_tokens(description)
    claims_tokens = count_tokens(' '.join(claims))
    total_tokens = count_tokens(total_text)

    print("\n📊 Stats:")
    print(f"   - Description Characters: {desc_chars}")
    print(f"   - Claims Characters: {claims_chars}")
    print(f"   - Total Fetched Size (UTF-8 bytes): {total_bytes}")
    print(f"   - Description Tokens: {desc_tokens}")
    print(f"   - Claims Tokens: {claims_tokens}")
    print(f"   - Total Tokens (GPT-4o): {total_tokens}")

except Exception as e:
    print("❌ Error:", e)
