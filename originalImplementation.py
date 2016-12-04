import util

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, shoppingList, categories, productCost):
        self.shoppingList = shoppingList
        self.categories = categories
        self.productCost = productCost
        self.numItems = len(self.shoppingList)
    
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.shoppingList
        # END_YOUR_CODE
    
    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        return len(state) == 0
        # END_YOUR_CODE
    
    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        results = []
        for option in self.categories[state[0]]:
            print option
            results.append((option, state[1:], self.productCost[option]))
        return results
        # END_YOUR_CODE

def shopify(shoppingList, categories, productCost):
    if len(shoppingList) == 0:
        return []

    ucs = util.UniformCostSearch(verbose=3)
    ucs.solve(SegmentationProblem(shoppingList, categories, productCost))
    
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    return ucs.actions
    # END_YOUR_CODE

#The T is for target, everything without a T was from Walmart
list = ('milk', 'cereal')
categories = {'milk': ['Soy Slender Vanilla Soy Milk, 32 fl oz', 'Parmalat 2 Reduced Fat Milk, 32 oz (Pack of 2)', 'Orgain Organic Protein Unweetened Vanilla Almondmilk, 32 fl oz'], 'cereal': ['Quaker Honey Graham Ohs Cereal 12ozT', 'Post Spoon Size Shredded Wheat 16.4 ozT', 'Cocoa Puffs Cereal 11.8 ozT', 'Cascadian Farms Cinnamon Crunch 10.3 ozT']}
productCost = {'Parmalat 2 Reduced Fat Milk, 32 oz (Pack of 2)': 3.72, 'Soy Slender Vanilla Soy Milk, 32 fl oz': 2.34, 'Orgain Organic Protein Unweetened Vanilla Almondmilk, 32 fl oz': 4.18, 'Quaker Honey Graham Ohs Cereal 12ozT': 2.12, 'Post Spoon Size Shredded Wheat 16.4 ozT': 2.59, 'Cocoa Puffs Cereal 11.8 ozT': 2.99, 'Cascadian Farms Cinnamon Crunch 10.3 ozT': 3.29}
print shopify(list, categories, productCost)
