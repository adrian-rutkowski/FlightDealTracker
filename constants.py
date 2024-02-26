from datetime import datetime, timedelta
import os

URL = 'https://api.tequila.kiwi.com/v2'
KIWI_API_KEY = os.environ.get("KIWI_API_KEY")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
TODAY = datetime.today().strftime('%d/%m/%Y')
DATE_FROM = (datetime.today() + timedelta(days=30)).strftime('%d/%m/%Y')
DATE_TO = (datetime.today() + timedelta(days=30*7)).strftime('%d/%m/%Y')
