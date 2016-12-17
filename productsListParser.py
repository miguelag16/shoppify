import re, os, json, collections, unitStandardizer

'''
Example string field variants:

	# price = "$5.99 each"

	# quantity1 = "32 lbs"

	# quantity2 = "32 x 54.1 fl oz"

	# quantity3 = "At $2.69/lb"
'''
def isFloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

class Product:
	def __init__(self):
		self.name = None
		self.price = None
		self.quantity = 0
		self.store = None
		self.department = None
		self.subdepartment = None

		self.parsedPrice = 0

		self.measurementUnit = None # fl oz
		self.pricePerUnit = 0 # $/fl oz
		self.massPerDollar = 0 # fl oz/$

		self.quantityPerPurchase = 0 # how many items are included
		self.massPerPurchase = 0 # quantity per purchase * mass of one item

		self.badUnitsFlag = -1


	def addProductInfo(self, productInfo):
		self.name = productInfo["name"]
		self.price = productInfo["price"]
		self.quantity = productInfo["quantity"]
		self.store = productInfo["store"]
		self.department = productInfo["department"]
		self.subdepartment = productInfo["subdepartment"]

		price = float(re.search("\d+[.]*\d*", self.price, flags=re.IGNORECASE).group())
		self.parsedPrice = price


	def addQtInfo(self, price, quantity):
		#reads in price
		# price = "$5.99 each"
		# quantity = "0.23 fl oz"
		# quantity = "0123.212 fl oz"

		# this is redundant with the one above, delete one of the two?
		price = float(re.search("\d+[.]*\d*", price, flags=re.IGNORECASE).group())
		self.parsedPrice = price

		if isFloat(quantity):
			self.measurementUnit = 'ct'
			self.quantityPerPurchase = 1
			self.pricePerUnit = price
			return

		# THE SEARCHES BELOW DEAL WITH THE QUANTITY FIELD

		# handles case of strings "At $2.69/lb", e.g.
		atString = re.search("[At]+\s*[$]", quantity, flags=re.IGNORECASE)

		# this search grabs "# units or # x"
		simpleUnitString = re.search('\d*[.]?\d*\s*([a-z]+\s*)+', quantity, flags=re.IGNORECASE)
		
		# this search grabs "x # units" if it is in the string
		detailedUnitString = re.search('[a-z]+\s*\d+[.]*\d*(\s*[a-z]+)+', quantity, flags=re.IGNORECASE)

		# don't use group until you make sure value is not None
		if atString == None:

			if detailedUnitString == None:
				self.massPerPurchase = float(re.search('\d*[.]?\d*', simpleUnitString.group(), flags=re.IGNORECASE).group())
				self.measurementUnit = re.search('([a-z]+\s*)+', simpleUnitString.group(), flags=re.IGNORECASE).group()
				self.quantityPerPurchase = 1
				self.pricePerUnit = price / self.massPerPurchase
				# self.massPerDollar = self.pricePerUnit**-1
			else:
				self.quantityPerPurchase = float(re.search('\d+[.]*\d*', simpleUnitString.group()[:-1], flags=re.IGNORECASE).group())
				self.massPerPurchase = self.quantityPerPurchase * float(re.search('\d+[.]*\d*', detailedUnitString.group()[1:], flags=re.IGNORECASE).group())
				self.measurementUnit = re.search('([a-z]+\s*)+', detailedUnitString.group()[1:], flags=re.IGNORECASE).group()
				self.pricePerUnit = price / self.massPerPurchase
				# self.massPerDollar = self.pricePerUnit**-1
		else:
			self.pricePerUnit = float(re.search('[$]\d+[.]*\d*', quantity, flags=re.IGNORECASE).group()[1:])
			self.measurementUnit = re.search('[/]+[a-z]+', quantity, flags=re.IGNORECASE).group()[1:]
			self.quantityPerPurchase = 1
			self.massPerPurchase = 1
			# self.massPerDollar = self.pricePerUnit**-1


 # Create product list from the JSON doc.
def createProductList(product_json):
	jsonProductList = product_json["product_list"]

	productList = []
  	for product in jsonProductList:
  		newProductObj = Product()
  		
  		productInfo = collections.defaultdict()
  		for key in product:
  			productInfo[key] = product[key]

  		if "quantity" in product:
  			if re.search('[0-9]+', product["quantity"], re.IGNORECASE) != None:
				newProductObj.addQtInfo(product["price"], product["quantity"])
		else:
			productInfo["quantity"] = None

		unitStandardizer.standardizeUnits(newProductObj)
		# print newProductObj.badUnitsFlag

		if newProductObj.badUnitsFlag != -1:
			newProductObj.addProductInfo(productInfo)
			productList.append(newProductObj)

	return productList


# Takes in a pathname "product_file", in this case a file that stores a JSON doc and prepares it for reading.
def addProducts(department_file):
	# Read in products (JSON) 
  	f =  open(department_file, 'r')
  	product_json = json.load(f)
  	f.close()

  	# Create the product list
  	productList = createProductList(product_json)
  	return productList

def main():
	allProducts = collections.defaultdict(list)

	x = 0

	for storeDir in os.listdir('../stores'):
		store = '../stores/' + storeDir
		if os.path.isdir(store):
	  	
	  		for subdepartment in os.listdir(store):
				if subdepartment.endswith('.json'):
					subdepartment_file = os.path.join(store, subdepartment)
	      			productList = addProducts(subdepartment_file)

	      			departmentName = productList[0].department
	      			
	      			for product in productList:
	      				x += 1
	      				allProducts[departmentName].append(product)
	      				

	print x
	return allProducts  

main()
