import json
import os
import pprint
import copy
import re
import time

pp = pprint.PrettyPrinter(indent=4)

'''
Returns and prints out the object allStores containing all products scraped. We can key into allStores with every store name 
(e.g. allStores['costco']), which returns the object storeObj. 

We can key into storeObj with every store department
(e.g. storeObj['eggs']), which returns a list of products in that department, store as objects.

We can retrive the product's name, price, and quantity from this object. 
'''

# Takes in a pathname "product_file", in this case a file that stores a JSON doc and prepares it for reading.
def addProducts(product_file):
  # Read in products (JSON) 
  f =  open(product_file, 'r')
  product_json = json.load(f)
  f.close()

  # Create the product list
  productList = createProductList(product_json)
  return productList

# Create product list from the JSON doc.
def createProductList(product_json):
  jsonProductList = product_json["product_list"]

  productList = []
  for product in jsonProductList:
    productInfo = {}

    if "name" in product:
      productInfo["name"] = product["name"]
    if "price" in product:
      productInfo["price"] = product["price"]
    if "quantity" in product:
      productInfo["quantity"] = product["quantity"]

    productList.append(productInfo)
      
  return productList
  
def main():
  allStores = {}
  for storeDir in os.listdir('./stores'):
    
    store = './stores/' + storeDir
    if os.path.isdir(store):
      storeObj = {}
      for department in os.listdir(store):
        
        if department.endswith('.json'):
          product_file = os.path.join(store, department)
          productList = addProducts(product_file)

          departmentName = department[len(storeDir)+1:-5]
          storeObj[departmentName] = productList

      allStores[storeDir] = storeObj

  # print allStores to file
  allStores_out = 'allStores.json'
  allStores_out_w = open(allStores_out, 'w')
  allStores_out_w.write(json.dumps(allStores))  

main()

  # The below is not important for Shopify, we need to return this list instead, or have one large list for every store

  
