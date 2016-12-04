import util, numpy, json, collections, re
#shoppingCart

class SegmentationProblem(util.SearchProblem):
    def __init__(self, shoppingList, categories, maxCost):
        self.shoppingList = shoppingList
        self.categories = categories
        self.maxCost = maxCost
    
    def startState(self):
        return self.shoppingList
    
    def isEnd(self, state):
        return len(state) == 0
    
    def succAndCost(self, state):
        results = []
        optionsList = []
        storesVisited = set()
        for store in categories.keys():
            for category in categories[store]:
                if category == state[0].category:
                    if state[0].specificItem in item.name:
                        optionsList.add(item)
        for option in optionsList:
            storesVisited.add(option.store)
            heuristicCost = ranking[state[0].category][option.store]
            weight = self.productCost[option] / self.maxCost
            if len(storesVisited) < 3:
                results.append((option, state[1:], option.price + heuristicCost*weight))
        return results

def shopify(shoppingList, categories, productCost):
    if len(shoppingList) == 0:
        return []
    
    maxCost = 0
    for item in shoppingList:
        if numpy.mean(avgCosts[item.category], key = lambda x:x[1]):
            maxCost = numpy.mean(avgCosts[item.category], key = lambda x:x[1])

    ucs = util.UniformCostSearch(verbose=3)
    ucs.solve(SegmentationProblem(shoppingList, categories, maxCost))

    return ucs.actions

#categories is coded by Miguel
#ranking is dict of category:(dict of store:ranking). ranking[category][store] = number 1-n
#avgCosts is dict of category:list of tuples (store, average cost in that category)

f = open('allStores.json', 'r')
categories = json.load(f)
f.close()
ranking = collections.defaultdict(lambda : collections.defaultdict(int))
avgCosts = collections.defaultdict(list)
for store in categories:
    for category in categories[store].keys():
        totalCost = 0
        numItems = 0
        for item in categories[store][category]:
            price = re.findall("\d+\.\d+", item['price'])[0]
            totalCost += float(price)
            numItems += 1
        avgCosts[category].append((store, totalCost / float(numItems)))
for category in avgCosts.keys():
    sortedList = sorted(avgCosts[category], key = lambda x:x[1])
    for i in range(0, len(sortedList)):
        ranking[category][sortedList[i][0]] = i + 1

print shopify(list, categories, productCost)