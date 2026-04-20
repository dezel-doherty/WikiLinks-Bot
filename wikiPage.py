import wikipediaapi

def GetPageLinks(page_title):
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='wikilinks-script/1.0 (github.com)')
    page = wiki.page(page_title)
    if not page.exists():
        raise SystemExit('Page doesnt exist')
    
    return [page.links[title] for title in sorted(page.links)]

def ExtractFromPage(page):
    return {
        "title": page.Title,
        "categories": page.Categories,
        "summary": page.summary,
    }
    
print(GetPageLinks("Miss_Meyers"))




