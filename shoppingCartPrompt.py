import json

CATEGORIES = ['Produce', 'Snacks', 'Dairy', 'Eggs', 'Beverages', 'Household', 'Frozen', 'Deli', 'Pantry', 'Meat & Seafood', 'Bakery', 'Canned Goods', 'Dry Goods & Pasta', 'International', 'Breakfast']

# Takes note of what categories have been selected of the user and returns a len(CATEGORIES) array with this info.
def selectCategories():
    print "Input 1 to select food category, 0 to skip category."
    
    
    selections = []
    for category in CATEGORIES:
        response = int(raw_input(category + "? "))
                
        while(response < 0 or response > 1):
            print "Please try again. Input 1 to select food category, 0 to skip category."
            response = int(raw_input(category + "? "))
        
        selections.append(response)
    
    return selections


class Request:
    def __init__(self, category, specificItem):
        self.category = category
        self.specificItem = specificItem

def returnRequests(selections):
    print "\n Add generic items to the shopping cart for each category (e.g. ham, milk, eggs, etc.).\n"
        
    requests = []
    for i, category in enumerate(CATEGORIES):
        if (selections[i] == 1):
            print category
                    
            specificItem = None
            while(True):
                specificItem = str(raw_input("    Specific item: "))
                                
                if(specificItem == ''):
                    break
                else:
                    requests.append(Request(category, specificItem))
                    
            print '\n'
    
    return requests

def pullRequests():	
    selections = selectCategories()
        
    requests = returnRequests(selections)
        
    polishedRequests = []
    for request in requests:
        polishedRequests.append((request.category, request.specificItem))
        
    return polishedRequests
