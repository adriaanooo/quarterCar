from quarter_car import QuarterCar
import matplotlib.pyplot as plt
import seaborn as sns
from input_profile import input_profile
from data_handling import write_to_excel


def main():
    time = 60
    n_samples = 1000

    my_car = QuarterCar(input_profile=input_profile, time=time, n_samples=n_samples)
    t, m1, m2, profile = my_car.get_displacements()

    write_to_excel('C:/Users/adrvb/OneDrive/Documents/OTR/Quarter Car Model/outputs.xlsx', t, m1, m2)

    fig, ax = plt.subplots()
    sns.lineplot(x=t, y=m1, alpha=0.25, label='Sprung Mass')
    sns.lineplot(x=t, y=m2, alpha=0.5, label='Unsprung Mass')
    sns.lineplot(x=t, y=profile, alpha=0.75, label='Input Profile')

    ax.set(ylabel='Displacement (m)', xlabel='Time (s)')
    fig.legend()

    plt.show()


if __name__ == '__main__':
    main()
