import yaml, os
from dotenv import load_dotenv
load_dotenv()
def load_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    config['env'] = {
        'TELEGRAM_BOT_TOKEN': os.getenv('TELEGRAM_BOT_TOKEN'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ROUTER_ADMIN_USER': os.getenv('ROUTER_ADMIN_USER'),
        'ROUTER_ADMIN_PASS': os.getenv('ROUTER_ADMIN_PASS')
    }
    return config
CONFIG = load_config()
