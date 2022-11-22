import random

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


class HestonModel(object):
    def __init__(self, s0, initial_variance, rho, kappa, theta, epsilon, T, K):
        """
        :param s0: Initial stock price
        :param initial_variance: Initial variance is square of volatility
        :param rho: Correlation
        :param kappa: Kappa mean reversion speed
        :param theta: Long-run variance
        :param epsilon: Volatility of volatility
        :param T: Time to maturity [years]
        :param K: Strike price
        """

        random.seed(5000)  # Set the random seed
        self.S0 = s0
        self.v0 = initial_variance
        self.rho = rho
        self.kappa = kappa
        self.theta = theta
        self.epsilon = epsilon
        self.T = T
        self.K = K

    def option_pricing(self, number_of_montecarlo_paths, number_of_time_steps, sigma):
        """
        Inputs:
         - S0, v0: initial parameters for asset and variance
         - rho   : correlation between asset returns and variance
         - kappa : rate of mean reversion in variance process
         - theta : long-term mean of variance process
         - sigma : vol of vol / volatility of variance process
         - T     : time of simulation
         - N     : number of time steps
         - M     : number of scenarios / simulations

        Outputs:
        - asset prices over time (numpy array)
        - variance over time (numpy array)

        :param number_of_montecarlo_paths: Number of Monte carlo paths
        :param number_of_time_steps: Number of small sub-steps (time)
        :return: Option price
        """

        dt = self.T / number_of_time_steps
        r = 0.03
        # Integrate equations: Euler method, Montecarlo vectorized
        # Create vector representing given number of paths
        V_t = np.ones(number_of_montecarlo_paths) * self.v0
        S_t = np.ones(number_of_montecarlo_paths) * self.S0
        SB_t = np.ones(number_of_montecarlo_paths) * self.S0

        # Generate Montecarlo paths
        for t in range(1, number_of_time_steps):
            # Random numbers for S_t and V_t
            Z_s = np.random.normal(size=number_of_montecarlo_paths)
            Z_v = self.rho * Z_s + np.sqrt(1 - self.rho ** 2) * np.random.normal(size=number_of_montecarlo_paths)

            # Volatility can be >= 0
            V_t = np.maximum(V_t, 0)

            # Calculate vector for given time
            # Stock price process driven by Heston
            S_t = S_t * np.exp(np.sqrt(V_t * dt) * Z_s + (r - 0.5 * V_t) * dt)

            # Stock price process driven by Black-Scholes
            SB_t = SB_t * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z_s)

            # Volatility process
            V_t = V_t + self.kappa * (self.theta - V_t) * dt + self.epsilon * np.sqrt(V_t * dt) * Z_v

        option_price = np.mean(np.maximum(S_t - self.K, 0))
        option_price_for_black_scholes = np.mean(np.maximum(SB_t - self.K, 0))

        price_for_heston = round(option_price, 2)
        price_black_scholes = round(option_price_for_black_scholes, 2)

        return price_for_heston, price_black_scholes

    def plot_heston(self, s_t: list, v_t: list, plot_directory: str):
        """
        Plot Hest volatility and option price.

        :param s_t: List of option prices
        :param v_t: List of volatilities
        :param plot_directory: Directory to store Heston plots
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='w')

        ax1.grid()
        ax1.plot(range(self.T), s_t)

        ax1.set(xlabel='T [Days]', ylabel='Option Price',
                title='Asset price calculated by Heston model')

        ax2.grid()
        ax2.plot(range(self.T), v_t, c='coral')
        ax2.set(xlabel='T [Days]', ylabel='Stochastic volatility',
                title='Volatility calculated for Heston model')

        fig.savefig("{}/{}".format(plot_directory, 'heston.png'))
        fig.clear()
        plt.close(fig)
