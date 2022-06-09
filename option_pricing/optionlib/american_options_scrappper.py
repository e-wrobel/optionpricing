import datetime
import math
import sqlite3
import statistics
from datetime import date
import yfinance as yf

DAYS_IN_YEAR = 252
DATE = 'date'
OPENNING_PRICE = 'openning_price'
MAX_PRICE = 'max_price'
LOW_PRICE = 'low_price'
ENDING_PRICE = 'ending_price'
VOLUME = 'volume'
LOP = 'lop'
OPTION = 'option'
ASSET = 'asset'


class AmericanOptions(object):

    def __init__(self, stock: str, option: str, r: float, database: str):
        self.stock = stock
        self.r = r
        self.option = option
        self.stock_data = None
        self.option_data = None
        self.db_conn = sqlite3.connect(database=database)
        self.db_cursor = self.db_conn.cursor()

    def save_data(self, path: str):
        """
        Download data for selected stock and option and save them in png file.

        :param path: path for storing stock/option data
        """

        option_data = yf.Ticker(self.option)
        option_values = option_data.history('max')
        start_date = str(option_values.head(1).index.values[0])
        start_date = start_date.split('T')[0]
        expiration_date = self.option[4:10]
        expiration_date = '20{}-{}-{}'.format(expiration_date[:2], expiration_date[2:4],
                                                             expiration_date[4:])
        option_type = 'Call' if self.option[10] == 'C' else 'Put'

        K = float('{}.{}'.format(self.option[13:16], self.option[16:]))

        for date, value in option_values.iterrows():
            print("Date: {}, Open: {}".format(date, value['Open']))

        stock_data = yf.Ticker(self.stock)
        stock_values = stock_data.history(start=start_date)
        for date, value in stock_values.iterrows():
            print("Date: {}, Open: {}".format(date, value['Open']))

        T = self._days_between_dates(start_date, expiration_date)


        # volatility = self._calculate_volatility(stock_open_prices, T)
        # option_price_from_boundary_conditions = max(stock_open_prices[-1] - K, 0)

    def _create_table(self, table_name):
        """
        Create DB table if not exists.

        :param table_name: Table name
        """

        sql_query = """
            CREATE TABLE IF NOT EXISTS {} (
                id integer PRIMARY KEY,
                {} text NOT NULL,
                {} text,
                {} text,
                {} text,
                {} text,
                {} text,
                {} text
            );
        """.format(table_name, DATE, OPENNING_PRICE, MAX_PRICE, LOW_PRICE, ENDING_PRICE, VOLUME, LOP)

        self.db_cursor.execute(sql_query)

    def _put_data_to_db(self, table_name, data):
        """
        Insert data into desired table.
        :param table_name: Table name
        :param data: Data to be inserted
        """
        for date, value in data.items():
            current_date = date
            current_data = value

            sql_query = '''INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", 
            "{}");''' \
                .format(table_name, DATE, OPENNING_PRICE, MAX_PRICE, LOW_PRICE, ENDING_PRICE, VOLUME, LOP,
                        current_date,
                        current_data[OPENNING_PRICE], current_data[MAX_PRICE], current_data[LOW_PRICE],
                        current_data[ENDING_PRICE], current_data[VOLUME], current_data[LOP])

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
    path = "/Users/marcinwroblewski/GolandProjects/optionpricing/option_pricing/option_data/American"
    db = "/var/tmp/american.db"
    stock = "aapl"

    with open('{}/{}'.format(path, 'apple_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock=stock, option=option, r=0.01, database=db)
            a.save_data(path=path)
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))

