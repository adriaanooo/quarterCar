from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import seaborn as sns


def plot_data(t, sprung, unsprung, profile):
    """
    Create a plot of the sprung and unsprung mass against time t. Displays input profile
    :param t:
    :param sprung:
    :param unsprung:
    :param profile:
    :return:
    """
    fig, ax = plt.subplots()

    sns.lineplot(x=t, y=sprung, alpha=0.5, lw=0.75, label='Sprung Mass')
    sns.lineplot(x=t, y=unsprung, alpha=0.5, lw=0.75, label='Unsprung Mass')
    sns.lineplot(x=t, y=profile, alpha=0.25, lw=0.75, label='Input Profile')
    ax.set(ylabel='Displacement (m)', xlabel='Time (s)')

    plt.show()


def animate_data(time, n_samples, t, m1, m2, profile):
    fig, ax = plt.subplots()
    sprung_plot, = ax.plot([], [], 'o', markersize=10)
    unsprung_plot, = ax.plot([], [], 'o', markersize=10)
    plt.plot(t, profile)

    ax.set_xlim([min(t), max(t)])
    ax.set_ylim([-1, 1])

    def animate(n):
        sprung_plot.set_data([t[n]], [m1[n] + 0.15])
        unsprung_plot.set_data([t[n]], [m2[n] + 0.05])

        return sprung_plot, unsprung_plot

    animation = FuncAnimation(fig=fig, func=animate, frames=len(t), interval=(1 / (len(t) * n_samples)))

    plt.show()
