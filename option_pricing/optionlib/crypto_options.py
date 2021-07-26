from deribit_api import RestClient
client = RestClient(key='2AakQouj', secret='k758JijEUkrbDv9IFOPwU6X2iT4_Z6oNL8lZO7UcBks')
btc = client.index()
account = client.account()

# !!!!
instruments = client.getlasttrades(instrument='BTC-25JUN21')

currencies = client.getcurrencies()
summary = client.getsummary('BTC-25JUN21')

positions = client.positions()
history = client.tradehistory(instrument='BTC-25JUN21')
print()