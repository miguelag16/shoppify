import json

# CATEGORIES = ['Produce', 'Snacks', 'Dairy & Eggs', 'Beverages', 'Household', 'Frozen', 'Deli',\
	 # 'Pantry', 'Meat & Seafood', 'Bakery', 'Canned Goods', 'Dry Goods & Pasta', 'International', 'Breakfast']

DEPARTMENTS = ['Holiday Favorites', 'Produce', 'Dairy & Eggs', 'Snacks', 'Frozen', 'Beverages', 'Deli', 'Pantry',\
	 'Meat & Seafood', 'Bakery', 'Canned Goods', 'Bulk', 'Dry Goods & Pasta', 'International', 'Breakfast']

class Request:
	def __init__(self, department, genericItemName, specificDescriptors):
		self.department = department
		self.genericItemName = genericItemName
		self.specificDescriptors = specificDescriptors

def buildGroceryList():
	print "The following departments are available:"
	for department in DEPARTMENTS:
		print "- " + department


	print "\nAdd generic items to the shopping cart for each department (e.g. ham, milk, eggs, etc.). Leave empty and return to skip. \n"

	requests = []
	for i, department in enumerate(DEPARTMENTS):
		print department

		specificDescriptors = []
		while(True):
			genericItemName = str(raw_input("	Generic item name: "))
			if(genericItemName == ''):
				break
 
 			while(True):
 				descriptor = str(raw_input("	Specific descriptor: "))
 				if(descriptor == ''):
 					break
 				specificDescriptors.append(descriptor)
			
			requests.append(Request(department, genericItemName, specificDescriptors))

			print '\n'

		print '\n'

	budget = float(raw_input("Overall budget: $"))

	return (requests, budget)
				
	# polishedRequests = []
	# for request in requests:
	# 	print (request.department, request.genericItemName, request.specificDescriptors)
		

	# 	# polishedRequests.append((request.category, request.specificItem))

	# return polishedRequests	

