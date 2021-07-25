import numpy as np
import scipy.stats as si
# import sympy as sy
# import sympy.stats as systats


class Option(object):

    """
    Python Implementation of Black-Scholes formula for non-dividend paying options.

    Based on https://aaronschlegel.me/black-scholes-formula-python.html

    For sympy.stats install: pip install statistics
    """

    def __init__(self, S, K, T, r, sigma):

        """
        S: spot price
        K: strike price
        T: time to maturity in days
        r: interest rate
        sigma: volatility of underlying asset
        """

        self.S = float(S)
        self.K = float(K)
        self.T = float(T/365.0)
        self.r = float(r)
        self.sigma = float(sigma)

    def euro_vanilla_call(self):

        """
        Exact solution for call option.

        :return: call option price
        """

        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

        call = (self.S * si.norm.cdf(d1, 0.0, 1.0) - self.K * np.exp(-self.r * self.T) * si.norm.cdf(d2, 0.0, 1.0))

        return call

    def euro_vanilla_put(self):

        """
        Exact solution for put option.

        :return: put option price
        """

        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = (np.log(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

        put = (self.K * np.exp(-self.r * self.T) * si.norm.cdf(-d2, 0.0, 1.0) - self.S * si.norm.cdf(-d1, 0.0, 1.0))

        return put

    def euro_vanilla_call_symbolic(self):

        """
        Symbolic solution for call option.

        :return: call option price (symbolic)
        """

        N = systats.Normal(0.0, 1.0)

        d1 = (sy.ln(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sy.sqrt(self.T))
        d2 = (sy.ln(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sy.sqrt(self.T))

        call = (self.S * N.cdf(d1) - self.K * sy.exp(-self.r * self.T) * N.cdf(d2))

        return call

    def euro_vanilla_put_symbolic(self):

        """
        Symbolic solution for put option.

        :return: put option price (symbolic)
        """

        N = systats.Normal(0.0, 1.0)

        d1 = (sy.ln(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sy.sqrt(self.T))
        d2 = (sy.ln(self.S / self.K) + (self.r - 0.5 * self.sigma ** 2) * self.T) / (self.sigma * sy.sqrt(self.T))

        put = (self.K * sy.exp(-self.r * self.T) * N.cdf(-d2) - self.S * N.cdf(-d1))

        return put
