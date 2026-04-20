import wikipediaapi
from wikiObject import WikiObject

starting_page = "Spiderman"

def main():
    wiki = wikipediaapi.Wikipedia(language='en', user_agent='wikilinks-script/1.0 (github.com)')
    page = wiki.page(starting_page)
    if not page.exists():
        raise SystemExit('Page doesnt exist')

    wiki_objects = []
    
    for title in sorted(page.links.keys()):
        linked_page = wiki.page(title)
        category = list(linked_page.categories.keys())[0] if linked_page.categories else None
        summary = linked_page.summary if linked_page.exists() else None
        
        wiki_objects.append(WikiObject(
            title,
            category,
            summary
        ))
         
    print(wiki_objects)
    return wiki_objects
    

if __name__ == '__main__':
    main()
