from data_manager import DataManager
from flights_manager import FlightsManager

dm = DataManager()
fm = FlightsManager()


def check_deals():
    destinations = dm.get_destinations_data()
    for destination in destinations:
        fm.check_kiwi(destination=destination)
        if not destination.only_kiwi:
            fm.check_azair(destination=destination)


if __name__ == "__main__":
    check_deals()
