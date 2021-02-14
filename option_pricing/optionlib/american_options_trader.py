from pandas.io.data import Options

ticker = 'IBM'
x = Options(ticker)
calls, puts = x.get_options_data()