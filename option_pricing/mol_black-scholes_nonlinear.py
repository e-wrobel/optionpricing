import numpy as np
from numpy import linspace
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
from option_pricing.black_scholes_option_pricing import Option
np.seterr(all='ignore')

linear = 'Linear'
non_linear = 'Non-linear'

days_in_year = 252.0

# https://bankingschool.co.in/indian-financial-system/how-to-convert-volatility-from-annual-to-daily-weekly-or-monthly/
class Solver(object):
    """
        At the basis of:
        https://github.com/hplgit/num-methods-for-PDEs/blob/master/src/diffu/diffu1D_u0.py
    """

    def __init__(self, s_max, t_max, k, beta, sigma, r, s_price, t_days):
        """
        :param s_max: Max price
        :param t_max: Max expiration time
        :param k: Strike price
        :param beta: Non-linear parameter
        :param sigma: Asset price volatility
        :param r: Risk-free interest rate
        :param s_price: Asset price from the market
        :param t_days: Expiration time for option in days
        """

        self.equation_type = linear
        self.option_type = None

        # Option pricing parameters
        self.sigma = np.float64(sigma)
        self.r = np.float64(r)
        self.k = np.float64(k)
        self.beta = np.float64(beta)

        # Asset price and option expiration time (in years)
        self.s_price = s_price
        self.t_year = t_days/days_in_year
        self.found = False

        # Option price for given s_price and t_year
        self.calculated_option_price = None

        # Step/differential
        self.ds = np.float64(s_max / 100.0)
        self.dt = 0.0005
        # self.dt = self.r*self.ds/(self.sigma ** 2)
        # Max s, max t
        self.s_max = np.float64(s_max)
        self.t_max = np.float64(t_max)
        self.dt = (self.ds ** 2) / (39 * self.sigma ** 2 + 0.5 * self.r) / s_max ** 2
        self.s_array_size = int(self.s_max / self.ds)
        self.t_array_size = int(self.t_max / self.dt)

        # Mesh points in space
        self.s = linspace(0, self.s_max, self.s_array_size)
        self.ds = self.s[2] - self.s[1]
        # Mesh points in time
        self.t = linspace(0, self.t_max, self.t_array_size)
        self.U_st = np.zeros((self.s_array_size, self.t_array_size), dtype=np.float64)
        self.U_max = 0.0

    def initialFunction(self, s):
        """
        Initial value for given S: U(s, t=0).

        :param s: Option price at t=0

        :return: Initial value for given S
        """

        initial_value = max(s - self.k, 0)

        return initial_value

    def pdeSolver(self, equation_type=linear):
        """
        Pde solver.

        :type equation_type: Linear on NonLinear

        :return: True or False (in case of computation error)
        """

        self.option_type = "european"
        self.equation_type = equation_type

        # Set initial condition u(s,t=0) = initialFunction(s)
        for s_i in range(self.s_array_size):
            self.U_st[s_i, 0] = self.initialFunction(self.s[s_i])

        try:
            # Calculate for t + dt
            for t_i in range(1, self.t_array_size):
                # Starting from t_1 (for t_0 we have used initial condition
                # Value for t_i -> t
                t = self.t[t_i]
                s_i = 0

                # Compute U[x0...s_max, t_i]
                for s_i in range(1, self.s_array_size - 1):
                    # Compute U at spatial mesh points U(x_i, t_n)
                    # R stands for spatial ODE
                    s = self.s[s_i]

                    if equation_type == non_linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1] -self.beta * self.U_st[s_i, t_i - 1] ** 3
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i, t_i - 1]) / self.ds
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3
                    elif equation_type == linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1]
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i - 1, t_i - 1]) / (2 * self.ds)
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3

                    # Runge-Kutta4 coeficients
                    k1 = self.dt * R
                    k2 = self.dt * (R + 0.5 * k1)
                    k3 = self.dt * (R + 0.5 * k2)
                    k4 = self.dt * (R + k3)

                    # Deriviated function in time domain
                    self.U_st[s_i, t_i] = self.U_st[s_i, t_i - 1] + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

                    # Check option price for given S and t
                    if s >= self.s_price and t >= self.t_year and self.found == False:
                        print("got it")
                        self.calculated_option_price = (self.U_st[s_i, t_i], s, t)
                        self.found = True

                    # Find max U_st - important for plot function
                    if self.U_max < self.U_st[s_i, t_i]:
                        self.U_max = self.U_st[s_i, t_i]

                # Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
                self.U_st[0, t_i] = 0
                self.U_st[s_i + 1, t_i] = self.s[s_i + 1] - self.k

        except FloatingPointError as e:
            print("Exception at t = {} and s = {}, {}, exiting!".format(t, s, e))
            return False

        return True

    def pdeSolverAsian(self, equation_type=linear):
        """
        Pde solver.

        :type equation_type: Linear on NonLinear

        :return: True or False (in case of computation error)
        """

        self.equation_type = equation_type
        self.option_type = 'asian'

        # Set initial condition u(s,t=0) = initialFunction(s)
        s_sum = 0
        for s_i in range(self.s_array_size):
            s_sum = s_sum + self.s[s_i]
            s_avg = s_sum/(s_i +1)
            self.U_st[s_i, 0] = max(s_avg - self.k, 0)

        try:
            # Calculate for t + dt
            for t_i in range(1, self.t_array_size):
                # Starting from t_1 (for t_0 we have used initial condition
                # Value for t_i -> t
                t = self.t[t_i]
                s_i = 0

                # Compute U[x0...s_max, t_i]
                s_sum = 0
                for s_i in range(1, self.s_array_size - 1):
                    # Compute U at spatial mesh points U(x_i, t_n)
                    # R stands for spatial ODE
                    s = self.s[s_i]

                    if equation_type == non_linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1] -self.beta * self.U_st[s_i, t_i - 1] ** 3
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i, t_i - 1]) / self.ds
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3
                    elif equation_type == linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1]
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i - 1, t_i - 1]) / (2 * self.ds)
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3

                    # Runge-Kutta4 coeficients
                    k1 = self.dt * R
                    k2 = self.dt * (R + 0.5 * k1)
                    k3 = self.dt * (R + 0.5 * k2)
                    k4 = self.dt * (R + k3)

                    # Deriviated function in time domain
                    self.U_st[s_i, t_i] = self.U_st[s_i, t_i - 1] + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

                    # Check option price for given S and t
                    if s >= self.s_price and t >= self.t_year and self.found == False:
                        print("got it")
                        self.calculated_option_price = (self.U_st[s_i, t_i], s, t)
                        self.found = True

                    # Find max U_st - important for plot function
                    if self.U_max < self.U_st[s_i, t_i]:
                        self.U_max = self.U_st[s_i, t_i]
                    s_sum = s_sum + self.s[s_i + 1]
                # Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
                self.U_st[0, t_i] = 0

                s_avg = s_sum/s_i
                self.U_st[s_i + 1, t_i] = s_avg - self.k

        except FloatingPointError as e:
            print("Exception at t = {} and s = {}, {}, exiting!".format(t, s, e))
            return False

        return True

    def pdeSolverAmerican(self, equation_type=linear):
        """
        Pde solver.

        :type equation_type: Linear on NonLinear

        :return: True or False (in case of computation error)
        """

        self.option_type = "american"
        self.equation_type = equation_type

        # Set initial condition u(s,t=0) = initialFunction(s)
        for s_i in range(self.s_array_size):
            self.U_st[s_i, 0] = self.initialFunction(self.s[s_i])

        try:
            # Calculate for t + dt
            for t_i in range(1, self.t_array_size):
                # Starting from t_1 (for t_0 we have used initial condition
                # Value for t_i -> t
                t = self.t[t_i]
                s_i = 0

                # Compute U[x0...s_max, t_i]
                for s_i in range(1, self.s_array_size - 1):
                    # Compute U at spatial mesh points U(x_i, t_n)
                    # R stands for spatial ODE
                    s = self.s[s_i]

                    if equation_type == non_linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1] -self.beta * self.U_st[s_i, t_i - 1] ** 3
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i, t_i - 1]) / self.ds
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3
                    elif equation_type == linear:
                        R1 = -self.r * self.U_st[s_i, t_i - 1]
                        R2 = self.r * s * (self.U_st[s_i + 1, t_i - 1] - self.U_st[s_i - 1, t_i - 1]) / (2 * self.ds)
                        R3 = 0.5 * (self.sigma ** 2) * (s ** 2) * (
                                self.U_st[s_i - 1, t_i - 1] - 2 * self.U_st[s_i, t_i - 1] + self.U_st[
                            s_i + 1, t_i - 1]) / (self.ds ** 2)

                        R = R1 + R2 + R3

                    # Runge-Kutta4 coeficients
                    k1 = self.dt * R
                    k2 = self.dt * (R + 0.5 * k1)
                    k3 = self.dt * (R + 0.5 * k2)
                    k4 = self.dt * (R + k3)

                    # Deriviated function in time domain
                    actual_price1 = max(s - self.k, 0.0)
                    o = Option(s, self.k, 1, self.r, self.sigma)
                    actual_price = o.euro_vanilla_call()
                    calculated_price = self.U_st[s_i, t_i - 1] + (1.0 / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

                    if actual_price >= calculated_price:
                        self.U_st[s_i, t_i] = actual_price
                    else:
                        self.U_st[s_i, t_i] = calculated_price

                        # Check option price for given S and t
                    if s >= self.s_price and t >= self.t_year and self.found == False:
                        print("got it")
                        self.calculated_option_price = (self.U_st[s_i, t_i], s, t)
                        self.found = True

                    # Find max U_st - important for plot function
                    if self.U_max < self.U_st[s_i, t_i]:
                        self.U_max = self.U_st[s_i, t_i]

                # Insert boundary conditions / Runge-Kutta at s = 0, and s = s_max
                self.U_st[0, t_i] = 0
                self.U_st[s_i + 1, t_i] = self.s[s_i + 1] - self.k

        except FloatingPointError as e:
            print("Exception at t = {} and s = {}, {}, exiting!".format(t, s, e))
            return False

        return True

    def plot(self, name_prefix):
        """
        Plot 3D chart for given option and save it on disk.

        :param name_prefix: Prefix for filename
        """

        fig = plt.figure(figsize=(12, 8))
        fig.subplots_adjust(left=0, bottom=0, right=1, top=0.86)

        # 3D Plot - Runge-Kutta Method
        ax = fig.gca(projection='3d')
        ax.view_init(azim=-100, elev=18)
        self.s, self.t = np.meshgrid(self.s, self.t)

        Uxt = np.transpose(self.U_st)
        surf = ax.plot_surface(self.s, self.t, Uxt, cmap=cm.jet, antialiased=True)

        fig.tight_layout()
        ax.set_xlabel('S')
        ax.set_ylabel('t')
        ax.set_zlabel('V[S,t]')

        beta_info = "\nbeta={:0.6f}".format(self.beta) if self.equation_type == non_linear else ''
        ax.text2D(0.8, 0.83, "Method of lines: {} Black-Scholes equation."
                              "\nStrike price: K={}"
                              "\nInitial condition: V(S, t=0)=max(S-K, 0)"
                              "\nBoundary condition: V(S=0, t)=0"
                              "\nBoundary condition: V(S=$S_M)=S_M - K$"
                              "\n$S\in$(0, {:0.2f}) and $t\in$(0, {})"
                              "\n$\sigma=${}, $r=${}"
                  .format(self.equation_type, self.k, self.s_max, self.t_max, self.sigma, self.r) + beta_info, size=10,
                  transform=ax.transAxes)

        # Customize the z axis.
        ax.set_zlim(0, self.U_max)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        file_name = "{}_K{}_sigma{}_r{}_T{}_linear_{}".format(name_prefix, self.k, self.sigma, self.r, self.t_max, self.option_type)
        if self.equation_type == non_linear:
            file_name = "{}_K{}_sigma{}_r{}_beta{}_T{}_nonlinear_{}".format(name_prefix, self.k, self.sigma, self.r, self.beta, self.t_max, self.option_type)
        plt.savefig('numerical_computations/' + file_name + '.png')


if __name__ == '__main__':

    s_max = 2350
    t_max = 0.9
    k = 1500
    beta = 0.000002
    sigma = 0.02
    r = 0.01

    p_european = Solver(s_max=s_max, t_max=t_max, k=k, beta=beta, sigma=sigma, r=r, s_price=1200, t_days=40)
    if p_european.pdeSolver(equation_type=non_linear):
        p_european.plot('Black-Scholes')
        option_price, asset_price, expiration_time_in_years = p_european.calculated_option_price
        print('Option price: {}, asset price: {}, expiration time [{} years, {} days]'.format(option_price,
                                                                                          asset_price,
                                                                                          expiration_time_in_years,
                                                                                          expiration_time_in_years*days_in_year))
    p_american = Solver(s_max=s_max, t_max=t_max, k=k, beta=beta, sigma=sigma, r=r, s_price=1200, t_days=40)
    if p_american.pdeSolverAmerican(equation_type=non_linear):
        p_american.plot('Black-Scholes')
        option_price, asset_price, expiration_time_in_years = p_american.calculated_option_price
        print('Option price: {}, asset price: {}, expiration time [{} years, {} days]'.format(option_price,
                                                                                          asset_price,
                                                                                          expiration_time_in_years,
                                                                                          expiration_time_in_years*days_in_year))