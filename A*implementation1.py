import util2, numpy, json, collections, re, shoppingCartPrompt, measurementUnitsParser

translateCategory = {'spices&Seasonings':'Pantry', 'eggs':'Eggs', 'latinoFoods':'International', 'grains,Rice&DriedGoods':'Dry Goods & Pasta', 'juice&Nectars':'Beverages', 'freshFruits':'Produce', 'oils&Vinegars':'Oils', 'milk':'Dairy', 'hotDogsBacon&Sausage':'Meat & Seafood', 'packagedMeat':'Deli', 'cannedMeals&Beans': 'Canned Goods', 'tortillas&flatBread':'Bakery'}

translateStore = {'wholeFoods': 'Whole Foods', 'safeway': 'Safeway', 'costco': 'Costco'}

#min time of transport for each route, round trip
#{('wholeFoods', 'safeway'): 5, ('costco', 'wholeFoods'): 10, ('safeway', 'costco'): 13, ('costco'): 14, ('safeway'): 10, ('wholeFoods'): 9}
transportationConverter = {('all three'): 38, ('wholeFoods', 'safeway'): 24, ('safeway', 'wholeFoods'): 24, ('costco', 'wholeFoods'): 33, ('wholeFoods', 'costco'): 33, ('safeway', 'costco'): 37, ('costco', 'safeway'): 37, ('safeway',): 20, ('wholeFoods',): 18, ('costco',): 28}

class SegmentationProblem(util2.SearchProblem):
    def __init__(self, shoppingList, products, listLength):
        self.shoppingList = shoppingList
        self.productsTest = products
        if listLength > 18:
            self.listLength = 19
        else:
            self.listLength = listLength

    def startState(self):
        return self.shoppingList

    def isEnd(self, state):
        return len(state) == 1
    
    def succAndCost(self, state):
        results = []
        optionsList = []
        numStores = 0
        for store in self.productsTest.keys():
            for category in self.productsTest[store]:
                if translateCategory[category] == state[0][0]:
                    numStores += 1
                    for item in self.productsTest[store][category]:
                        if state[0][1] in item['name'].lower():
                            optionsList.append((item, store))
        for option in optionsList:
            print option
            newState = state
            if option[1] not in state[len(state) - 1]:
                newStoreList = state[len(state) - 1] + (option[1],)
                newState = state[:(len(state) - 1)] + (newStoreList,)
            transportationPrice = 0.0
            if len(newState) == 2:
                if len(newState[1]) == 3:
                    transportationPrice += (1 - self.listLength/float(20))*(transportationConverter[('all three')] / float(60))*10 #multiply by minimum wage, check re: consistency
                else:
                    transportationPrice += (1 - self.listLength/float(20))*(transportationConverter[newState[1]] / float(60))*10
            heuristicCost = ranking[state[0][0]][option[1]]
            weight = (1 / float(numStores)) * heuristicCost
            if 'quantity' in option[0] and any(char.isdigit() for char in option[0]['quantity']) and any(not char.isdigit() for char in option[0]['quantity']):
                adjustedProduct = measurementUnitsParser.createProduct(option[0]['name'], re.findall("\d+\.\d+", option[0]['price'])[0], option[0]['quantity'])
                adjUnits = ''
                adjPrice = 0.0
                if adjustedProduct.measurementUnit == 'lb' or adjustedProduct.measurementUnit == 'lbs':
                    adjPrice = float(adjustedProduct.pricePerUnit)/16
                    adjUnits = 'oz'
                elif adjustedProduct.measurementUnit == 'gal' or adjustedProduct.measurementUnit == 'gallons':
                    adjPrice = float(adjustedProduct.pricePerUnit)/128
                    adjUnits = 'fl oz'
                elif adjustedProduct.measurementUnit == 'pt' or adjustedProduct.measurementUnit == 'pint':
                    adjPrice = float(adjustedProduct.pricePerUnit)/16
                    adjUnits = 'fl oz'
                elif adjustedProduct.measurementUnit == 'qt' or adjustedProduct.measurementUnit == 'quart':
                    adjPrice = float(adjustedProduct.pricePerUnit)/32
                    adjUnits = 'fl oz'
                elif adjustedProduct.measurementUnit == 'l':
                    adjPrice = float(adjustedProduct.pricePerUnit)/34
                    adjUnits = 'fl oz'
                elif adjustedProduct.measurementUnit == 'doz' or adjustedProduct.measurementUnit == 'dzn' or adjustedProduct.measurementUnit == 'dozen':
                    adjPrice = float(adjustedProduct.pricePerUnit)/12
                    adjUnits = 'ct'
                elif adjustedProduct.measurementUnit == adjustedProduct.measurementUnit == 'cnt':
                    adjPrice = adjustedProduct.pricePerUnit
                    adjUnits = 'ct'
                else:
                    adjPrice = adjustedProduct.pricePerUnit
                    adjUnits = adjustedProduct.measurementUnit
                print adjPrice
                option = option + ('%f per %s' % (adjPrice, adjUnits),)
                results.append((option, newState[1:], float(adjPrice) + float(adjPrice)*weight + transportationPrice))
            else:
                price = re.findall("\d+\.\d+", option[0]['price'])[0]
                results.append((option, newState[1:], float(price) + float(price)*weight + transportationPrice))
        return results

