if len(option[0]) > 2 and any(char.isdigit() for char in option[0]['quantity']):
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
