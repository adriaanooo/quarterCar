import matplotlib.pyplot as plt


def plot_data(t, m1, m2, profile):
    fig, ax = plt.subplots()
    animated_plot1, = ax.plot([], [], 'o', markersize=10)
    animated_plot2, = ax.plot([], [], 'o', markersize=10)
    plt.plot(t, profile)

    ax.set_xlim([min(t), max(t)])
    ax.set_ylim([-1, 1])

    def update_data(frame):

        animated_plot1.set_data([t[frame]], [m1[frame]])
        animated_plot2.set_data([t[frame]], [m2[frame]])

        return

    animation = FuncAnimation(fig=fig, func=update_data, frames=len(t), interval=(1000 * (time / n_samples)))

    plt.show()