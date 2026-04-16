import os
import requests
from bs4 import BeautifulSoup

# Directory to save web pages
SAVE_DIR = "web_pages"

# A list of URLs to fetch
URLS = [
    "https://www.google.com/search?q=play+snake+game",
    "https://example.com",
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.medium.com",
    "https://www.stackoverflow.com",
    "https://www.reddit.com",
    "https://news.ycombinator.com",
    "https://www.djangoproject.com",
]

# Fetch and save webpages
def fetch_and_save_webpages():
    os.makedirs(SAVE_DIR, exist_ok=True)
    for i, url in enumerate(URLS):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Ensure we got a valid response
            filename = f"{SAVE_DIR}/page_{i + 1}.html"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Saved {url} -> {filename}")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

# Build an in-memory index of saved HTML files
def build_index():
    index = {}
    for file in os.listdir(SAVE_DIR):
        if file.endswith(".html"):
            filepath = os.path.join(SAVE_DIR, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")
                text_content = soup.get_text()
                index[filepath] = text_content
    return index

# Search the index for a query
def search_index(index, query):
    results = []
    for filepath, content in index.items():
        if query.lower() in content.lower():
            results.append(filepath)
    return results

# Main search engine
if __name__ == "__main__":
    print("Fetching and saving web pages...")
    fetch_and_save_webpages()

    print("Building index...")
    index = build_index()

    print("Search engine ready!")
    while True:
        query = input("Enter search query (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        results = search_index(index, query)
        if not results:
            print("No results found.")
        else:
            print("Results:")
            for result in results:
                print(f" - {result}")