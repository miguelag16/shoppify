import productsListParser

def standardizeUnits(Product):
    # print (Product.name, Product.price, Product.pricePerUnit, Product.measurementUnit, Product.badUnitsFlag)
    
    if Product.measurementUnit == 'lb' or Product.measurementUnit == 'lbs':
        Product.pricePerUnit = float(Product.pricePerUnit)/16
        Product.measurementUnit = 'oz'
    elif Product.measurementUnit == 'gal' or Product.measurementUnit == 'gallons':
        Product.pricePerUnit = float(Product.pricePerUnit)/128
        Product.measurementUnit = 'fl oz'
    elif Product.measurementUnit == 'pt' or Product.measurementUnit == 'pint':
        Product.pricePerUnit = float(Product.pricePerUnit)/16
        Product.measurementUnit = 'fl oz'
    elif Product.measurementUnit == 'qt' or Product.measurementUnit == 'quart':
        Product.pricePerUnit = float(Product.pricePerUnit)/32
        Product.measurementUnit = 'fl oz'
    elif Product.measurementUnit == 'l':
        Product.pricePerUnit = float(Product.pricePerUnit)/34
        Product.measurementUnit = 'fl oz'
    elif Product.measurementUnit == 'doz' or Product.measurementUnit == 'dzn' or Product.measurementUnit == 'dozen':
        Product.pricePerUnit = float(Product.pricePerUnit)/12
        Product.measurementUnit = 'ct'
    elif Product.measurementUnit == 'count' or Product.measurementUnit == 'cnt':
        Product.measurementUnit = 'ct'

    if Product.measurementUnit == 'oz' or Product.measurementUnit == 'fl oz' or Product.measurementUnit == 'ct':
        Product.massPerDollar = Product.pricePerUnit**-1
        Product.badUnitsFlag = None

    # print (Product.name, Product.price, Product.pricePerUnit, Product.measurementUnit, Product.badUnitsFlag)
