import httpx
from embedder import *

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "wikilinks-script/1.0 (github.com)"
BATCH_SIZE = 50

def query_batch(client, titles, include_links=False):
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles),
        "prop": "extracts|categories" + ("|links" if include_links else ""),
        "exintro": 1,
        "explaintext": 1,
        "cllimit": "max",
        "pllimit": "max",  # needed for links
        "plnamespace": 0,  # article links only
        "redirects": 1,    # follow redirects like "Spider-man" → "Spider-Man"
    }
    
    pages = {}
    
    while True:
        result = client.get(API_URL, params=params)
        result.raise_for_status()
        data = result.json()
        
        for pid, p in data["query"]["pages"].items():
            entry = pages.setdefault(pid, {
                "title": p.get("title"),
                "summary": p.get("extract"),
                "links": []
            })
            
            if include_links and "links" in p:
                entry["links"].extend(link["title"] for link in p["links"])
                
        if "continue" not in data:
            break
        params.update(data["continue"])
    
    return list(pages.values())

def get_page(title):
    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30) as client:
        pages = query_batch(client, [title])
        return pages[0] if pages else None

def get_page_links(page_title):
    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30) as client:
        pages = query_batch(client, [page_title], include_links=True)
        if not pages:
            return []
        return pages[0]["links"]

def get_n_closest_page(page, target_page, page_number):
    current_links = get_page_links(page["title"])

    if target_page["title"] in current_links:
        return [target_page]

    top = get_n_most_similar(target_page["title"], current_links, page_number)
    titles = [title for title, _ in top]

    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30) as client:
        fetched = query_batch(client, titles)

    by_title = {p["title"]: p for p in fetched}
    return [by_title[t] for t in titles if t in by_title]
    
def get_closest_page(page, target_page):
    get_n_closest_page(page, target_page, 1)
    
    
    
    
    
if __name__ == "__main__":
    starting_title = "Technical report"
    destination_title = "British Standard Pipe"
    
    current_page = get_page(starting_title)
    destination_page = get_page(destination_title)

    links = []
    
    print(starting_title)
    
    while current_page != destination_page:
        n_most_similar = get_n_closest_page(current_page, destination_page, 10)
        most_similar = n_most_similar[0]
        
        if destination_page in n_most_similar:
            current_page = destination_page
        else:
            if most_similar["title"] in links:
                rank = 1
                while current_page["title"] in links:
                    current_page = n_most_similar[rank]
                    rank += 1           
            else:
                current_page = most_similar
            
        links.append(current_page["title"])
        print(current_page["title"])