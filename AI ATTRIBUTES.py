import requests
from bs4 import BeautifulSoup

# Pages we want to scrape
pages = {
    "Schools of Learning": "https://chanakyauniversity.edu.in/schools-of-learning/",
    "Fee Structure": "https://chanakyauniversity.edu.in/admissions/fee-structure/",
    "Research": "https://chanakyauniversity.edu.in/research/",
    "Scholarships": "https://chanakyauniversity.edu.in/research/scholarships/"
}

def fetch_page_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Grab visible text content
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
        return {
            "headings": headings,
            "paragraphs": paragraphs[:10]  # limit for preview
        }
    except Exception as e:
        return {"error": str(e)}

# Fetch all pages
for name, url in pages.items():
    print(f"\n=== {name} ===")
    data = fetch_page_content(url)
    if "error" in data:
        print("Error:", data["error"])
    else:
        print("Headings:", data["headings"])
        print("Sample Content:", data["paragraphs"])
