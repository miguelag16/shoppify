import json, util, backtrack, shoppingCartPrompt, productsListParser, re

'''
Advantage of CSP: Returns all possible assignments. 

NOTE: To perform error analysis on this, we will compare to the oracle, is the minimum price product assignment 
for every request. 

******** Use lower() for case insensitivity or re.search(str, str, re.IgnoreCase) *******
'''

def constructDepartments():
	f =  open('./departments.json', 'r')
  	departments_json = json.load(f)
  	f.close()

  	departmentDirectory = {}

	for department in departments_json:
		departmentDirectory[department] = departments_json[department]

	return departmentDirectory


def findRequestDomain(request_department, departmentDirectory):
	dictOfDepartmentProducts = productsListParser.retrieveAllProducts()

	if request_department in dictOfDepartmentProducts.keys():
		return dictOfDepartmentProducts[request_department]
	else:
		print "Request department not found: " + str(request_department)

# need to change this to add the entire request as a variable, so that we can take into account substring specifications provided by user
def addVariablesWithDomains(csp, departmentDirectory, requestList):
	for request in requestList:
		domain = findRequestDomain(request.department, departmentDirectory) #find the product domain for the request
		# domain = [(request, product) for product in request_domainProducts] # add the request to the domain for every product, useful for factors
		csp.add_variable(request, domain)


def addUnaryFactors(csp):
	# rpt = (request, product) tuple 
	for variable in csp.variables:
		csp.add_unary_factor(variable, lambda Product: Product.massPerDollar)
		csp.add_unary_factor(variable, lambda Product: float(re.search(variable.genericItemName, Product.name, flags=re.IGNORECASE) != None)*1 + 0.1)
		for descriptor in variable.specificDescriptors:
			csp.add_unary_factor(variable, lambda Product: float(re.search(descriptor, Product.name, flags=re.IGNORECASE) != None)*1 + 0.1)



def setupCSP(csp, departmentDirectory):
	# buildGroceryList returns a tuple of (a list of all requests, overall budget)
	requests = shoppingCartPrompt.buildGroceryList()

	requestList = requests[0]
	budget = requests[1]
	
	# variable = request, domain = all products in the request's main department
	# (e.g. domain = all products in "Meat & Seafood" department)
	addVariablesWithDomains(csp, departmentDirectory, requestList)

	# unaryFactors:
	# weight of products increases with match to user provided substrings in product name. Try out diff weighings
	# qt < quantity requested, the closer the amount, the better weighted. NOTE: on second thought, a price max would be more 
	# realistic to implement. better weights correspond to better match with price max.
	addUnaryFactors(csp)

	# binaryFactors: 
	# add auxiliary sum variables from pset to keep cost under the budget


def main():
	departmentDirectory = constructDepartments()
	print departmentDirectory

	csp = util.CSP()
	setupCSP(csp, departmentDirectory)

	# A backtracking algorithm that solves weighted CSP.
	search = backtrack.BacktrackingSearch()
	search.solve(csp)

main()


