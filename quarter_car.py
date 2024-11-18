from math import *
import pandas as pd
import numpy as np
from scipy.integrate import solve_ivp
from data_handling import load_from_excel


class QuarterCar:
    """
    A quarter car model.
    """
    def __init__(self, m1=0.0, m2=0.0, k1=0.0, c1=0.0, k2=0.0, c2=0.0,
                 time=60, n_samples=5000,
                 input_profile=None,
                 path="C:/Users/adrvb/OneDrive/Documents/OTR/Quarter Car Model/inputs.xlsx"):

        self.t = np.linspace(0, time, n_samples)

        # If no Excel file, take arguments.
        if path is None:
            self.m1 = m1 / 4                                        # Sprung mass (kg)
            self.m2 = m2 + self.m1                                    # Unsprung mass (kg)
            self.k1 = k1                                            # Spring constant (N/m)
            self.c1 = c1 * 2 * self.m1 * sqrt(self.k1 / self.m1)    # Damping coefficient to constant
            self.k2 = k2                                            # Tire stiffness (N/m)
            self.c2 = c2
        else:
            # Grab data from Excel sheet.
            self.m1, self.m2, self.k1, self.c1, self.k2 = load_from_excel(path=path)

        # Set initial conditions and input profile.
        self.input_profile = input_profile
        self.X_0 = (0, 0, 0, 0, input_profile(0))

    def __input_profile_velocity(self, x):
        """
        Gets the derivative of the input profile for system of equations.
        :param x:
        :return:
        """
        h = 1e-5
        return (self.input_profile(x + h) - self.input_profile(x - h)) / (2 * h)

    def __dXdt(self, t, X):
        """
        Sets up a system of linear DEs for sprung and unsprung masses.
        """
        # System equations (to be solved)
        x1, x2, x3, x4, input_profile_disp = X
        return [
            (self.k1 / self.m1) * (x4 - x2) + (self.c1 / self.m1) * (x3 - x1),  # Sprung mass velocity.
            x1,                                                                 # Sprung mass acceleration.
            (self.k2 / self.m2) * (input_profile_disp - x4) - (self.k1 / self.m2) * \
            (x4 - x2) - (self.c1 / self.m2) * (x3 - x1),                        # Unsprung mass velocity.
            x3,                                                                 # Unsprung mass acceleration.
            self.__input_profile_velocity(t)                                    # Input profile velocity.
        ]

    def get_displacements(self):
        """
        Returns time array, sprung mass disp, unsprung mass disp, and input profile.
        :return:
        """
        solns = solve_ivp(self.__dXdt, [0, self.t[-1]], y0=self.X_0, t_eval=self.t, method='LSODA')
        return self.t, solns.y[0], solns.y[2], solns.y[4]
