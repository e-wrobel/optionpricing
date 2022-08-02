import ssl

ssl._create_default_https_context = ssl._create_unverified_context
from six.moves.urllib.request import urlopen

import matplotlib

matplotlib.use('Agg')
from matplotlib import ticker
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12})
import numpy as np
from scipy.stats import norm
import seaborn as sns
from option_pricing.black_scholes_option_pricing import Option

from option_pricing.optionlib.stooq_trader_base import StooqBase
import option_pricing.grpc_option.option_pb2 as message

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
DAYS_IN_YEAR = 252
TABLE_NAME_FILE = 'OPTIONS_SUMMARY'
european = "European"


class Stooq(StooqBase):

    def get_stock(self, stock_name):
        """
        To get historical data for option
        :param stock_name: Stock symbol
        :return: header and historical trading
        """

        url = "{}={}{}".format(self.baseurl, stock_name, self.endurl)
        req = urlopen(url)
        data = req.readlines()

        header, stock_data = self._data_parser(data, asset=stock_name)

        return header, stock_data

    def get_option(self, option_name):
        """
        To get historical data for option
        :param option_name: Option symbol

        :return: header and historical trading
        """

        url = "{}={}{}{}".format(self.baseurl, option_name, '.pl', self.endurl)
        req = urlopen(url)
        data = req.readlines()

        if len(data) < 2:
            raise Exception("no data found for option: {}".format(option_name))

        header, option_data = self._data_parser(data, asset=option_name)

        return header, option_data

    def plot_asset(self, asset, years):
        """
        Plot data for asset.

        :param asset: Asset
        :param years: Plots for given years ranger
        """

        sql = '''select * from {} order by date({}) ASC;'''.format(asset, DATE)

        data = self.db_cursor.execute(sql).fetchall()

        dates = []
        openings = []

        is_data_found = False

        for d in data:
            y = int(d[1].split("-")[0])
            if y in years:
                is_data_found = True
                dates.append(d[1])
                openings.append(float(d[2]))

        if is_data_found:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

            # Find Gaussian distribution parameters
            mean, standard_deviation = norm.fit(openings)

            # First plot: Price vs time
            ax1.grid()
            ax1.set(xlabel='Time (days)', ylabel='Price (pln)', title='{} price'.format(asset))

            ax1.plot(dates, openings, lw=1, label='Open Price')
            ax1.plot(dates, [mean for a in openings], lw=1, label='$\mu$ Price')

            # For x (time) axis
            every_xaxis_tick = int(0.05 * len(dates)) if len(dates) > 100 else 1
            ax1.xaxis.set_ticks(dates[::every_xaxis_tick])
            ax1.set_xticklabels(dates[::every_xaxis_tick], minor=False, rotation=30)

            # Fox y (Price) axis
            every_yaxis_tick = (max(openings) - min(openings)) / 10
            start, end = ax1.get_ylim()
            ax1.yaxis.set_ticks(np.arange(start, end, every_yaxis_tick))
            ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x}'))

            # Set up grid, legend, and limits
            ax1.legend(frameon=False)

            print("Saving data, number of points: {}".format(len(dates)))

            # Second plot: Histogram and Gauss distribution fit
            ax2.grid()
            ax2.set(xlabel='Price (pln)', ylabel='Number of shares',
                    title="{} Histogram, $\sigma$ = {:.2f}, $\mu$ = {:.2f}".format(asset, standard_deviation, mean))

            sns.distplot(openings, ax=ax2)

            # ax2.hist(openings, color='green', bins=15, density=False)
            ax2.legend(frameon=False)
            fig.tight_layout()
            plt.savefig("{}.png".format(asset))
        else:
            print("No data for asset: {}, for year: {}".format(asset, years))

    def calculate_option_and_asset_data(self, option_name, asset_name, r=None):
        """
        Prepare combined dictionary containing option

        :param r: risk free interest rate (for example: 0.01)
        :param option_name: Option name (for example: OW20F192175)
        :param asset_name: Asset name (for example: WIG20)

        :return: option and asset data struct, volatility, B-S calclulated price, option price at boundary condition,
        option price at first day, strike price
        """

        # Strike price from option name
        K = float(option_name[-4::])

        if r is None:
            r = 0.01

        option_asset_data_structure = self._make_option_asset_data_structure(asset_name, option_name)

        if len(option_asset_data_structure) < 3:
            raise Exception("Not enough data for option: {}".format(option_name))

        start_date = sorted(option_asset_data_structure)[0]
        end_time = sorted(option_asset_data_structure)[-1]
        stock_price = float(option_asset_data_structure[start_date][ASSET][OPENNING_PRICE])
        T = self._days_between_dates(start_date, end_time)

        volatility = self._calculate_volatility(asset=option_asset_data_structure, t=ASSET)
        bs_calculus = Option(stock_price, K, T, r, volatility)
        bs_price = bs_calculus.euro_vanilla_call()

        asset_price_at_strike_date = float(option_asset_data_structure[end_time][ASSET][OPENNING_PRICE])
        option_price_from_boundary_condition = max(asset_price_at_strike_date - K, 0)
        option_price_from_the_first_day = float(option_asset_data_structure[start_date][OPTION][OPENNING_PRICE])

        # Add grpc call here
        request = message.ComputeRequest()
        request.maxPrice = 2350
        request.volatility = volatility
        request.r = r
        request.tMax = 0.9
        request.strikePrice = K
        request.calculationType = 'NonLinear'
        request.beta = 0.0
        request.startPrice = stock_price
        request.expectedPrice = option_price_from_boundary_condition
        request.maturityTimeDays = T
        request.optionStyle = european

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

        return option_asset_data_structure, volatility, bs_price, option_price_from_boundary_condition, \
               option_price_from_the_first_day, K, T, r, calculated_option_dict

    def plot_option_asset(self, option_name, option_asset_data_structure, volatility, bs_price,
                          option_price_from_bondary_condition,
                          option_price_from_the_first_day, K, T, r, plot_directory,
                          calculated_option_dict):
        """

        :param option_name:
        :param option_asset_data_structure:
        :param volatility:
        :param bs_price:
        :param option_price_from_bondary_condition:
        :param option_price_from_the_first_day:
        :param K:
        :param T:
        :param plot_directory:
        :param calculated_option_dict:

        :return:
        """

        dates = sorted(option_asset_data_structure)

        option_openings = [float(option_asset_data_structure[date_key][OPTION][OPENNING_PRICE]) for date_key in dates]
        asset_openings = [float(option_asset_data_structure[date_key][ASSET][OPENNING_PRICE]) for date_key in dates]

        # First plot: Price vs time
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

        ax1.grid()
        ax1.set(ylabel='Price (pln)')
        ax1.set(title='{}'.format(option_name))

        # Find Gaussian distribution parameters
        mean, standard_deviation = norm.fit(option_openings)
        ax1.plot(dates, option_openings, lw=2)
        # ax1.plot(dates, option_openings, lw=2, label="\n$\sigma$: {:.2f}, "
        #                                              "\nr: {:.2f}, "
        #                                              "\nK: {:.2f}, "
        #                                              "\nMax(S(t=T) - K, 0): {:.2f}, "
        #                                              "\nCalculated B-S price: {:.2f}, "
        #                                              "\nT: {:.0f} days, "
        #                                              "\nCalculated Non-linear B-S price: {:.2f}, "
        #                                              "\nCalculated beta: {:.8f}".
        #          format(volatility, r, K, option_price_from_bondary_condition, bs_price, T,
        #                 calculated_option_dict["calculated_option_price"],
        #                 calculated_option_dict["calculated_beta"]))

        ax1.plot(dates[0], option_price_from_the_first_day, marker='o', markersize=6, color="red",
                 label='V(t={}): {:.2f}'.format(dates[0], option_price_from_the_first_day))
        ax1.plot(len(dates) - 1, option_openings[-1], marker='o', markersize=6, color="green",
                 label='V(t={}): {:.2f}'.format(dates[-1], option_openings[-1]))

        # Set up grid, legend, and limits
        ax1.legend(loc='upper left', shadow=False)
        ax1.legend(frameon=True)

        # # For x (time) axis
        every_xaxis_tick = int(0.1 * len(dates)) if len(dates) > 10 else 1
        ax1.xaxis.set_ticks(dates[::every_xaxis_tick])
        ax1.set_xticklabels(dates[::every_xaxis_tick], minor=False, rotation=30)
        ax2.grid()

        ax2.set(ylabel='Price (pln)', title="{}".format('WIG20'))

        ax2.plot(dates, asset_openings, lw=2)
        ax2.plot(dates[0], asset_openings[0], marker='o', markersize=6, color="red",
                 label='S(t={}): {:.2f}'.format(dates[0], asset_openings[0]))
        ax2.plot(len(dates) - 1, asset_openings[-1], marker='o', markersize=6, color="green",
                 label='S(t={}): {:.2f}'.format(dates[-1], asset_openings[-1]))
        # ax2.axhline(y=K, color='c', linestyle='--', label='K: {:.2f}'.format(K))
        ax2.legend(loc='lower right', shadow=True)
        ax2.legend(frameon=True)
        ax2.xaxis.set_ticks(dates[::every_xaxis_tick])
        ax2.set_xticklabels(dates[::every_xaxis_tick], minor=False, rotation=30)
        fig.tight_layout()

        plt.savefig("{}/{}.png".format(plot_directory, option_name))
        fig.clear()
        plt.close(fig)

    def plot_summary_table(self, data: list, plot_directory: str):
        """
        
        :param data: List containing data for options
        :param plot_dir: Filename to save table
        """

        # define figure and axes
        fig, ax = plt.subplots()

        # hide the axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')

        # create data
        column_labels = ["Option", "BS Analytical", "S-K", "BS Nonlinear", "Beta", "Volatility", "r", "T"]

        # create table
        table = ax.table(cellText=data, colLabels=column_labels, loc='center', cellLoc='center')
        table.set_fontsize(14)
        table.scale(1, 2)

        # print table in latex format

        head = []
        for row in column_labels:
            head.append(str(row))
            head.append('&')
        head = head[:-1]
        head.append('{}'.format('\\\\'))
        line = ' '.join(head)
        print('{}'.format(line))
        beginning = '''
\\begin{table}[ht]
\\caption{Nonlinear Model Results}
\\centering
\\begin{tabular}{c c c c c c c c}
\\hline\hline
         '''
        print(beginning)
        for row in data:
            col = []
            for column in row:
                col.append(str(column))
                col.append('&')
            col = col[:-1]
            col.append('{}'.format('\\\\'))
            line = ' '.join(col)
            print('{}'.format(line))
        end = '''
\hline
\end{tabular}
\label{table:nonlin}
\end{table}        
        '''
        print(end)

        # display table
        fig.tight_layout()
        plt.savefig("{}/{}.png".format(plot_directory, TABLE_NAME_FILE), dpi=600)
        fig.clear()
        plt.close(fig)

    def prepare_neural_data(self, data: list, directory: str):
        """
        Prepare data for neural network.

        :param data: option data
        :param directory: directory to save neural file
        """

        raw_data = "{}/{}".format(directory, 'raw_data.txt')
        path_input = "{}/{}".format(directory, 'neural_input.txt')
        path_values = "{}/{}".format(directory, 'neural_values.txt')
        vals = []

        with open(raw_data, 'w') as file:
            file.write("Option, BS Analytical, S-K, BS Nonlinear, Beta, Volatility, r, T\n")
            for d in data:
                i = "[{}, {}, {}, {}, {}, {}, {}, {}]\n".format(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7])
                file.write(i)

        with open(path_input, 'w') as file:
            for d in data:
                i = "[{}, {}], ".format(d[5], d[7])
                vals.append(d[4])
                file.write(i)

        with open(path_values, 'w') as file:
            file.write('[')
            for v in vals:
                i = "{}, ".format(v)
                file.write(i)
            file.write(']')

    def prepare_sigma_beta(self, beta_data: list, sigma_data: list, plot_directory: str):
        """
        Prepares plot for sigma vs beta
        :param plot_directory: directory to save neural file
        :param sigma_data: List of sigma values
        :param beta_data: List of corresponding beta values

        :return: None
        """

        dist = norm()
        # Data for plotting
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

        ax1.grid()
        ax1.scatter(beta_data, sigma_data)

        ax1.set(xlabel='Beta', ylabel='Sigma',
                title='Beta vs Sigma relation from calculated data')

        ax2.grid()
        ax2.hist(beta_data, density=True, bins=len(beta_data))
        ax2.set(xlabel='Beta', ylabel='Probability',
                title='Histogram for beta')
        ax2.legend(loc='best', frameon=False)
        fig.savefig("{}/{}".format(plot_directory, 'beta_vs_sigma.png'))
        fig.clear()
        plt.close(fig)
