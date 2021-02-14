import os

import configparser
import argparse

from option_pricing.stooq_trader import Stooq

PARAMS = 'params'
DB = 'db'
CLEANDB = 'cleandb'
PLOTDIR = 'plotdir'

FINANCIAL = 'financial'
R = 'r'
OPTIONS = 'options'
ASSET = 'asset'
GRPC = 'grpc'


def get_configuration():
    parser = argparse.ArgumentParser(description='Configuration file for stooq runner.')
    parser.add_argument('config', metavar='N', type=str,
                        help='config file')
    args = parser.parse_args()
    config_file = args.config
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_file)
    # Database params
    db_name = config[PARAMS][DB]
    clean_db = config[PARAMS][CLEANDB]
    plot_dir = config[PARAMS][PLOTDIR]
    grpc_host = config[PARAMS][GRPC]
    # Financial params
    r = float(config[FINANCIAL][R])
    options = config[FINANCIAL][OPTIONS].split(",")
    asset = config[FINANCIAL][ASSET]

    return db_name, clean_db, plot_dir, grpc_host, r, options, asset


if __name__ == "__main__":

    db_name, clean_db, plot_dir, grpc_host, r, options, asset = get_configuration()
    s = None
    available_options = options

    if clean_db == 'yes':
        available_options = []
        if os.path.isfile(db_name):
            print("Removing old database")
            os.remove(db_name)

        print("Initializing Stooq trader")
        s = Stooq(database=db_name)
        print("Downloading data for asset: {}".format(asset))
        s.get_stock(stock_name=asset)

        for option in options:
            print("Downloading data for option: {}".format(option))
            try:
                s.get_option(option_name=option)
                available_options.append(option)
            except Exception as e:
                print("Skipping option: {}, exception: {}".format(option, e))
    else:
        s = Stooq(database=db_name)

    options_calculated = []
    options_data = []
    for option in available_options:
        print("Performing calculation for option: {}".format(option))

        try:
            option_asset_data_structure, volatility, bs_price, option_price_from_boundary_condition, \
            option_price_from_the_first_day, K, T, r, calculated_option_dict = s.calculate_option_and_asset_data(
                option_name=option,
                asset_name=asset,
                r=r)

            print("Performing plot for option: {}".format(option))
            s.plot_option_asset(option_name=option,
                                option_asset_data_structure=option_asset_data_structure,
                                volatility=volatility,
                                bs_price=bs_price,
                                option_price_from_bondary_condition=option_price_from_boundary_condition,
                                option_price_from_the_first_day=option_price_from_the_first_day,
                                K=K,
                                T=T,
                                r=r,
                                plot_directory=plot_dir,
                                calculated_option_dict=calculated_option_dict)
            options_calculated.append(option)
            # Option, BS Analytical Price, S-K, BS Nonlinear numerical price, Beta
            options_data.append([option, bs_price, option_price_from_boundary_condition, calculated_option_dict["calculated_option_price"], calculated_option_dict["calculated_beta"]])
        except Exception as e:
            print("Skipping calculation for option: {}, not enough data, exception: {} ".format(option, e))

    if len(options_data) == 0:
        s.end_connection()
        exit(0)

    print("Finished. Calculations were performed for options: {}".format(','.join(options_calculated)))
    s.plot_summary_table(options_data, plot_directory=plot_dir)
    s.end_connection()
