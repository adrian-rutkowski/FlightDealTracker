from bs4 import BeautifulSoup
import requests
import constants
from data_manager import DataManager
from data_models import DestinationModel
from notifications_manager import NotificationsManager

dm = DataManager()
nm = NotificationsManager()

class FlightsManager:

    def check_kiwi(self, destination: DestinationModel):
        params = dm.prepare_kiwi_params(destination=destination)
        try:
            response = requests.get(url=f"{constants.KIWI_URL}/search", headers={'apikey': constants.KIWI_API_KEY}, params=params)
            print(response.status_code)
            response.raise_for_status()
            trip = response.json()['data'][0]
            deal = dm.get_trip(trip=trip)
            if deal.price < destination.acceptable_price:
                nm.notify_about_deal(deal=deal)
            else:
                print(f'KIWI: No deals to {deal.fly_to} found below the threshold of {destination.acceptable_price} PLN')
        except requests.HTTPError as e:
            print(e)
            print(response.json())
        except IndexError as e:
            print(f"KIWI: No deals to {destination.fly_to} found.")


    def check_azair(self, destination: DestinationModel):
        # Send a GET request to the URL
        search = dm.prepare_azair_url(destination=destination)
        response = requests.get(constants.AZAIR_URL+search)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            try:
                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find the main <div> element with class "list" and id "reslist"
                main_div = soup.find('div', {'class': 'list', 'id': 'reslist'})
                
                # Find the first <div> element with class "text" inside the main <div>
                text_div = main_div.find('div', {'class': 'text'})
                
                departure_date = text_div.find('span', class_='date').text
                departure_location = text_div.find_all('span', class_='from')[0].text.strip().split()[-1]
                arrival_location = text_div.find_all('span', class_='to')[0].text.strip().split()[-1]
                price = int(''.join(filter(str.isdigit, text_div.find('div', class_='totalPrice').find('span', class_='tp').text)))
                length_of_stay = text_div.find('div', class_='totalPrice').find('span', class_='lengthOfStay').text.split(':')[-1].strip()
                url = main_div.find('div', {'class': 'result'}).find('div', class_='bookmark').find('a')['href'].replace("¤", "&curren")
                
                if price < destination.acceptable_price:
                    message = f"AZAIR: {departure_location} to {arrival_location} on {departure_date} for {length_of_stay}. {price} PLN.\nMore details here: {nm.shorten_url(constants.AZAIR_URL+url)}"
                    print(message)
                else:
                    print(f'AZAIR: No deals to {destination.fly_to} found below the threshold of {destination.acceptable_price} PLN')
            except AttributeError:
                print(f"AZAIR: No deals to {destination.fly_to} found.")
        else:
            print('AZAIR: Failed to retrieve data. Status code:', response.status_code)
