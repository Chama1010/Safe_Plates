# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
#     EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')


import os

# Only load .env locally (e.g., your dev machine)
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
    EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')
















    