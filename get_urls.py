from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

base_url = "https://www.fullerton.edu/ecs/cs"

def get_internal_links(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    anchors = soup.find_all('a', href=True)
    print(f"Found {len(anchors)} <a> tags.")

    internal_links = set()
    for anchor in anchors:
        href = anchor['href']
        # print(href)
        
        # Skip invalid or irrelevant links
        if href.startswith('javascript:') or href.startswith('#'):
            continue

        # Convert relative links to absolute
        full_url = urljoin(base_url, href)
        print(full_url)
        
        # Filter for internal links within the CSUF domain
        if "csuf.edu" in urlparse(full_url).netloc.lower():
            internal_links.add(full_url)

    return list(internal_links)

# Extract and save links
internal_links = get_internal_links(base_url)
print(f"Extracted {len(internal_links)} internal links.")
for link in internal_links:  # Print all valid links
    print(link)

# # Save links to a file
# with open("internal_links.txt", "w") as file:
#     for link in internal_links:
#         file.write(link + "\n")
# print("Links saved to internal_links.txt.")
