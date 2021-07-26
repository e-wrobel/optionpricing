import math
import ssl
from datetime import date

import grpc

from option_pricing.black_scholes_option_pricing import Option
from yahoo_fin import stock_info
import option_pricing.grpc_option.option_pb2_grpc as stub
import option_pricing.grpc_option.option_pb2 as message

ssl._create_default_https_context = ssl._create_unverified_context
import statistics

DAYS_IN_YEAR = 252


class BtcOptions(object):

    def __init__(self, stock: str, k: float, r: float, scaling=1):
        self.stock = stock
        self.K = k
        self.R = r
        self.scaling = scaling
        channel = grpc.insecure_channel('localhost:9000')
        self.grpc_client = stub.OptionPricingStub(channel=channel)

    def crypto_data(self, since: str, until: str, max_num_price: float):
        """

        :param since:
        :param until:
        :return:
        """

        stock_data = stock_info.get_data(self.stock, start_date=since, end_date=until)
        stock_values = stock_data.open

        stock_open_prices = []
        for _, price in stock_values.items():
            stock_open_prices.append(price)

        T = self._days_between_dates(since, until)
        volatility = self._calculate_volatility(prices=stock_open_prices, t=T)

        option_price_from_boundary_conditions = max(stock_open_prices[-1] - self.K, 0)
        bs_calculus = Option(stock_open_prices[0], self.K, T, self.R, volatility)
        bs_price = bs_calculus.euro_vanilla_call()

        out = self.calculate_nonlinear_bs(T, option_price_from_boundary_conditions, stock_open_prices, volatility, max_num_price)
        calculated_option_price = out['calculated_option_price']
        calculated_beta = out['calculated_beta']

        return volatility, bs_price, calculated_option_price, calculated_beta

    def calculate_nonlinear_bs(self, T, option_price_from_boundary_conditions, stock_open_prices, volatility, max_num_price):
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
        request.maxPrice = max_num_price/self.scaling
        request.volatility = volatility
        request.r = self.R
        request.tMax = 0.9
        request.strikePrice = self.K/self.scaling
        request.calculationType = 'NonLinear'
        request.beta = 0.0
        request.startPrice = stock_open_prices[-1]/self.scaling
        request.expectedPrice = option_price_from_boundary_conditions/self.scaling
        request.maturityTimeDays = T
        out = self.grpc_client.ComputePrice(request=request)

        calculated_option_dict = {
            "calculated_option_price": out.CalculatedOptionprice,
            "calculated_expiration_days": out.CalculatedExpirationDays,
            "calculated_asset_price": out.CalculatedAssetPrice,
            "calculated_beta": out.CalculatedBeta,
            "volatility": volatility,
            "r": self.R,
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
    b = BtcOptions(stock='BTC-USD', k=46000, r=0.01, scaling=100)
    volatility, bs_price, calculated_option_price, calculated_beta = b.crypto_data(since='2021-04-23',
                                                                                   until='2021-05-28',
                                                                                   max_num_price=60000)
    print()

