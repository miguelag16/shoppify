import json
import random
import re

def readAllStoresJSON():
	allStoresFile = './allStores.json'
	f =  open(allStoresFile, 'r')
	allStores_json = json.load(f)
 	f.close()

 	return allStores_json

def organizeByDepartment(allStores_json):
	departmentList = {}
 	for storeName, department in allStores_json.items():
 		for departmentName, products in department.items():	
 			storeDepartmentTuple = (storeName, products)
 			
 			if departmentName not in departmentList:
 				departmentList[departmentName] = list()

 			departmentList[departmentName].append(storeDepartmentTuple)

 	print json.dumps(departmentList, indent=4)

 	byDepartments_out = 'byDepartments.json'
  	byDepartments_out_w = open(byDepartments_out, 'w')
  	byDepartments_out_w.write(json.dumps(departmentList, indent=4))  

 	return departmentList

# Iterates over all departments, picking a random store and then a random item to add to the shopping cart. 
def returnBaselineShoppingCart(departmentList):
	baselineShoppingCart = list()

	for departmentName, departmentProducts in departmentList.items():
 		randomStoreIndex = random.randint(0, len(departmentProducts)-1)
 		randomStore = departmentList[departmentName][randomStoreIndex]
 		
 		storeName = randomStore[0]
 		storeDepartmentProducts = randomStore[1]

 		randomProductIndex = random.randint(0, len(storeDepartmentProducts) - 1)
 		randomProduct = storeDepartmentProducts[randomProductIndex]

 		baselineShoppingCart.append((storeName, randomProduct))

 	# print baselineShoppingCart

 	return baselineShoppingCart

# Iterates over the baseline shopping cart, totaling the shopping cart cost and tracking what stores were visited.
def returnBaseline(baselineShoppingCart):
	cost = 0
 	storesVisited = list()

 	for storeName, product in baselineShoppingCart:
 		if storeName not in storesVisited:
 			storesVisited.append(storeName)

 		productStr = re.findall("\d+\.\d+", product['price'])
 		cost += float(productStr[0])
 	
 	# print cost
 	# print storesVisited

 	return (cost, storesVisited)

# def returnOracleShoppingCart(departmentList):


def main():
	allStores_json = readAllStoresJSON()
 	departmentList = organizeByDepartment(allStores_json)

 	baselineShoppingCart = returnBaselineShoppingCart(departmentList)
 	baseline = returnBaseline(baselineShoppingCart)

 	#oracleShoppingCart = returnOracleShoppingCart(departmentList)

main() 


