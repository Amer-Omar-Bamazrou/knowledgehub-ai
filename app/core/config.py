import os


from dotenv import load_dotenv


load_dotenv(".env")


DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]