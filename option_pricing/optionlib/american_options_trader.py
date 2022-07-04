import math
import sqlite3
from datetime import date

import grpc
from option_pricing.black_scholes_option_pricing import Option
import numpy as np
import option_pricing.grpc_option.option_pb2_grpc as stub
import option_pricing.grpc_option.option_pb2 as message
import pandas as pd
import matplotlib
import statistics

matplotlib.use('Agg')
import matplotlib.pyplot as plt

DAYS_IN_YEAR = 252
american = "American"
european = "European"


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
        channel = grpc.insecure_channel('localhost:9000')
        self.grpc_client = stub.OptionPricingStub(channel=channel)

    def calculate_option_data(self):
        """
        Calculation data for given option.
        """
        data = self.load_data()
        stock_open_prices = []
        option_open_prices = []
        dates = []
        for e in data:
            date = e[1]
            option_openning_price = e[2]
            stock_openning_price = e[3]
            dates.append(date)
            option_open_prices.append(float(option_openning_price))
            stock_open_prices.append(float(stock_openning_price))

        T = self._days_between_dates(dates[0], dates[-1])
        stock_open_prices[-1] = self.K
        volatility = self._calculate_volatility(stock_open_prices, T)
        option_price_from_last_day = option_open_prices[-1]
        out = self.calculate_nonlinear_bs(T, option_price_from_last_day, stock_open_prices, volatility, 0.0)
        calculated_beta = out['calculated_beta']
        calculated_values = out['calculated_price_3d']
        price_index = out['price_index']
        option_prices_for_given_s0 = calculated_values.U[price_index].Ut[0:len(option_open_prices)]
        shifted_prices_for_given_s0 = list(map(lambda x: x +(option_open_prices[0] - option_prices_for_given_s0[0]), option_prices_for_given_s0))

        fig1, ax1 = plt.subplots(figsize=(16, 10), facecolor='w')
        ax1.grid()
        ax1.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data, beta: {}'.
                format(self.option.upper(), calculated_beta))

        ax1.plot(option_open_prices[0], marker='o', markersize=6, color="red",
                 label='Market and Calculated V(t={}): {:.2f}'.format(dates[0], option_open_prices[0]))
        ax1.plot(len(option_open_prices), option_open_prices[-1], marker='o', markersize=6, color="green",
                 label='Market V(t={}): {:.2f}'.format(dates[-1], option_open_prices[-1]))
        ax1.plot(len(option_open_prices), shifted_prices_for_given_s0[-1], marker='o', markersize=6, color="blue",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[-1], shifted_prices_for_given_s0[-1]))

        ax1.plot(shifted_prices_for_given_s0)
        ax1.plot(option_open_prices)
        ax1.legend(loc='upper left', shadow=False)
        ax1.legend(frameon=True)

        fig1.tight_layout()
        plt.savefig("{}/{}_shifted.png".format(".", self.option))

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10), facecolor='w')
        ax1.grid()
        ax1.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data, beta: {}'.
                format(self.option.upper(), calculated_beta))

        ax1.plot(option_open_prices[0], marker='o', markersize=6, color="red",
                 label='Market V(t={}): {:.2f}'.format(dates[0], option_open_prices[0]))
        ax1.plot(len(option_open_prices), option_open_prices[-1], marker='o', markersize=6, color="green",
                 label='Market V(t={}): {:.2f}'.format(dates[-1], option_open_prices[-1]))

        ax1.plot(option_prices_for_given_s0[0], marker='o', markersize=6, color="orange",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[0], option_prices_for_given_s0[0]))
        ax1.plot(len(option_open_prices), option_prices_for_given_s0[-1], marker='o', markersize=6, color="blue",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[-1], option_prices_for_given_s0[-1]))

        ax1.plot(option_prices_for_given_s0)
        ax1.plot(option_open_prices)
        ax1.legend(loc='upper left', shadow=False)
        ax1.legend(frameon=True)

        out = self.calculate_nonlinear_bs(T, option_price_from_last_day, stock_open_prices, volatility, 0.05)
        calculated_beta = out['calculated_beta']
        calculated_values = out['calculated_price_3d']
        price_index = out['price_index']
        option_prices_for_given_s0 = calculated_values.U[price_index].Ut[0:len(option_open_prices)]

        ax2.grid()
        ax2.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data, beta: {}'.
                format(self.option.upper(), calculated_beta))

        ax2.plot(option_open_prices[0], marker='o', markersize=6, color="red",
                 label='Market V(t={}): {:.2f}'.format(dates[0], option_open_prices[0]))
        ax2.plot(len(option_open_prices), option_open_prices[-1], marker='o', markersize=6, color="green",
                 label='Market V(t={}): {:.2f}'.format(dates[-1], option_open_prices[-1]))

        ax2.plot(option_prices_for_given_s0[0], marker='o', markersize=6, color="orange",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[0], option_prices_for_given_s0[0]))
        ax2.plot(len(option_open_prices), option_prices_for_given_s0[-1], marker='o', markersize=6, color="blue",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[-1], option_prices_for_given_s0[-1]))

        ax2.plot(option_prices_for_given_s0)
        ax2.plot(option_open_prices)
        ax2.legend(loc='upper left', shadow=False)
        ax2.legend(frameon=True)

        out = self.calculate_nonlinear_bs(T, option_price_from_last_day, stock_open_prices, volatility, 0.005)
        calculated_beta = out['calculated_beta']
        calculated_values = out['calculated_price_3d']
        price_index = out['price_index']
        option_prices_for_given_s0 = calculated_values.U[price_index].Ut[0:len(option_open_prices)]

        ax3.grid()
        ax3.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data, beta: {}'.
                format(self.option.upper(), calculated_beta))

        ax3.plot(option_open_prices[0], marker='o', markersize=6, color="red",
                 label='Market V(t={}): {:.2f}'.format(dates[0], option_open_prices[0]))
        ax3.plot(len(option_open_prices), option_open_prices[-1], marker='o', markersize=6, color="green",
                 label='Market V(t={}): {:.2f}'.format(dates[-1], option_open_prices[-1]))

        ax3.plot(option_prices_for_given_s0[0], marker='o', markersize=6, color="orange",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[0], option_prices_for_given_s0[0]))
        ax3.plot(len(option_open_prices), option_prices_for_given_s0[-1], marker='o', markersize=6, color="blue",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[-1], option_prices_for_given_s0[-1]))

        ax3.plot(option_prices_for_given_s0)
        ax3.plot(option_open_prices)
        ax3.legend(loc='upper left', shadow=False)
        ax3.legend(frameon=True)

        out = self.calculate_nonlinear_bs(T, option_price_from_last_day, stock_open_prices, volatility, 0.0005)
        calculated_beta = out['calculated_beta']
        calculated_values = out['calculated_price_3d']
        price_index = out['price_index']
        option_prices_for_given_s0 = calculated_values.U[price_index].Ut[0:len(option_open_prices)]

        ax4.grid()
        ax4.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data, beta: {}'.
                format(self.option.upper(), calculated_beta))

        ax4.plot(option_open_prices[0], marker='o', markersize=6, color="red",
                 label='Market V(t={}): {:.2f}'.format(dates[0], option_open_prices[0]))
        ax4.plot(len(option_open_prices), option_open_prices[-1], marker='o', markersize=6, color="green",
                 label='Market V(t={}): {:.2f}'.format(dates[-1], option_open_prices[-1]))

        ax4.plot(option_prices_for_given_s0[0], marker='o', markersize=6, color="orange",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[0], option_prices_for_given_s0[0]))
        ax4.plot(len(option_open_prices), option_prices_for_given_s0[-1], marker='o', markersize=6, color="blue",
                 label='Nls-BS V(t={}): {:.2f}'.format(dates[-1], option_prices_for_given_s0[-1]))

        ax4.plot(option_prices_for_given_s0)
        ax4.plot(option_open_prices)
        ax4.legend(loc='upper left', shadow=False)
        ax4.legend(frameon=True)

        fig.tight_layout()
        plt.savefig("{}/{}.png".format(".", self.option))

    def load_data(self):
        """
        Load option and stock data from database
        :rtype dict
        """

        sql_query = '''SELECT * FROM {};'''.format(self.option)

        data = self.db_cursor.execute(sql_query)

        return data.fetchall()

    def calculate_nonlinear_bs(self, T, option_price_from_boundary_conditions, stock_open_prices, volatility, beta):
        """
        Make grpc connection and calculate
        :param T:
        :param beta: 0 means that it we will calibrate, otherwise we will calculate for the given number
        :param option_price_from_boundary_conditions:
        :param stock_open_prices:
        :param volatility:
        :return:
        """
        # Add grpc call here
        request = message.ComputeRequest()
        request.maxPrice = 200
        request.volatility = volatility
        request.r = self.r
        request.tMax = 0.7
        request.strikePrice = self.K
        request.calculationType = 'NonLinear'
        request.beta = beta
        request.startPrice = stock_open_prices[0]
        request.expectedPrice = option_price_from_boundary_conditions
        request.maturityTimeDays = T
        request.optionStyle = european
        out = self.grpc_client.ComputePrice(request=request)

        calculated_option_dict = {
            "calculated_price_3d": out,
            "calculated_option_price": out.CalculatedOptionprice,
            "calculated_expiration_days": out.CalculatedExpirationDays,
            "calculated_asset_price": out.CalculatedAssetPrice,
            "calculated_beta": out.CalculatedBeta,
            "price_index": out.PriceIndex,
            "volatility": volatility,
            "r": self.r,
            "T": T,
        }

        return calculated_option_dict

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
    # a = AmericanOptions("APPL", "AAPL220617C00143000", 0.03, "/Users/marcinwroblewski/GolandProjects/optionpricing/american.db")
    a = AmericanOptions("APPL", "AAPL220617C00155000", 0.03,
                        "/Users/marcinwroblewski/GolandProjects/optionpricing/american.db")
    a.calculate_option_data()
