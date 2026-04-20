import wikipediaapi
import httpx

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "wikilinks-script/1.0 (github.com)"
BATCH_SIZE = 50


def GetPage(page_title):
    wiki = wikipediaapi.Wikipedia(language='en', user_agent=USER_AGENT)
    page = wiki.page(page_title)
    if not page.exists():
        raise SystemExit('Page doesnt exist')
    return page
    
def GetPageLinks(page_title):
    page = GetPage(page_title)
    titles = sorted(page.links)
    with httpx.Client(headers={"User-Agent": USER_AGENT}, timeout=30) as client:
        results = []
        for i in range(0, len(titles), BATCH_SIZE):
            results.extend(_query_batch(client, titles[i:i + BATCH_SIZE]))
    return results

def GetCategorySimilarity(cat, target_cat):
    count = 0
    
    for category in target_cat:
        if category in cat:
            count+=1
    return count/len(target_cat)
          
comp1 = "Spiderman"  
comp2 = "Spiderman"
print(GetCategorySimilarity(
    GetPage(comp1).categories, 
    GetPage(comp2).categories)
      )
    
    
    
    
    
    
    
    
def _query_batch(client, titles):
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles),
        "prop": "extracts|categories",
        "exintro": 1,
        "explaintext": 1,
        "cllimit": "max",
    }
    
    pages = {}
    
    while True:
        r = client.get(API_URL, params=params)
        r.raise_for_status()
        data = r.json()
        
        for pid, p in data["query"]["pages"].items():
            entry = pages.setdefault(pid, {
                "title": p.get("title"),
                "summary": p.get("extract"),
                "categories": [],
            })
            
            for c in p.get("categories", []):
                entry["categories"].append(c["title"])
                
        if "continue" not in data:
            break
        params.update(data["continue"])
    return list(pages.values())


# extracted = GetPageLinks("Miss_Meyers")
# print(extracted)
