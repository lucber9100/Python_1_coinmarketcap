import json
import requests
import time

class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start' : '1',
            'limit' : '100',
            'convert' : 'USD'
        }
        self.headers = {
            'Accepts' : 'application/json',
            'X-CMC_PRO_API_KEY' : 'ecf05818-bb13-4edf-8bca-a5f2d5105fb7'
        }
        self.orders = []

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']

    @staticmethod
    def sortByPercentChange24h(c):
        return c['quote']['USD']['percent_change_24h']

    @staticmethod
    def sortByMarketCap(c):
        return c['quote']['USD']['market_cap']

    @staticmethod
    def getPriceDeltaYesterday(c):
        # calcolo la differenza di prezzo della currency tra ieri ed oggi
        priceDelta = (c['quote']['USD']['price'] * c['quote']['USD']['percent_change_24h'] / 100)
        # restituice il prezzo di ieri della currency
        return c['quote']['USD']['price'] - priceDelta



# START
#------------------------------------------------------------------------------------------------------------------
# 1. La criptovaluta con il volume maggiore (in $) delle ultime 24 ore
print('\n***** ESERCIZIO 1 *****')
impactBot = Bot()
currencyVolumeHigh = None
currencies = impactBot.fetchCurrenciesData()
for currency in currencies:
    if not currencyVolumeHigh or currency['quote']['USD']['volume_24h'] > currencyVolumeHigh['quote']['USD']['volume_24h']:
        currencyVolumeHigh = currency
print('La criptovaluta con il volume maggiore (in $) delle ultime 24 ore è ' + currencyVolumeHigh['symbol'] + ' ' + currencyVolumeHigh['slug'])

# JSON
timestr = time.strftime("Ex1_%d-%m-%YT%H-%M-%S")
filename1 = timestr+".json"
with open(filename1, "w") as outfile:
    json.dump(currencyVolumeHigh, outfile, indent=4)


#------------------------------------------------------------------------------------------------------------------
# 2. Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
print('\n\n***** ESERCIZIO 2 *****')
currenciesBest = []
currenciesWorst = []
currencies.sort(key=impactBot.sortByPercentChange24h)
currenciesWorst = currencies[0:10]
currencies.reverse()
currenciesBest = currencies[0:10]
i = 0
print('Le peggiori 10 criptovalute')
for currency in currenciesWorst:
    i+=1
    print(f'{i}. ' + currency['symbol'] + ' (' + currency['slug'] + ') ' + str(currency['quote']['USD']['percent_change_24h']) + '%')
print('\nLe migliori 10 criptovalute')
i=0
for currency in currenciesBest:
    i+=1
    print(f'{i}. ' + currency['symbol'] + ' (' + currency['slug'] + ') ' + str(currency['quote']['USD']['percent_change_24h']) + '%')

# JSON
timestr = time.strftime("Ex2_%d-%m-%YT%H-%M-%S")
filename2 = timestr+".json"
with open(filename2, "w") as outfile:
    json.dump(currenciesWorst + currenciesBest, outfile, indent=4)


#------------------------------------------------------------------------------------------------------------------
# 3. La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute
print('\n\n***** ESERCIZIO 3 *****')
currencies.sort(key=impactBot.sortByMarketCap)
currencies.reverse() # ordinate da quella con capitalizzazione maggiore
currencies20 = currencies[0:20]
i = 0
totalAmount = 0
for currency in currencies20:
    i+=1
    g = float("{:.2f}".format(currency['quote']['USD']['price']))
    totalAmount += currency['quote']['USD']['price']
    print(f'{i}. ' + currency['symbol'] + ' (' + currency['slug'] + ') - Prezzo singola unità = $ ' + str(g))
totalAmount = float("{:.2f}".format(totalAmount))
print(f'Quantità di denaro totale necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute = $ ' + str(totalAmount))

# JSON
out3 = { "Quantita di denaro in $ totale necessaria per acquistare una unita di ciascuna delle prime 20 criptovalute" : totalAmount}
timestr = time.strftime("Ex3_%d-%m-%YT%H-%M-%S")
filename3 = timestr+".json"
with open(filename3, "w") as outfile:
    json.dump(out3, outfile, indent=1)


#------------------------------------------------------------------------------------------------------------------
# 4. La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
print('\n\n***** ESERCIZIO 4 *****')
totalAmount = 0
i = 0
for currency in currencies:
    if currency['quote']['USD']['volume_24h'] > 76000000:
        totalAmount += currency['quote']['USD']['price']
totalAmount = float("{:.2f}".format(totalAmount))

print(str(totalAmount) + '$ : quantità che spenderei oggi per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$')

# JSON
out4 = { "Quantita in $ che spenderei oggi per acquistare una unita di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$" : totalAmount}
timestr = time.strftime("Ex4_%d-%m-%YT%H-%M-%S")
filename4 = timestr+".json"
with open(filename4, "w") as outfile:
    json.dump(out4, outfile, indent=1)


#------------------------------------------------------------------------------------------------------------------
# 5. La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute*
# il giorno prima (ipotizzando che la classifica non sia cambiata)
print('\n\n***** ESERCIZIO 5 *****')
currencies.sort(key=impactBot.sortByMarketCap)
currencies.reverse() # ordinate da quella con capitalizzazione maggiore
currencies20 = currencies[0:20]
totalPriceToday = 0
totalPriceYesterday = 0
for currency in currencies20:
    totalPriceToday += currency['quote']['USD']['price']
    totalPriceYesterday = totalPriceYesterday + impactBot.getPriceDeltaYesterday(currency)

print(str(float("{:.2f}".format(totalPriceYesterday))) + '$ : quantità che ho speso ieri per acquistare una unità di ciascuna delle prime 20 criptovalute')
print(str(float("{:.2f}".format(totalPriceToday))) + '$ : il mio saldo ad oggi')
if totalPriceToday > totalPriceYesterday:
    print(str(float("{:.2f}".format(totalPriceToday - totalPriceYesterday))) + '$ : operazione in profitto (' + str(float("{:.2f}".format(((totalPriceToday-totalPriceYesterday)/totalPriceYesterday)*100))) + '% : variazione percentuale realizzata)')
else:
    print(str(float("{:.2f}".format(totalPriceToday - totalPriceYesterday))) + '$ : operazione in perdita (' + str(float("{:.2f}".format(((totalPriceToday-totalPriceYesterday)/totalPriceYesterday)*100))) + '% : variazione percentuale realizzata)')

# JSON
out5 = {
    "quantita che ho speso ieri per acquistare una unita di ciascuna delle prime 20 criptovalute" : float("{:.2f}".format(totalPriceYesterday)),
    "il mio saldo ad oggi" : float("{:.2f}".format(totalPriceToday)),
    "variazione realizzata in $" : float("{:.2f}".format(totalPriceToday - totalPriceYesterday)),
    "variazione realizzata in %" : float("{:.2f}".format(((totalPriceToday-totalPriceYesterday)/totalPriceYesterday)*100))
}
timestr = time.strftime("Ex5_%d-%m-%YT%H-%M-%S")
filename5 = timestr+".json"
with open(filename5, "w") as outfile:
    json.dump(out5, outfile, indent=4)