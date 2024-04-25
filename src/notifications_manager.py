from data_manager import DataManager
from data_models import TripModel

import boto3
import constants
import pyshorteners

from enums import DataSource


class NotificationsManager:

    def shorten_url(self, long_url):
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(long_url)
        return short_url

    def send_text_message(self, message):
        client = boto3.client(service_name="sns",
                              aws_access_key_id=constants.AWS_ROOT_ACCESS_KEY_ID,
                              aws_secret_access_key=constants.AWS_ROOT_SECRET_ACCESS_KEY,
                              region_name=constants.AWS_REGION_NAME)

        response = client.publish(PhoneNumber=constants.MY_PHONE_NUMBER,
                                  Message=message)

        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def prepare_message_text(self, source: DataSource, deal: TripModel):
        msg = None
        match source:
            case DataSource.KIWI:
                airline = f"Unknown airline {deal.airline}"
                for row in DataManager().get_airlines_data():
                    if row.code == deal.airline:
                        airline = row.name
                        break
                msg = (f"{source.value.upper()}: {deal.fly_from} to {deal.fly_to} on {deal.departure_date} with "
                       f"{airline}. {deal.length_of_stay} nights for {deal.price} PLN. "
                       f"{self.shorten_url(deal.url)}")

            case DataSource.AZAIR:
                msg = (f"{source.value.upper()}: {deal.fly_from} to {deal.fly_to} on {deal.departure_date} "
                       f"for {deal.length_of_stay}. {deal.price} PLN. "
                       f"{self.shorten_url(constants.AZAIR_URL+deal.url)}")
        return msg

    def notify_about_deal(self, source: DataSource, deal: TripModel):
        msg = self.prepare_message_text(source=source, deal=deal)
        print(msg)
        # self.send_text_message(message=msg)
