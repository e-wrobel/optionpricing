import math
import ssl
from datetime import date

import grpc

from option_pricing.black_scholes_option_pricing import Option
import numpy as np
from yahoo_fin import stock_info
import option_pricing.grpc_option.option_pb2_grpc as stub
import option_pricing.grpc_option.option_pb2 as message

ssl._create_default_https_context = ssl._create_unverified_context
import matplotlib
import statistics

matplotlib.use('Agg')
import matplotlib.pyplot as plt

DAYS_IN_YEAR = 252
american = "American"


class AmericanOptions(object):

    def __init__(self, stock: str, option: str):
        self.stock = stock
        self.option = option
        self.stock_data = None
        self.option_data = None
        channel = grpc.insecure_channel('localhost:9000')
        self.grpc_client = stub.OptionPricingStub(channel=channel)

    def get_data(self, path: str):
        """
        Scrapping data for selected stock and option and save them in png file.

        :param path: path for storing stock/option data
        """

        r = 0.01
        self.option_data = stock_info.get_data(self.option)
        option_values = self.option_data.open

        expiration_date = self.option[4:10]
        expiration_date_human_readable = '20{}-{}-{}'.format(expiration_date[:2], expiration_date[2:4],
                                                             expiration_date[4:])
        option_type = 'Call' if self.option[10] == 'C' else 'Put'
        # Because we've got some missing points
        option_mask = np.isfinite(option_values)

        K = float('{}.{}'.format(self.option[13:16], self.option[16:]))
        start_time = None

        # There could be different end dates for option and stock -> sometimes data are missing
        end_option_date = None
        end_stock_date = None

        for date, price in option_values.items():
            if start_time is None:
                start_time = date
            end_option_date = date

        self.stock_data = stock_info.get_data(self.stock, start_date=start_time, end_date=end_option_date)
        stock_values = self.stock_data.open

        stock_open_prices = []
        for date, price in stock_values.items():
            end_stock_date = date
            stock_open_prices.append(price)

        T = self._days_between_dates(start_time, end_option_date)
        volatility = self._calculate_volatility(stock_open_prices, T)
        option_price_from_boundary_conditions = max(stock_open_prices[-1] - K, 0)
        bs_calculus = Option(stock_open_prices[0], K, T, r, volatility)
        bs_price = bs_calculus.euro_vanilla_call()

        out = self.calculate_nonlinear_bs(K, T, option_price_from_boundary_conditions, r, stock_open_prices, volatility)
        calculated_option_price = out['calculated_option_price']
        calculated_beta = out['calculated_beta']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

        ax1.grid()
        ax1.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data'.format(self.option.upper()))

        ax1.plot(option_values[option_mask], zorder=2, label=
        "$\sigma$: {:.2f},\n"
        "K: {},\n"
        "T: {} days,\n"
        "Expiration date: {},\n"
        "Option type: {},\n"
        "Max(S(t=T) - K, 0): {:.2f},\n"
        "Calculated B-S price: {:.2f}\n"
        "Calculated Non-linear B-S price: {:.2f}\n"
        "Calculated beta: {:.8f}".format(volatility, K, T,
                                         expiration_date_human_readable,
                                         option_type, option_price_from_boundary_conditions, bs_price,
                                         calculated_option_price,
                                         calculated_beta))

        ax1.plot(start_time, option_values[0], marker='o', markersize=6, color="red",
                 label='V(t={}): {:.2f}'.format(start_time, option_values[0]))
        ax1.plot(end_option_date, option_values[-1], marker='o', markersize=6, color="green",
                 label='V(t={}): {:.2f}'.format(end_option_date, option_values[-1]))

        # Set up grid, legend, and limits
        ax1.legend(loc='upper left', shadow=False)
        ax1.legend(frameon=True)

        every_xaxis_tick = int(0.1 * len(option_values.keys())) if len(option_values) > 10 else 1
        ax1.xaxis.set_ticks(option_values.keys()[::every_xaxis_tick])
        ax1.set_xticklabels(option_values.keys()[::every_xaxis_tick], minor=False, rotation=30)

        ax2.grid()
        ax2.set(xlabel='Time (days)', ylabel='Price (usd)',
                title="{} Market data".format(self.stock.upper()))

        ax2.plot(stock_values, lw=2, label="K: {}".format(K))

        # Strike price:
        # ax2.axhline(y=K, color='c', linestyle='--', label='K: {}'.format(K))

        ax2.plot(start_time, stock_values[0], marker='o', markersize=6, color="red",
                 label='S(t={}): {:.2f}'.format(start_time, stock_values[0]))
        ax2.plot(end_stock_date, stock_values[-1], marker='o', markersize=6, color="green",
                 label='S(t={}): {:.2f}'.format(end_stock_date, stock_values[-1]))

        ax2.legend(loc='lower right', shadow=True)
        ax2.legend(frameon=True)
        ax2.xaxis.set_ticks(stock_values.keys()[::every_xaxis_tick])
        ax2.set_xticklabels(stock_values.keys()[::every_xaxis_tick], minor=False, rotation=30)
        fig.tight_layout()

        plt.savefig("{}/{}.png".format(path, self.option))

    def calculate_nonlinear_bs(self, K, T, option_price_from_boundary_conditions, r, stock_open_prices, volatility):
        """
        Make grpc connection and calculate
        :param K:
        :param T:
        :param option_price_from_boundary_conditions:
        :param r:
        :param stock_open_prices:
        :param volatility:
        :return:
        """
        # Add grpc call here
        request = message.ComputeRequest()
        request.maxPrice = 2350
        request.volatility = volatility
        request.r = r
        request.tMax = 0.9
        request.strikePrice = K
        request.calculationType = 'NonLinear'
        request.beta = 0.0
        request.startPrice = stock_open_prices[0]
        request.expectedPrice = option_price_from_boundary_conditions
        request.maturityTimeDays = T
        request.optionStyle = american
        out = self.grpc_client.ComputePrice(request=request)

        calculated_option_dict = {
            "calculated_option_price": out.CalculatedOptionprice,
            "calculated_expiration_days": out.CalculatedExpirationDays,
            "calculated_asset_price": out.CalculatedAssetPrice,
            "calculated_beta": out.CalculatedBeta,
            "volatility": volatility,
            "r": r,
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
    path = "/Users/marcinwroblewski/GolandProjects/optionpricing/option_pricing/option_data/American"

    # # Netflix
    stock = "nflx"

    with open('{}/{}'.format(path, 'netflix_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock=stock, option=option)
            a.get_data(path=path)
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))

    # Apple
    stock = "aapl"

    with open('{}/{}'.format(path, 'apple_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock=stock, option=option)
            a.get_data(path=path)
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))

    # Tesla
    stock = "tsla"
    with open('{}/{}'.format(path, 'tsla_options.txt')) as f:
        options = [x.rstrip() for x in f]

    for option in options:
        try:
            a = AmericanOptions(stock=stock, option=option)
            a.get_data(path=path)
        except Exception as e:
            print('Unable to make calculation for option: {}, error: {}'.format(option, e))
