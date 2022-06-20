import datetime
import math
import sqlite3
import statistics
from datetime import date
import yfinance as yf

DAYS_IN_YEAR = 252
DATE = 'date'
OPTIONOPEN = 'option_open'
STOCKOPEN = 'stock_open'


class AmericanOptions(object):

    def __init__(self, stock_name: str, option_name: str, r: float, database: str):
        self.stock = stock_name
        self.r = r
        self.option = option_name
        self.stock_data = None
        self.option_data = None
        self.db_conn = sqlite3.connect(database=database)
        self.db_cursor = self.db_conn.cursor()
        expiration_date = self.option[4:10]
        self.expiration_date = '20{}-{}-{}'.format(expiration_date[:2], expiration_date[2:4],
                                                   expiration_date[4:])
        self.option_type = 'Call' if self.option[10] == 'C' else 'Put'
        self.K = float('{}.{}'.format(self.option[13:16], self.option[16:]))
        self.data = {}

    def get_data(self):
        """
        Download data for selected stock and option and corresponding stock.

        """

        option_data = yf.Ticker(self.option)
        option_values = option_data.history('max')
        start_date = str(option_values.head(1).index.values[0])
        start_date = start_date.split('T')[0]

        stock_values_dict = {}
        stock_data = yf.Ticker(self.stock)
        stock_values = stock_data.history(start=start_date)
        for date, value in stock_values.iterrows():
            stock_values_dict[str(date).split(" ")[0]] = value['Open']
            print("Date: {}, Open: {}".format(date, value['Open']))

        for date, value in option_values.iterrows():
            key = str(date).split(" ")[0]
            self.data[key] = {
                'Option': value['Open'],
                'Stock': stock_values_dict[key]
            }

    def __create_table(self, table_name):
        """
        Create DB table if not exists.

        :param table_name: Table name
        """

        sql_query = """
            CREATE TABLE IF NOT EXISTS {} (
                id integer PRIMARY KEY,
                {} text NOT NULL,
                {} text NOT NULL,
                {} text NOT NULL
            );
        """.format(table_name, DATE, OPTIONOPEN, STOCKOPEN)

        self.db_cursor.execute(sql_query)

    def put_data_to_db(self):
        """
        Insert data into desired table in database.
        """

        self.__create_table(self.option)
        for key, val in self.data.items():

            sql_query = '''INSERT INTO {} ({}, {}, {}) VALUES ("{}", "{}", "{}");''' \
                .format(self.option, DATE, OPTIONOPEN, STOCKOPEN,
                        key, val['Option'], val['Stock'])

            self.db_cursor.execute(sql_query)
            self.db_conn.commit()

    def _days_between_dates(self, current_date, expiration_date):
        """
        Calculates days between two dates: current and expiration date.

        :param current_date: Current date
        :param expiration_date: Expiration date

        :return: Date between dates
        """

        current = str(current_date).split()[0].split('-')
        expiration = str(expiration_date).split()[0].split('-')
        days_obj = date(int(expiration[0]), int(expiration[1]), int(expiration[2])) - date(int(current[0]),
                                                                                           int(current[1]),
                                                                                           int(current[2]))
        days = days_obj.days

        return days

    def _calculate_volatility(self, prices: list, t: int):
        """
        Calculate volatility for asset

        :param prices: List of asset prices
        :param t: Number of days

        :return: Asset volatility
        """

        i = 0
        vol = []

        for _ in prices[:-1]:
            v = math.log(prices[i + 1] / prices[i])
            vol.append(abs(v))
            i += 1

        if len(vol) == 0:
            return None

        std_dev = statistics.stdev(vol)
        tau = math.sqrt(t / float(DAYS_IN_YEAR))

        volatility = std_dev / tau

        return volatility


if __name__ == '__main__':
    db = "/var/tmp/american.db"

    stock = "aapl"
    path = "/Users/marcinwroblewski/PycharmProjects/optionpricing/option_pricing/option_data/American"
    with open('{}/{}'.format(path, 'apple_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock_name=stock, option_name=option, r=0.01, database=db)
            a.get_data()
            a.put_data_to_db()
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))

    stock = "nflx"
    path = "/Users/marcinwroblewski/PycharmProjects/optionpricing/option_pricing/option_data/American"
    with open('{}/{}'.format(path, 'netflix_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock_name=stock, option_name=option, r=0.01, database=db)
            a.get_data()
            a.put_data_to_db()
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))

    stock = "gdrx"
    path = "/Users/marcinwroblewski/PycharmProjects/optionpricing/option_pricing/option_data/American"
    with open('{}/{}'.format(path, 'goodrx_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock_name=stock, option_name=option, r=0.01, database=db)
            a.get_data()
            a.put_data_to_db()
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))