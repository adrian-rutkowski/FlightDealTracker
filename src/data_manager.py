from datetime import datetime
import json

from data_models import AirlineModel, DestinationModel, TripModel
from urllib.parse import urlencode


class DataManager():

    def get_destinations_data(self, file_path='data/destinations.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            destinations = [DestinationModel(
                **destination) for destination in data]
            return destinations

    def get_airlines_data(self, file_path='data/airlines.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            airlines = [AirlineModel(code=code, name=name)
                        for code, name in data.items()]
            return airlines

    def get_trip(self, trip):
        return TripModel(fly_from=f"{trip['cityFrom']} {trip['flyFrom']}",
                         fly_to=f"{trip['cityTo']} {trip['flyTo']}",
                         departure_date=datetime.strptime(
                             trip['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y'),
                         length_of_stay=trip['nightsInDest'],
                         price=trip['price'],
                         airline=trip['airlines'][0],
                         url=trip['deep_link']
                         )

    def prepare_kiwi_params(self, destination: DestinationModel):
        params = {
            'fly_from': destination.fly_from,
            'fly_to': destination.fly_to,
            'date_from': destination.date_from,
            'date_to': destination.date_to,
            'nights_in_dst_from': destination.stay_min,
            'nights_in_dst_to': destination.stay_max,
            'ret_from_diff_city': destination.ret_from_diff_city,
            'ret_to_diff_city':  destination.ret_to_diff_city,
            'max_stopovers': destination.max_stopovers,
            'adults': 1,
            'curr': 'PLN',
            'sort': 'price',
            'limit': 10
        }
        return params

    def prepare_airport_codes(self, airport_codes):
        # Split the airport codes by comma
        airport_codes_list = airport_codes.split(',')

        # If there's only one airport code, return it as is
        if len(airport_codes_list) == 1:
            return f"[{airport_codes_list[0]}]"
        else:
            # Join the additional airport codes with comma and wrap in parentheses
            additional_airports = ','.join(airport_codes_list[1:])
            additional_airports = f'(+{additional_airports})'

            # Return the main airport code wrapped in square brackets and
            # concatenated with additional airports
            return f'[{airport_codes_list[0]}] {additional_airports}'

    def prepare_azair_url(self, destination: DestinationModel):

        parameters = {
            'searchtype': 'flexi',
            'srcAirport': self.prepare_airport_codes(destination.fly_from),
            'dstAirport': self.prepare_airport_codes(destination.fly_to),
            'adults': 1,
            'depdate': destination.date_from.replace('/', '.'),
            'arrdate': destination.date_to.replace('/', '.'),
            'minDaysStay': destination.stay_min+1,
            'maxDaysStay': destination.stay_max+1,
            'currency': 'PLN',
            'samedep': not destination.ret_to_diff_city,
            'samearr': not destination.ret_from_diff_city,
            'maxChng': destination.max_stopovers,
            'isOneway': 'return'
        }

        if destination.stay_max < 7:
            city_break_params = {'dep2': True,
                                 'dep3': True,
                                 'dep4': True,
                                 'dep5': True,
                                 'arr0': True,
                                 'arr1': True,
                                 'arr2': True,
                                 'arr3': False,
                                 'arr4': False,
                                 'arr5': True,
                                 'arr6': True,
                                 'minHourOutbound': '7:00',
                                 'maxHourOutbound': '17:00',
                                 'minHourInbound': '7:00',
                                 'maxHourInbound': '20:00'
                                 }

            parameters.update(city_break_params)

        # Construct URL with parameters
        url = 'azfin.php?' + urlencode(parameters)

        return url
