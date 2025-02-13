from math import *
import numpy as np
from scipy.integrate import solve_ivp
from scipy.misc import derivative


class QuarterCar:
    """
    A quarter car model.
    """
    def __init__(self, m1=0.0, m2=0.0, k1=0.0, c1=0.0, k2=0.0, c2=0.02, time=60, n_samples=5000, input_profile=None):
        """
        Initialize vehicle and run parameters. Solve system of equations.
        :param m1:
        :param m2:
        :param k1:
        :param c1:
        :param k2:
        :param c2:
        :param time:
        :param n_samples:
        :param input_profile:
        """
        # Vehicle params
        self.m1 = m1 / 4                                            # Sprung mass (kg)
        self.m2 = m2                                                # Unsprung mass (kg)
        self.k1 = k1                                                # Spring rate (N/m)
        self.c1 = c1                                                # Damping Ratio
        self.beta1 = self.__get_damping_constant(self.m1, k1, c1)   # Turns damping ratio in damping constant
        self.k2 = k2                                                # Tire stiffness (N/m)
        self.c2 = c2
        self.beta2 = self.__get_damping_constant(self.m2, k2, c2)   # Tire damping constant.

        # Set up run time and resolution
        self.t = np.linspace(0, time, n_samples)               # Time sample array.

        # Set up input profile for input and plotting
        self.__input_profile = input_profile                        # Input profile for use in class.
        self.input_profile = input_profile(self.t)                  # Input profile for attribute.

        # Solve for vehicle displacement
        self.X_0 = (0, 0, 0, 0)                                     # Initial conditions.
        solns = solve_ivp(self.__dXdt, [0, self.t[-1]], y0=self.X_0, t_eval=self.t, method='RK45')
        self.sprung_disp = solns.y[1]
        self.unsprung_disp = solns.y[3]

    def __dXdt(self, t, X):
        """
        Sets up a system of linear DEs for sprung and unsprung masses.
        """
        u = np.interp(t, self.t, self.input_profile)
        du = derivative(self.__input_profile, t)
        x1, x2, x3, x4 = X
        return [
            (self.k1 / self.m1) * (x4 - x2) + (self.beta1 / self.m1) * (x3 - x1),
            x1,
            (self.k2 / self.m2) * (u - x4) + (self.beta2 / self.m2) * (du - x3) - (self.k1 / self.m2) * (x4 - x2)
            - (self.beta1 / self.m2) * (x3 - x1),
            x3
        ]

    @staticmethod
    def __get_damping_constant(m, k, c):
        """
        Get damping constant given mass, spring constant, and damping ratio.
        :param m:
        :param k:
        :param c:
        :return:
        """
        return c * 2 * m * sqrt(k / m)

    def print_vehicle_params(self):
        """
        Prints the vehicle's parameters.
        :return:
        """
        print(f'Sprung mass:        {self.m1} kg\n'
              f'Unsprung mass:      {self.m2} kg\n'
              f'Spring Rate:        {self.k1} N/m\n'
              f'Damping Ratio:      {self.c1}\n'
              f'Damping Constant:   {self.beta1} Ns/m\n'
              f'Tire Stiffness:     {self.k2} N/m')
