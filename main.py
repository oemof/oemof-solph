import feedinlib.feedin as feed


def main():

    #use the Timeseries. factory to instantiate a new timeseries
    #implemented so far are "wind" and "pv"

    wind = feed.create_timeseries("wind", "2012", "Hamburg")

    print wind.get_timeseries()

if __name__ == "__main__":
    main()