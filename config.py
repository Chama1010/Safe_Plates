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

if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     EDAMAM_APP_ID = os.getenv('EDAMAM_APP_ID')
#     EDAMAM_APP_KEY = os.getenv('EDAMAM_APP_KEY')

class Config:
    SECRET_KEY = 'J0aLz8%w3R$k9vL@T!h2f*XlQZ*BnM7eC6DpY'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chama922:arrowf78@chama922.mysql.pythonanywhere-services.com/chama922$AllergyFreeRecipeFinder'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EDAMAM_APP_ID = 'b265e1fa'
    EDAMAM_APP_KEY = 'a583d55aed858297e1d720888d787f52'
















    