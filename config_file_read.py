import configparser

def write():
    config = configparser.ConfigParser()

    city = input("Which city are you looking for housing in?")
    state = input("What state is that city located in?")
    
    config['Location'] = {
    'city': city,
    'state': state
    }

    Max_price = input("max_price: ")
    Min_price = input("min_price: ")
    Bedrooms = input("Preferred amount of bedrooms(1-4): ")
    House_type = input("Preferred housing type(Apartments, Houses, Condos, TownHouse, No preference)? Seperate with commas: ")

    config['Details'] = {
    'max': Max_price,
    'min': Min_price,
    'beds':Bedrooms,
    'type': House_type
    }

    with open('info.ini','w') as f:
        config.write(f)

def read(parser):
    parser.read('info.ini')