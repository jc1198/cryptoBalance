# CRYPTOBALANCE by Jorge Cazares


import requests
import json


def cryptoBalance(initial_value, current_value):
    balance = float(current_value) - float(initial_value)
    return round(balance, 2)

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}


def getWithCaching(baseURL, params = {}): # cache function
    req = requests.Request(method='GET',url=baseURL,params={})
    prepped = req.prepare()
    fullURL = prepped.url
    if fullURL not in CACHE_DICTION: # makes requests and stores response
        response = requests.Session().send(prepped)
        CACHE_DICTION[fullURL] = response.text
        # writes updated cache file
        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()
    return CACHE_DICTION[fullURL]


def getCrypto_USD(crypto): # returns the current value of crypto in dollars – takes in a string
    info = requests.get('https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)).text
    # info = getWithCaching(
    # 'https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)
    # )
    full_ticker = json.loads(info)
    price_USD = full_ticker[0]['price_usd']
    return price_USD

def getCrypto_24hr(crypto): # returns the percent change of the currency over the past 24 hours
    baseURL = requests.get('https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)).text
    full_ticker = json.loads(baseURL)
    percent_change = full_ticker[0]['percent_change_24h']
    return percent_change

def getCrypto_7days(crypto): # returns the percent change of the currency over the past 7 days
    baseURL = requests.get('https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)).text
    full_ticker = json.loads(baseURL)
    percent_change = full_ticker[0]['percent_change_7d']
    return percent_change


def getBalance(balance): # calculates the balance of portfolio, rounded to 2 decimals
    return round(sum(portfolio.values()),2)



portfolio = {}

crypto = input('Welcome to cryptoBalance! Please enter a cryptocurrency:')
while crypto != 'quit':
    try:
        price_USD = getCrypto_USD(crypto)
        percent_change_24 = getCrypto_24hr(crypto)
        percent_change_7 = getCrypto_7days(crypto)
        print('--'*30)
        print('The current price of one {} is ${}! The value has changed by {}% over the past 24 hours and {}% over the past 7 days.'.format(crypto,price_USD, percent_change_24, percent_change_7))
        print('--'*30)
        price_purchased = float(input('At what price in USD did you purchase this cryptocurrency?'))
        print('--'*30)
        quantity_purchased = float(input('How many coins did you purchase?'))
        initial_value = round((float(price_purchased)*float(quantity_purchased)),2)
        current_value = round((float(price_USD)*float(quantity_purchased)),2)
        print('--'*30)
        print('The initial value of your investment was {}'.format(initial_value))
        print('This is your current value: {}'.format(current_value))
        print('--'*30)
        balance = cryptoBalance(initial_value, current_value)
        portfolio[crypto] = balance
        print('Your return on this currency is ${} since you initially invested.'.format(balance))
        print('--'*30)
        print('Your porfolio: {}'.format(portfolio))
        print('--'*30)
        crypto = input('Please enter a cryptocurrency:')
        if crypto == 'find balance':
            asset_balance = getBalance(balance)
            print('The balance of your cryptocurrency assets is ${}'.format(asset_balance))
            break
    except:
        print("There was an error – please make sure you entered a valid cryptocurrency and that you are connected to the internet")
        break
