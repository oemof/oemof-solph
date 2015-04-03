import matplotlib.pyplot as plt


def simple_plot(object, fields):

    for f in fields:
        plt.plot(object[f])
    plt.show()