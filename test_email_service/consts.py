import os
import dotenv


dotenv.load_dotenv()


CI_RUN = os.getenv('CI')
MIDDLEWARE_ADDRESS = os.getenv('MIDDLEWARE_ADDRESS', 'http://127.0.0.1:80')
APP_CUSTOMER_ADDRESS = os.getenv('APP_CUSTOMER_ADDRESS')
APP_OUR_ADDRESS = os.getenv('APP_OUR_ADDRESS')

# Appgrid instance
APP_INSTANCE_URL = os.getenv('APP_INSTANCE_URL')
APP_INSTANCE_TOKEN = os.getenv('APP_INSTANCE_TOKEN')

# SMTP
SMTP_API_URL_V2 = os.getenv('SMTP_API_URL_V2')
SMTP_API_URL_V1 = os.getenv('SMTP_API_URL_V1')
ENVIRONMENT_DOMAIN = os.getenv('ENVIRONMENT_DOMAIN')

LANDING_PAGE_URL = os.getenv('LANDING_PAGE_URL')

