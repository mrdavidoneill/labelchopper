import os
from dotenv import load_dotenv


def load():
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path)
