import random

import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import ticker
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
        self.N = 1000  # Number of small sub-steps (time)

        self.S0 = s0
        self.v0 = initial_variance
        self.rho = rho
        self.kappa = kappa
        self.theta = theta
        self.epsilon = epsilon
        self.T = T
        self.K = K

    def option_pricing(self, number_of_montecarlo_paths, number_of_time_steps):
        """

        :param number_of_montecarlo_paths: Number of Monte carlo paths
        :param number_of_time_steps: Number of small sub-steps (time)
        :return: Option price
        """

        dt = self.T / number_of_time_steps

        # Integrate equations: Euler method, Montecarlo vectorized
        V_t = np.ones(number_of_montecarlo_paths) * self.v0
        S_t = np.ones(number_of_montecarlo_paths) * self.S0

        # Generate Montecarlo paths
        for t in range(1, self.N):
            # Random numbers for S_t and V_t
            Z_s = np.random.normal(size=number_of_montecarlo_paths)
            Z_v = self.rho * Z_s + np.sqrt(1 - self.rho ** 2) * np.random.normal(size=number_of_montecarlo_paths)

            # Euler integration
            V_t = np.maximum(V_t, 0)
            S_t = S_t * np.exp(np.sqrt(V_t * dt) * Z_s - V_t * dt / 2)  # Stock price process
            V_t = V_t + self.kappa * (self.theta - V_t) * dt + self.epsilon * np.sqrt(V_t * dt) * Z_v  # Volatility process

        option_price = np.mean(np.maximum(S_t - self.K, 0))

        price = round(option_price, 2)

        return price

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
