import requests
from bs4 import BeautifulSoup


def scrape_job_description(url: str) -> str:
    """Scrape job description from URL with error handling."""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise exception for bad status codes
    except requests.RequestException as e:
        raise ValueError(f"Failed to fetch job description from {url}: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove noisy elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    clean = " ".join(text.split())

    if len(clean) < 100:
        raise ValueError(f"Scraped content too short ({len(clean)} chars). URL may be invalid.")

    return clean[:6000]