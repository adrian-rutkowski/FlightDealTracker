import requests
import constants
from data_manager import DataManager
from notifications_manager import NotificationsManager

def check_deals():
    dm = DataManager()
    nm = NotificationsManager()
    destinations = dm.get_destinations_data()
    for destination in destinations:
        params = dm.prepare_params(destination=destination)
        try:
            response = requests.get(url=f"{constants.URL}/search", headers={'apikey': constants.KIWI_API_KEY}, params=params)
            print(response.status_code)
            response.raise_for_status()
            trip = response.json()['data'][0]
            deal = dm.get_trip(trip=trip)
            if deal.price < destination.acceptable_price:
                nm.notify_about_deal(deal=deal)
                dm.store_deal_details(deal=deal)
            else:
                print(f'No deals to {deal.fly_to} found below the threshold of {destination.acceptable_price} PLN')
        except requests.HTTPError as e:
            print(e)
            print(response.json())
        except IndexError as e:
            print(f"No deals to {destination.fly_to} found.")

if __name__ == "__main__":
    check_deals()
