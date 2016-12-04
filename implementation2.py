import util, numpy, json, collections, re, shoppingCartPrompt

translateCategory = {'spices&Seasonings':'Pantry', 'eggs':'Eggs', 'hispanicFood':'International', 'dryGoods&Pasta':'Dry Goods & Pasta', 'juice&Nectars':'Beverages', 'fruit':'Produce', 'oils&Vinegars':'Pantry', 'milk':'Dairy', 'hotDogsBacon&Sausage':'Meat & Seafood', 'packagedMeat':'Deli', 'cannedMeals&Beans': 'Canned Goods', 'tortillas&flatBread':'Bakery'}

class SegmentationProblem(util.SearchProblem):
    def __init__(self, shoppingList, products, bestStores, maxCost):
        self.shoppingList = shoppingList
        self.products = products
        self.bestStores = bestStores
        self.maxCost = maxCost
    
    def startState(self):
        return self.shoppingList
    
    def isEnd(self, state):
        return len(state) == 0
    
    def succAndCost(self, state):
        results = []
        optionsList = []
        for store in bestStores:
            for category in products[store]:
                if translateCategory[category] == state[0][0]:
                    for item in products[store][category]:
                        if state[0][1] in item['name'].lower():
                            optionsList.append((item, store))
        for option in optionsList:
            price = re.findall("\d+\.\d+", option[0]['price'])[0]
            results.append((option, state[1:], float(price)))
        return results

def shopify(shoppingList, products, bestStores):
    if len(shoppingList) == 0:
        return []
    
    maxCost = 0
    for item in shoppingList:
        totalCost = 0
        storeCount = 0
        for i in range(len(avgCosts[item[0]])):
            totalCost += avgCosts[item[0]][i][1]
            storeCount += 1
        if totalCost / float(storeCount) > maxCost:
            maxCost = totalCost / float(storeCount)

    ucs = util.UniformCostSearch(verbose=3)
    ucs.solve(SegmentationProblem(shoppingList, products, bestStores, maxCost))
    
    return ucs.actions

#Builds dictionaries of average costs and rankings among stores, both by category.
#ranking is dict of category:(dict of store:ranking). ranking[category][store] = number between 1, number of stores inclusive
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
            price = re.findall("\d+\.\d+", item['price'])[0]
            totalCost += float(price)
            numItems += 1
        avgCosts[translateCategory[category]].append((store, totalCost / float(numItems)))
for category in avgCosts.keys():
    sortedList = sorted(avgCosts[category], key = lambda x:x[1])
    for i in range(0, len(sortedList)):
        ranking[category][sortedList[i][0]] = i + 1

shoppingList = shoppingCartPrompt.pullRequests()

#Goes through each store and calculates heuristic value based on average cost of each item's category at that store. Takes two cheapest stores according to heuristic and limits UCS to those stores

storeHeuristic = collections.defaultdict(float)
completeStores = set()
bestStores = set()
for store in products.keys():
    itemsAdded = 0
    for item in shoppingList:
        for pair in avgCosts[item[0]]:
            if pair[0] == store:
                storeHeuristic[store] += pair[1] + ranking[item[0]][store]
                itemsAdded += 1
    if itemsAdded == len(shoppingList):
        completeStores.add(store)
for store in storeHeuristic.keys():
    if store not in completeStores:
        del storeHeuristic[store]
bestStores.add(min(storeHeuristic))
del storeHeuristic[min(storeHeuristic)]
bestStores.add(min(storeHeuristic))

print shopify(tuple(shoppingList), products, bestStores)
