from app import create_app
from sys import exit
from config import config_dict
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.environ.get('FLASK_DEBUG')

# The configuration
get_config_mode = 'development' if DEBUG else 'production'

app_config = config_dict.get(get_config_mode)

if app_config is None:
    exit('Error: Invalid <config_mode>. Expected values [development, production]')

app = create_app(app_config)

# Initialize Celery app
celery_app = app.extensions.get("celery")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
