import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import ticker
import matplotlib.pyplot as plt


class HestonModel(object):
    def __init__(self, s0, mu, v0, rho, kappa, theta, xi, T, dt):
        self.S0 = s0
        self.mu = mu
        self.v0 = v0
        self.rho = rho
        self.kappa = kappa
        self.theta = theta
        self.xi = xi
        self.T = T
        self.dt = dt

        self.w_s = None
        self.w_v = None

    def generate_brownian_motion(self):
        """
        Generate random Brownian Motion
        """

        mu = np.array([0, 0])
        cov = np.matrix([[1, self.rho], [self.rho, 1]])
        w = np.random.multivariate_normal(mu, cov, self.T)
        self.w_s = w[:, 0]
        self.w_v = w[:, 1]

    def heston_pricing(self):
        """
        Generate a Monte Carlo simulation for the Heston model
        """

        # Generate paths
        vt = np.zeros(self.T)
        vt[0] = self.v0
        s_t = np.zeros(self.T)
        s_t[0] = self.S0
        for t in range(1, self.T):
            vt[t] = np.abs(
                vt[t - 1] + self.kappa * (self.theta - np.abs(vt[t - 1])) * self.dt + self.xi * np.sqrt(np.abs(vt[t - 1])) * self.w_v[t] * np.sqrt(self.dt))
            s_t[t] = s_t[t - 1] * np.exp((self.mu - 0.5 * vt[t-1]) * self.dt + np.sqrt(vt[t-1] * self.dt) * self.w_s[t])

        return s_t, vt

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