def shopify(shoppingList, products):
    if len(shoppingList) == 0:
        return []

    ucs = util2.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(shoppingList, products, len(shoppingList) - 1))

    return ucs.actions

#products is coded by Miguel
#ranking is dict of category:(dict of store:ranking). ranking[category][store] = number 1-n
#avgCosts is dict of category:list of tuples (store, average cost in that category)

f = open('allStores.json', 'r')
products = json.load(f)
f.close()
ranking = collections.defaultdict(lambda : collections.defaultdict(int))
avgCosts = collections.defaultdict(list)
for store in products:
    for category in products[store].keys():
        totalCost = 0
        numItems = 0
        for item in products[store][category]:
            if 'quantity' in item:
                if any(char.isdigit() for char in item['quantity']) and any(not char.isdigit() for char in item['quantity']):
                    adjustedProduct = measurementUnitsParser.createProduct(item['name'], re.findall("\d+\.\d+", item['price'])[0], item['quantity'])
                    adjPrice = 0.0
                    if adjustedProduct.measurementUnit == 'lb' or adjustedProduct.measurementUnit == 'lbs':
                        adjPrice = float(adjustedProduct.pricePerUnit)/16
                    elif adjustedProduct.measurementUnit == 'gal' or adjustedProduct.measurementUnit == 'gallons':
                        adjPrice = float(adjustedProduct.pricePerUnit)/128
                    elif adjustedProduct.measurementUnit == 'pt' or adjustedProduct.measurementUnit == 'pint':
                        adjPrice = float(adjustedProduct.pricePerUnit)/16
                    elif adjustedProduct.measurementUnit == 'qt' or adjustedProduct.measurementUnit == 'quart':
                        adjPrice = float(adjustedProduct.pricePerUnit)/32
                    elif adjustedProduct.measurementUnit == 'l':
                        adjPrice = float(adjustedProduct.pricePerUnit)/34
                    elif adjustedProduct.measurementUnit == 'doz' or adjustedProduct.measurementUnit == 'dzn' or adjustedProduct.measurementUnit == 'dozen':
                        adjPrice = float(adjustedProduct.pricePerUnit)/12
                    else:
                        adjPrice = adjustedProduct.pricePerUnit
                    totalCost += float(adjPrice)
                    numItems += 1
        avgCosts[translateCategory[category]].append((store, totalCost / float(numItems)))
for category in avgCosts.keys():
    sortedList = sorted(avgCosts[category], key = lambda x:x[1])
    for i in range(0, len(sortedList)):
        ranking[category][sortedList[i][0]] = i + 1

shoppingList = shoppingCartPrompt.pullRequests()
shoppingList.append(())

actions = shopify(tuple(shoppingList), products)
for action in actions:
    print "Item:", action[0]['name'], "| Price:", action[2], "| Store:", translateStore[action[1]]
