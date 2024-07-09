from bs4 import BeautifulSoup
import requests
import constants
from data_manager import DataManager
from data_models import DestinationModel, TripModel
from enums import DataSource
from logger import Logger
from notifications_manager import NotificationsManager

dm = DataManager()
nm = NotificationsManager()
log = Logger()


class FlightsManager:

    def check_kiwi(self, destination: DestinationModel):
        params = dm.prepare_kiwi_params(destination=destination)
        try:
            response = requests.get(url=f"{constants.KIWI_URL}/search",
                                    headers={'apikey': constants.KIWI_API_KEY},
                                    params=params)
            response.raise_for_status()
            trip = response.json()['data'][0]
            deal = dm.get_trip(trip=trip)
            if deal.price < destination.target_price:
                nm.notify_about_deal(source=DataSource.KIWI, deal=deal)
                dm.update_target_price(
                    fly_to=destination.fly_to, new_price=deal.price)
            else:
                msg = (f"KIWI: No deals to {deal.fly_to} found below the threshold of {destination.target_price} PLN. "
                       f"Lowest price is {deal.price} PLN")
                print(msg)
                log.log_info(msg)

        except requests.HTTPError as e:
            print(e)
            print(response.json())
            log.log_critical(e)
        except IndexError:
            error_msg = f"KIWI: No deals to {destination.fly_to} found."
            print(error_msg)
            log.log_info(error_msg)

    def check_azair(self, destination: DestinationModel):
        search = dm.prepare_azair_url(destination=destination)
        response = requests.get(constants.AZAIR_URL+search)

        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                top_record = soup.find('div', {'class': 'result'})
                data = top_record.find('div', {'class': 'text'})

                deal = TripModel()
                deal.departure_date = data.find('span', class_='date').text
                deal.fly_from = ' '.join(
                    data.find('span', class_='from').get_text().split()[1:3])
                deal.fly_to = (f"{data.find('span', class_='to').text.split(' ')[1]} "
                               f"{data.find('span', class_='to').find('span', class_='code').text[:3]}")

                deal.price = int(''.join(filter(str.isdigit, data.find(
                    'div', class_='totalPrice').find('span', class_='tp').text)))
                deal.length_of_stay = data.find('div', class_='totalPrice').find(
                    'span', class_='lengthOfStay').text.split(':')[-1].strip()
                deal.url = top_record.find('div', class_='bookmark').find('a')[
                    'href'].replace("¤", "&curren")

                if deal.price < destination.target_price:
                    nm.notify_about_deal(source=DataSource.AZAIR, deal=deal)
                    dm.update_target_price(
                        fly_to=destination.fly_to, new_price=deal.price)
                else:
                    no_deals_msg = (f"AZAIR: No deals to {deal.fly_to} found below the "
                                    f"threshold of {destination.target_price} PLN. Lowest price is {deal.price} PLN")
                    print(no_deals_msg)
                    log.log_info(no_deals_msg)
            except AttributeError:
                no_flights_msg = f"AZAIR: No deals to {destination.fly_to} found."
                print(no_flights_msg)
                log.log_info(no_flights_msg)
        else:
            no_data_msg = f'AZAIR: Failed to retrieve data. Status code: {response.status_code}'
            print(no_data_msg)
            log.log_error(no_data_msg)
