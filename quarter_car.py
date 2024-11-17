import pandas as pd
import numpy as np
import math
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import seaborn as sns


class QuarterCar:
    """
    A quarter car model.
    """
    def __init__(self, m1=0.0, m2=0.0, k1=0.0, c1=0.0, k2=0.0, c2=0.0,
                 time=60, n_samples=5000,
                 input_profile=None,
                 data="C:/Users/adrvb/OneDrive/Documents/OTR/Quarter Car Model/inputs.xlsx"):

        self.t = np.linspace(0, time, n_samples)

        # If no Excel file, take arguments.
        if data is None:
            self.m1 = m1 / 4
            self.m2 = m2
            self.k1 = k1
            self.c1 = c1 * 2 * self.m1 * math.sqrt(self.k1 / self.m1)
            self.k2 = k2
            self.c2 = c2
        else:
            # Grab data from Excel sheet.
            data = pd.read_excel(data, index_col='Parameter')
            self.m1 = data.iloc[0]['Value'] / 4
            self.m2 = data.iloc[1]['Value']
            self.k1 = data.iloc[2]['Value']
            self.c1 = data.iloc[3]['Value'] * 2 * self.m1 * math.sqrt(self.k1 / self.m1)
            self.k2 = data.iloc[4]['Value']

        # Set initial conditions and input
        self.input_profile = input_profile
        self.X_0 = (0, 0, 0, 0, input_profile(0))

    def __dXdt(self, t, X):
        """
        Sets up a system of linear DEs for sprung and unsprung masses.
        """
        x1, x2, x3, x4, u = X
        return [
            (self.k1 / self.m1) * (x4 - x2) + (self.c1 / self.m1) * (x3 - x1),
            x1,
            (self.k2 / self.m2) * (u - x4) - (self.k1 / self.m2) * (x4 - x2) - (self.c1 / self.m2) * (x3 - x1),
            x3,
            self.input_profile(t)
        ]

    def get_displacements(self):
        solns = solve_ivp(self.__dXdt, [0, self.t[-1]], y0=self.X_0, t_eval=self.t)
        return self.t, solns.y[0], solns.y[2]


def main():
    def input_profile(t):
        f_min = 0.1  # Start frequency in Hz
        f_max = 2.0  # End frequency in Hz
        T = 60  # Total duration in seconds

        frequency = f_min + (f_max - f_min) * (t / T)  # Linearly increasing frequency
        return 0.1 * math.sin(2 * math.pi * frequency * t)

    my_car = QuarterCar(input_profile=input_profile)
    t, m1, m2 = my_car.get_displacements()

    data = pd.DataFrame(columns=['Road Displacement (m)', 'Unsprung Mass Displacement (m)',
                                 'Sprung Mass Displacement (m)'])
    data['Road Displacement (m)'] = t
    data['Unsprung Mass Displacement (m)'] = m2
    data['Sprung Mass Displacement (m)'] = m1

    data.to_excel('C:/Users/adrvb/OneDrive/Documents/OTR/Quarter Car Model/outputs.xlsx')

    ax1 = sns.lineplot(x=t, y=[input_profile(n) for n in t], alpha=0.25, label='Input Profile')
    ax2 = sns.lineplot(x=t, y=m1, label='Sprung', alpha=0.5)
    ax3 = sns.lineplot(x=t, y=m2, label='Unsprung', alpha=0.5)

    ax1.set(xlabel='time (s)', ylabel='displacement (m)')
    ax1.legend(loc='upper right')

    plt.show()


if __name__ == '__main__':
    main()
