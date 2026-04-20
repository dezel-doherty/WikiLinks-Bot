import embedPage

starting_page = "Spiderman"
destination_page = "Batman"

def run():
    current_page = starting_page
    
    while current_page != destination_page:
        current_page = embedPage(current_page)
        print(current_page)
        
run()