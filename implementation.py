import util, numpy, json, collections, re, shoppingCartPrompt

translateCategory = {'spices&Seasonings':'Pantry', 'eggs':'Eggs', 'hispanicFood':'International', 'dryGoods&Pasta':'Dry Goods & Pasta', 'juice&Nectars':'Beverages', 'fruit':'Produce', 'oils&Vinegars':'Pantry', 'milk':'Dairy', 'hotDogsBacon&Sausage':'Meat & Seafood', 'packagedMeat':'Deli', 'cannedMeals&Beans': 'Canned Goods', 'tortillas&flatBread':'Bakery'}

class SegmentationProblem(util.SearchProblem):
    def __init__(self, shoppingList, products, maxCost):
        self.shoppingList = shoppingList
        self.products = products
        self.maxCost = maxCost
    
    def startState(self):
        return self.shoppingList
    
    def isEnd(self, state):
        return len(state) == 0
    
    def succAndCost(self, state):
        results = []
        optionsList = []
        for store in products.keys():
            for category in products[store]:
                if translateCategory[category] == state[0][0]:
                    for item in products[store][category]:
                        print item
                        if state[0][1] in item['name'].lower():
                            optionsList.append((item, store))
        for option in optionsList:
            heuristicCost = ranking[state[0][0]][option[1]]
            price = re.findall("\d+\.\d+", option[0]['price'])[0]
            weight = float(price) / self.maxCost
            results.append((option, state[1:], float(price) + heuristicCost*weight))
        return results

def shopify(shoppingList, products):
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
    print type(shoppingList), type(products)
    ucs.solve(SegmentationProblem(shoppingList, products, maxCost))

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
            price = re.findall("\d+\.\d+", item['price'])[0]
            totalCost += float(price)
            numItems += 1
        avgCosts[translateCategory[category]].append((store, totalCost / float(numItems)))
for category in avgCosts.keys():
    sortedList = sorted(avgCosts[category], key = lambda x:x[1])
    for i in range(0, len(sortedList)):
        ranking[category][sortedList[i][0]] = i + 1

shoppingList = shoppingCartPrompt.pullRequests()

print shopify(tuple(shoppingList), products)
