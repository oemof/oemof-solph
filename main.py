import oemof.feedinlib.feedin as feed


def main():

    #use the Timeseries. factory to instantiate a new timeseries
    #implemented so far are "wind" and "pv"

    test = feed.Feedin(Grid(params))

if __name__ == "__main__":
    main()