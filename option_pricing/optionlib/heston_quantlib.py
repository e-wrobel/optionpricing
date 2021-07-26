# Import the libraries , !pip install "library" for first time installing
# https://blog.quantinsti.com/heston-model/
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import random
from math import sqrt, exp

# Pricing option using heston can be done with the package 'QuantLib'
#!pip install QuantLib
import QuantLib as ql


# set the style for graphs
plt.rcParams["figure.figsize"] = (10, 7)
plt.style.use('seaborn-darkgrid')

# Payoff function inputs are option type and strike price
strike_price = 100
option_type = ql.Option.Call

call_payoff = ql.PlainVanillaPayoff(option_type, strike_price)

# Exercise function takes maturity date of the option as input
day_count = ql.Actual365Fixed()
calendar = ql.UnitedStates()
maturity = ql.Date(3, 8, 2021)
today = ql.Date(4, 8,2020)

call_exercise = ql.EuropeanExercise(maturity)

# Function inputs are striked type payoff and exercise
option = ql.VanillaOption(call_payoff, call_exercise)

# Option input values
spot_price = 105
strike_price = 100
yearly_historical_volatility = 0.1
riskfree_rate = 0.01
dividend = 0

variance = 0.01 # Initial variance is square of volatility
kappa = 2       # Speed of mean reversion
theta = 0.01    # Long-run variance
epsilon = 0.1   # Volatility of volatility
rho = 0.0       # Correlation

initial_value = ql.QuoteHandle(ql.SimpleQuote(spot_price))

# Setting up flat risk free curves
discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, riskfree_rate,day_count))
dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(today, dividend, day_count))

heston_process = ql.HestonProcess(discount_curve,dividend_yield, initial_value,variance,kappa,theta,epsilon,rho)

# Inputs used for the engine are model, Tolerance level, maximum evaluations
engine = ql.AnalyticHestonEngine(ql.HestonModel(heston_process),0.001,1000)
option.setPricingEngine(engine)
price = option.NPV()
print ("option_price", round(price,2))