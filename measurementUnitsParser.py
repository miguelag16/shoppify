import re, collections

class Product:
	def __init__(self, name, price, qtInfo):
		self.name = name
		self.price = price

		self.measurementUnit = qtInfo["measurementUnit"] # fl oz
		self.pricePerUnit = qtInfo["pricePerUnit"] # $/fl oz

		self.quantityPerPurchase = qtInfo["quantityPerPurchase"] # how many items are included
		self.massPerPurchase = qtInfo["massPerPurchase"] # quantity per purchase * mass of one item
		


def main():

	# price = "$5.99 each"

	# string3 = "32 lbs"

	# string1 = "32 x 54.1 fl oz"

	# string2 = "At $2.69/lb"
	
	#reads in price
	price = float(re.search("\d+[.]*\d*", price, flags=re.IGNORECASE).group())

	# THE SEARCHES BELOW DEAL WITH THE QUANTITY FIELD

	# handles case of strings "At $2.69/lb", e.g.
	atString = re.search("[At]+\s*[$]", string3, flags=re.IGNORECASE)

	# this search grabs "# units or # x"
	simpleUnitString = re.search('\d+[.]*\d*\s*([a-z]+\s*)+', string3, flags=re.IGNORECASE)
	
	# this search grabs "x # units" if it is in the string
	detailedUnitString = re.search('[a-z]+\s*\d+[.]*\d*(\s*[a-z]+)+', string3, flags=re.IGNORECASE)

	qtInfo = collections.defaultdict()

	if atString == None:
		if detailedUnitString == None:
			print simpleUnitString.group()
			qtInfo["massPerPurchase"] = float(re.search('\d+[.]*\d*', simpleUnitString.group(), flags=re.IGNORECASE).group())
			qtInfo["measurementUnit"] = re.search('([a-z]+\s*)+', simpleUnitString.group(), flags=re.IGNORECASE).group()
			qtInfo["quantityPerPurchase"] = 1
			qtInfo["pricePerUnit"] = price
		else:
			qtInfo["quantityPerPurchase"] = float(re.search('\d+[.]*\d*', simpleUnitString.group()[:-1], flags=re.IGNORECASE).group())
			qtInfo["massPerPurchase"] = qtInfo["quantityPerPurchase"] * float(re.search('\d+[.]*\d*', detailedUnitString.group()[1:], flags=re.IGNORECASE).group())
			qtInfo["measurementUnit"] = re.search('([a-z]+\s*)+', detailedUnitString.group()[1:], flags=re.IGNORECASE).group()
			qtInfo["pricePerUnit"] = price / qtInfo["massPerPurchase"]
	else:
		# print re.search('[$]\d+[.]*\d*', atString.group()[2:], flags=re.IGNORECASE)
		qtInfo["pricePerUnit"] = re.search('[$]\d+[.]*\d*', string3, flags=re.IGNORECASE).group()[1:]
		qtInfo["measurementUnit"] = re.search('[/]+[a-z]+', string3, flags=re.IGNORECASE).group()[1:]
		qtInfo["quantityPerPurchase"] = 1
		qtInfo["massPerPurchase"] = 1

	print qtInfo


main()



