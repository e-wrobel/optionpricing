import math
import sqlite3

import matplotlib
import statistics

matplotlib.use('Agg')
from datetime import date
from option_pricing.black_scholes_option_pricing import Option


# Stock:
# https://stooq.pl/q/d/l/?s=wig20&i=d
#
# Option:
# https://stooq.pl/q/d/l/?s=ow20f192175.pl&i=d

DATE = 'date'
OPENNING_PRICE = 'openning_price'
MAX_PRICE = 'max_price'
LOW_PRICE = 'low_price'
ENDING_PRICE = 'ending_price'
VOLUME = 'volume'
LOP = 'lop'
OPTION = 'option'
ASSET = 'asset'
DAYS_IN_YEAR = 365


class StooqBase(object):

    def __init__(self, database=':memory:'):
        self.baseurl = 'https://stooq.pl/q/d/l/?s'
        self.endurl = '&i=d'
        self.db_conn = sqlite3.connect(database=database)
        self.db_cursor = self.db_conn.cursor()

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

    def _data_parser(self, data, asset):
        """
        Parse data from input for given asset and insert it into DB.

        :param data: Data gathered for given asset
        :param asset: Asset

        :return: Header and gathered data
        """

        # Create relevant table
        self._create_table(table_name=asset)

        asset_data = {}
        header = None
        i = 0

        for line in data:
            if i == 0:
                header = line
                i += 1
            else:
                single_line = line.rstrip().split(",")
                date = single_line[0]
                openning_price = single_line[1]
                max_price = single_line[2]
                low_price = single_line[3]
                ending_price = single_line[4]
                volume = single_line[5]
                lop = single_line[6] if len(single_line) == 7 else 0

                asset_data[date] = {
                    OPENNING_PRICE: openning_price,
                    MAX_PRICE: max_price,
                    LOW_PRICE: low_price,
                    ENDING_PRICE: ending_price,
                    VOLUME: volume,
                    LOP: lop
                }

        self._put_data(table_name=asset, data=asset_data)

        return header, asset_data

    def _put_data(self, table_name, data):
        """
        Insert data into desired table.
        :param table_name: Table name
        :param data: Data to be inserted
        """
        for date, value in data.items():
            current_date = date
            current_data = value

            sql_query = '''INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");''' \
                .format(table_name, DATE, OPENNING_PRICE, MAX_PRICE, LOW_PRICE, ENDING_PRICE, VOLUME, LOP,
                        current_date,
                        current_data[OPENNING_PRICE], current_data[MAX_PRICE], current_data[LOW_PRICE],
                        current_data[ENDING_PRICE], current_data[VOLUME], current_data[LOP])

            self.db_cursor.execute(sql_query)
            self.db_conn.commit()

    def _make_option_asset_data_structure(self, asset_name, option_name):
        """
        Prepare Combined data structure.

        :param asset_name: Asset name
        :param option_name: Option name

        :return: Combined data structure
        """

        option_asset_data = {}
        sql_option = '''select * from {} order by date({}) ASC;'''.format(option_name, DATE)
        option_data = self.db_cursor.execute(sql_option).fetchall()
        option_years = {}
        for data in option_data:
            self._fill_data(data, option_asset_data, t=OPTION)
            date = data[1]
            year = str(date.split("-")[0])
            option_years[year] = True
        wig_years = ["\'%{}%\'".format(x) for x in option_years.keys()]

        for wig_year in wig_years:
            sql_asset = '''select * from {} where date like {} order by date({}) ASC;'''.format(asset_name,
                                                                                                wig_year,
                                                                                                DATE)
            asset_data = self.db_cursor.execute(sql_asset).fetchall()
            for data in asset_data:
                self._fill_data(data, option_asset_data, t=ASSET)

        return option_asset_data

    def _fill_data(self, data, option_asset_data, t):
        """
        Fills data from combined data structure.

        :param data: asset or option data structure
        :param option_asset_data: option and asset combined data structure
        """

        date = data[1]

        if t == OPTION:
            option_asset_data[date] = {
                t: {
                    OPENNING_PRICE: data[2],
                    MAX_PRICE: data[3],
                    LOW_PRICE: data[4],
                    ENDING_PRICE: data[5],
                    VOLUME: data[6],
                    LOP: data[7]
                }
            }
        else:
            if date in option_asset_data.keys():
                option_asset_data[date].update({
                    t: {
                        OPENNING_PRICE: data[2],
                        MAX_PRICE: data[3],
                        LOW_PRICE: data[4],
                        ENDING_PRICE: data[5],
                        VOLUME: data[6],
                        LOP: data[7]
                    }
                })

    def _calculate_volatility(self, asset, t=ASSET):
        """
        Calculate volatility for given type (ASSET or OPTION).

        :param asset: Stock prices (list)

        :return: volatility
        """

        # Prepare storted pricess for given asset
        sorted_dates_keys = sorted(asset)
        T = self._days_between_dates(sorted_dates_keys[0], sorted_dates_keys[-1])
        openning_prices = [float(asset[date][t][OPENNING_PRICE]) for date in sorted_dates_keys]
        i = 0
        vol = []

        for _ in openning_prices[:-1]:
            v = math.log(openning_prices[i + 1] / openning_prices[i])
            vol.append(abs(v))
            i += 1

        if len(vol) == 0:
            return None

        std_dev = statistics.stdev(vol)
        tau = math.sqrt(T / float(DAYS_IN_YEAR))

        volatility = std_dev / tau

        return volatility

    def _calculate_option_price(self, asset_price, r, sigma, K, current_date, expiration_date):
        """
        Calculates call price at the basis of Black-Scholes model.

        :param asset_price: Current asset price
        :param r: Risk free interest rate
        :param sigma: Asset volatility
        :param K: Strike price
        :param current_date: Current date
        :param expiration_date: Expiration date

        :return: Call price
        """

        T = self._days_between_dates(current_date=current_date, expiration_date=expiration_date)

        o = Option(asset_price, K, T, r, sigma)

        call_price = o.euro_vanilla_call()

        return call_price

    def _days_between_dates(self, current_date, expiration_date):
        """
        Calculates days between two dates: current and expiration date.

        :param current_date: Current date
        :param expiration_date: Expiration date

        :return: Date between dates
        """

        current_date = map(lambda x: int(x), current_date.split("-"))
        expiration_date = map(lambda x: int(x), expiration_date.split("-"))
        days_obj = date(expiration_date[0], expiration_date[1], expiration_date[2]) - date(current_date[0],
                                                                                           current_date[1],
                                                                                           current_date[2])

        days = days_obj.days

        return days

    def end_connection(self):
        """
        Commit changes and close db connection.
        """

        self.db_conn.commit()
        self.db_conn.close()
