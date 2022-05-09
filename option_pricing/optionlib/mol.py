import time
import numpy as np
from numpy import linspace
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm


class Solver(object):
    """
        At the basis of:
        https://github.com/hplgit/num-methods-for-PDEs/blob/master/src/diffu/diffu1D_u0.py

    """

    def __init__(self, x_max, t_max):
        """
        :param a: Variable coefficient (constant).
        :param L: Length of the domain ([0,L]).
        :param N: The total number of mesh cells; mesh points are numbered
                  from 0 to N.
        :param F: The dimensionless number a*dt/dx**2, which implicitly
                  specifies the time step.
        :param T: The stop time for the simulation.
        """

        # Boundary condition in U(x=0, t) and U(x=x_max, 0)
        self.boundary_condition = 0.0

        # Step/differential
        self.dx = 0.05
        self.dt = 0.005

        # Option pricing parameters
        self.sigma = 0.001
        self.r = 0.001

        # Max x, max t
        self.x_max = x_max
        self.t_max = t_max

        self.x_array_size = int(self.x_max / self.dx) + 1
        self.t_array_size = int(self.t_max / self.dt) + 1

        # Mesh points in space
        self.x = linspace(0, self.x_max, self.x_array_size)

        # Mesh points in time
        self.t = linspace(0, self.t_max, self.t_array_size)
        self.U_xt = np.zeros((self.x_array_size, self.t_array_size), dtype=np.float)
        self.U_max = 0

    def initialFunction(self, x):
        """
        U(x, t=0)
        """

        initial_value = np.math.sin(x)
        return initial_value

    def pdeSolver(self):
        """
        Pde solver
        :return: self.U_xt, self.x, self.t, t1 - self.t0
        """

        # Set initial condition u(x,t=0) = initialFunction(x)

        for x_i in range(self.x_array_size):
            self.U_xt[x_i, 0] = self.initialFunction(self.x[x_i])

        # Calculate for t + dt
        for t_i in range(1, self.t_array_size):

            # Starting from t_1 (for t_0 we have used initial condition

            # Value for t_i -> t
            t = self.t[t_i]

            # Compute U[x0...x_max, t_i]
            for x_i in range(self.x_array_size -1):
                # Compute U at spatial mesh points U(x_i, t_n)
                # R stands for spatial discretitized ODE
                x = self.x[x_i]
                R = 0.1*np.math.tanh(x)*(self.U_xt[x_i -1, t_i -1] -2 *self.U_xt[x_i, t_i -1] + self.U_xt[x_i +1, t_i -1])/(self.dx*self.dx)

                k1 = self.dt * R
                k2 = self.dt * (R + 0.5 * k1)
                k3 = self.dt * (R + 0.5 * k2)
                k4 = self.dt * (R + k3)

                # Deriviated function in time domain
                self.U_xt[x_i, t_i] = self.U_xt[x_i, t_i - 1] + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

                # Find max U_xt - important for plot function
                if self.U_max < self.U_xt[x_i, t_i]:
                    self.U_max = self.U_xt[x_i, t_i]

            # Insert boundary conditions / Runge-Kutta at x = 0, and x = x_max
            self.U_xt[0, t_i] = self.boundary_condition
            self.U_xt[self.x_array_size - 1, t_i] = self.boundary_condition

        return self.U_xt, self.x, self.t

    def plot(self):
        fig = plt.figure()

        # 3D Plot - Runge-Kutta Method
        ax = fig.gca(projection='3d')
        ax.view_init(azim=30, elev=10)
        self.x, self.t = np.meshgrid(self.x, self.t)
        surf = ax.plot_surface(self.x, self.t, np.transpose(self.U_xt), cmap=cm.coolwarm,
                               antialiased=True)

        ax.set_xlabel('x')
        ax.set_ylabel('t')
        ax.set_zlabel('U[x,t]')
        ax.text2D(0.05, 0.95, "Runge-Kutta Method", transform=ax.transAxes)

        # Customize the z axis.
        ax.set_zlim(0, self.U_max)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.002f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.show()


if __name__ == '__main__':
    x_max = np.math.pi
    t_max = 25
    p = Solver(x_max, t_max)
    p.pdeSolver()
    p.plot()
