from data_manager import DataManager
from flights_manager import FlightsManager

dm = DataManager()
fm = FlightsManager()


def check_deals():
    destinations = dm.get_destinations_data()
    for destination in destinations:
        if destination.only_kiwi:
            fm.check_kiwi(destination=destination)
        else:
            fm.check_azair(destination=destination)


if __name__ == "__main__":
    check_deals()
