from data_manager import DataManager
from data_models import TripModel
import boto3
import constants

class NotificationsManager:

    def send_text_message(self, message):
        client = boto3.client(service_name="sns", 
                      aws_access_key_id=constants.AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=constants.AWS_SECRET_ACCESS_KEY, 
                      region_name=constants.AWS_REGION_NAME)
        
        response = client.publish(PhoneNumber=constants.MY_PHONE_NUMBER,
                                  Message=message)

        print(response)
    
    def notify_about_deal(self, deal: TripModel):
        for row in DataManager().get_airlines_data():
            if row.code == deal.airline:
                airline = row.name
        msg =  f"{deal.fly_from} to {deal.fly_to} on {deal.departure_date} with {airline}. {deal.length_of_stay} nights for {deal.price} PLN. More details here: {deal.url}"
        print(msg)
        self.send_text_message(message=msg)
