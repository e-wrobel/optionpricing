from yahoo_fin import options, stock_info
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


class AmericanOptions(object):

    def __init__(self, stock: str, option: str):
        self.stock = stock
        self.option = option
        self.stock_data = None
        self.option_data = None

    def get_data(self, path: str):
        """
        Scrapping data for selected stock and option and save them in png file.

        :param path: path for storing stock/option data
        """

        self.option_data = stock_info.get_data(self.option)
        option_values = self.option_data.open
        start_time = None
        end_date = None
        for date, price in option_values.items():
            if start_time is None:
                start_time = date
            end_date = date

        self.stock_data = stock_info.get_data(self.stock, start_date=start_time, end_date=end_date)
        stock_values = self.stock_data.open

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

        ax1.grid()
        ax1.set(xlabel='Time (days)', ylabel='Price (usd)', title='{} Market data'.format(self.option.upper()))

        ax1.plot(option_values, 'o', label="Market price for {} option".format(self.option.upper()))

        # Set up grid, legend, and limits
        ax1.legend(loc='upper left', shadow=False)
        ax1.legend(frameon=True)

        every_xaxis_tick = int(0.1 * len(option_values.keys())) if len(option_values) > 10 else 1
        ax1.xaxis.set_ticks(option_values.keys()[::every_xaxis_tick])
        ax1.set_xticklabels(option_values.keys()[::every_xaxis_tick], minor=False, rotation=30)

        ax2.grid()
        ax2.set(xlabel='Time (days)', ylabel='Price (usd)',
                title="{} Market data".format(self.stock.upper()))

        ax2.plot(stock_values, lw=2, label="Market price for {} stock".format(self.stock.upper()))
        ax2.legend(loc='lower right', shadow=True)
        ax2.legend(frameon=True)
        ax2.xaxis.set_ticks(stock_values.keys()[::every_xaxis_tick])
        ax2.set_xticklabels(stock_values.keys()[::every_xaxis_tick], minor=False, rotation=30)
        fig.tight_layout()

        plt.savefig("{}/{}.png".format(path, self.option))


if __name__ == '__main__':
    a = AmericanOptions(stock="nflx", option="NFLX210226C00492500")
    path = "/Users/marcinwroblewski/GolandProjects/optionpricing/option_pricing/option_data"
    a.get_data(path=path)
