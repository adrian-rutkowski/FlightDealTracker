from bs4 import BeautifulSoup
import requests
import constants
from data_manager import DataManager
from data_models import DestinationModel, TripModel
from enums import DataSource
from notifications_manager import NotificationsManager

dm = DataManager()
nm = NotificationsManager()


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
            if deal.price < destination.acceptable_price:
                nm.notify_about_deal(source=DataSource.KIWI, deal=deal)
            else:
                print(
                    f'KIWI: No deals to {deal.fly_to} found below the threshold of {destination.acceptable_price} PLN')
        except requests.HTTPError as e:
            print(e)
            print(response.json())
        except IndexError:
            print(f"KIWI: No deals to {destination.fly_to} found.")

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

                if deal.price < destination.acceptable_price:
                    nm.notify_about_deal(source=DataSource.AZAIR, deal=deal)
                else:
                    print(
                        (f'AZAIR: No deals to {deal.fly_to} found below the threshold '
                         f'of {destination.acceptable_price} PLN'))
            except AttributeError:
                print(f"AZAIR: No deals to {destination.fly_to} found.")
        else:
            print('AZAIR: Failed to retrieve data. Status code:',
                  response.status_code)
