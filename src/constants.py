from datetime import datetime, timedelta
import os

KIWI_URL = 'https://api.tequila.kiwi.com/v2'
KIWI_API_KEY = os.environ.get("KIWI_API_KEY")
AWS_ROOT_ACCESS_KEY_ID = os.environ.get("AWS_ROOT_ACCESS_KEY_ID")
AWS_ROOT_SECRET_ACCESS_KEY = os.environ.get("AWS_ROOT_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")
DATE_FROM = (datetime.today() + timedelta(days=30)).strftime('%d/%m/%Y')
DATE_TO = (datetime.today() + timedelta(days=30*4)).strftime('%d/%m/%Y')
AZAIR_URL = 'https://www.azair.com/'
